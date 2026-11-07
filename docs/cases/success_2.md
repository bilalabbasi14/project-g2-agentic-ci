# Success case: `PR-1642_build1` at the 10% budget

- **Run:** `E3_test_seed1` · **method:** `Full system` compared with `DANTE-CCH`
- **Why this case:** rank 2 by %DTC gain of Full system over DANTE-CCH at 10% (gain +1.000; ties by build key)
- **Categories of this pair:** S (org.apache.karaf.itests.examples.GraphQLExampleTest)

## What happened

- Candidates: 210; failing candidates: 1; shortlist size: 20.
- Orchestrator: w = 0.7, confidence 0.8, source `agent`, reason: "High relevance signal from specific changed files and low recent failure density.".

| Metric | Full system | DANTE-CCH |
|---|---|---|
| %DTC | 1.000 | 0.000 |
| SAPFDc | 0.698 | 0.000 |
| APFDc (full order) | 0.970 | 0.921 |
| Selected tests | 29 | 145 |
| Failing tests found | 1 | 0 |
| Selected duration (s) | 108.655 | 108.569 |

Failing candidates:

| Test | Selected by Full system | Selected by DANTE-CCH | On shortlist | LLM relevance | Rank by value (Full system) |
|---|---|---|---|---|---|
| `org.apache.karaf.itests.examples.GraphQLExampleTest` | yes | no | yes | 0.00 | 7 |

LLM relevance reasons for the failing candidates:

- `org.apache.karaf.itests.examples.GraphQLExampleTest`: "The test class does not interact with the `ListFeaturesCommand` or any of its dependencies."

## Trajectory

Full trace: [logs_sample/E3_test_seed1/PR-1642_build1.md](../../logs_sample/E3_test_seed1/PR-1642_build1.md) (raw events: `logs_sample/E3_test_seed1/PR-1642_build1.jsonl`), exported with `src.obs.export_sample`.

