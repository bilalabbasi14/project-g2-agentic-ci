# Trace of PR-1427_build2

Run: `E3_test_seed1` · events: 57

## 1. pipeline · state

- time: 2026-11-07T14:54:24.956Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 208,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T14:54:25.042Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 208
}
```

## 3. pipeline · state

- time: 2026-11-07T14:54:25.046Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.ConfigExampleTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.obr.command.util.FileUtilTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:33.857Z
- latency: 8.789 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1180,
  "completion_tokens": 56
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.JpaExampleTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.bundle.core.BundleService;
import org.apache.karaf.itests.BaseTest;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class JpaExampleTest extends BaseTest {

    private static final RolePrincipal[] ADMIN_ROLES = {
            new RolePrincipal(BundleService.SYSTEM_BUNDLES_ROLE),
            new RolePrincipal("admin"),
            new RolePrincipal("manager")
    };

    @Test
    public void test() throws Exception {
        // adding jpa example features repository
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-jpa-example-features/" + System.getProperty("karaf.version") + "/xml");

        // install the karaf-jpa-example-datasource & karaf-jpa-example-common
        executeCommand("feature:install karaf-jpa-example-datasource", ADMIN_ROLES);
        executeCommand("feature:install karaf-jpa-example-common", ADMIN_ROLES);

        // declarative service EclipseLink
        executeCommand("feature:install karaf-jpa-example-provider-ds-eclipselink", ADMIN_ROLES);
        // install the karaf-jpa-example-command feature
        installAndAssertFeature("karaf-jpa-example-command");
        testCommand();
        executeCommand("feature:uninstall karaf-jpa-example-provider-ds-eclipselink", ADMIN_ROLES);

        // declarative service Hibernate
        executeCommand("feature:install karaf-jpa-example-provider-ds-hibernate", ADMIN_ROLES);
        testCommand();
        executeCommand("feature:uninstall karaf-jpa-example-provider-ds-hibernate", ADMIN_ROLES);

        // blueprint EclipseLink
        executeCommand("feature:install karaf-jpa-example-provider-blueprint-eclipselink", ADMIN_ROLES);
        testCommand();
        executeCommand("feature:uninstall karaf-jpa-example-provider-blueprint-eclipselink", ADMIN_ROLES);

        // blueprint Hibernate
        executeCommand("feature:install karaf-jpa-example-provider-blueprint-hibernate", ADMIN_ROLES);
        testCommand();
        executeCommand("feature:uninstall karaf-jpa-example-provider-blueprint-hibernate", ADMIN_ROLES);
    }

    private void testCommand() {
        // ad
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.JpaExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with SSH sessions or related components.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:36.016Z
- latency: 2.152 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 815,
  "completion_tokens": 68
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.karaf.shell.impl.console.session;

import static org.easymock.EasyMock.createMock;

import java.io.PrintStream;
import java.io.UnsupportedEncodingException;

import org.apache.felix.service.threadio.ThreadIO;
import org.apache.karaf.shell.api.console.SessionFactory;
import org.apache.karaf.shell.impl.console.SessionFactoryImpl;

import org.junit.Test;

public class SessionFactoryImplTest {
    
    @Test
    public void createWithNullInputStream() throws UnsupportedEncodingException {
        final SessionFactory sessionFactory = new SessionFactoryImpl(createMock(ThreadIO.class));
        sessionFactory.create(null, createMock(PrintStream.class), createMock(PrintStream.class));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
  "relevance": 0.2,
  "reason": "The test does not directly involve the `ShellCommand` or `ShellFactoryImpl` classes that were changed.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:38.287Z
- latency: 2.263 s

```json
{
  "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 863,
  "completion_tokens": 69
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.event.command.EventDisplayCommandTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.event.command;

import static org.easymock.EasyMock.createControl;
import static org.easymock.EasyMock.expect;

import java.util.HashMap;

import org.apache.karaf.event.command.EventDisplayCommand;
import org.apache.karaf.event.service.EventCollector;
import org.apache.karaf.shell.api.console.Session;
import org.easymock.IMocksControl;
import org.junit.Test;
import org.osgi.service.event.Event;

public class EventDisplayCommandTest {

    @Test
    public void testExecute() throws Exception {
        IMocksControl c = createControl();
        EventDisplayCommand display = new EventDisplayCommand();
        display.session = c.createMock(Session.class);
        expect(display.session.getConsole()).andReturn(System.out);
        display.collector = new EventCollector();
        display.collector.handleEvent(new Event("myTopic", new HashMap<>()));
        c.replay();
        display.execute();
        c.verify();
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.command.EventDisplayCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:40.641Z
- latency: 2.342 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1172,
  "completion_tokens": 60
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.ConfigManagedServiceFactoryTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.replaceConfigurationFile;

import java.io.IOException;

import javax.inject.Inject;

import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.CoreOptions;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ConfigManagedServiceFactoryTest extends BaseTest {

	@Inject
	ConfigurationAdmin configAdmin;

	@org.ops4j.pax.exam.Configuration
	public Option[] config() {
		return new Option[] {
				CoreOptions.composite(super.config()),
				replaceConfigurationFile("etc/myconfig-test1.cfg",
						getConfigFile("/etc/myconfig-test1.cfg")),
		// KarafDistributionOption.debugConfiguration()
		};
	}

	@Test
	public void updateProperties() throws IOException, InvalidSyntaxException {
		checkInitialValuesFromFelixConfigAdmin();
		checkEditByFactoryPid();
		checkEditByArbitraryAttribute();
	}
	
	@Test
	public void createNewFactoryConfig() throws Exception {
		executeCommand("config:edit --factory myconfig2\n"
				+ "config:property-set test1 data1\n"
				+ "config:update", new RolePrincipal("manager"));
		Configuration config = configAdmin.listConfigurations("(service.factorypid=myconfig2)")[0];
		assertEquals("data1", config.getProcessedProperties(null).get("test1"));
	}

	private void checkInitialValuesFromFelixConfigAdmin() throws IOException,
			InvalidSyntaxException {
		Configuration config = readConfig();
		assertNotNull("The configuration is null", config);
		assertEquals("data1", config.getProcessedProperties(null).get("test1"));
		assertEquals("data2", config.getProcessedProperties(null).get("test2"));
	}

	private void checkEditByFactoryPid() throws 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or related components.",
  "confidence": 0.8
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:42.953Z
- latency: 2.301 s

```json
{
  "test": "org.apache.karaf.itests.XATest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1199,
  "completion_tokens": 58
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.XATest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests;

import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.itests.util.RunIfRule;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.CoreOptions;
import org.ops4j.pax.exam.MavenUtils;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.framework.Bundle;

import java.util.Arrays;
import java.util.EnumSet;
import java.util.LinkedList;
import java.util.List;

import static org.junit.Assert.assertNotNull;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.replaceConfigurationFile;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class XATest extends BaseTest {

    private static final EnumSet<FeaturesService.Option> NO_AUTO_REFRESH = EnumSet.of(FeaturesService.Option.NoAutoRefreshBundles);

    @Rule
    public RunIfRule rule = new RunIfRule();

    @Configuration
    public Option[] config() {
        String version = MavenUtils.getArtifactVersion("org.apache.karaf", "apache-karaf");
        List<Option> result = new LinkedList<>(Arrays.asList(super.config()));
        result.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresRepositories",
                "mvn:org.apache.karaf.features/framework/" + version + "/xml/features, " +
                "mvn:org.apache.karaf.features/enterprise/" + version + "/xml/features, " +
                "mvn:org.apache.karaf.features/spring-legacy/" + version + "/xml/features, " +
                "mvn:org.apache.karaf.features/standard/" + version + "/xml/features, " +
                "mvn:org.apache.activemq/artemis-features/2.6.0/xml/features, " +
                "mvn:org.apache.camel.karaf/apache-camel/2.20.1/xml/features"
            ));
        result.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresBoot",
                "instance,package,log,ssh,framew
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.XATest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.XATest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or related components.",
  "confidence": 0.8
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:42.961Z
- latency: 2.332 s

```json
{
  "test": "org.apache.karaf.itests.ssh.SshKeyFormatTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1197,
  "completion_tokens": 64
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.ssh.SshKeyFormatTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */


package org.apache.karaf.itests.ssh;

import com.google.common.io.ByteSource;
import com.google.common.io.Resources;

import org.apache.sshd.client.SshClient;
import org.apache.sshd.client.future.ConnectFuture;
import org.apache.sshd.client.keyverifier.RequiredServerKeyVerifier;
import org.apache.sshd.client.session.ClientSession;
import org.apache.sshd.client.session.ClientSession.ClientSessionEvent;
import org.bouncycastle.openssl.PEMKeyPair;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;
import org.junit.Test;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.security.GeneralSecurityException;
import java.security.KeyPair;
import java.util.EnumSet;
import java.util.Set;

import static org.ops4j.pax.exam.CoreOptions.*;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;

/**
 * Test use of PEM keys.
 */
public class SshKeyFormatTest extends SshCommandTestBase {

    @Configuration
    public Option[] config() {
        File keyFile = new File("src/test/resources/org/apache/karaf/itests/ssh/test.pem");
        return options(composite(super.config()),
                editConfigurationFilePut("etc/org.apache.karaf.shell.cfg", "hostKey", keyFile.getAbsolutePath()),
                bundle("mvn:org.bouncycastle/bcprov-jdk15on/1.66"),
                bundle("mvn:org.bouncycastle/bcpkix-jdk15on/1.66"),
                bundle("mvn:com.google.guava/guava/16.0.1")
                );
    }


    @Test
    public void usePemKey() throws Exception {
        SshClient client = SshClient.setUpDefaultClient();
        URL testPemURL = Resources.getResource(SshKeyFormatTest.class, "test.pem");
        ByteSource source = Resources.asByteSource(testPemURL);
        KeyPair keyPair = getKeyPair(source.openStream());

        String sshPort = getSshPort();

        client.setServerKeyVerifier(new RequiredServerKeyVerifier(keyPair.getPublic()));
        client.start();
        ConnectFuture future = client.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ssh.SshKeyFormatTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ssh.SshKeyFormatTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or the ShellCommand class.",
  "confidence": 0.8
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:42.967Z
- latency: 2.212 s

```json
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1079,
  "completion_tokens": 62
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.config.command.EditCommandTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.config.command;

import java.util.Dictionary;
import java.util.Hashtable;

import junit.framework.TestCase;
import org.apache.felix.utils.properties.TypedProperties;
import org.apache.karaf.config.core.impl.ConfigRepositoryImpl;
import org.apache.karaf.shell.api.console.Session;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

import static org.easymock.EasyMock.createMock;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.replay;

/**
 * Test cases for {@link EditCommand}
 */
public class EditCommandTest extends TestCase {

    private static final String PID = "my.test.persistent.id";

    private EditCommand command;
    private ConfigurationAdmin admin;
    private Session session;

    @Override
    protected void setUp() throws Exception {
        command = new EditCommand();

        admin = createMock(ConfigurationAdmin.class);
        command.setConfigRepository(new ConfigRepositoryImpl(admin));

        session = new MockCommandSession();
        command.setSession(session);
    }
    
    public void testExecuteOnExistingPid() throws Exception {        
        Configuration config = createMock(Configuration.class);
        expect(admin.getConfiguration(PID, null)).andReturn(config);
        replay(admin);
        
        // the ConfigAdmin service returns a Dictionary for an existing PID
        Dictionary<String, Object> props = new Hashtable<>();
        expect(config.getProcessedProperties(null)).andReturn(props);
        replay(config);
        
        command.pid = PID; 
        command.execute();
        
        // the PID and Dictionary should have been set on the session
        assertEquals("The PID should be set on the session",
                     PID, session.get(ConfigCommandSupport.PROPERTY_CONFIG_PID));
        assertEquals("The Dictionary returned by the ConfigAdmin service should be set on the session",
                   props, session.get(ConfigCommandSupport.PROPERTY_CONFIG_PROPS));
    }
    
    @SuppressWarnings("rawtypes")
    public void testExecuteOnNewPid() throws Exception {        
        Configuration config = createMo
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.config.command.EditCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the SSH or session management code that was changed.",
  "confidence": 0.9
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:42.973Z
- latency: 1.931 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 979,
  "completion_tokens": 56
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.JdbcExampleTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.examples.jdbc.api.BookingService;
import org.apache.karaf.itests.BaseTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class JdbcExampleTest extends BaseTest {

    @Test
    public void test() throws Exception {
        // adding jdbc example features repository
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-jdbc-example-features/" + System.getProperty("karaf.version") + "/xml");

        // install the karaf-jdbc-example-provider feature
        installAndAssertFeature("karaf-jdbc-example-provider");
        assertServiceAvailable(BookingService.class);

        // install the karaf-jdbc-example feature
        installAndAssertFeature("karaf-jdbc-example");

        // add booking
        executeCommand("booking:add Foo AF520");
        // list booking
        String bookings = executeCommand("booking:list");
        System.out.println(bookings);
        assertContains("AF520", bookings);
        // get booking
        String booking = executeCommand("booking:get 1");
        System.out.println(booking);
        assertContains("AF520", booking);
        // remove booking
        executeCommand("booking:remove 1");
        bookings = executeCommand("booking:list");
        System.out.println(bookings);
        assertContainsNot("AF520", bookings);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.JdbcExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "relevance": 0,
  "reason": "The test class does not interact with SSH sessions or the ShellCommand class.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:45.462Z
- latency: 2.482 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1122,
  "completion_tokens": 65
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.ServletExampleTest` (source, may be truncated):
<<<TEST
/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.itests.BaseTest;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class ServletExampleTest extends BaseTest {

    private void setup() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-servlet-example-features/" + System.getProperty("karaf.version") + "/xml");
        installAndAssertFeature("http");
        installAndAssertFeature("http-whiteboard");
    }

    private void verify() throws Exception {
        String command = executeCommand("http:list");
        while (!command.contains("servlet-example")) {
            Thread.sleep(200);
            command = executeCommand("http:list");
        }
        System.out.println(command);

        URL url = new URL("http://localhost:" + getHttpPort() + "/servlet-example");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setDoInput(true);

        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String line;
        StringBuilder buffer = new StringBuilder();
        while ((line = reader.readLine()) != null) {
            buffer.append(line);
        }

        String output = buffer.toString();
        System.out.println(output);
        assertContains("<h1>Example Servlet</h1>", output);
    }

    @Test
    public void testWithRegistration() throws Exception {
        setup();

        installAndAssertFeature("karaf-servlet-example-registration");

        verify();
    }

    @Test
    public void testWithAnnota
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.ServletExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with SSH or session management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:47.913Z
- latency: 2.439 s

```json
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1124,
  "completion_tokens": 63
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.WebSocketExampleTest` (source, may be truncated):
<<<TEST
/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.itests.BaseTest;
import org.eclipse.jetty.websocket.api.Session;
import org.eclipse.jetty.websocket.api.StatusCode;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketClose;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketConnect;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketMessage;
import org.eclipse.jetty.websocket.api.annotations.WebSocket;
import org.eclipse.jetty.websocket.client.ClientUpgradeRequest;
import org.eclipse.jetty.websocket.client.WebSocketClient;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.framework.Bundle;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertTrue;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class WebSocketExampleTest extends BaseTest {

    @Test(timeout = 60000)
    public void test() throws Exception {
        featureService.installFeature("scr");
        featureService.installFeature("http");

        Bundle bundle = bundleContext.installBundle("mvn:org.apache.karaf.examples/karaf-websocket-example/" + System.getProperty("karaf.version"));
        bundle.start();

        String httpList = executeCommand("http:list");
        while (!httpList.contains("Deployed")) {
            Thread.sleep(1000);
            httpList = executeCommand("http:list");
        }
        System.out.println(httpList);

        WebSocketClient client = new WebSocketClient();
        SimpleSocket socket = new SimpleSocket();
        client.start();
        URI uri = new URI("ws://localhost:" + getHttpPort() + "/example-websocket");
        ClientUpgradeRequest request = new ClientUpgradeRequest();
        client.connect(socket, uri, request);

        socket.awaitClose(10, TimeUnit.SECONDS);

        assertTrue(socket.messages.size
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.WebSocketExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "relevance": 0,
  "reason": "The test class does not involve SSH or session management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:50.371Z
- latency: 2.449 s

```json
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1008,
  "completion_tokens": 69
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.event.command.EventTailCommandTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.event.command;

import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.mock;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;

import java.io.PrintStream;
import java.util.HashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.karaf.event.command.EventTailCommand;
import org.apache.karaf.event.service.EventCollector;
import org.apache.karaf.shell.api.console.Session;
import org.junit.Test;
import org.osgi.service.event.Event;

public class EventTailCommandTest {

    private Exception exception;

    @Test
    public void testTail() throws Exception {
        EventTailCommand tail = new EventTailCommand();
        tail.session = mock(Session.class);
        tail.collector = new EventCollector();
        PrintStream out = System.out;
        expect(tail.session.getConsole()).andReturn(out);
        exception = null;
        replay(tail.session);
        
        ExecutorService executor = Executors.newSingleThreadExecutor();
        executor.execute(() -> {
            try {
                tail.execute();
            } catch (Exception e) {
                exception = e;
            }
        });
        tail.collector.handleEvent(event());
        Thread.sleep(200);
        executor.shutdownNow(); // Will interrupt the tail
        executor.awaitTermination(10, TimeUnit.SECONDS);
        if (exception != null) {
            throw exception;
        }
        verify(tail.session);
    }

    private Event event() {
        return new Event("myTopic", new HashMap<>());
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.command.EventTailCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:52.734Z
- latency: 2.353 s

```json
{
  "test": "org.apache.karaf.itests.LogTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1149,
  "completion_tokens": 59
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.LogTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import javax.management.Attribute;
import javax.management.MBeanServer;
import javax.management.ObjectName;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.management.ManagementFactory;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class LogTest extends BaseTest {

    private static final Logger LOGGER = LoggerFactory.getLogger(LogTest.class);

    @Test
    public void setDebugAndDisplay() throws Exception {
        assertSetLevel("DEBUG");
        LOGGER.debug("Making sure there is DEBUG level output");
        assertContains("DEBUG", executeCommand("log:display -n 200"));
    }

    @Test
    public void setDebugAndDisplayAlias() throws Exception {
        assertSetLevel("DEBUG");
        LOGGER.debug("Making sure there is DEBUG level output");
        assertContains("DEBUG", executeAlias("ld -n 200"));
    }

    @Test
    public void setDebugViaMBean() throws Exception {
        assertSetLevel("INFO");
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        ObjectName name = new ObjectName("org.apache.karaf:type=log,name=root");
        Attribute attribute = new Attribute("Level", "DEBUG");
        mbeanServer.setAttribute(name, attribute);
        String logLevel = (String) mbeanServer.getAttribute(name, "Level");
        assertEquals("DEBUG", logLevel);
    }

    @Test
    public void setGetDebugAndClear() throws Exception {
        assertSetLevel("DEBUG");
        assertSetLevel("INFO");
        System.out.println(executeCommand("log:clear"));
        String displayOutput = executeCommand("log:display").trim();
        assertTrue("Should be empty but was: " + displayOutput, displayOutput.trim().isEmpty());
    }

    @Test
    public void setGetDebugAndClearAlias() throws Exception {
        assertSetLevel("DEBUG");
        assertSetLevel("INFO");
        System.out.println(executeCommand("log:clear"));
        String displayOutput = executeAlias("ld").trim();
        assertTrue("Should be empty but was: " + displayOutput, displayOutput.trim().isEmpty());
    }
    
    public void 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.LogTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.LogTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or the ShellCommand class.",
  "confidence": 0.9
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:52.744Z
- latency: 2.414 s

```json
{
  "test": "org.apache.karaf.config.command.UpdateCommandTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1120,
  "completion_tokens": 68
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.config.command.UpdateCommandTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.config.command;

import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.replay;

import java.util.Dictionary;
import java.util.Enumeration;
import java.util.Hashtable;

import org.apache.felix.utils.properties.TypedProperties;
import org.apache.karaf.config.core.ConfigRepository;
import org.easymock.EasyMock;

import junit.framework.TestCase;

/**
 * Test cases for {@link EditCommand}
 */
public class UpdateCommandTest extends TestCase {

    private static final String FACTORY_PID = "myFactoryPid";
    private static final String PID = "myPid";

    public void testupdateRegularConfig() throws Exception {
        Hashtable<String, Object> props = new Hashtable<>();

        UpdateCommand command = new UpdateCommand();
        ConfigRepository configRepo = EasyMock.createMock(ConfigRepository.class);
        configRepo.update(EasyMock.eq(PID), EasyMock.eq(props), EasyMock.eq(null));
        EasyMock.expectLastCall();
		command.setConfigRepository(configRepo);

        MockCommandSession session = createMockSessionForFactoryEdit(PID, false, props);
        command.setSession(session);
        replay(configRepo);

        command.execute();
        EasyMock.verify(configRepo);
    }

    public void testupdateOnNewFactoryPid() throws Exception {
		Hashtable<String, Object> props = new Hashtable<>();

        UpdateCommand command = new UpdateCommand();
        ConfigRepository configRepo = EasyMock.createMock(ConfigRepository.class);
        expect(configRepo.createFactoryConfiguration(EasyMock.eq(FACTORY_PID), EasyMock.eq(null), EasyMock.eq(props), EasyMock.eq(null)))
        	.andReturn(PID + ".35326647");
		command.setConfigRepository(configRepo);

        MockCommandSession session = createMockSessionForFactoryEdit(FACTORY_PID, true, props);
        command.setSession(session);
        replay(configRepo);

        command.execute();
        EasyMock.verify(configRepo);
    }

	private MockCommandSession createMockSessionForFactoryEdit(String pid, boolean isFactory,
			Dictionary<String, Object> props) {
		MockCommandSession session = new MockCommandSession();
        session.put(ConfigCommandSupport.PROPERTY
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.config.command.UpdateCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.config.command.UpdateCommandTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:55.389Z
- latency: 2.636 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1220,
  "completion_tokens": 66
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests.ssh;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

/**
 * This test exercises the Shell Command ACL for the config scope commands as defined in
 * /framework/src/main/resources/resources/etc/org.apache.karaf.command.acl.config.cfg
 */
@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ConfigSshCommandSecurityTest extends SshCommandTestBase {

    private static int counter = 0;
    
    

    @Test
    public void testConfigCommandSecurityViaSsh() throws Exception {
        String manageruser = "man" + System.nanoTime() + "_" + counter++;
        String vieweruser = "view" + System.nanoTime() + "_" + counter++;

        addUsers(manageruser, vieweruser);

        // A viewer cannot do anything to ConfigAdmin
        assertCommand(vieweruser, "config:edit cfg." + vieweruser, Result.NOT_FOUND);
        assertCommand(vieweruser, "config:delete cfg." + vieweruser, Result.NOT_FOUND);

        testConfigEdits(manageruser, Result.OK, "cfg." + manageruser, false);
        testConfigEdits(manageruser, Result.NO_CREDENTIALS, "jmx.acl.test_" + counter++, false);
        testConfigEdits(manageruser, Result.NO_CREDENTIALS, "org.apache.karaf.command.acl.test_" + counter++, false);
        testConfigEdits(manageruser, Result.NO_CREDENTIALS, "org.apache.karaf.service.acl.test_" + counter++, false);
        testConfigEdits("karaf", Result.OK, "cfg.karaf_" + counter++, true);
        testConfigEdits("karaf", Result.OK, "jmx.acl.test_" + counter++, true);
        testConfigEdits("karaf", Result.OK, "org.apache.karaf.command.acl.test_" + counter++, true);
        testConfigEdits("karaf", Result.OK, "org.apache.karaf.service.acl.test_" + counter++, true);
    }

    private void testConfigEdits(String user, Result expectedEditResult, String pid, boolean isAdmin) throws Exception {
        assertCommand(user, "config:edit " + pid + "\n" +
                "config:property-set x y\n" +
                "config:property-set a b\n" +
                "config:property-append x z\n" +
                "config:update", expectedEditResult);
        if (expectedEditResult != Result.OK)
            // If we're expecting failure, don't continue any further...
            return;

        String result = assertCommand
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or the ShellCommand class directly.",
  "confidence": 0.8
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T14:54:57.804Z
- latency: 2.407 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1155,
  "completion_tokens": 59
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.FeatureTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.openmbean.TabularData;

import org.apache.karaf.jaas.boot.principal.RolePrincipal;

import org.junit.Test;
import org.junit.runner.RunWith;

import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.MavenUtils;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.io.File;
import java.lang.management.ManagementFactory;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class FeatureTest extends BaseTest {


    @Configuration
    public Option[] config() {
        String version = MavenUtils.getArtifactVersion("org.apache.karaf", "apache-karaf");
        List<Option> result = new LinkedList<>(Arrays.asList(super.config()));
        result.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresRepositories",
                        "mvn:org.apache.karaf.features/framework/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/spring/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/spring-legacy/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/enterprise/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/standard/" + version + "/xml/features"));
        return result.toArray(new Option[result.size()]);
    }

    @Test
    public void bootFeatures() throws Exception {
        assertFeaturesInstalled("jaas", "ssh", "management", "bundle", "config", "deployer", "diagnostic",
                                "instance", "kar", "log", "package", "service", "system");
    }

    @Test
    public void listCommand() throws Exception {
        String featureListOutput = executeCommand("feature:list");
        System.out.println(featureListOutput);
        assertFalse(featureListOutput.isEmpty());
        featureListOutput = executeCommand("feature:list -i");
        System.out.println
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.FeatureTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to directly interact with the SSH or session management code.",
  "confidence": 0.8
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T14:55:00.436Z
- latency: 2.625 s

```json
{
  "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1109,
  "completion_tokens": 65
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.ConfigExampleTest` (source, may be truncated):
<<<TEST
/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.itests.BaseTest;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;
import org.osgi.service.cm.Configuration;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Dictionary;
import java.util.Hashtable;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class ConfigExampleTest extends BaseTest {

    private ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
    private PrintStream originStream;
    private PrintStream outStream = new PrintStream(byteArrayOutputStream);

    @Before
    public void setUp() throws Exception {
        originStream = System.out;
        System.setOut(outStream);
    }

    public void addFeaturesRepository() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-config-example-features/" + System.getProperty("karaf.version") + "/xml");
    }

    @Test
    public void testStatic() throws Exception {
        addFeaturesRepository();

        installAndAssertFeature("karaf-config-example-static");

        System.out.flush();
        System.setOut(originStream);

        String output = byteArrayOutputStream.toString();

        System.out.println(output);

        assertContains("foo = bar", output);
        assertContains("hello = world", output);
    }

    @Test
    public void testManaged() throws Exception {
        addFeaturesRepository();

        installAndAssertFeature("karaf-config-example-managed");

        System.out.flush();
        assertContains("Configuration changed", byteArrayOutputStream.toString());

        Configuration configuration = configurationAdmin.getConfiguration("org.apache.karaf.example.config", null);
        Dictionary<String, Object> properties = configuration.getProcessedProperties(null);
        if (properties == null) {
            properties = new Hashtable<>();
        }
        properties.put("exam", "test");
        configuration.u
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.ConfigExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH sessions or the code changes made in the provided diff.",
  "confidence": 0.8
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T14:55:03.246Z
- latency: 2.803 s

```json
{
  "test": "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1148,
  "completion_tokens": 71
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.karaf.shell.impl.action.command;

import org.apache.felix.gogo.runtime.CommandProcessorImpl;
import org.apache.felix.gogo.runtime.threadio.ThreadIOImpl;
import org.apache.felix.service.command.CommandProcessor;
import org.apache.felix.service.threadio.ThreadIO;
import org.apache.karaf.shell.api.action.Action;
import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Option;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.apache.karaf.shell.api.console.Session;
import org.apache.karaf.shell.api.console.SessionFactory;
import org.apache.karaf.shell.impl.console.HeadlessSessionImpl;
import org.apache.karaf.shell.impl.console.SessionFactoryImpl;
import org.apache.karaf.shell.impl.console.parsing.KarafParser;
import org.jline.reader.Parser;
import org.junit.Before;
import org.junit.Test;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;

import static org.junit.Assert.assertEquals;

public class ActionMaskingCallbackTest {

    private Parser parser;
    private ActionMaskingCallback cb;

    @Before
    public void setUp() {
        ThreadIO tio = new ThreadIOImpl();
        CommandProcessor cp = new CommandProcessorImpl(tio);
        SessionFactory sf = new SessionFactoryImpl(tio);
        InputStream is = new ByteArrayInputStream(new byte[0]);
        PrintStream os = new PrintStream(new ByteArrayOutputStream());
        Session session = new HeadlessSessionImpl(sf, cp, is, os, os);
        parser = new KarafParser(session);

        ActionCommand cmd = new ActionCommand(null, UserAddCommand.class);
        cb = ActionMaskingCallback.build(cmd);
    }

    @Test
    public void testJaasUserAdd() throws Exception {
        check("user-add user password ", "user-add user ######## ");
        check("user-add --help user password ", "user-add --help user ######## ");
        check("user-add --help user password foo", "user-add --help user ######## foo");
        check("user-add --opt1 user password foo", "user-add --opt1 user ######## foo");
        check("
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
  "relevance": 0.1,
  "reason": "The test class does not directly interact with the `ShellCommand` or `ShellFactoryImpl` classes that were modified.",
  "confidence": 0.8
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T14:55:06.055Z
- latency: 2.798 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1206,
  "completion_tokens": 69
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.JmsExampleTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.itests.examples;

import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.itests.BaseTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.MavenUtils;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.util.Arrays;
import java.util.EnumSet;
import java.util.LinkedList;
import java.util.List;

import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.replaceConfigurationFile;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class JmsExampleTest extends BaseTest {

    private static final EnumSet<FeaturesService.Option> NO_AUTO_REFRESH = EnumSet.of(FeaturesService.Option.NoAutoRefreshBundles);

    @Configuration
    public Option[] config() {
        String version = MavenUtils.getArtifactVersion("org.apache.karaf", "apache-karaf");
        List<Option> result = new LinkedList<>(Arrays.asList(super.config()));
        result.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresRepositories",
                "mvn:org.apache.karaf.features/framework/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/enterprise/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/spring-legacy/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/standard/" + version + "/xml/features, " +
                        "mvn:org.apache.activemq/artemis-features/2.6.0/xml/features"
        ));
        result.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresBoot",
                "instance,package,log,ssh,framework,system,eventadmin,feature,shell,management,service,jaas,deployer,diagnostic,wrap,bundle,config,kar,aries-blueprint,artemis,jms,pax-jms-artemis"));
        result.add(replaceConfigurationFile("etc/org.ops4j.connectionfactory-artemis.cfg", getConfigFile("/org/apache/karaf/itests/features/org.ops4j.connectionfactory-artemis.cfg")));
        return result.toArray(new Option[result.size()]);
    }

    @Test
    public void test() throws Exception {
        Thread.sleep(10000);
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.JmsExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with SSH or session management, which are the areas affected by the code change.",
  "confidence": 0.8
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T14:55:06.063Z
- latency: 2.355 s

```json
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1071,
  "completion_tokens": 64
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
@@ -145,6 +145,9 @@ public void run() {
         } finally {
             callback.onExit(exitStatus);
             StreamUtils.close(in, out, err);
+            if (session != null) {
+                session.close(true);
+            }
         }
     }
 
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java
@@ -119,6 +119,7 @@ public void destroy() {
             if (!closed) {
                 closed = true;
                 callback.onExit(0);
+                session.close(true);
             }
         }
 
DIFF>>>

Test class `org.apache.karaf.obr.command.util.FileUtilTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.karaf.obr.command.util;

import org.junit.Test;

import static org.junit.Assert.fail;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.jar.JarInputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class FileUtilTest {

    @Test
    public void goodExtractTest() throws Exception {
        File base = new File("target/test");
        base.mkdirs();
        File goodKarFile = new File(base, "good.kar");
        ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(goodKarFile));
        ZipEntry entry = new ZipEntry("foo.bar");
        zos.putNextEntry(entry);

        byte[] data = "Test Data".getBytes();
        zos.write(data, 0, data.length);
        zos.closeEntry();
        zos.close();

        JarInputStream jis = new JarInputStream(new FileInputStream(goodKarFile));
        FileUtil.unjar(jis, base);

        goodKarFile.delete();
    }

    @Test
    public void badExtractTest() throws Exception {
        File base = new File("target/test");
        base.mkdirs();
        File badKarFile = new File(base, "bad.kar");
        ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(badKarFile));
        ZipEntry entry = new ZipEntry("../../../../../../../../../tmp/foo.bar");
        zos.putNextEntry(entry);

        byte[] data = "Test Data".getBytes();
        zos.write(data, 0, data.length);
        zos.closeEntry();
        zos.close();

        JarInputStream jis = new JarInputStream(new FileInputStream(badKarFile));
        try {
            FileUtil.unjar(jis, base);
            fail("Failure expected on extracting a jar with relative file paths");
        } catch (Exception ex) {
            // expected
        }

        badKarFile.delete();
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.obr.command.util.FileUtilTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "relevance": 0,
  "reason": "The test class does not involve any SSH or session management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 23. orchestrator · llm_call

- time: 2026-11-07T14:55:08.758Z
- latency: 2.573 s

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

Relevance source for this build: llm_shortlist

Build features:
- n_code_files = 2: number of changed code files in the diff
- n_dirs = 1: number of distinct folders those files are in
- lines_added = 4: added lines in the diff
- lines_removed = 0: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 208: number of candidate test classes
- shortlist_size = 19: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.0631579: mean relevance used over the shortlisted tests
- rel_max = 0.2: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.177158: highest history score over all candidates
- hist_mean_shortlist = 0.01978: mean history score over the shortlisted tests

Changed files (2):
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.itests.examples.JpaExampleTest | 0.177 | 0.000 | 0.000 | 40.83
- org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest | 0.000 | 1.000 | 0.200 | 0.414
- org.apache.karaf.event.command.EventDisplayCommandTest | 0.000 | 0.834 | 0.000 | 0.047
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.072 | 0.000 | 0.100 | 0.455
- org.apache.karaf.itests.XATest | 0.021 | 0.000 | 0.100 | 30.09
- org.apache.karaf.itests.ssh.SshKeyFormatTest | 0.000 | 0.698 | 0.100 | 0.802
- org.apache.karaf.config.command.EditCommandTest | 0.000 | 0.684 | 0.100 | 0.074
- org.apache.karaf.itests.examples.JdbcExampleTest | 0.021 | 0.000 | 0.000 | 363.125
- org.apache.karaf.itests.examples.ServletExampleTest | 0.021 | 0.284 | 0.000 | 80.279
- org.apache.karaf.itests.examples.WebSocketExampleTest | 0.000 | 0.668 | 0.000 | 14.223
- org.apache.karaf.event.command.EventTailCommandTest | 0.000 | 0.609 | 0.000 | 0.205
- org.apache.karaf.itests.LogTest | 0.021 | 0.000 | 0.100 | 3.202
- org.apache.karaf.config.command.UpdateCommandTest | 0.000 | 0.596 | 0.000 | 0.06
- org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest | 0.013 | 0.567 | 0.100 | 43.253
- org.apache.karaf.itests.FeatureTest | 0.010 | 0.000 | 0.100 | 11.988
- org.apache.karaf.itests.examples.ConfigExampleTest | 0.010 | 0.000 | 0.100 | 58.815
- org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest | 0.000 | 0.495 | 0.100 | 0.027
- org.apache.karaf.itests.examples.JmsExampleTest | 0.010 | 0.000 | 0.100 | 13.589
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 0.490 | 0.000 | 0.043

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
{"action": "final", "w": 0.2, "confidence": 0.8, "reason": "Low relevance signal and weak history signal"}
```

## 24. orchestrator · decision

- time: 2026-11-07T14:55:08.776Z
- latency: —

```json
{
  "w": 0.2,
  "confidence": 0.8,
  "source": "agent",
  "reason": "Low relevance signal and weak history signal",
  "tool_calls": 0
}
```

## 25. pipeline · state

- time: 2026-11-07T14:55:08.980Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.packages.command.PackageImportTest"
  ]
}
```

## 26. pipeline · state

- time: 2026-11-07T14:55:08.996Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.profile.impl.PropertiesTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T14:55:09.012Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.profile.impl.PropertiesTest",
    "org.apache.karaf.features.internal.service.StateStorageTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T14:55:09.101Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.main.lock.StatementsTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T14:55:09.116Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T14:55:09.133Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jpm.ProcessTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.itests.features.EnterpriseFeaturesTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T14:55:09.223Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.PropertiesTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T14:55:09.239Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T14:55:09.255Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ConfigExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T14:55:09.347Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.PropertiesTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T14:55:09.363Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T14:55:09.379Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ConfigExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T14:55:09.470Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.PropertiesTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T14:55:09.486Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T14:55:09.502Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ConfigExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T14:55:09.547Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.PropertiesTest"
  ]
}
```

## 41. explainer · explanation

- time: 2026-11-07T14:55:15.359Z
- latency: 5.792 s

```json
{
  "test": "org.apache.karaf.itests.XATest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.XATest",
    "rank_by_value": 10,
    "n_candidates": 208,
    "n_selected": 32,
    "history": {
      "test": "org.apache.karaf.itests.XATest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
      "last_failure_distance": 31,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with SSH sessions or related components.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 30.09,
    "budget_s": 75.674,
    "remaining_budget_at_turn_s": 4.293,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 101.471
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with SSH sessions or related components, and it only needs 30.09 s but only 4.293 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 30.09",
    "remaining_budget_at_turn_s: 4.293"
  ],
  "ok": true,
  "error": null
}
```

## 42. explainer · explanation

- time: 2026-11-07T14:55:19.588Z
- latency: 4.209 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 11,
    "n_candidates": 208,
    "n_selected": 32,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 6,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.013,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with SSH sessions or the ShellCommand class directly.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 43.253,
    "budget_s": 75.674,
    "remaining_budget_at_turn_s": 4.293,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 114.634
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with SSH sessions or the ShellCommand class directly, and it only needs 43.253 s but only 4.293 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "duration_s: 43.253",
    "remaining_budget_at_turn_s: 4.293"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T14:55:25.251Z
- latency: 5.649 s

```json
{
  "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
    "rank_by_value": 12,
    "n_candidates": 208,
    "n_selected": 32,
    "history": {
      "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 32,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with SSH sessions or the code changes made in the provided diff.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 58.815,
    "budget_s": 75.674,
    "remaining_budget_at_turn_s": 4.293,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 130.196
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not appear to interact with SSH sessions or the code changes made in the provided diff. It needs 58.815 s but only 4.293 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 58.815",
    "remaining_budget_at_turn_s: 4.293"
  ],
  "ok": true,
  "error": null
}
```

## 44. explainer · explanation

- time: 2026-11-07T14:55:31.272Z
- latency: 6.004 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 13,
    "n_candidates": 208,
    "n_selected": 32,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 28,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with SSH or session management, which are the primary changes in the provided code diff.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 80.279,
    "budget_s": 75.674,
    "remaining_budget_at_turn_s": 4.293,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 151.66
  },
  "justification": "Skipping it is risky: it has a low relevance of 0.0 because it does not interact with SSH or session management, which are the primary changes in the provided code diff. It needs 80.279 s but only 4.293 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
    "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 80.279",
    "remaining_budget_at_turn_s: 4.293"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T14:55:35.349Z
- latency: 4.062 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 14,
    "n_candidates": 208,
    "n_selected": 32,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 54,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 24.366,
    "budget_s": 75.674,
    "remaining_budget_at_turn_s": 4.293,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 95.747
  },
  "justification": "Skipping it is risky: it has a 1% failure rate and its duration of 24.366 s exceeds the remaining budget of 4.293 s.",
  "cited_facts": [
    "failures: 1 of 100 runs",
    "failure_rate: 0.01",
    "duration_s: 24.366",
    "remaining_budget_at_turn_s: 4.293"
  ],
  "ok": true,
  "error": null
}
```

## 46. pipeline · state

- time: 2026-11-07T14:55:35.433Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 47. explainer · explanation

- time: 2026-11-07T14:55:42.278Z
- latency: 6.829 s

```json
{
  "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
    "rank_by_value": 12,
    "n_candidates": 208,
    "n_selected": 34,
    "history": {
      "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 32,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with SSH sessions or the code changes made in the provided diff.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 58.815,
    "budget_s": 151.349,
    "remaining_budget_at_turn_s": 6.625,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 203.539
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not appear to interact with SSH sessions or the code changes made in the provided diff, and it failed once in 97 runs. It needs 58.815 s but only 6.625 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "failures: 1 of 97 runs",
    "duration_s: 58.815",
    "remaining_budget_at_turn_s: 6.625"
  ],
  "ok": true,
  "error": null
}
```

## 48. explainer · explanation

- time: 2026-11-07T14:55:50.300Z
- latency: 8.008 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 13,
    "n_candidates": 208,
    "n_selected": 34,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 28,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with SSH or session management, which are the primary changes in the provided code diff.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 80.279,
    "budget_s": 151.349,
    "remaining_budget_at_turn_s": 6.625,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 225.003
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with SSH or session management, which are the primary changes in the provided code diff. It also has a failure rate of 0.021, indicating it is relatively stable. However, it needs 80.279 s but only 6.625 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "failures: 2 of 97 runs",
    "failure_rate: 0.021",
    "duration_s: 80.279",
    "remaining_budget_at_turn_s: 6.625"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T14:55:56.960Z
- latency: 6.646 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 14,
    "n_candidates": 208,
    "n_selected": 34,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 54,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 24.366,
    "budget_s": 151.349,
    "remaining_budget_at_turn_s": 6.625,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 169.09
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 because it is not related to any changed files, and it failed once in 100 runs. It needs 24.366 s but only 6.625 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "failures: 1 of 100 runs",
    "duration_s: 24.366",
    "remaining_budget_at_turn_s: 6.625"
  ],
  "ok": true,
  "error": null
}
```

## 50. explainer · explanation

- time: 2026-11-07T14:56:02.920Z
- latency: 5.947 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
    "rank_by_value": 15,
    "n_candidates": 208,
    "n_selected": 34,
    "history": {
      "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 28,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with SSH sessions or the ShellCommand class.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 363.125,
    "budget_s": 151.349,
    "remaining_budget_at_turn_s": 6.625,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 507.849
  },
  "justification": "Skipping it is risky: it has a relevance of 0.0 because it does not interact with SSH sessions or the ShellCommand class, and it needs 363.125 s but only 6.625 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 363.125",
    "remaining_budget_at_turn_s: 6.625"
  ],
  "ok": true,
  "error": null
}
```

## 51. explainer · explanation

- time: 2026-11-07T14:56:06.370Z
- latency: 3.437 s

```json
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.audit.logger.EventLoggerTest",
    "rank_by_value": 68,
    "n_candidates": 208,
    "n_selected": 34,
    "history": {
      "test": "org.apache.karaf.audit.logger.EventLoggerTest",
      "history_builds": 100,
      "runs": 99,
      "failures": 0,
      "failure_rate": 0.0,
      "last_failure_distance": null,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 1.017,
    "budget_s": 151.349,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 152.358
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration of 1.017 s exceeds the remaining budget of 0.008 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 1.017",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```

## 52. pipeline · state

- time: 2026-11-07T14:56:06.461Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ConfigExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.features.PaxCdiFeaturesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest"
  ]
}
```

## 53. explainer · explanation

- time: 2026-11-07T14:56:11.102Z
- latency: 4.625 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 14,
    "n_candidates": 208,
    "n_selected": 49,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 54,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 24.366,
    "budget_s": 302.697,
    "remaining_budget_at_turn_s": 18.879,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 308.184
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 100 runs. It needs 24.366 s but only 18.879 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 100 runs",
    "duration_s: 24.366",
    "remaining_budget_at_turn_s: 18.879"
  ],
  "ok": true,
  "error": null
}
```

## 54. explainer · explanation

- time: 2026-11-07T14:56:16.927Z
- latency: 5.811 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
    "rank_by_value": 15,
    "n_candidates": 208,
    "n_selected": 49,
    "history": {
      "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 28,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with SSH sessions or the ShellCommand class.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 363.125,
    "budget_s": 302.697,
    "remaining_budget_at_turn_s": 18.879,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 646.943
  },
  "justification": "Skipping it is risky: it has a relevance of 0.0 because it does not interact with SSH sessions or the ShellCommand class, and it needs 363.125 s but only 18.879 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 363.125",
    "remaining_budget_at_turn_s: 18.879"
  ],
  "ok": true,
  "error": null
}
```

## 55. explainer · explanation

- time: 2026-11-07T14:56:20.163Z
- latency: 3.222 s

```json
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.audit.logger.EventLoggerTest",
    "rank_by_value": 68,
    "n_candidates": 208,
    "n_selected": 49,
    "history": {
      "test": "org.apache.karaf.audit.logger.EventLoggerTest",
      "history_builds": 100,
      "runs": 99,
      "failures": 0,
      "failure_rate": 0.0,
      "last_failure_distance": null,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 1.017,
    "budget_s": 302.697,
    "remaining_budget_at_turn_s": 0.23,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 303.484
  },
  "justification": "Skipping it is risky: it has no relevance and its duration of 1.017 s exceeds the remaining budget of 0.23 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 1.017",
    "remaining_budget_at_turn_s: 0.23"
  ],
  "ok": true,
  "error": null
}
```

## 56. explainer · explanation

- time: 2026-11-07T14:56:23.678Z
- latency: 3.494 s

```json
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "rank_by_value": 72,
    "n_candidates": 208,
    "n_selected": 49,
    "history": {
      "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
      "history_builds": 100,
      "runs": 99,
      "failures": 0,
      "failure_rate": 0.0,
      "last_failure_distance": null,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 0.076,
    "budget_s": 302.697,
    "remaining_budget_at_turn_s": 0.051,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 302.722
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.076 s, which is less than the remaining budget of 0.051 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.076",
    "remaining_budget_at_turn_s: 0.051"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T14:56:29.447Z
- latency: 5.749 s

```json
{
  "test": "org.apache.karaf.config.command.UpdateCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.config.command.UpdateCommandTest",
    "rank_by_value": 74,
    "n_candidates": 208,
    "n_selected": 49,
    "history": {
      "test": "org.apache.karaf.config.command.UpdateCommandTest",
      "history_builds": 100,
      "runs": 99,
      "failures": 0,
      "failure_rate": 0.0,
      "last_failure_distance": null,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified.",
    "changed_files": [
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java"
    ],
    "duration_s": 0.06,
    "budget_s": 302.697,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 302.749
  },
  "justification": "Skipping it is reasonable: its relevance is 0.0 because it does not interact with the `ShellCommand` or `ShellFactoryImpl` classes, which are the ones that have been modified. It only took 0.06 s, which was well within the remaining budget of 0.008 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellCommand.java",
    "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/ShellFactoryImpl.java",
    "duration_s: 0.06",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```
