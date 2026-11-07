# Explanation rating sheet (Gap 2, RQ2)

**Rating rule** (docs/PROJECT_CONTEXT.md §8): rate every one independently as *sound*, *partly sound* or *unsound*, using this rule: **sound** = every factual statement is supported by the evidence the explainer was given, *and* the stated reason for skipping follows from that evidence.

**Rate on your own. Do not look at the other rater's sheet. Do not use any AI tool to rate.**

Write one of `sound`, `partly`, `unsound` in the `rating` column of your own sheet (`ratings_ali.csv` or `ratings_bilal.csv`), and a short note when it helps.

## R001

Build `PR-1657_build1`, budget 10%, test `org.apache.karaf.itests.examples.WarExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.WarExampleTest
- Rank by value: 21
- Candidate tests: 215
- Selected tests: 21
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 18
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, -, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 9.014
- Budget (s): 151.637
- Budget left when the test was reached (s): 0.023
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 160.628

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration of 9.014 s exceeds the remaining budget of 0.023 s.

**Cited facts**

- failures: 1 of 97 runs
- failure_rate: 0.010309278350515464
- duration_s: 9.014
- remaining_budget_at_turn_s: 0.023

## R002

Build `PR-1656_build1`, budget 20%, test `org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest
- Rank by value: 17
- Candidate tests: 211
- Selected tests: 34
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 46
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 15.641
- Budget (s): 197.844
- Budget left when the test was reached (s): 10.85
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 202.635

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration of 15.641 s exceeds the remaining budget of 10.85 s.

**Cited facts**

- failures: 1 of 97 runs
- failure_rate: 0.010309278350515464
- duration_s: 15.641
- remaining_budget_at_turn_s: 10.85

## R003

Build `PR-1552_build5`, budget 20%, test `org.apache.karaf.itests.examples.ConfigExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ConfigExampleTest
- Rank by value: 20
- Candidate tests: 210
- Selected tests: 35
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 52
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/src/main/java/org/apache/karaf/config/core/impl/JsonConfigInstaller.java`
  - `config/src/test/java/org/apache/karaf/config/core/impl/JsonConfigInstallerTest.java`
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 61.745
- Budget (s): 232.653
- Budget left when the test was reached (s): 15.998
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 278.4

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 61.745 s but only 15.998 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 61.745
- remaining_budget_at_turn_s: 15.998

## R004

Build `PR-1782_build2`, budget 10%, test `org.apache.karaf.itests.examples.JdbcExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JdbcExampleTest
- Rank by value: 29
- Candidate tests: 204
- Selected tests: 44
- History:
  - builds in the history window: 100
  - runs: 95
  - failures: 3
  - failure rate: 0.031578947368421054
  - builds since the last failure: 25
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.032
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the karaf.bat script or any of the Java 9/10 specific options removed in the code change.
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
- Test duration (s): 730.33
- Budget (s): 173.37
- Budget left when the test was reached (s): 18.16
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 885.54

**Justification**

> Skipping it is risky: its relevance is 0.1 because it does not interact with the karaf.bat script or Java 9/10 specific options, and it has a failure rate of 3.16%. It needs 730.33 s but only 18.16 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat
- failures: 3 of 95 runs
- failure_rate: 0.031578947368421054
- duration_s: 730.33
- remaining_budget_at_turn_s: 18.16

## R005

Build `PR-1492_build2`, budget 10%, test `org.apache.karaf.features.RepositoryTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.features.RepositoryTest
- Rank by value: 66
- Candidate tests: 114
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java`
- Test duration (s): 0.008
- Budget (s): 8.735
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 8.743

**Justification**

> Skipping it is reasonable: it has a duration of 0.008 s, which fits within the remaining budget of 0.0 s when it was reached.

**Cited facts**

- duration_s: 0.008
- remaining_budget_at_turn_s: 0.0

## R006

Build `PR-1816_build1`, budget 20%, test `org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest
- Rank by value: 71
- Candidate tests: 111
- Selected tests: 37
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
  - `features/core/src/main/java/org/apache/karaf/features/internal/service/BootFeaturesInstaller.java`
  - `instance/src/main/java/org/apache/karaf/instance/core/internal/InstanceServiceImpl.java`
  - `itests/common/src/main/java/org/apache/karaf/itests/KarafTestSupport.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/mavenresolver/KarafMinimalMonitoredTestSupport.java`
  - `specs/activator/src/main/java/org/apache/karaf/specs/activator/Activator.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/MockCallable.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/MockCallable2.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/OsgiLocatorTest.java`
  - `specs/java.xml.ws/src/main/java/javax/xml/bind/ContextFinder.java`
- Test duration (s): 0.893
- Budget (s): 17.157
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 18.049

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.893 s, but only 0.001 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.893
- remaining_budget_at_turn_s: 0.001

## R007

Build `PR-1827_build1`, budget 5%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 10
- Candidate tests: 200
- Selected tests: 16
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 2
  - failure rate: 0.020833333333333332
  - builds since the last failure: 28
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, -, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the network or socket operations that are modified in the code change.
- Changed files:
  - `main/src/main/java/org/apache/karaf/main/Status.java`
- Test duration (s): 18.928
- Budget (s): 128.599
- Budget left when the test was reached (s): 4.022
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 143.505

**Justification**

> Skipping it is reasonable: its relevance is 0.1 because it does not interact with the network or socket operations that are modified in the code change, and it has only failed 2 out of 96 runs. It needs 18.928 s but only 4.022 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: main/src/main/java/org/apache/karaf/main/Status.java
- failures: 2 of 96 runs
- duration_s: 18.928
- remaining_budget_at_turn_s: 4.022

## R008

Build `PR-1627_build5`, budget 5%, test `org.apache.karaf.itests.JmsTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.JmsTest
- Rank by value: 10
- Candidate tests: 209
- Selected tests: 33
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 4
  - failure rate: 0.04
  - builds since the last failure: 53
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.04
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the Karaf shell or its logout functionality.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 47.884
- Budget (s): 53.418
- Budget left when the test was reached (s): 7.459
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 93.843

**Justification**

> Skipping it is reasonable: it has a low relevance of 0.0 because it does not interact with the Karaf shell or its logout functionality. It also has a failure rate of 0.04, indicating it is generally stable. It needs 47.884 s but only 7.459 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- history_score: 0.04
- failures: 4 of 100 runs
- duration_s: 47.884
- remaining_budget_at_turn_s: 7.459

## R009

Build `PR-1662_build1`, budget 5%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 11
- Candidate tests: 214
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 61
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `manual/src/main/asciidoc/developer-guide/karaf-maven-plugin.adoc`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/commands/FormatEnum.java`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/commands/GenerateHelpMojo.java`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/commands/MarkdownCommandHelpPrinter.java`
- Test duration (s): 9.278
- Budget (s): 64.528
- Budget left when the test was reached (s): 2.655
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 71.151

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 9.278 s but only 2.655 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 9.278
- remaining_budget_at_turn_s: 2.655

## R010

Build `PR-1677_build3`, budget 10%, test `org.apache.karaf.itests.WebTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.WebTest
- Rank by value: 15
- Candidate tests: 221
- Selected tests: 17
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 49
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `cache/api/src/main/java/org/apache/karaf/cache/api/CacheService.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/CacheCommandSupport.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Create.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Get.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Invalidate.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/ListCaches.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Put.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/completers/CacheNameCompleter.java`
  - `cache/core/src/main/java/org/apache/karaf/cache/core/Activator.java`
  - `cache/core/src/main/java/org/apache/karaf/cache/core/EhcacheService.java`
- Test duration (s): 8.145
- Budget (s): 143.546
- Budget left when the test was reached (s): 0.027
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 151.663

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 8.145 s but only 0.027 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 8.145
- remaining_budget_at_turn_s: 0.027

## R011

Build `PR-1649_build1`, budget 20%, test `org.apache.karaf.itests.examples.SoapExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.SoapExampleTest
- Rank by value: 17
- Candidate tests: 208
- Selected tests: 29
- History:
  - builds in the history window: 100
  - runs: 98
  - failures: 1
  - failure rate: 0.01020408163265306
  - builds since the last failure: 32
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, -, 0, -
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `profile/src/main/java/org/apache/karaf/profile/assembly/Builder.java`
  - `profile/src/test/java/org/apache/karaf/profile/assembly/BuilderTest.java`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/AssemblyMojo.java`
- Test duration (s): 37.66
- Budget (s): 282.033
- Budget left when the test was reached (s): 15.031
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 304.662

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 98 runs. It needs 37.66 s but only 15.031 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 98 runs
- duration_s: 37.66
- remaining_budget_at_turn_s: 15.031

## R012

Build `PR-1656_build2`, budget 5%, test `org.apache.karaf.itests.examples.JmsExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JmsExampleTest
- Rank by value: 18
- Candidate tests: 212
- Selected tests: 60
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 5
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, -, 0, 0, 0, 1, 0, 0, 0, 0
- History score: 0.014
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not mention or interact with Spring Security or WebSocket features.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 81.706
- Budget (s): 298.116
- Budget left when the test was reached (s): 44.393
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 335.429

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with Spring Security or WebSocket features, and it has only failed once in 97 runs. It needs 81.706 s but only 44.393 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- failures: 1 of 97 runs
- duration_s: 81.706
- remaining_budget_at_turn_s: 44.393

