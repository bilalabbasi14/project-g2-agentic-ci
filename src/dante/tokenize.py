"""Source cleaning, tokenisation and test-source lookup.

Ported from DANTE's source_processor.py (clean_java_source, clean_scala_source,
clean_generic_source, tokenize_java_code, tokenize_scala_code,
tokenize_generic_code, clean_and_tokenize_source,
find_test_source_file_aggressively) with DANTE config.py defaults
(USE_GENERIC_TOKENIZER_ONLY = False, GENERIC_KEYWORDS_TO_FILTER).
The source lookup works on a list of repo paths instead of walking a worktree.
"""
import os
import re

# GENERIC_KEYWORDS_TO_FILTER from DANTE config.py
GENERIC_KEYWORDS = {
    "if", "else", "for", "while", "return", "new", "try", "catch", "finally", "this", "self",
    "true", "false", "null", "none", "def", "class", "public", "private", "protected", "static",
    "void", "int", "string", "function", "var", "let", "const", "import", "from", "package",
    "extends", "implements", "interface", "enum", "func", "go", "defer", "chan", "select",
    "range", "type", "struct", "map", "error", "nil", "util", "io", "lang", "net", "org",
    "apache", "common", "utils", "base", "abstract", "helper",
}


def clean_java_source(code):
    if not code:
        return ""
    c = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    c = re.sub(r'//.*', '', c)
    c = re.sub(r'@\w+(\s*\(.*?\))?', '', c)
    return re.sub(r'\s+', ' ', c).strip()


def clean_scala_source(code):
    if not code:
        return ""
    c = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    c = re.sub(r'//.*', '', c)
    c = re.sub(r'@\w+(\s*\(.*?\))?', '', c)
    c = re.sub(r'\"\"\"[\s\S]*?\"\"\"', '', c)
    return re.sub(r'\s+', ' ', c).strip()


def clean_generic_source(code):
    if not code:
        return ""
    c = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    c = re.sub(r'//.*', '', c)
    c = re.sub(r'#.*', '', c)
    c = re.sub(r'\"\"\"[\s\S]*?\"\"\"', '', c)
    c = re.sub(r"\'\'\'[\s\S]*?\'\'\'", '', c)
    return re.sub(r'\s+', ' ', c).strip()


def _split_identifiers(identifiers):
    out = []
    for ident in identifiers:
        parts_camel = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', ident)).split()
        final_parts = []
        for part in parts_camel:
            final_parts.extend(part.split('_'))
        out.extend(p.lower() for p in final_parts if len(p) > 2)
    return out


def tokenize_java_code(cleaned):
    if not cleaned:
        return [], set()
    method_pat = (r'\b(?:public|protected|private|static|final|synchronized|native|abstract|\s)*\s*'
                  r'(?:<[^>]+>\s+)?([a-zA-Z_]\w*(?:<.*?>)?(?:\[\])?)\s+(\b[a-zA-Z_]\w*\b)\s*\(')
    names = {name.lower() for _, name in re.findall(method_pat, cleaned)}
    ctor_pat = r'\b(?:public|private|protected)\s+([A-Z]\w*)\s*\('
    names |= {n.lower() for n in re.findall(ctor_pat, cleaned)}
    tokens = _split_identifiers(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_$]*\b', cleaned))
    for s_tuple in re.findall(r'"([^"\\]*(\\.[^"\\]*)*)"', cleaned):
        s = s_tuple[0]
        if len(s) > 3:
            tokens.extend(w for w in re.findall(r'\b\w+\b', s.lower()) if len(w) > 2)
    return list(set(tokens)), names


def tokenize_scala_code(cleaned):
    if not cleaned:
        return [], set()
    names = {n.lower().strip('`') for n in re.findall(r'def\s+([a-zA-Z_][\w`]+)\s*(?:\[|\(|\:|\=)', cleaned)}
    tokens = _split_identifiers(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', cleaned))
    return list(set(tokens)), names


def tokenize_generic_code(cleaned):
    if not cleaned:
        return [], set()
    return list(set(t.lower() for t in re.findall(r'\b[a-zA-Z_]\w*\b', cleaned) if len(t) > 2)), set()


_STRATEGIES = {".java": (clean_java_source, tokenize_java_code),
               ".scala": (clean_scala_source, tokenize_scala_code)}


def clean_and_tokenize_source(code, file_extension):
    """Return (tokens, method_names). Tokens are unique (set semantics, list order arbitrary)."""
    if not code:
        return [], set()
    cleaner, tokenizer = _STRATEGIES.get(file_extension, (clean_generic_source, tokenize_generic_code))
    tokens, names = tokenizer(cleaner(code))
    return ([t for t in tokens if t not in GENERIC_KEYWORDS],
            {n for n in names if n not in GENERIC_KEYWORDS})


def find_test_source_path(repo_paths, test_fqn):
    """Pick the repo path for a test class from a list of '/'-separated repo paths.

    Same rules as find_test_source_file_aggressively: match file stem to the
    simple class name (case-insensitive, inner class stripped), skip
    directories starting with '.', prefer the longest package-suffix match,
    +0.5 for test-like directories, first best candidate wins.
    """
    if not test_fqn:
        return None
    simple = test_fqn.split('.')[-1].split('$')[0].lower()
    pkg = test_fqn.split('.')[:-1]
    cands = []
    for p in repo_paths:
        parts = p.split('/')
        if any(d.startswith('.') for d in parts[:-1]):
            continue
        if os.path.splitext(parts[-1])[0].lower() == simple:
            cands.append(p)
    if not cands:
        return None
    if len(cands) == 1:
        return cands[0]
    best, best_score = None, -1
    for c in cands:
        dir_parts = c.split('/')[:-1] or ['.']
        depth = 0
        if pkg and dir_parts:
            for i in range(1, min(len(pkg), len(dir_parts)) + 1):
                if pkg[-i].lower() == dir_parts[-i].lower():
                    depth += 1
                else:
                    break
        score = depth
        # DANTE tests the absolute worktree path; a leading '/' keeps root-level dirs matchable
        if any(ind in ('/' + c).lower() for ind in ("/test/", "/tests/", "/itest/", "/it/")):
            score += 0.5
        if score > best_score:
            best, best_score = c, score
    return best or cands[0]
