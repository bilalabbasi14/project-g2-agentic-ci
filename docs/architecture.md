# Architecture

```mermaid
flowchart LR
    subgraph Data["Data (src/data)"]
        LRTS[(LRTS: dataset.csv,<br/>test_class.csv.zip, diffs)]
        GIT[(karaf partial clone)]
        LOADER[Data loader<br/>loader.py, splitter.py, sources.py]
        LRTS --> LOADER
        GIT --> LOADER
    end

    subgraph Baseline["DANTE baseline (src/dante)"]
        HIST[History score<br/>THFR + sticky P_n/n]
        TFIDF[TF-IDF relevance]
        CCH[Combine + CCH value]
        GREEDY[Greedy budget selection]
        HIST --> CCH
        TFIDF --> CCH
        CCH --> GREEDY
    end

    subgraph Agent["Agent layer (src/agent, src/tools)"]
        SHORT[Candidate shortlister<br/>top-K history and TF-IDF]
        SEM[Semantic analyzer<br/>local LLM via Ollama]
        FB[Fallback router]
        ORCH[Orchestrator<br/>planned: per-commit weight]
        EXPL[Explainer<br/>planned: skipped-test reasons]
        TOOLS[Tools: history_retrieval,<br/>diff_reader, budget_tracker]
    end

    EVAL[Evaluator (src/eval)<br/>%DTC, APFDc, SAPFDc, SDS]
    STORED[(Stored DANTE results<br/>RQ1 CSV, solution JSONs)]

    LOADER --> HIST
    LOADER --> TFIDF
    HIST --> SHORT
    TFIDF --> SHORT
    SHORT --> SEM
    SEM --> FB
    FB -- "LLM relevance replaces TF-IDF" --> CCH
    FB -. "on timeout / invalid JSON / low confidence:<br/>use DANTE ranking" .-> GREEDY
    TOOLS -.-> ORCH
    ORCH -.-> CCH
    GREEDY --> EVAL
    GREEDY -.-> EXPL
    STORED --> EVAL

    classDef baseline fill:#e8f0fe,stroke:#4a6fa5;
    classDef planned stroke-dasharray: 5 5;
    class HIST,TFIDF,CCH,GREEDY baseline;
    class ORCH,EXPL planned;
```

Baseline path (shaded): data loader -> history + TF-IDF -> CCH value -> greedy
selection -> evaluator. `run_end_to_end.py` runs the LLM path for one build.

## Components

| Component | Code | Status |
|---|---|---|
| Data loader | `src/data/loader.py`, `splitter.py`, `sources.py` | implemented |
| DANTE baseline | `src/dante/` | implemented |
| Candidate shortlister | `src/agent/shortlister.py` | implemented |
| Semantic analyzer | `src/agent/semantic_analyzer.py`, `llm_provider.py` | implemented |
| Fallback router | `src/agent/fallback_router.py` | implemented |
| Tools | `src/tools/` | implemented |
| Evaluator | `src/eval/` | implemented |
| Orchestrator (per-commit history/relevance weight) | not yet created | planned |
| Explainer (reasons for skipped tests) | not yet created | planned |

## Where each research gap is addressed

Gap numbers follow the proposal diagram (`docs/architecture.png`).

| Gap | Where | Phase 1 status |
|---|---|---|
| Gap 1: lexical TF-IDF relevance misses semantic links between a change and a test | semantic analyzer (local LLM) replaces TF-IDF relevance for the shortlist; tools `history_retrieval`, `diff_reader` | implemented, initial run |
| Gap 2: skipped tests are not explained | explainer (natural-language reasons for skipped tests) | planned |
| Gap 3: LLM output can be slow, malformed or unsure | fallback router: timeout / invalid JSON / schema / low confidence -> DANTE ranking, every fallback recorded | implemented |
| Fixed history/relevance weight for every commit | orchestrator choosing the weight per commit | planned |
| Reproducibility of the baseline | `src/dante/compare_stored.py`, `src/eval/compare_baselines.py`, `docs/dante_notes.md` | implemented |