## R013

Build `PR-1548_build1`, budget 20%, test `org.apache.karaf.bundle.command.bundletree.TreeTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.bundletree.TreeTest
- Rank by value: 73
- Candidate tests: 209
- Selected tests: 33
- History:
  - builds in the history window: 100
  - runs: 98
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/src/main/java/org/apache/karaf/config/core/impl/JsonConfigInstaller.java`
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 0.006
- Budget (s): 381.127
- Budget left when the test was reached (s): 0.005
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 381.128

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.006 s, which is very short but still needs 0.005 s of the budget to run, leaving no room for other tests.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.006
- remaining_budget_at_turn_s: 0.005

## R014

Build `PR-1816_build1`, budget 20%, test `org.apache.karaf.config.command.EditCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.EditCommandTest
- Rank by value: 69
- Candidate tests: 111
- Selected tests: 37
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
  - `features/core/src/main/java/org/apache/karaf/features/internal/service/BootFeaturesInstaller.java`
  - `instance/src/main/java/org/apache/karaf/instance/core/internal/InstanceServiceImpl.java`
  - `itests/common/src/main/java/org/apache/karaf/itests/KarafTestSupport.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/mavenresolver/KarafMinimalMonitoredTestSupport.java`
  - `specs/activator/src/main/java/org/apache/karaf/specs/activator/Activator.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/MockCallable.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/MockCallable2.java`
  - `specs/activator/src/test/java/org/apache/karaf/specs/locator/OsgiLocatorTest.java`
  - `specs/java.xml.ws/src/main/java/javax/xml/bind/ContextFinder.java`
- Test duration (s): 0.097
- Budget (s): 17.157
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 17.253

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.097 s, which is less than the remaining budget of 0.001 s when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.097
- remaining_budget_at_turn_s: 0.001

## R015

Build `PR-1840_build4`, budget 5%, test `org.apache.karaf.itests.examples.GraphQLExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.GraphQLExampleTest
- Rank by value: 8
- Candidate tests: 207
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 13
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.031
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the configuration files or features related to Spring versions.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 2.429
- Budget (s): 18.051
- Budget left when the test was reached (s): 2.114
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 18.366

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with the configuration files or features related to Spring versions. It only took 2.429 s to run, and there was enough budget left (2.114 s) when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java
- itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java
- itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java
- duration_s: 2.429
- remaining_budget_at_turn_s: 2.114

## R016

Build `PR-1427_build3`, budget 20%, test `org.apache.karaf.config.command.UpdateCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.UpdateCommandTest
- Rank by value: 69
- Candidate tests: 203
- Selected tests: 48
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified.
- Changed files:
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java`
- Test duration (s): 0.009
- Budget (s): 256.73
- Budget left when the test was reached (s): 0.006
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 256.733

**Justification**

> Skipping it is reasonable: its relevance is 0.0 because it does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified. It only took 0.009 s, which was well within the remaining budget of 0.006 s.

**Cited facts**

- relevance_used: 0.0
- changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
- duration_s: 0.009
- remaining_budget_at_turn_s: 0.006

## R017

Build `PR-1536_build3`, budget 10%, test `org.apache.karaf.itests.examples.JdbcExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JdbcExampleTest
- Rank by value: 16
- Candidate tests: 213
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 74
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 11.954
- Budget (s): 143.69
- Budget left when the test was reached (s): 4.667
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 150.977

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 11.954 s but only 4.667 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 11.954
- remaining_budget_at_turn_s: 4.667

## R018

Build `PR-1701_build1`, budget 10%, test `org.apache.karaf.itests.examples.HttpResourceExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.HttpResourceExampleTest
- Rank by value: 14
- Candidate tests: 215
- Selected tests: 25
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 58
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, -, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/instance.bat`
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/shell.bat`
- Test duration (s): 3.33
- Budget (s): 137.121
- Budget left when the test was reached (s): 0.72
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 139.731

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs. It needs 3.33 s but only 0.72 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 3.33
- remaining_budget_at_turn_s: 0.72

## R019

Build `PR-1624_build3`, budget 20%, test `org.apache.karaf.bundle.command.bundletree.TreeTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.bundletree.TreeTest
- Rank by value: 83
- Candidate tests: 210
- Selected tests: 50
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/command/src/main/java/org/apache/karaf/features/command/StatusCommand.java`
  - `features/command/src/main/java/org/apache/karaf/features/command/completers/FeatureVersionCompleter.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java`
- Test duration (s): 0.006
- Budget (s): 242.548
- Budget left when the test was reached (s): 0.002
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 242.552

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.006 s, which is less than the remaining budget of 0.002 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.006
- remaining_budget_at_turn_s: 0.002

## R020

Build `PR-1814_build2`, budget 10%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 18
- Candidate tests: 207
- Selected tests: 17
- History:
  - builds in the history window: 100
  - runs: 95
  - failures: 2
  - failure rate: 0.021052631578947368
  - builds since the last failure: 13
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/command/src/main/java/org/apache/karaf/config/command/ConfigPropertyCommandSupport.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/EditCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/MetaCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropAppendCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropGetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropSetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/ConfigurationPropertyCompleter.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/MetaCompleter.java`
  - `config/core/src/main/java/org/apache/karaf/config/core/MetaServiceCaller.java`
- Test duration (s): 11.06
- Budget (s): 121.688
- Budget left when the test was reached (s): 0.05
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 132.698

**Justification**

> Skipping it is risky: it has a failure rate of 0.021 and its duration of 11.06 s exceeds the remaining budget of 0.05 s.

**Cited facts**

- failure_rate: 0.021
- duration_s: 11.06
- remaining_budget_at_turn_s: 0.05

## R021

Build `PR-1657_build1`, budget 5%, test `org.apache.karaf.itests.examples.WarExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.WarExampleTest
- Rank by value: 21
- Candidate tests: 215
- Selected tests: 42
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 18
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, -, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 9.014
- Budget (s): 75.818
- Budget left when the test was reached (s): 5.289
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 79.543

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 97 runs. It needs 9.014 s but only 5.289 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 9.014
- remaining_budget_at_turn_s: 5.289

## R022

Build `PR-1725_build1`, budget 20%, test `org.apache.karaf.audit.util.FastDateFormatTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.audit.util.FastDateFormatTest
- Rank by value: 72
- Candidate tests: 217
- Selected tests: 39
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/examples/ConfigExampleTest.java`
- Test duration (s): 0.049
- Budget (s): 223.756
- Budget left when the test was reached (s): 0.003
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 223.802

**Justification**

> Skipping it is reasonable: it has no relevance and its duration is 0.049 s, which fits within the remaining budget of 0.003 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.049
- remaining_budget_at_turn_s: 0.003

## R023

Build `PR-1814_build1`, budget 10%, test `org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest
- Rank by value: 27
- Candidate tests: 211
- Selected tests: 44
- History:
  - builds in the history window: 100
  - runs: 94
  - failures: 1
  - failure rate: 0.010638297872340425
  - builds since the last failure: 76
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.011
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/command/src/main/java/org/apache/karaf/config/command/ConfigPropertyCommandSupport.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/EditCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/MetaCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropAppendCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropGetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropSetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/ConfigurationPropertyCompleter.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/MetaCompleter.java`
  - `config/core/src/main/java/org/apache/karaf/config/core/MetaServiceCaller.java`
- Test duration (s): 16.14
- Budget (s): 93.346
- Budget left when the test was reached (s): 2.474
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 107.012

**Justification**

> Skipping it is risky: it has a failure rate of 0.0106 and its duration of 16.14 s exceeds the remaining budget of 2.474 s.

**Cited facts**

- failures: 1 of 94 runs
- failure_rate: 0.010638297872340425
- duration_s: 16.14
- remaining_budget_at_turn_s: 2.474

## R024

