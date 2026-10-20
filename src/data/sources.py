"""Test-class sources at a build commit, read from a partial (blob-less) clone.

Instead of checking out a worktree per build, the file list of the commit is
read with `git ls-tree` and only the needed blobs are fetched (one batched
fetch) and read with `git cat-file --batch`. Nothing is written outside the
clone directory.
"""
import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


class SourceRepo:
    def __init__(self, repo_path, repo_url=None):
        self.path = Path(repo_path)
        self.repo_url = repo_url
        self._trees = {}

    def _git(self, *args, input=None, check=True):
        r = subprocess.run(["git", "-C", str(self.path), *args], input=input,
                           capture_output=True, check=False)
        if check and r.returncode != 0:
            raise GitError(f"git {' '.join(args[:3])}: {r.stderr.decode(errors='ignore').strip()}")
        return r

    def ensure_clone(self):
        if (self.path / ".git").exists() or (self.path / "HEAD").exists():
            return
        if not self.repo_url:
            raise GitError(f"no clone at {self.path} and no repo_url")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout",
                            self.repo_url, str(self.path)], capture_output=True)
        if r.returncode != 0:
            raise GitError(r.stderr.decode(errors="ignore"))

    def has_commit(self, sha):
        return self._git("cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0

    def ensure_commit(self, sha):
        """Fetch the commit by SHA if it is not in the clone. Returns False if unavailable."""
        if self.has_commit(sha):
            return True
        self._git("fetch", "--quiet", "--no-tags", "--filter=blob:none", "origin", sha, check=False)
        return self.has_commit(sha)

    def tree(self, sha):
        """{path: blob_oid} for every file at the commit."""
        if sha not in self._trees:
            out = self._git("ls-tree", "-r", "--full-tree", sha).stdout.decode("utf-8", errors="ignore")
            files = {}
            for line in out.splitlines():
                meta, _, path = line.partition("\t")
                parts = meta.split()
                if len(parts) == 3 and parts[1] == "blob":
                    files[path] = parts[2]
            self._trees = {sha: files}          # keep one tree in memory
        return self._trees[sha]

    def read_blobs(self, oids):
        """Return {oid: text}. Missing blobs are fetched in one batch first."""
        oids = list(dict.fromkeys(oids))
        if not oids:
            return {}
        missing = self._git("cat-file", "--batch-check", input="\n".join(oids).encode() + b"\n")
        need = [ln.split()[0] for ln in missing.stdout.decode().splitlines() if ln.endswith("missing")]
        if need:
            self._git("-c", "fetch.negotiationAlgorithm=noop", "fetch", "--quiet", "--no-tags",
                      "--no-write-fetch-head", "--filter=blob:none", "--stdin", "origin",
                      input="\n".join(need).encode() + b"\n", check=False)
        out = {}
        env_input = "\n".join(oids).encode() + b"\n"
        data = subprocess.run(["git", "-C", str(self.path), "-c", "fetch.negotiationAlgorithm=noop",
                               "cat-file", "--batch"], input=env_input, capture_output=True).stdout
        pos = 0
        for oid in oids:
            nl = data.index(b"\n", pos)
            header = data[pos:nl].decode().split()
            pos = nl + 1
            if len(header) < 3 or header[1] == "missing":
                continue
            size = int(header[2])
            out[oid] = data[pos:pos + size].decode("utf-8", errors="ignore")
            pos += size + 1
        return out
