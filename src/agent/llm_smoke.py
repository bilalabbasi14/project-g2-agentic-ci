"""Smoke test: one real relevance call on a small made-up diff and test class.

    python -m src.agent.llm_smoke [--repeat N] [--model NAME]

Prints the raw model output, the validated response and per-call latency/tokens.
"""
import argparse
import json
import statistics

from src.agent.llm_provider import OllamaProvider
from src.agent.semantic_analyzer import build_prompt, make_request, parse_response
from src.settings import load_config

DIFF = """diff --git a/core/src/main/java/org/example/cache/LruCache.java b/core/src/main/java/org/example/cache/LruCache.java
index 1a2b3c4d5e..6f7a8b9c0d 100644
--- a/core/src/main/java/org/example/cache/LruCache.java
+++ b/core/src/main/java/org/example/cache/LruCache.java
@@ -40,7 +40,7 @@ public class LruCache<K, V> {
     public void put(K key, V value) {
         map.put(key, value);
-        if (map.size() > maxSize) {
+        if (map.size() >= maxSize) {
             evictOldest();
         }
     }
"""

TEST_NAME = "org.example.cache.LruCacheTest"
TEST_SOURCE = """package org.example.cache;

public class LruCacheTest {
    @Test
    public void evictsOldestEntryWhenFull() {
        LruCache<String, Integer> c = new LruCache<>(2);
        c.put("a", 1); c.put("b", 2); c.put("c", 3);
        assertNull(c.get("a"));
        assertEquals(2, c.size());
    }
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--model")
    args = ap.parse_args()
    cfg = load_config()
    if args.model:
        cfg["llm"]["model"] = args.model
    provider = OllamaProvider.from_config(cfg)
    req = make_request("smoke", TEST_NAME, DIFF, TEST_SOURCE,
                       cfg["llm"]["max_diff_chars"], cfg["llm"]["max_test_chars"])
    for i in range(args.repeat):
        raw = provider.complete(build_prompt(req))
        rec = provider.calls[-1]
        print(f"call {i + 1}: latency={rec.latency_s:.2f}s prompt_tokens={rec.prompt_tokens} "
              f"completion_tokens={rec.completion_tokens}")
        print("raw:", raw)
        print("validated:", json.dumps(parse_response(raw, TEST_NAME).to_dict()))
    lat = [c.latency_s for c in provider.calls]
    print(f"model={provider.model} calls={len(lat)} mean={statistics.mean(lat):.2f}s "
          f"max={max(lat):.2f}s min={min(lat):.2f}s")


if __name__ == "__main__":
    main()