Build `PR-1840_build6`, budget 10%, test `org.apache.karaf.itests.features.Spring52FeaturesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.features.Spring52FeaturesTest
- Rank by value: 47
- Candidate tests: 216
- Selected tests: 55
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 2
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
- History score: 0.032
- Relevance used: 0.2
- Semantic analyzer's reason: The test class does not directly reference or test the new properties added in the BaseTest class.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 10.303
- Budget (s): 186.293
- Budget left when the test was reached (s): 0.149
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 196.447

**Justification**

> Skipping it is risky: its relevance is 0.2 because it does not directly reference or test the new properties added in the BaseTest class, although it has a 1% failure rate in 97 runs. It needs 10.303 s but only 0.149 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.2
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java
- failures: 1 of 97 runs
- duration_s: 10.303
- remaining_budget_at_turn_s: 0.149

## R025

Build `PR-1550_build2`, budget 20%, test `org.apache.karaf.itests.SystemShutdownTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.SystemShutdownTest
- Rank by value: 16
- Candidate tests: 210
- Selected tests: 41
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 69
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with Maven or Karaf features related to Maven.
- Changed files:
  - `manual/src/main/asciidoc/user-guide/urls.adoc`
- Test duration (s): 38.334
- Budget (s): 290.067
- Budget left when the test was reached (s): 33.916
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 294.485

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with Maven or Karaf features related to Maven. It also has a failure rate of 0.021, indicating it is generally stable. However, it needs 38.334 s but only 33.916 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: manual/src/main/asciidoc/user-guide/urls.adoc
- failures: 2 of 97 runs
- failure_rate: 0.021
- duration_s: 38.334
- remaining_budget_at_turn_s: 33.916

## R026

Build `PR-1552_build5`, budget 5%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 12
- Candidate tests: 210
- Selected tests: 22
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 8
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 1, 0, 0, 0, 0, 0, 0, 0
- History score: 0.012
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/src/main/java/org/apache/karaf/config/core/impl/JsonConfigInstaller.java`
  - `config/src/test/java/org/apache/karaf/config/core/impl/JsonConfigInstallerTest.java`
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 8.796
- Budget (s): 58.163
- Budget left when the test was reached (s): 6.637
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 60.322

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 96 runs. It needs 8.796 s but only 6.637 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 8.796
- remaining_budget_at_turn_s: 6.637

## R027

Build `PR-1624_build3`, budget 10%, test `org.apache.karaf.bundle.command.ListServicesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.ListServicesTest
- Rank by value: 68
- Candidate tests: 210
- Selected tests: 38
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/command/src/main/java/org/apache/karaf/features/command/StatusCommand.java`
  - `features/command/src/main/java/org/apache/karaf/features/command/completers/FeatureVersionCompleter.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java`
- Test duration (s): 0.062
- Budget (s): 121.274
- Budget left when the test was reached (s): 0.033
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 121.303

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.062 s, which is less than the remaining budget of 0.033 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.062
- remaining_budget_at_turn_s: 0.033

## R028

Build `PR-1624_build3`, budget 10%, test `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.core.internal.MavenConfigServiceTest
- Rank by value: 70
- Candidate tests: 210
- Selected tests: 38
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/command/src/main/java/org/apache/karaf/features/command/StatusCommand.java`
  - `features/command/src/main/java/org/apache/karaf/features/command/completers/FeatureVersionCompleter.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java`
- Test duration (s): 0.115
- Budget (s): 121.274
- Budget left when the test was reached (s): 0.02
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 121.369

**Justification**

> Skipping it is reasonable: it has no relevance and its duration of 0.115 s is negligible compared to the remaining budget of 0.02 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.115
- remaining_budget_at_turn_s: 0.02

## R029

Build `PR-1627_build5`, budget 20%, test `org.apache.karaf.audit.util.FastDateFormatTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.audit.util.FastDateFormatTest
- Rank by value: 68
- Candidate tests: 209
- Selected tests: 31
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 0.043
- Budget (s): 213.672
- Budget left when the test was reached (s): 0.002
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 213.713

**Justification**

> Skipping it is risky: it has no relevance and its duration is 0.043 s, which is negligible compared to the remaining budget of 0.002 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.043
- remaining_budget_at_turn_s: 0.002

## R030

Build `PR-1497_build1`, budget 10%, test `org.apache.karaf.itests.WebTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.WebTest
- Rank by value: 19
- Candidate tests: 205
- Selected tests: 26
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 52
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java`
- Test duration (s): 7.638
- Budget (s): 105.876
- Budget left when the test was reached (s): 1.015
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 112.499

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 7.638 s but only 1.015 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 7.638
- remaining_budget_at_turn_s: 1.015

## R031

Build `PR-1725_build1`, budget 10%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 15
- Candidate tests: 217
- Selected tests: 30
- History:
  - builds in the history window: 100
  - runs: 98
  - failures: 2
  - failure rate: 0.02040816326530612
  - builds since the last failure: 93
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.02
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the code changes made in MyComponent.java.
- Changed files:
  - `examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/examples/ConfigExampleTest.java`
- Test duration (s): 38.288
- Budget (s): 111.878
- Budget left when the test was reached (s): 1.428
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 148.738

**Justification**

> Skipping it is reasonable: it has a relevance of 0.0 because it does not interact with the code changes made in MyComponent.java. It only took 38.288 s, leaving 1.428 s of the budget, which was not enough to run it.

**Cited facts**

- relevance_used: 0.0
- changed_files: examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java
- duration_s: 38.288
- remaining_budget_at_turn_s: 1.428

## R032

Build `PR-1536_build3`, budget 20%, test `org.apache.karaf.config.command.UpdateCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.UpdateCommandTest
- Rank by value: 72
- Candidate tests: 213
- Selected tests: 34
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 0.057
- Budget (s): 287.38
- Budget left when the test was reached (s): 0.004
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 287.433

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.057 s, which is less than the remaining budget of 0.004 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.057
- remaining_budget_at_turn_s: 0.004

## R033

Build `PR-1656_build1`, budget 20%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 14
- Candidate tests: 211
- Selected tests: 34
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 4
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 1, 0, 0, 0, 1, 0, -, 0
- History score: 0.025
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not involve Spring Security or related features.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 35.628
- Budget (s): 197.844
- Budget left when the test was reached (s): 10.85
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 222.622

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not involve Spring Security or related features, and it only needs 35.628 s, which is well within the remaining budget of 10.85 s.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- duration_s: 35.628
- remaining_budget_at_turn_s: 10.85

## R034

Build `PR-1648_build2`, budget 10%, test `org.apache.karaf.client.ClientConfigTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.client.ClientConfigTest
- Rank by value: 44
- Candidate tests: 137
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `wrapper/src/main/resources/org/apache/karaf/wrapper/internal/unix/karaf-wrapper-java11.conf`
- Test duration (s): 0.32
- Budget (s): 15.176
- Budget left when the test was reached (s): 0.191
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 15.305

**Justification**

> Skipping it is reasonable: it has no relevance and its duration of 0.32 s is negligible compared to the remaining budget of 0.191 s when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.32
- remaining_budget_at_turn_s: 0.191

## R035

Build `PR-1827_build1`, budget 10%, test `org.apache.karaf.itests.examples.ServletExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ServletExampleTest
- Rank by value: 17
- Candidate tests: 200
- Selected tests: 30
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 2
  - failure rate: 0.020833333333333332
  - builds since the last failure: 92
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, -, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the network or socket operations that are modified in the code change.
- Changed files:
  - `main/src/main/java/org/apache/karaf/main/Status.java`
- Test duration (s): 122.415
- Budget (s): 257.199
- Budget left when the test was reached (s): 9.609
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 370.005

**Justification**

> Skipping it is risky: its relevance is 0.1 because it does not interact with the network or socket operations that are modified in the code change, although it has a failure rate of 0.021. It needs 122.415 s but only 9.609 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: main/src/main/java/org/apache/karaf/main/Status.java
- failures: 2 of 96 runs
- failure_rate: 0.021
- duration_s: 122.415
- remaining_budget_at_turn_s: 9.609

## R036

Build `PR-1492_build2`, budget 20%, test `org.apache.karaf.features.ConditionalTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.features.ConditionalTest
- Rank by value: 68
- Candidate tests: 114
- Selected tests: 60
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java`
- Test duration (s): 0.905
- Budget (s): 17.471
- Budget left when the test was reached (s): 0.008
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 18.368

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.905 s, but only 0.008 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.905
- remaining_budget_at_turn_s: 0.008

## R037

Build `PR-1840_build5`, budget 5%, test `org.apache.karaf.itests.JMXSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.JMXSecurityTest
- Rank by value: 36
- Candidate tests: 200
- Selected tests: 46
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 7
  - failure rate: 0.07216494845360824
  - builds since the last failure: 1
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
- History score: 0.172
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with the configuration changes made in the BaseTest class.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 15.97
- Budget (s): 37.324
- Budget left when the test was reached (s): 4.824
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 48.47