| Step | Component | Event | Summary |
|---|---|---|---|
| 1 | pipeline | state | loaded, 210 candidates |
| 2 | pipeline | state | dante_scored, 210 candidates |
| 3 | pipeline | state | shortlisted, 20 shortlisted |
| 4 | semantic_analyzer | llm_call | `org.apache.karaf.features.command.ListFeaturesCommandTest`, attempt 0, cached False, {'relevance': 0.2} |
| 5 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.GraphQLExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 6 | semantic_analyzer | llm_call | `org.apache.karaf.itests.FeatureTest`, attempt 0, cached False, {'relevance': 0.2} |
| 7 | semantic_analyzer | llm_call | `org.apache.karaf.itests.FelixHttpTest`, attempt 0, cached False, {'relevance': 0} |
| 8 | semantic_analyzer | llm_call | `org.apache.karaf.features.command.RepoListCommandTest`, attempt 0, cached False, {'relevance': 0.1} |
| 9 | semantic_analyzer | llm_call | `org.apache.karaf.itests.XATest`, attempt 0, cached False, {'relevance': 0.1} |
| 10 | semantic_analyzer | llm_call | `org.apache.karaf.features.internal.region.SubsystemTest`, attempt 0, cached False, {'relevance': 0.1} |
| 11 | semantic_analyzer | llm_call | `org.apache.karaf.itests.ConfigManagedServiceFactoryTest`, attempt 0, cached False, {'relevance': 0} |
| 12 | semantic_analyzer | llm_call | `org.apache.karaf.itests.JmsTest`, attempt 0, cached False, {'relevance': 0} |
| 13 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.SchedulerExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 14 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.JmsExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 15 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.LogAppenderExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 16 | semantic_analyzer | llm_call | `org.apache.karaf.features.internal.region.FeaturesDependenciesTest`, attempt 0, cached False, {'relevance': 0.1} |
| 17 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.HttpResourceExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 18 | semantic_analyzer | llm_call | `org.apache.karaf.itests.JMXSecurityTest`, attempt 0, cached False, {'relevance': 0} |
| 19 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.ScrExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 20 | semantic_analyzer | llm_call | `org.apache.karaf.examples.itests.ExampleWithConfigITest`, attempt 0, cached False, {'relevance': 0} |
| 21 | semantic_analyzer | llm_call | `org.apache.karaf.itests.examples.CommandExampleTest`, attempt 0, cached False, {'relevance': 0} |
| 22 | semantic_analyzer | llm_call | `org.apache.karaf.features.internal.model.JsonTest`, attempt 0, cached False, {'relevance': 0.1} |
| 23 | semantic_analyzer | llm_call | `org.apache.karaf.itests.LogTest`, attempt 0, cached False, {'relevance': 0} |
| 24 | orchestrator | llm_call | step 1, attempt 0, cached False, {'w': 0.7, 'action': 'final'} |
| 25 | orchestrator | decision | w = 0.7, confidence 0.8, source agent |
| 26 | pipeline | state | selected, DANTE-CCH at 5%, 121 selected |
| 27 | pipeline | state | selected, DANTE-CCH at 10%, 145 selected |
| 28 | pipeline | state | selected, DANTE-CCH at 20%, 142 selected |
| 29 | pipeline | state | selected, DANTE-CCH-shipped at 5%, 23 selected |
| 30 | pipeline | state | selected, DANTE-CCH-shipped at 10%, 27 selected |
| 31 | pipeline | state | selected, DANTE-CCH-shipped at 20%, 40 selected |
| 32 | pipeline | state | selected, LLM-relevance at 5%, 27 selected |
| 33 | pipeline | state | selected, LLM-relevance at 10%, 29 selected |
| 34 | pipeline | state | selected, LLM-relevance at 20%, 33 selected |
| 35 | pipeline | state | selected, Tuned-weight (LLM) at 5%, 27 selected |
| 36 | pipeline | state | selected, Tuned-weight (LLM) at 10%, 29 selected |
| 37 | pipeline | state | selected, Tuned-weight (LLM) at 20%, 33 selected |
| 38 | pipeline | state | selected, Agent-weighted at 5%, 27 selected |
| 39 | pipeline | state | selected, Agent-weighted at 10%, 29 selected |
| 40 | pipeline | state | selected, Agent-weighted at 20%, 33 selected |
| 41 | pipeline | state | selected, Full system at 5%, 27 selected |
| 42 | explainer | explanation | `org.apache.karaf.itests.examples.GraphQLExampleTest` at 5%, ok = False |
| 43 | explainer | explanation | `org.apache.karaf.itests.JmsTest` at 5%, ok = False |
| 44 | explainer | explanation | `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest` at 5%, ok = True |
| 45 | explainer | explanation | `org.apache.karaf.itests.FeatureTest` at 5%, ok = False |
| 46 | explainer | explanation | `org.apache.karaf.itests.JMXSecurityTest` at 5%, ok = False |
| 47 | pipeline | state | selected, Full system at 10%, 29 selected |
| 48 | explainer | explanation | `org.apache.karaf.itests.examples.JmsExampleTest` at 10%, ok = False |
| 49 | explainer | explanation | `org.apache.karaf.itests.JmsTest` at 10%, ok = False |
| 50 | explainer | explanation | `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest` at 10%, ok = True |
| 51 | explainer | explanation | `org.apache.karaf.itests.FeatureTest` at 10%, ok = False |
| 52 | explainer | explanation | `org.apache.karaf.itests.JMXSecurityTest` at 10%, ok = False |
| 53 | pipeline | state | selected, Full system at 20%, 33 selected |
| 54 | explainer | explanation | `org.apache.karaf.itests.examples.SoapExampleTest` at 20%, ok = False |
| 55 | explainer | explanation | `org.apache.karaf.itests.examples.ServletExampleTest` at 20%, ok = False |
| 56 | explainer | explanation | `org.apache.karaf.bundle.command.ListServicesTest` at 20%, ok = True |
| 57 | explainer | explanation | `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest` at 20%, ok = True |
| 58 | explainer | explanation | `org.apache.karaf.client.ClientConfigTest` at 20%, ok = True |
