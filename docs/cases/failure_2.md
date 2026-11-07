# Failure (F2) case: `PR-1462_build1` at the 5% budget

- **Run:** `E3_test_seed1` · **method:** `Full system` compared with `DANTE-CCH`
- **Why this case:** first pair (by build key, then budget) of F2, the second most frequent failure category (41 pairs)
- **Categories of this pair:** F2 (org.apache.karaf.shell.ssh.SshUtilsTest), F5 (Agent-weighted %DTC 0.000 < DANTE-CCH 1.000), F6 (org.apache.karaf.config.core.impl.JsonConfigInstallerTest)

## What happened

- Candidates: 130; failing candidates: 1; shortlist size: 11.
- Orchestrator: w = 0.2, confidence 0.8, source `agent`, reason: "Low relevance signal and weak history indicate a need to trust relevance more.".

| Metric | Full system | DANTE-CCH |
|---|---|---|
| %DTC | 0.000 | 1.000 |
| SAPFDc | 0.000 | 0.691 |
| APFDc (full order) | 0.388 | 0.988 |
| Selected tests | 42 | 92 |
| Failing tests found | 0 | 1 |
| Selected duration (s) | 4.885 | 4.882 |

Failing candidates:

| Test | Selected by Full system | Selected by DANTE-CCH | On shortlist | LLM relevance | Rank by value (Full system) |
|---|---|---|---|---|---|
| `org.apache.karaf.shell.ssh.SshUtilsTest` | no | yes | no | - | 56 |

## Trajectory

Full trace: [logs_sample/E3_test_seed1/PR-1462_build1.md](../../logs_sample/E3_test_seed1/PR-1462_build1.md) (raw events: `logs_sample/E3_test_seed1/PR-1462_build1.jsonl`), exported with `src.obs.export_sample`.

| Step | Component | Event | Summary |
|---|---|---|---|
| 1 | pipeline | state | loaded, 130 candidates |
| 2 | pipeline | state | dante_scored, 130 candidates |
| 3 | pipeline | state | shortlisted, 11 shortlisted |
| 4 | semantic_analyzer | llm_call | `org.apache.karaf.audit.util.FastDateFormatTest`, attempt 0, cached False, {'relevance': 0} |
| 5 | semantic_analyzer | llm_call | `org.apache.karaf.main.MainLockingTest`, attempt 0, cached False, {'relevance': 0.1} |
| 6 | semantic_analyzer | llm_call | `org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest`, attempt 0, cached False, {'relevance': 0} |
| 7 | semantic_analyzer | llm_call | `org.apache.karaf.obr.command.util.FileUtilTest`, attempt 0, cached False, {'relevance': 0} |
| 8 | semantic_analyzer | llm_call | `org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest`, attempt 0, cached False, {'relevance': 0} |
| 9 | semantic_analyzer | llm_call | `org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest`, attempt 0, cached False, {'relevance': 0} |
| 10 | semantic_analyzer | llm_call | `org.apache.karaf.specs.locator.OsgiLocatorTest`, attempt 0, cached False, {'relevance': 0} |
| 11 | semantic_analyzer | llm_call | `org.apache.karaf.deployer.spring.SpringDeploymentListenerTest`, attempt 0, cached False, {'relevance': 0} |
| 12 | semantic_analyzer | llm_call | `org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest`, attempt 0, cached False, {'relevance': 0} |
| 13 | semantic_analyzer | llm_call | `org.apache.karaf.main.lock.MySQLJDBCLockTest`, attempt 0, cached False, {'relevance': 0} |
| 14 | semantic_analyzer | llm_call | `org.apache.karaf.config.core.impl.ConfigMBeanImplTest`, attempt 0, cached False, {'relevance': 0} |
| 15 | orchestrator | llm_call | step 1, attempt 0, cached False, {'w': 0.2, 'action': 'final'} |
| 16 | orchestrator | decision | w = 0.2, confidence 0.8, source agent |
| 17 | pipeline | state | selected, DANTE-CCH at 5%, 92 selected |
| 18 | pipeline | state | selected, DANTE-CCH at 10%, 105 selected |
| 19 | pipeline | state | selected, DANTE-CCH at 20%, 117 selected |
| 20 | pipeline | state | selected, DANTE-CCH-shipped at 5%, 42 selected |
| 21 | pipeline | state | selected, DANTE-CCH-shipped at 10%, 62 selected |
| 22 | pipeline | state | selected, DANTE-CCH-shipped at 20%, 54 selected |
| 23 | pipeline | state | selected, LLM-relevance at 5%, 42 selected |
| 24 | pipeline | state | selected, LLM-relevance at 10%, 62 selected |
| 25 | pipeline | state | selected, LLM-relevance at 20%, 54 selected |
| 26 | pipeline | state | selected, Tuned-weight (LLM) at 5%, 42 selected |
| 27 | pipeline | state | selected, Tuned-weight (LLM) at 10%, 62 selected |
| 28 | pipeline | state | selected, Tuned-weight (LLM) at 20%, 54 selected |
| 29 | pipeline | state | selected, Agent-weighted at 5%, 42 selected |
| 30 | pipeline | state | selected, Agent-weighted at 10%, 62 selected |
| 31 | pipeline | state | selected, Agent-weighted at 20%, 54 selected |
| 32 | pipeline | state | selected, Full system at 5%, 42 selected |
| 33 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 5%, ok = False |
| 34 | explainer | explanation | `org.apache.karaf.config.core.impl.JsonConfigInstallerTest` at 5%, ok = True |
| 35 | explainer | explanation | `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest` at 5%, ok = True |
| 36 | explainer | explanation | `org.apache.karaf.bundle.command.ListServicesTest` at 5%, ok = True |
| 37 | explainer | explanation | `org.apache.karaf.event.service.EventCollectorTest` at 5%, ok = True |
| 38 | pipeline | state | selected, Full system at 10%, 62 selected |
| 39 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 10%, ok = False |
| 40 | explainer | explanation | `org.apache.karaf.event.service.EventCollectorTest` at 10%, ok = True |
| 41 | explainer | explanation | `org.apache.karaf.event.command.EventTailCommandTest` at 10%, ok = True |
| 42 | explainer | explanation | `org.apache.karaf.event.command.EventSendCommandTest` at 10%, ok = True |
| 43 | explainer | explanation | `org.apache.karaf.deployer.spring.SpringDeploymentListenerTest` at 10%, ok = False |
| 44 | pipeline | state | selected, Full system at 20%, 54 selected |
| 45 | explainer | explanation | `org.apache.karaf.main.MainLockingTest` at 20%, ok = True |
| 46 | explainer | explanation | `org.apache.karaf.event.service.EventCollectorTest` at 20%, ok = True |
| 47 | explainer | explanation | `org.apache.karaf.event.command.EventTailCommandTest` at 20%, ok = True |
| 48 | explainer | explanation | `org.apache.karaf.event.command.EventSendCommandTest` at 20%, ok = True |
| 49 | explainer | explanation | `org.apache.karaf.event.command.EventDisplayCommandTest` at 20%, ok = True |