**Justification**

> Skipping it is reasonable: it has a relevance of 0.0 because it does not appear to interact with the configuration changes made in the BaseTest class. It only took 15.97 s, leaving 4.824 s of the budget, which was not enough to run it.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java
- duration_s: 15.97
- remaining_budget_at_turn_s: 4.824

## R038

Build `PR-1840_build7`, budget 20%, test `org.apache.karaf.itests.examples.JpaExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JpaExampleTest
- Rank by value: 63
- Candidate tests: 207
- Selected tests: 79
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 3
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 1, 0, 0
- History score: 0.033
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 59.128
- Budget (s): 421.321
- Budget left when the test was reached (s): 0.799
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 479.65

**Justification**

> Skipping it is risky: it has a failure rate of 0.0206 and its duration of 59.128 s exceeds the remaining budget of 0.799 s.

**Cited facts**

- failures: 2 of 97 runs
- failure_rate: 0.020618556701030927
- duration_s: 59.128
- remaining_budget_at_turn_s: 0.799

## R039

Build `PR-1840_build6`, budget 10%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 49
- Candidate tests: 216
- Selected tests: 55
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 2
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
- History score: 0.053
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 25.564
- Budget (s): 186.293
- Budget left when the test was reached (s): 0.149
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 211.708

**Justification**

> Skipping it is risky: it has a failure rate of 0.031 and needs 25.564 s, but only 0.149 s of the budget was left when it was reached.

**Cited facts**

- failures: 3 of 97 runs
- failure_rate: 0.030927835051546393
- duration_s: 25.564
- remaining_budget_at_turn_s: 0.149

## R040

Build `PR-1641_build3`, budget 20%, test `org.apache.karaf.config.core.impl.KarafConfigurationPluginTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.core.impl.KarafConfigurationPluginTest
- Rank by value: 112
- Candidate tests: 116
- Selected tests: 61
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java`
- Test duration (s): 0.006
- Budget (s): 14.15
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 14.156

**Justification**

> Skipping it is reasonable: it has a relevance score of 0.0 and a duration of 0.006 s, which fits exactly within the remaining budget of 0.0 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.006
- remaining_budget_at_turn_s: 0.0

## R041

Build `PR-1550_build2`, budget 10%, test `org.apache.karaf.itests.FelixHttpTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FelixHttpTest
- Rank by value: 14
- Candidate tests: 210
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 6
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
- History score: 0.012
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with Maven or Karaf features related to Maven.
- Changed files:
  - `manual/src/main/asciidoc/user-guide/urls.adoc`
- Test duration (s): 63.274
- Budget (s): 145.034
- Budget left when the test was reached (s): 21.248
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 187.06

**Justification**

> Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with Maven or Karaf features related to Maven, and it only needs 63.274 s but only 21.248 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: manual/src/main/asciidoc/user-guide/urls.adoc
- duration_s: 63.274
- remaining_budget_at_turn_s: 21.248

## R042

Build `PR-1725_build1`, budget 5%, test `org.apache.karaf.itests.examples.GraphQLExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.GraphQLExampleTest
- Rank by value: 12
- Candidate tests: 217
- Selected tests: 32
- History:
  - builds in the history window: 100
  - runs: 94
  - failures: 4
  - failure rate: 0.0425531914893617
  - builds since the last failure: 30
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, -, -, 0, 0, 0, 0
- History score: 0.043
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the code changes made in MyComponent.java.
- Changed files:
  - `examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/examples/ConfigExampleTest.java`
- Test duration (s): 62.081
- Budget (s): 55.939
- Budget left when the test was reached (s): 20.245
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 97.775

**Justification**

> Skipping it is reasonable: it has a relevance of 0.0 because it does not interact with the code changes made in MyComponent.java. It needs 62.081 s but only 20.245 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java
- duration_s: 62.081
- remaining_budget_at_turn_s: 20.245

## R043

Build `PR-1840_build4`, budget 10%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 18
- Candidate tests: 207
- Selected tests: 24
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 90
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 2.996
- Budget (s): 36.102
- Budget left when the test was reached (s): 0.047
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 39.051

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration is 2.996 s, but only 0.047 s of the budget was left when it was reached.

**Cited facts**

- failures: 1 of 97 runs
- failure_rate: 0.010309278350515464
- duration_s: 2.996
- remaining_budget_at_turn_s: 0.047

## R044

Build `PR-1626_build2`, budget 20%, test `org.apache.karaf.client.ClientConfigTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.client.ClientConfigTest
- Rank by value: 68
- Candidate tests: 202
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java`
  - `manual/src/main/asciidoc/user-guide/instances.adoc`
- Test duration (s): 0.022
- Budget (s): 234.772
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 234.793

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.022 s, which is negligible compared to the remaining budget of 0.001 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.022
- remaining_budget_at_turn_s: 0.001

## R045

Build `PR-1536_build3`, budget 20%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 21
- Candidate tests: 213
- Selected tests: 34
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 66
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 44.355
- Budget (s): 287.38
- Budget left when the test was reached (s): 4.022
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 327.713

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration of 44.355 s exceeds the remaining budget of 4.022 s.

**Cited facts**

- failures: 1 of 97 runs
- failure_rate: 0.010309278350515464
- duration_s: 44.355
- remaining_budget_at_turn_s: 4.022

## R046

Build `PR-1552_build4`, budget 5%, test `org.apache.karaf.itests.examples.ConfigExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ConfigExampleTest
- Rank by value: 17
- Candidate tests: 206
- Selected tests: 29
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 47
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/src/main/java/org/apache/karaf/config/core/impl/JsonConfigInstaller.java`
  - `config/src/test/java/org/apache/karaf/config/core/impl/JsonConfigInstallerTest.java`
  - `manual/src/main/asciidoc/user-guide/configuration.adoc`
- Test duration (s): 46.342
- Budget (s): 183.702
- Budget left when the test was reached (s): 7.583
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 222.461

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 46.342 s but only 7.583 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 46.342
- remaining_budget_at_turn_s: 7.583

## R047

Build `PR-1462_build1`, budget 20%, test `org.apache.karaf.event.service.EventCollectorTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.event.service.EventCollectorTest
- Rank by value: 78
- Candidate tests: 130
- Selected tests: 54
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
- Test duration (s): 0.011
- Budget (s): 19.543
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 19.554

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.011 s, which is less than the remaining budget of 0.0 s when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.011
- remaining_budget_at_turn_s: 0.0

## R048

Build `PR-1627_build5`, budget 5%, test `org.apache.karaf.itests.examples.JpaExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JpaExampleTest
- Rank by value: 14
- Candidate tests: 209
- Selected tests: 33
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 85
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 26.235
- Budget (s): 53.418
- Budget left when the test was reached (s): 2.273
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 77.38

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 100 runs. It needs 26.235 s but only 2.273 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 100 runs
- duration_s: 26.235
- remaining_budget_at_turn_s: 2.273

## R049

Build `PR-1840_build6`, budget 20%, test `org.apache.karaf.itests.JmsTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.JmsTest
- Rank by value: 67
- Candidate tests: 216
- Selected tests: 86
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 2
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
- History score: 0.042
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 42.563
- Budget (s): 372.586
- Budget left when the test was reached (s): 4.108
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 411.041

**Justification**

> Skipping it is risky: it has a failure rate of 0.0206 and its duration of 42.563 s exceeds the remaining budget of 4.108 s.

**Cited facts**

- failures: 2 of 97 runs
- failure_rate: 0.020618556701030927
- duration_s: 42.563
- remaining_budget_at_turn_s: 4.108

## R050

Build `PR-1427_build3`, budget 10%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 12
- Candidate tests: 203
- Selected tests: 52
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 7
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 1, 0, 0, 0, 0, 0, 0
- History score: 0.012
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with SSH sessions or the session management code that was changed.
- Changed files:
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java`
- Test duration (s): 44.824
- Budget (s): 128.365
- Budget left when the test was reached (s): 15.777
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 157.412

**Justification**

> Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with SSH sessions or the session management code that was changed. It only needs 44.824 s but only 15.777 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
- duration_s: 44.824
- remaining_budget_at_turn_s: 15.777

## R051

Build `PR-1501_build2`, budget 10%, test `org.apache.karaf.itests.features.Spring43FeaturesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.features.Spring43FeaturesTest
- Rank by value: 18
- Candidate tests: 204
- Selected tests: 70
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 52
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java`
  - `obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java`
- Test duration (s): 44.836
- Budget (s): 150.335
- Budget left when the test was reached (s): 8.743
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 186.428

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 44.836 s but only 8.743 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 44.836
- remaining_budget_at_turn_s: 8.743

## R052

Build `PR-1462_build2`, budget 10%, test `org.apache.karaf.itests.features.Spring43FeaturesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.features.Spring43FeaturesTest
- Rank by value: 14
- Candidate tests: 205
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 6
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 1, 0, 0, 0, 0, -
- History score: 0.015
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java`
- Test duration (s): 11.267
- Budget (s): 82.687
- Budget left when the test was reached (s): 8.038
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 85.916

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 11.267 s but only 8.038 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 11.267
- remaining_budget_at_turn_s: 8.038

## R053

Build `PR-1627_build5`, budget 5%, test `org.apache.karaf.audit.util.FastDateFormatTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.audit.util.FastDateFormatTest
- Rank by value: 68
- Candidate tests: 209
- Selected tests: 33
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 0.043
- Budget (s): 53.418
- Budget left when the test was reached (s): 0.022
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 53.439

