# Failure (F3) case: `PR-1427_build2` at the 5% budget

- **Run:** `E3_test_seed1` · **method:** `Full system` compared with `DANTE-CCH`
- **Why this case:** first pair (by build key, then budget) of F3, the most frequent failure category (48 pairs)
- **Categories of this pair:** F3 (org.apache.karaf.itests.examples.JdbcExampleTest)

## What happened

- Candidates: 208; failing candidates: 1; shortlist size: 19.
- Orchestrator: w = 0.2, confidence 0.8, source `agent`, reason: "Low relevance signal and weak history signal".

| Metric | Full system | DANTE-CCH |
|---|---|---|
| %DTC | 0.000 | 0.000 |
| SAPFDc | 0.000 | 0.000 |
| APFDc (full order) | 0.679 | 0.632 |
| Selected tests | 32 | 52 |
| Failing tests found | 0 | 0 |
| Selected duration (s) | 75.674 | 75.674 |

Failing candidates:

| Test | Selected by Full system | Selected by DANTE-CCH | On shortlist | LLM relevance | Rank by value (Full system) |
|---|---|---|---|---|---|
| `org.apache.karaf.itests.examples.JdbcExampleTest` | no | no | yes | 0.00 | 15 |

LLM relevance reasons for the failing candidates:

- `org.apache.karaf.itests.examples.JdbcExampleTest`: "The test class does not interact with SSH sessions or the ShellCommand class."

## Trajectory

Full trace: [logs_sample/E3_test_seed1/PR-1427_build2.md](../../logs_sample/E3_test_seed1/PR-1427_build2.md) (raw events: `logs_sample/E3_test_seed1/PR-1427_build2.jsonl`), exported with `src.obs.export_sample`.

| Step | Component | Event | Summary |
|---|---|---|---|
| 1 | pipeline | state | loaded, 208 candidates |
| 2 | pipeline | state | dante_scored, 208 candidates |
| 3 | pipeline | state | shortlisted, 19 shortlisted |
| 4 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.JpaExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 5 | semantic_analyzer | llm_call | `org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest`, attempt 0, cached False, {'relevance': 0.2} |
| 6 | semantic_analyzer | llm_call | `org.apache.karaf.event.command.EventDisplayCommandTest`, attempt 0, cached False, {'relevance': 0} |
| 7 | semantic_analyzer | llm_call | `org.apache.karaf.itests.ConfigManagedServiceFactoryTest`, attempt 0, cached False, {'relevance': 0.1} |
| 8 | semantic_analyzer | llm_call | `org.apache.karaf.itests.XATest`, attempt 0, cached False, {'relevance': 0.1} |
| 9 | semantic_analyzer | llm_call | `org.apache.karaf.itests.ssh.SshKeyFormatTest`, attempt 0, cached True, {'relevance': 0.1} |
| 10 | semantic_analyzer | llm_call | `org.apache.karaf.config.command.EditCommandTest`, attempt 0, cached True, {'relevance': 0.1} |
| 11 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.JdbcExampleTest`, attempt 0, cached True, {'relevance': 0} |
| 12 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.ServletExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 13 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.WebSocketExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 14 | semantic_analyzer | llm_call | `org.apache.karaf.event.command.EventTailCommandTest`, attempt 0, cached False, {'relevance': 0} |
| 15 | semantic_analyzer | llm_call | `org.apache.karaf.itests.LogTest`, attempt 0, cached False, {'relevance': 0.1} |
| 16 | semantic_analyzer | llm_call | `org.apache.karaf.config.command.UpdateCommandTest`, attempt 0, cached True, {'relevance': 0} |
| 17 | semantic_analyzer | llm_call | `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`, attempt 0, cached False, {'relevance': 0.1} |
| 18 | semantic_analyzer | llm_call | `org.apache.karaf.itests.FeatureTest`, attempt 0, cached False, {'relevance': 0.1} |
| 19 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.ConfigExampleTest`, attempt 0, cached False, {'relevance': 0.1} |
| 20 | semantic_analyzer | llm_call | `org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest`, attempt 0, cached False, {'relevance': 0.1} |
| 21 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.JmsExampleTest`, attempt 0, cached False, {'relevance': 0.1} |
| 22 | semantic_analyzer | llm_call | `org.apache.karaf.obr.command.util.FileUtilTest`, attempt 0, cached True, {'relevance': 0} |
| 23 | orchestrator | llm_call | step 1, attempt 0, cached False, {'w': 0.2, 'action': 'final'} |
| 24 | orchestrator | decision | w = 0.2, confidence 0.8, source agent |
| 25 | pipeline | state | selected, DANTE-CCH at 5%, 52 selected |
| 26 | pipeline | state | selected, DANTE-CCH at 10%, 49 selected |
| 27 | pipeline | state | selected, DANTE-CCH at 20%, 58 selected |
| 28 | pipeline | state | selected, DANTE-CCH-shipped at 5%, 10 selected |
| 29 | pipeline | state | selected, DANTE-CCH-shipped at 10%, 29 selected |
| 30 | pipeline | state | selected, DANTE-CCH-shipped at 20%, 40 selected |
| 31 | pipeline | state | selected, LLM-relevance at 5%, 32 selected |
| 32 | pipeline | state | selected, LLM-relevance at 10%, 34 selected |
| 33 | pipeline | state | selected, LLM-relevance at 20%, 49 selected |
| 34 | pipeline | state | selected, Tuned-weight (LLM) at 5%, 32 selected |
| 35 | pipeline | state | selected, Tuned-weight (LLM) at 10%, 34 selected |
| 36 | pipeline | state | selected, Tuned-weight (LLM) at 20%, 49 selected |
| 37 | pipeline | state | selected, Agent-weighted at 5%, 32 selected |
| 38 | pipeline | state | selected, Agent-weighted at 10%, 34 selected |
| 39 | pipeline | state | selected, Agent-weighted at 20%, 49 selected |
| 40 | pipeline | state | selected, Full system at 5%, 32 selected |
| 41 | explainer | explanation | `org.apache.karaf.itests.XATest` at 5%, ok = True |
| 42 | explainer | explanation | `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest` at 5%, ok = True |
| 43 | explainer | explanation | `org.apache.karaf.itests.examples.ConfigExampleTest` at 5%, ok = True |
| 44 | explainer | explanation | `org.apache.karaf.itests.examples.ServletExampleTest` at 5%, ok = True |
| 45 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 5%, ok = True |
| 46 | pipeline | state | selected, Full system at 10%, 34 selected |
| 47 | explainer | explanation | `org.apache.karaf.itests.examples.ConfigExampleTest` at 10%, ok = True |
| 48 | explainer | explanation | `org.apache.karaf.itests.examples.ServletExampleTest` at 10%, ok = True |
| 49 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 10%, ok = True |
| 50 | explainer | explanation | `org.apache.karaf.itests.examples.JdbcExampleTest` at 10%, ok = True |
| 51 | explainer | explanation | `org.apache.karaf.audit.logger.EventLoggerTest` at 10%, ok = True |
| 52 | pipeline | state | selected, Full system at 20%, 49 selected |
| 53 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 20%, ok = True |
| 54 | explainer | explanation | `org.apache.karaf.itests.examples.JdbcExampleTest` at 20%, ok = True |
| 55 | explainer | explanation | `org.apache.karaf.audit.logger.EventLoggerTest` at 20%, ok = True |
| 56 | explainer | explanation | `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest` at 20%, ok = True |
| 57 | explainer | explanation | `org.apache.karaf.config.command.UpdateCommandTest` at 20%, ok = True |
