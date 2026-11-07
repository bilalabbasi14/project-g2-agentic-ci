# Trace of PR-1497_build1

Run: `E3_test_seed1` · events: 58

## 1. pipeline · state

- time: 2026-11-07T14:58:50.036Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 205,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T14:58:50.117Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 205
}
```

## 3. pipeline · state

- time: 2026-11-07T14:58:50.121Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.itests.examples.RestExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:52.581Z
- latency: 2.443 s

```json
{
  "test": "org.apache.karaf.itests.examples.LogAppenderExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 752,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.LogAppenderExampleTest` (source, may be truncated):
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

import org.apache.karaf.itests.BaseTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class LogAppenderExampleTest extends BaseTest {

    @Test
    public void test() throws Exception {
        // adding karaf-log-appender-example features repository
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-log-appender-example-features/" + System.getProperty("karaf.version") + "/xml");

        // install the karaf-log-appender-example feature
        installAndAssertFeature("karaf-log-appender-example");

        String output = executeCommand("log:log TEST");
        System.out.println(output);
        assertContains("INFO - TEST", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.LogAppenderExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.LogAppenderExampleTest",
  "relevance": 0,
  "reason": "The test class does not interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:55.173Z
- latency: 2.582 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1055,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.jaas.modules.ldap.LdapCacheTest` (source, may be truncated):
<<<TEST
/*
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *  under the License.
 */
package org.apache.karaf.jaas.modules.ldap;

import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.io.IOException;

import javax.naming.NamingException;
import javax.naming.directory.Attribute;
import javax.naming.directory.Attributes;
import javax.naming.directory.BasicAttribute;
import javax.naming.directory.BasicAttributes;
import javax.naming.directory.DirContext;
import javax.security.auth.Subject;
import javax.security.auth.callback.CallbackHandler;

import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.AbstractLdapTestUnit;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(FrameworkRunner.class)
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapLoginModuleTest-class",
        partitions = {@CreatePartition(name = "example", suffix = "dc=example,dc=com")})
@ApplyLdifFiles(
        "org/apache/karaf/jaas/modules/ldap/example.com.ldif"
)
public class LdapCacheTest extends AbstractLdapTestUnit {

    @Before
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldap.properties", 
                  LdapLoginModuleTest::replacePort);
    }

    @After
    public void tearDown() {
        LDAPCache.clear();
    }

    @Test
    public void testAdminLogin() throws Exception {
        Properties options = ldapLoginModuleOptions();
        LDAPLoginModule module = new LDAPLoginModule();
        Cal
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:57.609Z
- latency: 2.426 s

```json
{
  "test": "org.apache.karaf.examples.itests.ExampleITest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 825,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.examples.itests.ExampleITest` (source, may be truncated):
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
package org.apache.karaf.examples.itests;

import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.itests.KarafTestSupport;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ExampleITest extends KarafTestSupport {

    @Test
    public void listBundleCommand() throws Exception {
        // assert on an available service
        assertServiceAvailable(FeaturesService.class);

        // installing a feature and verifying that it's correctly installed
        installAndAssertFeature("scr");

        // testing a command execution
        String bundles = executeCommand("bundle:list -t 0");
        System.out.println(bundles);
        assertContains("junit", bundles);

        String features = executeCommand("feature:list -i");
        System.out.print(features);
        assertContains("scr", features);

        // using a service and assert state or result
        FeaturesService featuresService = getOsgiService(FeaturesService.class);
        Feature scr = featuresService.getFeature("scr");
        Assert.assertEquals("scr", scr.getName());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.examples.itests.ExampleITest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.examples.itests.ExampleITest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:00.278Z
- latency: 2.662 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1090,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:02.807Z
- latency: 2.521 s

```json
{
  "test": "org.apache.karaf.itests.examples.HttpResourceExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 958,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.HttpResourceExampleTest` (source, may be truncated):
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
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class HttpResourceExampleTest extends BaseTest {

    @Test(timeout = 60000L)
    public void test() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-http-resource-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("karaf-http-resource-example-whiteboard");

        String command = executeCommand("http:list");
        while (!command.contains("Deployed")) {
            Thread.sleep(200);
            command = executeCommand("http:list");
        }
        assertContains("ResourceServlet", command);
        assertContains("Deployed", command);

        URL url = new URL("http://localhost:" + getHttpPort() + "/example/index.html");
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
        assertContains("<h2>Resource Example</h2>", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.HttpResourceExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.HttpResourceExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:04.960Z
- latency: 2.144 s

```json
{
  "test": "org.apache.karaf.itests.examples.SchedulerExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 799,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.SchedulerExampleTest` (source, may be truncated):
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
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class SchedulerExampleTest extends BaseTest {

    @Test
    public void test() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-scheduler-example-features/" + System.getProperty("karaf.version") + "/xml");
        installAndAssertFeature("karaf-scheduler-example");

        String output = executeCommand("scheduler:list");
        System.out.println(output);
        assertContains("org.apache.karaf.example.scheduler.runnable", output);
        assertContains("org.apache.karaf.example.scheduler.foo", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.SchedulerExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.SchedulerExampleTest",
  "relevance": 0,
  "reason": "The test does not interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:07.117Z
- latency: 2.148 s

```json
{
  "test": "org.apache.karaf.itests.KarTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 763,
  "completion_tokens": 57
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.KarTest` (source, may be truncated):
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

import java.lang.management.ManagementFactory;
import java.util.List;

import javax.management.MBeanServer;
import javax.management.ObjectName;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class KarTest extends BaseTest {

    @Test
    public void listCommand() throws Exception {
        System.out.println(executeCommand("kar:list"));
    }

    @Test
    public void listViaMBean() throws Exception {
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        ObjectName name = new ObjectName("org.apache.karaf:type=kar,name=root");
        @SuppressWarnings("unchecked")
        List<String> kars = (List<String>) mbeanServer.getAttribute(name, "Kars");
        assertEquals(0, kars.size());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.KarTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.KarTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:09.406Z
- latency: 2.282 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 889,
  "completion_tokens": 57
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "reason": "The test class does not interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:11.474Z
- latency: 2.061 s

```json
{
  "test": "org.apache.karaf.client.ClientConfigTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 759,
  "completion_tokens": 54
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.client.ClientConfigTest` (source, may be truncated):
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
package org.apache.karaf.client;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;

public class ClientConfigTest {

    @Test
    public void testDefaultUser() throws Exception {

        String etc = System.getProperty("karaf.etc");

        System.setProperty("karaf.etc", "src/test/resources/etc1");
        ClientConfig cc = new ClientConfig(new String[0]);
        assertThat(cc.getUser(), equalTo("karaf"));

        cc = new ClientConfig(new String[] { "-u", "different-one" });
        assertThat(cc.getUser(), equalTo("different-one"));

        System.setProperty("karaf.etc", "src/test/resources/etc2");
        cc = new ClientConfig(new String[0]);
        assertThat(cc.getUser(), equalTo("test"));

        if (etc != null) {
            System.setProperty("karaf.etc", etc);
        }
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.client.ClientConfigTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.client.ClientConfigTest",
  "relevance": 0,
  "reason": "The test class does not interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:14.077Z
- latency: 2.595 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1072,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.RestExampleTest` (source, may be truncated):
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
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import static org.junit.Assert.assertEquals;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class RestExampleTest extends BaseTest {

    private void setup() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-rest-example-features/" + System.getProperty("karaf.version") + "/xml");
        installAndAssertFeature("http");
        installAndAssertFeature("http-whiteboard");
    }

    private void verify() throws Exception {
        String location = "http://localhost:" + getHttpPort() + "/cxf/booking/";
        executeCommand("booking:add --url " + location + " 1 Foo TST001");

        String output = executeCommand("booking:list --url " + location);
        System.out.println(output);
        assertContains("TST001", output);
    }

    private void verifyAttachments() throws Exception {
        String location = "http://localhost:" + getHttpPort() + "/cxf/booking/all";

        String output = executeCommand("booking:list-all --url " + location);
        System.out.println(output);
        assertContains("stream: application/octet-stream: important information", output);
        assertContains("image: application/octet-stream: UGhvdG8=", output);
    }

    @Test
    public void testBlueprintWithHttpClient() throws Exception {
        setup();

        installAndAssertFeature("karaf-rest-example-blueprint");

        installAndAssertFeature("karaf-rest-example-client-http");

        verify();
    }

    @Test
    public void testBlueprintWithCxfClient() throws Exception {
        setup();

        installAndAssertFeature("karaf-rest-example-blueprint");

        installAndAssertFeature("karaf-rest-example-client-cxf");

        verify();
    }

    @Test
    public void testScrWithHt
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.RestExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.9
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:16.571Z
- latency: 2.484 s

```json
{
  "test": "org.apache.karaf.itests.JndiTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 871,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.JndiTest` (source, may be truncated):
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

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.apache.karaf.jndi.JndiService;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)

public class JndiTest extends BaseTest {

    @Before
    public void installJndiFeature() throws Exception {
        installAndAssertFeature("jndi");
        getOsgiService(JndiService.class, 30000);
    }
    
    
    @Test
    public void testCommand() throws Exception {
        String output = executeCommand("jndi:names");
        System.out.println(output);
        assertContains("osgi:service/jndi", output);
        output = executeCommand("jndi:alias osgi:service/jndi /test/foo");
        System.out.println(output);
        output = executeCommand("jndi:names");
        System.out.println(output);
        assertContains("/test/foo", output);
        output = executeCommand("jndi:bind 40 /test/bar");
        System.out.println(output);
        output = executeCommand("jndi:names");
        System.out.println(output);
        assertContains("/test/bar", output);
        output = executeCommand("jndi:unbind /test/bar");
        System.out.println(output);
        assertContainsNot("/test/bar", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.JndiTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.JndiTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:19.182Z
- latency: 2.603 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1032,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:21.502Z
- latency: 2.311 s

```json
{
  "test": "org.apache.karaf.itests.examples.CdiExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 741,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.CdiExampleTest` (source, may be truncated):
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

import org.apache.karaf.itests.BaseTest;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class CdiExampleTest extends BaseTest {

    @Test
    public void test() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-cdi-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("karaf-cdi-example-provider");

        Object object = getOsgiService("org.apache.karaf.examples.cdi.api.MyService");

        Assert.assertNotNull(object);

        installAndAssertFeature("karaf-cdi-example-consumer");
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.CdiExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.CdiExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:24.068Z
- latency: 2.556 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1022,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.SoapExampleTest` (source, may be truncated):
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
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class SoapExampleTest extends BaseTest {

    @Test
    public void testBlueprint() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-soap-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("karaf-soap-example-blueprint");
        installAndAssertFeature("karaf-soap-example-client");

        String url = "http://localhost:" + getHttpPort() + "/cxf/example";
        executeCommand("booking:add --url " + url + " 1 Foo TST001");

        String output = executeCommand("booking:list --url " + url);
        System.out.println(output);
        assertContains("TST001", output);
    }

    @Test
    public void testScr() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-soap-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("karaf-soap-example-scr");

        URL url = new URL("http://localhost:" + getHttpPort() + "/cxf");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        StringBuilder builder = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                builder.append(line).append("\n");
            }
        }

        assertContains("BookingServiceSoap", builder.toString());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.SoapExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:26.418Z
- latency: 2.343 s

```json
{
  "test": "org.apache.karaf.itests.examples.CommandExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 796,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.CommandExampleTest` (source, may be truncated):
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

import org.apache.karaf.examples.command.api.BookingService;
import org.apache.karaf.itests.BaseTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class CommandExampleTest extends BaseTest {

    @Test
    public void test() throws Exception {
        // add command example features repository
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-command-example-features/" + System.getProperty("karaf.version") + "/xml");

        // install karaf-command-example-provider feature
        installAndAssertFeature("karaf-command-example-provider");
        assertServiceAvailable(BookingService.class);

        // install karaf-command-example feature
        installAndAssertFeature("karaf-command-example");

        // execute booking commands
        executeCommand("booking:add AF520 Foo");
        String output = executeCommand("booking:list");
        System.out.println(output);
        assertContains("AF520", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.CommandExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.CommandExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:28.867Z
- latency: 2.441 s

```json
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1034,
  "completion_tokens": 57
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "reason": "The test class does not interact with the JaasHelper class or its methods.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:31.501Z
- latency: 2.628 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1082,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:34.253Z
- latency: 2.745 s

```json
{
  "test": "org.apache.karaf.itests.examples.JaasExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 772,
  "completion_tokens": 75
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.examples.JaasExampleTest` (source, may be truncated):
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

import org.apache.karaf.itests.BaseTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class JaasExampleTest extends BaseTest {

    @Test(expected = RuntimeException.class)
    public void testCommand() throws Exception {
        // add jaas example repository
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-jaas-example-features/" + System.getProperty("karaf.version") + "/xml");

        // install karaf-jaas-example-app feature
        installAndAssertFeature("karaf-jaas-example-app");

        // execute example:jaas command
        String output = executeCommand("example:jaas karaf karaf");
        assertContains("Authentication successful", output);
        output = executeCommand("example:jaas foo bar");
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.JaasExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.JaasExampleTest",
  "relevance": 0.8,
  "reason": "The test class includes a method that executes a command related to JAAS, which could potentially be affected by changes in the JaasHelper class.",
  "confidence": 0.9
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:37.038Z
- latency: 2.779 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1130,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
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
  "reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 23. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:39.584Z
- latency: 2.536 s

```json
{
  "test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 822,
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
diff --git a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
--- a/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
+++ b/util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java
@@ -134,7 +134,9 @@ public ProtectionDomain[] combine(ProtectionDomain[] currentDomains,
             for (int i = 0; i < cLen; i++) {
                 newDomains[i] = new DelegatingProtectionDomain(currentDomains[i], principals);
             }
-            System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            if (assignedDomains != null) {
+                System.arraycopy(assignedDomains, 0, newDomains, cLen, aLen);
+            }
             return optimize(newDomains);
         }
 
DIFF>>>

Test class `org.apache.karaf.itests.ssh.KarSshCommandSecurityTest` (source, may be truncated):
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
 * This test exercises the Shell Command ACL for the kar scope commands as defined in
 * /framework/src/main/resources/resources/etc/org.apache.karaf.command.acl.kar.cfg
 */
@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)

public class KarSshCommandSecurityTest extends SshCommandTestBase {
    private static int counter = 0;
        
    @Test
    public void testKarCommandSecurityViaSsh() throws Exception {
        String vieweruser = "view" + System.nanoTime() + "_" + counter++;

        addViewer(vieweruser);

        assertCommand(vieweruser, "kar:list", Result.OK);
        assertCommand(vieweruser, "kar:install", Result.NOT_FOUND);
        assertCommand(vieweruser, "kar:uninstall", Result.NOT_FOUND);

        assertCommand("karaf", "kar:list", Result.OK);
        assertCommand("karaf", "kar:install", Result.OK);
        assertCommand("karaf", "kar:uninstall", Result.OK);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest",
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the JaasHelper class or its methods.",
  "confidence": 0.8
}
```

## 24. orchestrator · llm_call

- time: 2026-11-07T14:59:42.608Z
- latency: 2.834 s

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
- n_code_files = 1: number of changed code files in the diff
- n_dirs = 1: number of distinct folders those files are in
- lines_added = 3: added lines in the diff
- lines_removed = 1: removed lines in the diff
- recent_failure_density = 0.1: share of the last 10 history builds with at least one failing test
- n_candidates = 205: number of candidate test classes
- shortlist_size = 20: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.105: mean relevance used over the shortlisted tests
- rel_max = 0.8: highest relevance used over all candidates
- n_rel_ge_05 = 1: shortlisted tests with relevance >= 0.5
- hist_max = 0.0554545: highest history score over all candidates
- hist_mean_shortlist = 0.0166903: mean history score over the shortlisted tests

Changed files (1):
- util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.itests.examples.LogAppenderExampleTest | 0.000 | 1.000 | 0.000 | 0.822
- org.apache.karaf.jaas.modules.ldap.LdapCacheTest | 0.055 | 0.386 | 0.000 | 0.609
- org.apache.karaf.examples.itests.ExampleITest | 0.000 | 0.996 | 0.100 | 1.961
- org.apache.karaf.itests.examples.JpaExampleTest | 0.052 | 0.636 | 0.100 | 33.468
- org.apache.karaf.itests.examples.HttpResourceExampleTest | 0.031 | 0.555 | 0.100 | 3.674
- org.apache.karaf.itests.examples.SchedulerExampleTest | 0.000 | 0.955 | 0.000 | 2.137
- org.apache.karaf.itests.KarTest | 0.000 | 0.930 | 0.000 | 1.214
- org.apache.karaf.itests.examples.JdbcExampleTest | 0.031 | 0.814 | 0.000 | 1.371
- org.apache.karaf.client.ClientConfigTest | 0.000 | 0.904 | 0.000 | 0.022
- org.apache.karaf.itests.examples.RestExampleTest | 0.031 | 0.421 | 0.100 | 100.159
- org.apache.karaf.itests.JndiTest | 0.000 | 0.896 | 0.100 | 1.854
- org.apache.karaf.itests.examples.ServletExampleTest | 0.031 | 0.349 | 0.100 | 66.297
- org.apache.karaf.itests.examples.CdiExampleTest | 0.000 | 0.896 | 0.100 | 3.787
- org.apache.karaf.itests.examples.SoapExampleTest | 0.031 | 0.574 | 0.100 | 29.258
- org.apache.karaf.itests.examples.CommandExampleTest | 0.000 | 0.896 | 0.100 | 1.065
- org.apache.karaf.itests.examples.WebSocketExampleTest | 0.031 | 0.362 | 0.000 | 13.799
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.021 | 0.000 | 0.100 | 1.373
- org.apache.karaf.itests.examples.JaasExampleTest | 0.000 | 0.879 | 0.800 | 10.925
- org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest | 0.021 | 0.549 | 0.100 | 36.314
- org.apache.karaf.itests.ssh.KarSshCommandSecurityTest | 0.000 | 0.876 | 0.200 | 6.132

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
{"action": "final", "w": 0.7, "confidence": 0.8, "reason": "High relevance signal with a focused change in a single file."}
```

## 25. orchestrator · decision

- time: 2026-11-07T14:59:42.625Z
- latency: —

```json
{
  "w": 0.7,
  "confidence": 0.8,
  "source": "agent",
  "reason": "High relevance signal with a focused change in a single file.",
  "tool_calls": 0
}
```

## 26. pipeline · state

- time: 2026-11-07T14:59:42.852Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.SimpleMavenResolverTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T14:59:42.868Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.SimpleMavenResolverTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T14:59:42.887Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.SimpleMavenResolverTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.WrapperTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.itests.examples.BlueprintExampleTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T14:59:42.994Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T14:59:43.010Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T14:59:43.025Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T14:59:43.117Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T14:59:43.133Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T14:59:43.148Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T14:59:43.237Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T14:59:43.253Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T14:59:43.268Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T14:59:43.357Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T14:59:43.373Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T14:59:43.390Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 41. pipeline · state

- time: 2026-11-07T14:59:43.437Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 42. explainer · explanation

- time: 2026-11-07T14:59:48.268Z
- latency: 4.811 s

```json
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "rank_by_value": 7,
    "n_candidates": 205,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 13.799,
    "budget_s": 52.938,
    "remaining_budget_at_turn_s": 12.358,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 54.379
  },
  "justification": "Skipping it is reasonable: it has a relevance of 0.0 because it does not interact with the JaasHelper class or its methods, and it only needs 13.799 s, which fits within the remaining budget of 12.358 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "duration_s: 13.799",
    "remaining_budget_at_turn_s: 12.358"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T14:59:54.061Z
- latency: 5.779 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 9,
    "n_candidates": 205,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 29.258,
    "budget_s": 52.938,
    "remaining_budget_at_turn_s": 10.722,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 71.474
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it has a failure rate of 0.031. It needs 29.258 s but only 10.722 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 3 of 97 runs",
    "failure_rate: 0.031",
    "duration_s: 29.258",
    "remaining_budget_at_turn_s: 10.722"
  ],
  "ok": true,
  "error": null
}
```

## 44. explainer · explanation

- time: 2026-11-07T14:59:59.584Z
- latency: 5.508 s

```json
{
  "test": "org.apache.karaf.itests.examples.JaasExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JaasExampleTest",
    "rank_by_value": 10,
    "n_candidates": 205,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.itests.examples.JaasExampleTest",
      "history_builds": 100,
      "runs": 97,
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
        null,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.8,
    "relevance_reason": "The test class includes a method that executes a command related to JAAS, which could potentially be affected by changes in the JaasHelper class.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 10.925,
    "budget_s": 52.938,
    "remaining_budget_at_turn_s": 10.722,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 53.141
  },
  "justification": "Skipping it is reasonable: its relevance is 0.8 because it involves a method that could be affected by changes in the JaasHelper class, although it has never failed in 97 runs. It needs 10.925 s but only 10.722 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.8",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 0 of 97 runs",
    "duration_s: 10.925",
    "remaining_budget_at_turn_s: 10.722"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T15:00:05.064Z
- latency: 5.463 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 12,
    "n_candidates": 205,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 57,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 36.314,
    "budget_s": 52.938,
    "remaining_budget_at_turn_s": 6.939,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 82.313
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it failed 2 times in 97 runs. It needs 36.314 s but only 6.939 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 2 of 97 runs",
    "duration_s: 36.314",
    "remaining_budget_at_turn_s: 6.939"
  ],
  "ok": true,
  "error": null
}
```

## 46. explainer · explanation

- time: 2026-11-07T15:00:10.375Z
- latency: 5.296 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 13,
    "n_candidates": 205,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 66.297,
    "budget_s": 52.938,
    "remaining_budget_at_turn_s": 6.939,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 112.296
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it failed 3 times in 97 runs. It needs 66.297 s but only 6.939 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 3 of 97 runs",
    "duration_s: 66.297",
    "remaining_budget_at_turn_s: 6.939"
  ],
  "ok": true,
  "error": null
}
```

## 47. pipeline · state

- time: 2026-11-07T15:00:10.448Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.internal.model.JsonTest"
  ]
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:00:15.896Z
- latency: 5.433 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 12,
    "n_candidates": 205,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 57,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 36.314,
    "budget_s": 105.876,
    "remaining_budget_at_turn_s": 5.895,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 136.295
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it failed 2 times in 97 runs. It needs 36.314 s but only 5.895 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 2 of 97 runs",
    "duration_s: 36.314",
    "remaining_budget_at_turn_s: 5.895"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T15:00:20.530Z
- latency: 4.619 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 13,
    "n_candidates": 205,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 66.297,
    "budget_s": 105.876,
    "remaining_budget_at_turn_s": 5.895,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 166.278
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it only needs 66.297 s but only 5.895 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "duration_s: 66.297",
    "remaining_budget_at_turn_s: 5.895"
  ],
  "ok": true,
  "error": null
}
```

## 50. explainer · explanation

- time: 2026-11-07T15:00:26.250Z
- latency: 5.705 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 15,
    "n_candidates": 205,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 100.159,
    "budget_s": 105.876,
    "remaining_budget_at_turn_s": 4.83,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 201.205
  },
  "justification": "Skipping it is reasonable: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it has a failure rate of 0.031. It needs 100.159 s but only 4.83 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 3 of 97 runs",
    "failure_rate: 0.031",
    "duration_s: 100.159",
    "remaining_budget_at_turn_s: 4.83"
  ],
  "ok": true,
  "error": null
}
```

## 51. explainer · explanation

- time: 2026-11-07T15:00:30.498Z
- latency: 4.231 s

```json
{
  "test": "org.apache.karaf.itests.examples.WarExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.WarExampleTest",
    "rank_by_value": 17,
    "n_candidates": 205,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.WarExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 52,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 7.09,
    "budget_s": 105.876,
    "remaining_budget_at_turn_s": 2.976,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 109.99
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 7.09 s but only 2.976 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 7.09",
    "remaining_budget_at_turn_s: 2.976"
  ],
  "ok": true,
  "error": null
}
```

## 52. explainer · explanation

- time: 2026-11-07T15:00:34.713Z
- latency: 4.200 s

```json
{
  "test": "org.apache.karaf.itests.WebTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.WebTest",
    "rank_by_value": 19,
    "n_candidates": 205,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.WebTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 52,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 7.638,
    "budget_s": 105.876,
    "remaining_budget_at_turn_s": 1.015,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 112.499
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 7.638 s but only 1.015 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 7.638",
    "remaining_budget_at_turn_s: 1.015"
  ],
  "ok": true,
  "error": null
}
```

## 53. pipeline · state

- time: 2026-11-07T15:00:34.793Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JaasExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest"
  ]
}
```

## 54. explainer · explanation

- time: 2026-11-07T15:00:40.135Z
- latency: 5.322 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 15,
    "n_candidates": 205,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 49,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 100.159,
    "budget_s": 211.752,
    "remaining_budget_at_turn_s": 8.095,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 303.816
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not interact with the JaasHelper class or its methods, and it failed 3 times in 97 runs. It needs 100.16 s but only 8.095 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "failures: 3 of 97 runs",
    "duration_s: 100.159",
    "remaining_budget_at_turn_s: 8.095"
  ],
  "ok": true,
  "error": null
}
```

## 55. explainer · explanation

- time: 2026-11-07T15:00:44.261Z
- latency: 4.111 s

```json
{
  "test": "org.apache.karaf.itests.examples.WarExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.WarExampleTest",
    "rank_by_value": 17,
    "n_candidates": 205,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.examples.WarExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 52,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 7.09,
    "budget_s": 211.752,
    "remaining_budget_at_turn_s": 6.241,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 212.601
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 97 runs. It needs 7.09 s but only 6.241 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 7.09",
    "remaining_budget_at_turn_s: 6.241"
  ],
  "ok": true,
  "error": null
}
```

## 56. explainer · explanation

- time: 2026-11-07T15:00:48.400Z
- latency: 4.128 s

```json
{
  "test": "org.apache.karaf.itests.WebTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.WebTest",
    "rank_by_value": 19,
    "n_candidates": 205,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.WebTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 52,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 7.638,
    "budget_s": 211.752,
    "remaining_budget_at_turn_s": 4.28,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 215.11
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 7.638 s but only 4.28 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 7.638",
    "remaining_budget_at_turn_s: 4.28"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T15:00:53.034Z
- latency: 4.620 s

```json
{
  "test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest",
    "rank_by_value": 20,
    "n_candidates": 205,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.ssh.KarSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
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
        null,
        0
      ]
    },
    "history_score": 0.0,
    "relevance_used": 0.2,
    "relevance_reason": "The test class does not directly interact with the JaasHelper class or its methods.",
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 6.132,
    "budget_s": 211.752,
    "remaining_budget_at_turn_s": 4.28,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 213.604
  },
  "justification": "Skipping it is reasonable: its relevance is 0.2 because it does not directly interact with the JaasHelper class or its methods, and it only took 6.132 s, which was well within the remaining budget of 4.28 s.",
  "cited_facts": [
    "relevance_used: 0.2",
    "changed_files: util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java",
    "duration_s: 6.132",
    "remaining_budget_at_turn_s: 4.28"
  ],
  "ok": true,
  "error": null
}
```

## 58. explainer · explanation

- time: 2026-11-07T15:00:57.400Z
- latency: 4.352 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JmsExampleTest",
    "rank_by_value": 22,
    "n_candidates": 205,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.examples.JmsExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 77,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        null,
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "util/src/main/java/org/apache/karaf/util/jaas/JaasHelper.java"
    ],
    "duration_s": 14.995,
    "budget_s": 211.752,
    "remaining_budget_at_turn_s": 0.493,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 226.254
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential issues. It needs 14.995 s but only 0.493 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 14.995",
    "remaining_budget_at_turn_s: 0.493"
  ],
  "ok": true,
  "error": null
}
```