**Justification**

> Skipping it is risky: it has no relevance and its duration is 0.043 s, which is less than the remaining budget of 0.022 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.043
- remaining_budget_at_turn_s: 0.022

## R054

Build `PR-1550_build2`, budget 10%, test `org.apache.karaf.itests.JmsTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.JmsTest
- Rank by value: 13
- Candidate tests: 210
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 32
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with Maven or Karaf features related to Maven.
- Changed files:
  - `manual/src/main/asciidoc/user-guide/urls.adoc`
- Test duration (s): 59.734
- Budget (s): 145.034
- Budget left when the test was reached (s): 21.248
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 183.52

**Justification**

> Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with Maven or Karaf features related to Maven, and it only needs 59.734 s but only 21.248 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: manual/src/main/asciidoc/user-guide/urls.adoc
- duration_s: 59.734
- remaining_budget_at_turn_s: 21.248

## R055

Build `PR-1501_build3`, budget 20%, test `org.apache.karaf.config.command.EditCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.EditCommandTest
- Rank by value: 68
- Candidate tests: 206
- Selected tests: 40
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java`
  - `obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java`
- Test duration (s): 0.003
- Budget (s): 252.697
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 252.699

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.003 s, which is negligible compared to the remaining budget of 0.001 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.003
- remaining_budget_at_turn_s: 0.001

## R056

Build `PR-1462_build1`, budget 5%, test `org.apache.karaf.bundle.command.ListServicesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.ListServicesTest
- Rank by value: 47
- Candidate tests: 130
- Selected tests: 42
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
- Test duration (s): 0.062
- Budget (s): 4.886
- Budget left when the test was reached (s): 0.03
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 4.918

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.062 s, which is very short but still exceeds the remaining budget of 0.03 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.062
- remaining_budget_at_turn_s: 0.03

## R057

Build `PR-1641_build3`, budget 10%, test `org.apache.karaf.config.core.impl.JsonConfigInstallerTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.core.impl.JsonConfigInstallerTest
- Rank by value: 111
- Candidate tests: 116
- Selected tests: 44
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java`
- Test duration (s): 0.118
- Budget (s): 7.075
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 7.193

**Justification**

> Skipping it is reasonable: it has a relevance score of 0.0 and a duration of 0.118 s, which fits within the remaining budget of 0.0 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.118
- remaining_budget_at_turn_s: 0.0

## R058

Build `PR-1427_build2`, budget 20%, test `org.apache.karaf.main.MainLockingTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.main.MainLockingTest
- Rank by value: 14
- Candidate tests: 208
- Selected tests: 49
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 54
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java`
- Test duration (s): 24.366
- Budget (s): 302.697
- Budget left when the test was reached (s): 18.879
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 308.184

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 100 runs. It needs 24.366 s but only 18.879 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 100 runs
- duration_s: 24.366
- remaining_budget_at_turn_s: 18.879

## R059

Build `PR-1627_build4`, budget 5%, test `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.core.internal.MavenConfigServiceTest
- Rank by value: 70
- Candidate tests: 210
- Selected tests: 29
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 0.056
- Budget (s): 54.789
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 54.844

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.056 s, which is very short but still needs 54.844 s of the budget to run, leaving only 0.001 s remaining.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.056
- remaining_budget_at_turn_s: 0.001
- fits_if_budget_s: 54.844

## R060

Build `PR-1497_build1`, budget 5%, test `org.apache.karaf.itests.examples.SoapExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.SoapExampleTest
- Rank by value: 9
- Candidate tests: 205
- Selected tests: 31
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 49
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.031
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the JaasHelper class or its methods.
- Changed files:
  - `util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java`
- Test duration (s): 29.258
- Budget (s): 52.938
- Budget left when the test was reached (s): 10.722
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 71.474

**Justification**

> Skipping it is reasonable: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it has a failure rate of 0.031. It needs 29.258 s but only 10.722 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
- failures: 3 of 97 runs
- failure_rate: 0.031
- duration_s: 29.258
- remaining_budget_at_turn_s: 10.722

## R061

Build `PR-1648_build2`, budget 10%, test `org.apache.karaf.config.command.EditCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.EditCommandTest
- Rank by value: 54
- Candidate tests: 137
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `wrapper/src/main/resources/org/apache/karaf/wrapper/internal/unix/karaf-wrapper-java11.conf`
- Test duration (s): 0.058
- Budget (s): 15.176
- Budget left when the test was reached (s): 0.019
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 15.215

**Justification**

> Skipping it is reasonable: it has no relevance and its duration is 0.058 s, which fits within the remaining budget of 0.019 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.058
- remaining_budget_at_turn_s: 0.019

## R062

Build `PR-1627_build4`, budget 10%, test `org.apache.karaf.bundle.command.ListServicesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.ListServicesTest
- Rank by value: 68
- Candidate tests: 210
- Selected tests: 21
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/DisabledLogoutTest.java`
  - `manual/src/main/asciidoc/user-guide/console.adoc`
  - `manual/src/main/asciidoc/user-guide/remote.adoc`
  - `shell/commands/src/main/java/org/apache/karaf/shell/commands/impl/LogoutAction.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/api/console/Session.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/impl/console/ConsoleSessionImpl.java`
  - `shell/core/src/main/java/org/apache/karaf/shell/support/ShellUtil.java`
- Test duration (s): 0.102
- Budget (s): 109.578
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 109.679

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.102 s, which is very short but still exceeds the remaining budget of 0.001 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.102
- remaining_budget_at_turn_s: 0.001

## R063

Build `PR-1492_build2`, budget 10%, test `org.apache.karaf.features.FeaturesServiceTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.features.FeaturesServiceTest
- Rank by value: 67
- Candidate tests: 114
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh`
  - `tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java`
- Test duration (s): 0.068
- Budget (s): 8.735
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 8.803

**Justification**

> Skipping it is reasonable: it has no relevance and its duration is 0.068 s, which fits within the remaining budget of 0.0 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.068
- remaining_budget_at_turn_s: 0.0

## R064

Build `PR-1648_build2`, budget 5%, test `org.apache.karaf.bundle.command.bundletree.TreeTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.command.bundletree.TreeTest
- Rank by value: 42
- Candidate tests: 137
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 99
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `wrapper/src/main/resources/org/apache/karaf/wrapper/internal/unix/karaf-wrapper-java11.conf`
- Test duration (s): 0.005
- Budget (s): 7.588
- Budget left when the test was reached (s): 0.005
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 7.588

**Justification**

> Skipping it is reasonable: it has no relevance and its duration is 0.005 s, which fits exactly into the remaining budget of 0.005 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.005
- remaining_budget_at_turn_s: 0.005

## R065

Build `PR-1782_build2`, budget 20%, test `org.apache.karaf.itests.examples.JdbcExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JdbcExampleTest
- Rank by value: 29
- Candidate tests: 204
- Selected tests: 45
- History:
  - builds in the history window: 100
  - runs: 95
  - failures: 3
  - failure rate: 0.031578947368421054
  - builds since the last failure: 25
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.032
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the karaf.bat script or any of the Java 9/10 specific options removed in the code change.
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
- Test duration (s): 730.33
- Budget (s): 346.74
- Budget left when the test was reached (s): 1.435
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 1075.635

**Justification**

> Skipping it is risky: its relevance is 0.1 because it does not interact with the karaf.bat script or Java 9/10 specific options, and it needs 730.33 s but only 1.435 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat
- duration_s: 730.33
- remaining_budget_at_turn_s: 1.435

## R066

Build `PR-1645_build2`, budget 5%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 10
- Candidate tests: 203
- Selected tests: 23
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 48
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, -, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/Book.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/BookRepository.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/GraphQLSchemaProvider.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-commands/src/main/java/org/apache/karaf/examples/graphql/commands/Query.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/java/org/apache/karaf/examples/graphql/core/BookSchemaProvider.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/java/org/apache/karaf/examples/graphql/core/InMemoryBookRepository.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/resources/schema.graphql`
  - `examples/karaf-graphql-example/karaf-graphql-example-scr-servlet/src/main/java/org/apache/karaf/examples/graphql/servlet/ExampleGraphQLHttpServlet.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-websocket/src/main/java/org/apache/karaf/examples/graphql/websocket/GraphQLWebSocketExample.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-websocket/src/main/java/org/apache/karaf/examples/graphql/websocket/GraphQLWebSocketServlet.java`
