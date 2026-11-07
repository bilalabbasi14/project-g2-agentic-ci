# Trace of PR-1462_build1

Run: `E5_test_seed1` · events: 8

## 1. pipeline · state

- time: 2026-11-07T17:46:52.752Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 130,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T17:46:52.848Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 130
}
```

## 3. pipeline · state

- time: 2026-11-07T17:46:52.854Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest"
  ]
}
```

## 4. orchestrator · llm_call

- time: 2026-11-07T17:46:55.082Z
- latency: 2.104 s

```json
{
  "step": 1,
  "attempt": 0,
  "cached": false
}
```

**prompt**

```text
You help choose which regression tests to run for one code change (one CI build).
Each candidate test has two scores:
- history: how often and how recently the test failed in earlier builds (0 to 1);
- relevance: how closely the test is related to the changed code (0 to 1).
Tests are ranked by  w * history + (1 - w) * relevance^1.2 , and the top of the ranking is run.

Your task: decide how much to trust history versus relevance for THIS build only, as one number w
from 0 to 1. w = 1 ranks by history alone; w = 0 ranks by relevance alone. The DANTE method uses
one fixed w for every build; your value should come from this build's evidence.

How the evidence should move w:
- Lower w (trust relevance more) when the relevance signal is strong and specific: a high rel_max,
  shortlisted tests with clearly high relevance (n_rel_ge_05 above zero), and a focused change
  (few changed files and folders).
- Raise w (trust history more) when relevance is weak or flat (rel_max low, n_rel_ge_05 zero, all
  shortlisted relevances similar) or when history is informative (high hist_max, high
  recent_failure_density).
- When the signals disagree or are weak, stay closer to the middle of the range.
- If one test looks decisive but you are unsure, call a tool to check it before answering.
Builds differ, so different builds should usually get different values of w. Do not reuse a
number from these instructions; derive w from the features and the shortlist below.

Relevance source for this build: tfidf

Build features:
- n_code_files = 6: number of changed code files in the diff
- n_dirs = 3: number of distinct folders those files are in
- lines_added = 29: added lines in the diff
- lines_removed = 21: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 130: number of candidate test classes
- shortlist_size = 11: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.969798: mean relevance used over the shortlisted tests
- rel_max = 1: highest relevance used over all candidates
- n_rel_ge_05 = 11: shortlisted tests with relevance >= 0.5
- hist_max = 0.01: highest history score over all candidates
- hist_mean_shortlist = 0.000909091: mean history score over the shortlisted tests

Changed files (6):
- client/src/main/java/org/apache/karaf/client/Main.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java
- shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.audit.util.FastDateFormatTest | 0.000 | 1.000 | - | 0.004
- org.apache.karaf.main.MainLockingTest | 0.010 | 0.762 | - | 23.461
- org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest | 0.000 | 1.000 | - | 1.127
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 1.000 | - | 0.03
- org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest | 0.000 | 1.000 | - | 0.272
- org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest | 0.000 | 1.000 | - | 0.864
- org.apache.karaf.specs.locator.OsgiLocatorTest | 0.000 | 1.000 | - | 1.005
- org.apache.karaf.deployer.spring.SpringDeploymentListenerTest | 0.000 | 0.999 | - | 0.595
- org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest | 0.000 | 0.995 | - | 0.09
- org.apache.karaf.main.lock.MySQLJDBCLockTest | 0.000 | 0.985 | - | 0.047
- org.apache.karaf.config.core.impl.ConfigMBeanImplTest | 0.000 | 0.927 | - | 0.048

Tools you may call (at most 4 calls in total, 4 left):
- history_retrieval: Past outcomes of one test class over the history builds. Input: {"test": "string (fully qualified test class)"}. Output: {"test": "string", "history_builds": "int", "runs": "int", "failures": "int", "failure_rate": "float", "last_failure_distance": "int|null", "recent_outcomes": "list[int|null]"}.
- diff_reader: Changed lines of one file in the build's diff. Input: {"file": "string (repo-relative path)"}. Output: {"file": "string", "found": "bool", "hunk_text": "string", "changed_lines": "string", "added": "int", "removed": "int"}.

Observations from earlier tool calls:
(none yet)

Answer with a single JSON object and nothing else, in one of these two shapes
(replace every <...> with your own value):
To call a tool:
{"action": "call_tool", "tool": "<history_retrieval or diff_reader>", "args": {"<test or file>": "<a shortlisted test or a changed file>"}, "reason": "<what you want to check>"}
To give the final answer:
{"action": "final", "w": <your weight for this build, from 0 to 1>, "confidence": <from 0 to 1>, "reason": "<one sentence naming the features that decided w>"}
confidence is how sure you are that your w ranks this build's tests better than DANTE's fixed w.
```

**response**

```text
{"action": "final", "w": 0.8, "confidence": 0.9, "reason": "High relevance and specific changed files suggest trusting history less."}
```

## 5. orchestrator · decision

- time: 2026-11-07T17:46:55.100Z
- latency: —

```json
{
  "w": 0.8,
  "confidence": 0.9,
  "source": "agent",
  "reason": "High relevance and specific changed files suggest trusting history less.",
  "tool_calls": 0
}
```

## 6. pipeline · state

- time: 2026-11-07T17:46:55.335Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted (TF-IDF)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```

## 7. pipeline · state

- time: 2026-11-07T17:46:55.352Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted (TF-IDF)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```

## 8. pipeline · state

- time: 2026-11-07T17:46:55.374Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted (TF-IDF)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```