- Test duration (s): 9.789
- Budget (s): 56.2
- Budget left when the test was reached (s): 5.98
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 60.009

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration is 9.789 s, but only 5.98 s of the budget was left when it was reached.

**Cited facts**

- failure_rate: 0.010309278350515464
- duration_s: 9.789
- remaining_budget_at_turn_s: 5.98

## R067

Build `PR-1782_build2`, budget 5%, test `org.apache.karaf.itests.examples.RestExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.RestExampleTest
- Rank by value: 25
- Candidate tests: 204
- Selected tests: 37
- History:
  - builds in the history window: 100
  - runs: 95
  - failures: 2
  - failure rate: 0.021052631578947368
  - builds since the last failure: 47
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the karaf.bat script or any of the Java 9/10 specific flags that were removed.
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
- Test duration (s): 87.131
- Budget (s): 86.685
- Budget left when the test was reached (s): 6.915
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 166.901

**Justification**

> Skipping it is risky: its relevance is 0.1 because it does not interact with the karaf.bat script or Java 9/10 specific flags, and it failed 2 times in 95 runs. It needs 87.131 s but only 6.915 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat
- failures: 2 of 95 runs
- duration_s: 87.131
- remaining_budget_at_turn_s: 6.915

## R068

Build `PR-1536_build1`, budget 20%, test `org.apache.karaf.itests.examples.ConfigExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ConfigExampleTest
- Rank by value: 22
- Candidate tests: 213
- Selected tests: 36
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 22
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 63.013
- Budget (s): 259.344
- Budget left when the test was reached (s): 3.564
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 318.793

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential issues. It needs 63.013 s but only 3.564 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 63.013
- remaining_budget_at_turn_s: 3.564

## R069

Build `PR-1840_build7`, budget 5%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 37
- Candidate tests: 207
- Selected tests: 38
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 3
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 1, 0, 0
- History score: 0.044
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 19.621
- Budget (s): 105.33
- Budget left when the test was reached (s): 0.69
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 124.261

**Justification**

> Skipping it is risky: it has a failure rate of 0.0309 and its duration of 19.621 s exceeds the remaining budget of 0.69 s.

**Cited facts**

- failures: 3 of 97 runs
- failure_rate: 0.030927835051546393
- duration_s: 19.621
- remaining_budget_at_turn_s: 0.69

## R070

Build `PR-1814_build2`, budget 5%, test `org.apache.karaf.itests.EquinoxTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.EquinoxTest
- Rank by value: 15
- Candidate tests: 207
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 95
  - failures: 1
  - failure rate: 0.010526315789473684
  - builds since the last failure: 64
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.011
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/command/src/main/java/org/apache/karaf/config/command/ConfigPropertyCommandSupport.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/EditCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/MetaCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropAppendCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropGetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropSetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/ConfigurationPropertyCompleter.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/MetaCompleter.java`
  - `config/core/src/main/java/org/apache/karaf/config/core/MetaServiceCaller.java`
- Test duration (s): 1.222
- Budget (s): 60.844
- Budget left when the test was reached (s): 0.667
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 61.399

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 95 runs, indicating potential issues. It needs 1.222 s but only 0.667 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 95 runs
- duration_s: 1.222
- remaining_budget_at_turn_s: 0.667

## R071

Build `PR-1626_build2`, budget 10%, test `org.apache.karaf.itests.FeatureTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.FeatureTest
- Rank by value: 10
- Candidate tests: 202
- Selected tests: 23
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 88
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java`
  - `manual/src/main/asciidoc/user-guide/instances.adoc`
- Test duration (s): 8.954
- Budget (s): 117.386
- Budget left when the test was reached (s): 0.256
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 126.084

**Justification**

> Skipping it is risky: it has a failure rate of 0.01 and its duration of 8.954 s exceeds the remaining budget of 0.256 s.

**Cited facts**

- failures: 1 of 100 runs
- failure_rate: 0.01
- duration_s: 8.954
- remaining_budget_at_turn_s: 0.256

## R072

Build `PR-1656_build1`, budget 5%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 14
- Candidate tests: 211
- Selected tests: 25
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 4
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 1, 0, 0, 0, 1, 0, -, 0
- History score: 0.025
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not involve Spring Security or related features.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 35.628
- Budget (s): 49.461
- Budget left when the test was reached (s): 2.84
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 82.249

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not involve Spring Security or related features, and it only needs 35.628 s but only 2.84 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- duration_s: 35.628
- remaining_budget_at_turn_s: 2.84

## R073

Build `PR-1642_build1`, budget 5%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 15
- Candidate tests: 210
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 22
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java`
  - `features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java`
- Test duration (s): 9.623
- Budget (s): 54.328
- Budget left when the test was reached (s): 1.553
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 62.398

**Justification**

> Skipping it is risky: it has a low relevance of 0.0 and has failed once in 100 runs. It needs 9.623 s but only 1.553 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 100 runs
- duration_s: 9.623
- remaining_budget_at_turn_s: 1.553

## R074

Build `PR-1462_build2`, budget 5%, test `org.apache.karaf.itests.examples.WarExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.WarExampleTest
- Rank by value: 12
- Candidate tests: 205
- Selected tests: 28
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 15
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, -
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java`
- Test duration (s): 5.198
- Budget (s): 41.344
- Budget left when the test was reached (s): 3.203
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 43.339

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 5.198 s but only 3.203 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 5.198
- remaining_budget_at_turn_s: 3.203

## R075

Build `PR-1497_build1`, budget 5%, test `org.apache.karaf.itests.examples.ServletExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ServletExampleTest
- Rank by value: 13
- Candidate tests: 205
- Selected tests: 31
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 49
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.031
- Relevance used: 0.1
- Semantic analyzer's reason: The test class does not appear to interact with the JaasHelper class or its methods.
- Changed files:
  - `util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java`
- Test duration (s): 66.297
- Budget (s): 52.938
- Budget left when the test was reached (s): 6.939
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 112.296

**Justification**

> Skipping it is risky: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it failed 3 times in 97 runs. It needs 66.297 s but only 6.939 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.1
- changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
- failures: 3 of 97 runs
- duration_s: 66.297
- remaining_budget_at_turn_s: 6.939

## R076

Build `PR-1827_build1`, budget 20%, test `org.apache.karaf.audit.util.FastDateFormatTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.audit.util.FastDateFormatTest
- Rank by value: 71
- Candidate tests: 200
- Selected tests: 42
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `main/src/main/java/org/apache/karaf/main/Status.java`
- Test duration (s): 0.063
- Budget (s): 514.397
- Budget left when the test was reached (s): 0.015
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 514.445

**Justification**

> Skipping it is reasonable: it has no relevance and its duration is 0.063 s, which fits within the remaining budget of 0.015 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.063
- remaining_budget_at_turn_s: 0.015

## R077

Build `PR-1427_build3`, budget 20%, test `org.apache.karaf.itests.examples.ServletExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ServletExampleTest
- Rank by value: 15
- Candidate tests: 203
- Selected tests: 48
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 29
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with SSH or session management, which are the primary changes in the provided code diff.
- Changed files:
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java`
- Test duration (s): 103.436
- Budget (s): 256.73
- Budget left when the test was reached (s): 51.897
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 308.269

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with SSH or session management, which are the primary changes in the provided code diff. It also has a failure rate of 0.021, indicating it is relatively stable. It needs 103.436 s but only 51.897 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
- failures: 2 of 97 runs
- failure_rate: 0.021
- duration_s: 103.436
- remaining_budget_at_turn_s: 51.897

## R078

Build `PR-1827_build1`, budget 10%, test `org.apache.karaf.itests.examples.JpaExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JpaExampleTest
- Rank by value: 28
- Candidate tests: 200
- Selected tests: 30
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 30
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, -, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `main/src/main/java/org/apache/karaf/main/Status.java`
- Test duration (s): 53.005
- Budget (s): 257.199
- Budget left when the test was reached (s): 3.178
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 307.026

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential issues. It needs 53.005 s but only 3.178 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 96 runs
- duration_s: 53.005
- remaining_budget_at_turn_s: 3.178

## R079

Build `PR-1626_build2`, budget 5%, test `org.apache.karaf.itests.JmsTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.JmsTest
- Rank by value: 7
- Candidate tests: 202
- Selected tests: 26
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 4
  - failure rate: 0.04
  - builds since the last failure: 55
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.04
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with the newly added PackageCommand class.
- Changed files:
  - `instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java`
  - `manual/src/main/asciidoc/user-guide/instances.adoc`
- Test duration (s): 54.386
- Budget (s): 58.693
- Budget left when the test was reached (s): 9.203
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 103.876

**Justification**

> Skipping it is reasonable: its relevance is 0.0 because it does not interact with the newly added PackageCommand class, and it only needs 54.386 s while 9.203 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
- duration_s: 54.386
- remaining_budget_at_turn_s: 9.203

## R080

Build `PR-1462_build1`, budget 5%, test `org.apache.karaf.config.core.impl.JsonConfigInstallerTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.core.impl.JsonConfigInstallerTest
- Rank by value: 40
- Candidate tests: 130
- Selected tests: 42
- History:
  - builds in the history window: 100
  - runs: 90
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
- Test duration (s): 0.169
- Budget (s): 4.886
- Budget left when the test was reached (s): 0.117
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 4.938

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.169 s, which is very short but still needs 0.117 s of the remaining budget, leaving only 0.048 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.169
- remaining_budget_at_turn_s: 0.117

## R081

Build `PR-1645_build2`, budget 10%, test `org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest
- Rank by value: 11
- Candidate tests: 203
- Selected tests: 18
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 18
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/Book.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/BookRepository.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-api/src/main/java/org/apache/karaf/examples/graphql/api/GraphQLSchemaProvider.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-commands/src/main/java/org/apache/karaf/examples/graphql/commands/Query.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/java/org/apache/karaf/examples/graphql/core/BookSchemaProvider.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/java/org/apache/karaf/examples/graphql/core/InMemoryBookRepository.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-core/src/main/resources/schema.graphql`
  - `examples/karaf-graphql-example/karaf-graphql-example-scr-servlet/src/main/java/org/apache/karaf/examples/graphql/servlet/ExampleGraphQLHttpServlet.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-websocket/src/main/java/org/apache/karaf/examples/graphql/websocket/GraphQLWebSocketExample.java`
  - `examples/karaf-graphql-example/karaf-graphql-example-websocket/src/main/java/org/apache/karaf/examples/graphql/websocket/GraphQLWebSocketServlet.java`
- Test duration (s): 10.992
- Budget (s): 112.4
- Budget left when the test was reached (s): 0.446
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 122.946

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 100 runs, indicating potential issues. It needs 10.992 s but only 0.446 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 100 runs
- duration_s: 10.992
- remaining_budget_at_turn_s: 0.446

## R082

Build `PR-1656_build1`, budget 5%, test `org.apache.karaf.itests.XATest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.XATest
- Rank by value: 7
- Candidate tests: 211
- Selected tests: 25
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 17
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.031
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with Spring Security or related features, which are the focus of the code change.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 26.191
- Budget (s): 49.461
- Budget left when the test was reached (s): 23.313
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 52.339

**Justification**

> Skipping it is reasonable: its relevance is 0.0 because it does not interact with Spring Security or related features, which are the focus of the code change. It only needs 26.191 s but only 23.313 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- duration_s: 26.191
- remaining_budget_at_turn_s: 23.313

## R083

Build `PR-1656_build1`, budget 10%, test `org.apache.karaf.itests.XATest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.XATest
- Rank by value: 7
- Candidate tests: 211
- Selected tests: 29
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 3
  - failure rate: 0.030927835051546393
  - builds since the last failure: 17
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.031
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with Spring Security or related features, which are the focus of the code change.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 26.191
- Budget (s): 98.922
- Budget left when the test was reached (s): 7.142
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 117.971

**Justification**

> Skipping it is reasonable: its relevance is 0.0 because it does not interact with Spring Security or related features, which are the focus of the code change. It only needs 26.191 s but only 7.142 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- duration_s: 26.191
- remaining_budget_at_turn_s: 7.142

## R084

Build `PR-1626_build2`, budget 20%, test `org.apache.karaf.config.command.EditCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.EditCommandTest
- Rank by value: 69
- Candidate tests: 202
- Selected tests: 27
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java`
  - `manual/src/main/asciidoc/user-guide/instances.adoc`
- Test duration (s): 0.008
- Budget (s): 234.772
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 234.779

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.008 s, which is negligible compared to the remaining budget of 0.001 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.008
- remaining_budget_at_turn_s: 0.001

## R085

Build `PR-1536_build1`, budget 5%, test `org.apache.karaf.itests.SystemShutdownTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.SystemShutdownTest
- Rank by value: 16
- Candidate tests: 213
- Selected tests: 31
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 2
  - failure rate: 0.020833333333333332
  - builds since the last failure: 48
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.021
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not interact with logging configurations or services.
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 35.098
- Budget (s): 64.836
- Budget left when the test was reached (s): 9.167
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 90.767

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with logging configurations or services, and it only needs 35.098 s but only 9.167 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- duration_s: 35.098
- remaining_budget_at_turn_s: 9.167

## R086

Build `PR-1656_build1`, budget 10%, test `org.apache.karaf.itests.examples.WarExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.WarExampleTest
- Rank by value: 11
- Candidate tests: 211
- Selected tests: 29
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 15
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 5.056
- Budget (s): 98.922
- Budget left when the test was reached (s): 4.211
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 99.767

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 97 runs. It needs 5.056 s but only 4.211 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 5.056
- remaining_budget_at_turn_s: 4.211

## R087

Build `PR-1725_build1`, budget 20%, test `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.bundle.core.internal.MavenConfigServiceTest
- Rank by value: 75
- Candidate tests: 217
- Selected tests: 39
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `examples/karaf-config-example/karaf-config-example-scr/src/main/java/org/apache/karaf/example/config/scr/MyComponent.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/examples/ConfigExampleTest.java`
- Test duration (s): 0.061
- Budget (s): 223.756
- Budget left when the test was reached (s): 0.003
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 223.814

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.061 s, which is less than the remaining budget of 0.003 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.061
- remaining_budget_at_turn_s: 0.003

## R088

Build `PR-1536_build2`, budget 20%, test `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest
- Rank by value: 21
- Candidate tests: 212
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 96
  - failures: 1
  - failure rate: 0.010416666666666666
  - builds since the last failure: 51
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java`
  - `log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java`
  - `log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java`
  - `manual/src/main/asciidoc/user-guide/log.adoc`
- Test duration (s): 44.779
- Budget (s): 236.706
- Budget left when the test was reached (s): 11.306
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 270.179

**Justification**

> Skipping it is risky: it has a failure rate of 0.0104 and its duration of 44.779 s exceeds the remaining budget of 11.306 s.

**Cited facts**

- failures: 1 of 96 runs
- failure_rate: 0.010416666666666666
- duration_s: 44.779
- remaining_budget_at_turn_s: 11.306

## R089

Build `PR-1626_build3`, budget 20%, test `org.apache.karaf.config.command.EditCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.EditCommandTest
- Rank by value: 67
- Candidate tests: 205
- Selected tests: 30
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java`
  - `manual/src/main/asciidoc/user-guide/instances.adoc`
- Test duration (s): 0.007
- Budget (s): 210.354
- Budget left when the test was reached (s): 0.005
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 210.356

**Justification**

> Skipping it is risky: it has no relevance score and its duration is 0.007 s, which is less than the remaining budget of 0.005 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.007
- remaining_budget_at_turn_s: 0.005

## R090

Build `PR-1641_build4`, budget 20%, test `org.apache.karaf.config.command.UpdateCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.UpdateCommandTest
- Rank by value: 78
- Candidate tests: 217
- Selected tests: 41
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java`
- Test duration (s): 0.055
- Budget (s): 444.817
- Budget left when the test was reached (s): 0.001
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 444.871

**Justification**

> Skipping it is risky: it has no relevance and its duration is 0.055 s, which is less than the remaining budget of 0.001 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.055
- remaining_budget_at_turn_s: 0.001

## R091

Build `PR-1462_build2`, budget 5%, test `org.apache.karaf.itests.WebTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.WebTest
- Rank by value: 13
- Candidate tests: 205
- Selected tests: 28
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 15
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, -
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java`
- Test duration (s): 6.387
- Budget (s): 41.344
- Budget left when the test was reached (s): 3.203
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 44.528

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 6.387 s but only 3.203 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 6.387
- remaining_budget_at_turn_s: 3.203

## R092

Build `PR-1814_build1`, budget 5%, test `org.apache.karaf.itests.ssh.JaasSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.JaasSshCommandSecurityTest
- Rank by value: 21
- Candidate tests: 211
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 94
  - failures: 1
  - failure rate: 0.010638297872340425
  - builds since the last failure: 79
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.011
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `config/command/src/main/java/org/apache/karaf/config/command/ConfigPropertyCommandSupport.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/EditCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/MetaCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropAppendCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropGetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/PropSetCommand.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/ConfigurationPropertyCompleter.java`
  - `config/command/src/main/java/org/apache/karaf/config/command/completers/MetaCompleter.java`
  - `config/core/src/main/java/org/apache/karaf/config/core/MetaServiceCaller.java`
- Test duration (s): 4.442
- Budget (s): 46.673
- Budget left when the test was reached (s): 0.04
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 51.075

**Justification**

> Skipping it is risky: it has a failure rate of 0.0106 and its duration of 4.442 s exceeds the remaining budget of 0.04 s.

**Cited facts**

- failures: 1 of 94 runs
- failure_rate: 0.010638297872340425
- duration_s: 4.442
- remaining_budget_at_turn_s: 0.04

## R093

Build `PR-1462_build2`, budget 10%, test `org.apache.karaf.itests.examples.ServletExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.ServletExampleTest
- Rank by value: 10
- Candidate tests: 205
- Selected tests: 20
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 4
  - failure rate: 0.041237113402061855
  - builds since the last failure: 12
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, -
- History score: 0.041
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with the changed code in Main.java or Activator.java.
- Changed files:
  - `client/src/main/java/org/apache/karaf/client/Main.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java`
  - `shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java`
  - `shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java`
- Test duration (s): 58.216
- Budget (s): 82.687
- Budget left when the test was reached (s): 19.623
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 121.28

**Justification**

> Skipping it is reasonable: its relevance is 0.0 because it does not appear to interact with the changed code in Main.java or Activator.java, and it has a failure rate of 0.041237113402061855 over 97 runs. It needs 58.216 s but only 19.623 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: client/src/main/java/org/apache/karaf/client/Main.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
- failures: 4 of 97 runs
- duration_s: 58.216
- remaining_budget_at_turn_s: 19.623

## R094

Build `PR-1641_build4`, budget 5%, test `org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest
- Rank by value: 13
- Candidate tests: 217
- Selected tests: 26
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 1
  - failure rate: 0.01
  - builds since the last failure: 8
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 1, 0, 0, 0, 0, 0, 0, 0
- History score: 0.011
- Relevance used: 0.0
- Semantic analyzer's reason: The test class does not appear to interact with the ASMProxyFactory or any related classes.
- Changed files:
  - `services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java`
- Test duration (s): 9.236
- Budget (s): 111.204
- Budget left when the test was reached (s): 2.337
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 118.103

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with the ASMProxyFactory or related classes. It also has a recent failure rate of 0.01, indicating it might be flaky. It needs 9.236 s but only 2.337 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- changed_files: services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java
- failures: 1 of 100 runs
- failure_rate: 0.01
- duration_s: 9.236
- remaining_budget_at_turn_s: 2.337

## R095

Build `PR-1641_build3`, budget 20%, test `org.apache.karaf.config.command.UpdateCommandTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.config.command.UpdateCommandTest
- Rank by value: 109
- Candidate tests: 116
- Selected tests: 61
- History:
  - builds in the history window: 100
  - runs: 100
  - failures: 0
  - failure rate: 0.0
  - builds since the last failure: none
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.0
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `services/interceptor/impl/src/main/java/org/apache/karaf/service/interceptor/impl/runtime/proxy/AsmProxyFactory.java`
- Test duration (s): 0.006
- Budget (s): 14.15
- Budget left when the test was reached (s): 0.0
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 14.156

**Justification**

> Skipping it is reasonable: it has a relevance score of 0.0 and a duration of 0.006 s, which fits exactly within the remaining budget of 0.0 s.

**Cited facts**

- relevance_used: 0.0
- duration_s: 0.006
- remaining_budget_at_turn_s: 0.0

## R096

Build `PR-1782_build2`, budget 5%, test `org.apache.karaf.itests.ssh.ShellCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.ShellCommandSecurityTest
- Rank by value: 24
- Candidate tests: 204
- Selected tests: 37
- History:
  - builds in the history window: 100
  - runs: 94
  - failures: 1
  - failure rate: 0.010638297872340425
  - builds since the last failure: 44
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.011
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `assemblies/features/base/src/main/filtered-resources/resources/bin/karaf.bat`
- Test duration (s): 7.796
- Budget (s): 86.685
- Budget left when the test was reached (s): 6.915
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 87.566

**Justification**

> Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 94 runs. It needs 7.796 s but only 6.915 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 94 runs
- duration_s: 7.796
- remaining_budget_at_turn_s: 6.915

## R097

Build `PR-1840_build6`, budget 20%, test `org.apache.karaf.itests.examples.JpaExampleTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.examples.JpaExampleTest
- Rank by value: 70
- Candidate tests: 216
- Selected tests: 86
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 2
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
- History score: 0.042
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 60.056
- Budget (s): 372.586
- Budget left when the test was reached (s): 4.108
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 428.534

**Justification**

> Skipping it is risky: it has a failure rate of 0.0206 and its duration is 60.056 s, but only 4.108 s of the budget was left when it was reached.

**Cited facts**

- failures: 2 of 97 runs
- failure_rate: 0.020618556701030927
- duration_s: 60.056
- remaining_budget_at_turn_s: 4.108

## R098

Build `PR-1840_build7`, budget 10%, test `org.apache.karaf.itests.features.Spring53FeaturesTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.features.Spring53FeaturesTest
- Rank by value: 36
- Candidate tests: 207
- Selected tests: 47
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 2
  - failure rate: 0.020618556701030927
  - builds since the last failure: 2
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 1, 1, 0
- History score: 0.059
- Relevance used: 0.2
- Semantic analyzer's reason: The test class does not directly reference or test the new properties added in the BaseTest class.
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java`
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java`
- Test duration (s): 28.272
- Budget (s): 210.66
- Budget left when the test was reached (s): 4.082
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 234.85

**Justification**

> Skipping it is risky: its relevance is 0.2 because it does not directly reference or test the new properties added in the BaseTest class, although it has failed twice in 97 runs. It needs 28.272 s but only 4.082 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.2
- changed_files: itests/test/src/test/java/org/apache/karaf/itests/BaseTest.java
- itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java
- itests/test/src/test/java/org/apache/karaf/itests/features/Spring60FeaturesTest.java
- itests/test/src/test/java/org/apache/karaf/itests/features/Spring61FeaturesTest.java
- failures: 2 of 97 runs

## R099

Build `PR-1677_build3`, budget 5%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 14
- Candidate tests: 221
- Selected tests: 30
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 87
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `cache/api/src/main/java/org/apache/karaf/cache/api/CacheService.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/CacheCommandSupport.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Create.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Get.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Invalidate.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/ListCaches.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/Put.java`
  - `cache/commands/src/main/java/org/apache/karaf/cache/core/commands/completers/CacheNameCompleter.java`
  - `cache/core/src/main/java/org/apache/karaf/cache/core/Activator.java`
  - `cache/core/src/main/java/org/apache/karaf/cache/core/EhcacheService.java`
- Test duration (s): 6.958
- Budget (s): 71.773
- Budget left when the test was reached (s): 3.262
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 75.469

**Justification**

> Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 6.958 s but only 3.262 s of the budget was left when it was reached.

**Cited facts**

- relevance_used: 0.0
- failures: 1 of 97 runs
- duration_s: 6.958
- remaining_budget_at_turn_s: 3.262

## R100

Build `PR-1656_build1`, budget 5%, test `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest`

**Evidence given to the explainer**

- Test: org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest
- Rank by value: 13
- Candidate tests: 211
- Selected tests: 25
- History:
  - builds in the history window: 100
  - runs: 97
  - failures: 1
  - failure rate: 0.010309278350515464
  - builds since the last failure: 46
  - recent outcomes (oldest first; 1 = fail, 0 = pass, - = not run): 0, 0, 0, 0, 0, 0, 0, 0, -, 0
- History score: 0.01
- Relevance used: 0.0
- Semantic analyzer's reason: none
- Changed files:
  - `itests/test/src/test/java/org/apache/karaf/itests/features/Spring53FeaturesTest.java`
- Test duration (s): 7.078
- Budget (s): 49.461
- Budget left when the test was reached (s): 2.84
- Why it was skipped: did_not_fit
- Budget it would have needed (s): 53.699

**Justification**

> Skipping it is risky: it has a failure rate of 0.0103 and its duration of 7.078 s exceeds the remaining budget of 2.84 s.

**Cited facts**

- failures: 1 of 97 runs
- failure_rate: 0.010309278350515464
- duration_s: 7.078
- remaining_budget_at_turn_s: 2.84
