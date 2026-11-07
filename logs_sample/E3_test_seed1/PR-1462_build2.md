# Trace of PR-1462_build2

Run: `E3_test_seed1` · events: 57

## 1. pipeline · state

- time: 2026-11-07T14:56:34.289Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 205,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T14:56:34.383Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 205
}
```

## 3. pipeline · state

- time: 2026-11-07T14:56:34.387Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.RestExampleTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:37.362Z
- latency: 2.900 s

```json
{
  "test": "org.apache.karaf.audit.util.FastDateFormatTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1346,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.audit.util.FastDateFormatTest` (source, may be truncated):
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
package org.apache.karaf.audit.util;

import org.junit.Test;

import java.text.SimpleDateFormat;
import java.util.Locale;
import java.util.TimeZone;
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.assertEquals;

public class FastDateFormatTest {

    @Test
    public void test() throws Exception {
        FastDateFormat cal = new FastDateFormat();

        long time = new SimpleDateFormat("yyyy-MM-dd").parse("<date>").getTime();
        assertEquals("Nov  5", cal.getDate(time, FastDateFormat.MMM_D2));
        assertEquals("<date>", cal.getDate(time, FastDateFormat.YYYY_MM_DD));

        time += TimeUnit.DAYS.toMillis(5) + TimeUnit.HOURS.toMillis(1);
        assertEquals("Nov 10", cal.getDate(time, FastDateFormat.MMM_D2));
        assertEquals("<date>", cal.getDate(time, FastDateFormat.YYYY_MM_DD));
    }

    @Test
    public void testTimeZone() throws Exception {
        long time = new SimpleDateFormat("yyyy-MM-dd").parse("<date>").getTime();
        FastDateFormat cal = new FastDateFormat(TimeZone.getTimeZone("GMT+5"), Locale.ENGLISH);
        assertEquals("+05:00", cal.getDate(time, FastDateFormat.XXX));
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.audit.util.FastDateFormatTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.audit.util.FastDateFormatTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code in the provided diff.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:40.130Z
- latency: 2.761 s

```json
{
  "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1613,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.shell.ssh.SshUtilsTest` (source, may be truncated):
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
package org.apache.karaf.shell.ssh;

import java.io.IOException;
import java.util.List;
import org.apache.sshd.common.cipher.Cipher;
import org.apache.sshd.common.kex.KeyExchange;
import org.apache.sshd.common.kex.KeyExchangeFactory;
import org.apache.sshd.common.mac.Mac;
import org.apache.sshd.common.NamedFactory;

import org.junit.Assert;
import org.junit.Test;

public class SshUtilsTest {
   
    @Test
    public void testCiphersDefault() throws IOException {
        // verify our default configuration...
        String ciphers = "aes128-ctr,aes128-cbc";

        List<NamedFactory<Cipher>> list = SshUtils.buildCiphers(ciphers.split(","));

        // verify that all configured ciphers are actually resolved...
        for (String cipher : ciphers.split(",")) {
            boolean found = false;
            for (NamedFactory<Cipher> factory : list) {
                if (factory.getName().equalsIgnoreCase(cipher)) {
                    found = true;
                    break;
                }
            }

            if (!found) {
                Assert.fail("Configured default cipher '" + cipher + "' cannot be resolved");
            }
        }
    }

    @Test
    public void testMacsDefault() throws IOException {
        // verify our default configuration...
        String macs = "hmac-sha2-512,hmac-sha2-256,hmac-sha1";

        List<NamedFactory<Mac>> list = SshUtils.buildMacs(macs.split(","));

        // verify that all configured HMACs are actually resolved...
        for (String mac : macs.split(",")) {
            boolean found = false;
            for (NamedFactory<Mac> factory : list) {
                if (factory.getName().equalsIgnoreCase(mac)) {
                    found = true;
                    break;
                }
            }

            if (!found) {
                Assert.fail("Configured default HMAC '" + mac + "' cannot be resolved");
            }
        }
    }

    @Test
    public void testKexAlgorithmsDefault() throws IOException {
        // verify our default configuration...
        String kexAlgorithms = "diffie-hellman-group-exchange-sha256,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256";

        Li
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.ssh.SshUtilsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:42.841Z
- latency: 2.704 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1606,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not appear to interact with the SSH client or related components that were modified in the code change.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:45.676Z
- latency: 2.828 s

```json
{
  "test": "org.apache.karaf.itests.ssh.SshKeyFormatTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1623,
  "completion_tokens": 67
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not appear to interact with the changed code related to SSH client properties and timeouts.",
  "confidence": 0.8
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:48.180Z
- latency: 2.494 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1405,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client configuration.",
  "confidence": 1
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:48.187Z
- latency: 2.685 s

```json
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1497,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:50.704Z
- latency: 2.510 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1598,
  "completion_tokens": 61
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not appear to interact with the SSH client configuration or properties.",
  "confidence": 0.8
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:50.711Z
- latency: 2.370 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1241,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:53.282Z
- latency: 2.565 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1548,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:53.291Z
- latency: 2.817 s

```json
{
  "test": "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1544,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest` (source, may be truncated):
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
package org.apache.karaf.shell.ssh;

import static java.util.Collections.emptyMap;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.Map;

import javax.security.auth.Subject;
import javax.security.auth.callback.Callback;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.callback.NameCallback;
import javax.security.auth.callback.UnsupportedCallbackException;
import javax.security.auth.login.AppConfigurationEntry;
import javax.security.auth.login.Configuration;
import javax.security.auth.spi.LoginModule;

import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.mina.core.service.IoProcessor;
import org.apache.mina.core.session.DummySession;
import org.apache.mina.core.write.WriteRequest;
import org.apache.sshd.common.io.IoHandler;
import org.apache.sshd.common.io.IoSession;
import org.apache.sshd.common.random.SingletonRandomFactory;
import org.apache.sshd.common.util.Readable;
import org.apache.sshd.common.util.net.SshdSocketAddress;
import org.apache.sshd.common.util.security.SecurityUtils;
import org.apache.sshd.mina.MinaConnector;
import org.apache.sshd.mina.MinaSession;
import org.apache.sshd.server.SshServer;
import org.apache.sshd.server.session.ServerSessionImpl;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class KarafJaasAuthenticatorTest {

    private Configuration configuration;
    private ServerSessionImpl session;

    @Before
    public void init() throws Exception {
        configuration = Configuration.getConfiguration();
        Configuration.setConfiguration(new Configuration() {
            @Override
            public AppConfigurationEntry[] getAppConfigurationEntry(String name) {
                return new AppConfigurationEntry[] {
                        new AppConfigurationEntry(SayYes.class.getName(), AppConfigurationEntry.LoginModuleControlFlag.REQUIRED, emptyMap())
                };
            }
        });
        final SshServer server = new SshServer();
        IoHandler ioHandler = new IoHandler() {
 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:55.789Z
- latency: 2.491 s

```json
{
  "test": "org.apache.karaf.itests.examples.HttpResourceExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1474,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not interact with the SSH client or related configurations that were changed in the code diff.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:58.425Z
- latency: 2.628 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1588,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not appear to interact with the SSH client or related components that were modified in the code change.",
  "confidence": 1
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:58.431Z
- latency: 2.951 s

```json
{
  "test": "org.apache.karaf.specs.locator.OsgiLocatorTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1577,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.specs.locator.OsgiLocatorTest` (source, may be truncated):
<<<TEST
/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.specs.locator;

import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

public class OsgiLocatorTest extends Assert {
    
    @BeforeClass
    public static void setup() {
        OsgiLocator.register("Factory", new MockCallable());
        OsgiLocator.register("Factory", new MockCallable2());
    }

    @Test
    public void testLocatorWithSystemProperty() {
        System.setProperty(OsgiLocator.TIMEOUT, "0");
        System.setProperty("Factory", "org.apache.karaf.specs.locator.MockCallable");
        Class clazz = OsgiLocator.locate(Object.class, "Factory");
        assertNotNull("Expected to find a class", clazz);
        assertEquals("Got the wrong class", MockCallable.class.getName(), clazz.getName());

        System.setProperty("Factory", "org.apache.karaf.specs.locator");
        clazz = OsgiLocator.locate(Object.class, "Factory");
        assertNull("Did not expect to find a class", clazz);
    }

    @Test
    public void testLocatorWithoutSystemProperty() {
        System.setProperty(OsgiLocator.TIMEOUT, "0");
        System.clearProperty("Factory");
        Class clazz = OsgiLocator.locate(Object.class, "Factory");
        assertNotNull("Expected to find a class", clazz);
        assertEquals("Got the wrong class", MockCallable2.class.getName(), clazz.getName());
    }

    @Test
    public void testLocatorWithSystemPropertyAndTimeout() {
        long timeout = 1000;
        System.setProperty(OsgiLocator.TIMEOUT, Long.toString(timeout));
        System.setProperty("Factory", "org.apache.karaf.specs.locator.MockCallable");
        Class clazz = OsgiLocator.locate(Object.class, "Factory");
        assertNotNull("Expected to find a class", clazz);
        assertEquals("Got the wrong class.", MockCallable.class.getName(), clazz.getName());

        System.setProperty("Factory", "org.apache.karaf.specs.locator");
        long t0 = System.currentTimeMillis();
        clazz = OsgiLocator.locate(Object.class, "Factory");
        long t1 = System.currentTimeMillis();
        assertNull("Did not expect to find a class", clazz);
        assertTrue("Timeout issue", (t1 - t0) > timeout / 2);
    }

    @
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.specs.locator.OsgiLocatorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.specs.locator.OsgiLocatorTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code, which includes modifications to the `Main.java` and `Activator.java` files.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:58.437Z
- latency: 2.680 s

```json
{
  "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1383,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.deployer.spring.SpringDeploymentListenerTest` (source, may be truncated):
<<<TEST
/**
 *
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.deployer.spring;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Iterator;
import java.util.Set;
import java.util.jar.JarInputStream;
import javax.xml.transform.dom.DOMSource;

import junit.framework.TestCase;

public class SpringDeploymentListenerTest extends TestCase {

    public void testPackagesExtraction() throws Exception {
        SpringDeploymentListener l = new SpringDeploymentListener();
        File f = new File(getClass().getClassLoader().getResource("test.xml").toURI());
        Set<String> pkgs = SpringTransformer.analyze(new DOMSource(SpringTransformer.parse(f.toURL())));
        assertNotNull(pkgs);
        assertEquals(2, pkgs.size());
        Iterator<String> it = pkgs.iterator();
        assertEquals("org.apache.karaf.deployer.spring", it.next());
        assertEquals("org.osgi.service.url", it.next());
    }

    public void testCustomManifest() throws Exception {
        File f = File.createTempFile("smx", ".jar");
        try {
            OutputStream os = new FileOutputStream(f);
            SpringTransformer.transform(getClass().getClassLoader().getResource("test.xml"), os);
            os.close();
            InputStream is = new FileInputStream(f);
            JarInputStream jar = new JarInputStream(is);
            jar.getManifest().write(System.err);
            is.close();
        } finally {
            f.delete();
        }
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:01.093Z
- latency: 2.649 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1538,
  "completion_tokens": 61
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:03.760Z
- latency: 2.657 s

```json
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1550,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:03.767Z
- latency: 2.924 s

```json
{
  "test": "org.apache.karaf.main.lock.MySQLJDBCLockTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1529,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.main.lock.MySQLJDBCLockTest` (source, may be truncated):
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
package org.apache.karaf.main.lock;

import static org.junit.Assert.assertEquals;

import java.sql.Connection;
import java.util.logging.Level;

import org.apache.felix.utils.properties.Properties;

import org.junit.Before;
import org.junit.Test;


public class MySQLJDBCLockTest extends BaseJDBCLockTest {
    
    @Before
    @Override
    public void setUp() throws Exception {
        driver = "com.mysql.jdbc.Driver";
        url = "jdbc:mysql://127.0.0.1:3306/test";
        createTableStmtSuffix = " ENGINE=INNODB";
        
        super.setUp();
    }
    
    MySQLJDBCLock createLock(Properties props) {
        return new MySQLJDBCLock(props) {
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + "?createDatabaseIfNotExist=true", url);
                assertEquals(this.user, username);
                assertEquals(this.password, password);
                return connection;
            }

            @Override
            long getCurrentTimeMillis() {
                return 1;
            }
            
            @Override
            public void log(Level level, String msg, Exception e) {
                // Suppress log
            }
        };
    }
    
    @Test
    public void createConnectionShouldConcatinateOptionsCorrect() {
        props.put("karaf.lock.jdbc.url", this.url + "?connectTimeout=10000");
        
        lock = new MySQLJDBCLock(props) {
            @Override
            boolean schemaExists() {
                return true;
            }
            
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + "&createDatabaseIfNotExist=true", url);
                assertEquals(this.user, username);
                assertEquals(this.password, password);
                return connection;
            }

            @Override
            long getCurrentTimeMillis() {
                return 1;
            }
       
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.lock.MySQLJDBCLockTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.lock.MySQLJDBCLockTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:06.512Z
- latency: 2.737 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1646,
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
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
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
  "reason": "The test class does not appear to interact with the SSH client configuration or properties.",
  "confidence": 0.8
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:06.519Z
- latency: 2.971 s

```json
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1583,
  "completion_tokens": 72
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/client/src/main/java/org/apache/karaf/client/Main.java b/client/src/main/java/org/apache/karaf/client/Main.java
--- a/client/src/main/java/org/apache/karaf/client/Main.java
+++ b/client/src/main/java/org/apache/karaf/client/Main.java
@@ -28,6 +28,7 @@
 import java.nio.charset.Charset;
 import java.nio.file.Paths;
 import java.security.KeyPair;
+import java.time.Duration;
 import java.util.EnumSet;
 import java.util.HashMap;
 import java.util.List;
@@ -51,8 +52,9 @@
 import org.apache.sshd.common.channel.PtyMode;
 import org.apache.sshd.common.config.keys.FilePasswordProvider;
 import org.apache.sshd.common.keyprovider.FileKeyPairProvider;
-import org.apache.sshd.common.util.io.NoCloseInputStream;
-import org.apache.sshd.common.util.io.NoCloseOutputStream;
+import org.apache.sshd.common.util.io.input.NoCloseInputStream;
+import org.apache.sshd.common.util.io.output.NoCloseOutputStream;
+import org.apache.sshd.core.CoreModuleProperties;
 import org.jline.terminal.Attributes;
 import org.jline.terminal.Attributes.ControlChar;
 import org.jline.terminal.Attributes.InputFlag;
@@ -158,9 +160,9 @@ else if (console != null) {
 
             // define hearbeat (for the keep alive) and timeouts
             // TODO this should be dealt by Apache SSH client directly using .ssh/config
-            client.getProperties().put(ClientFactoryManager.HEARTBEAT_INTERVAL, "60000");
-            client.getProperties().put(ClientFactoryManager.IDLE_TIMEOUT, String.valueOf(config.getIdleTimeout()));
-            client.getProperties().put(ClientFactoryManager.NIO2_READ_TIMEOUT, String.valueOf(config.getIdleTimeout()));
+            CoreModuleProperties.HEARTBEAT_INTERVAL.set(client, Duration.ofMillis(60000));
+            CoreModuleProperties.IDLE_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
+            CoreModuleProperties.NIO2_READ_TIMEOUT.set(client, Duration.ofMillis(config.getIdleTimeout()));
 
             // TODO: remove the line below when SSHD-732 is fixed
             // client.setKeyPairProvider(new FileKeyPairProvider());
diff --git a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
--- a/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
+++ b/shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
@@ -21,6 +21,7 @@
 import java.io.IOException;
 import java.nio.file.Path;
 import java.nio.file.Paths;
+import java.time.Duration;
 import java.util.Collections;
 
 import org.apache.karaf.shell.api.action.lifecycle.Manager;
@@ -35,10 +36,11 @@
 import org.apache.karaf.util.tracker.annotation.Services;
 import org.apache.sshd.common.file.virtualfs.VirtualFileSystemFactory;
 import org.apache.sshd.common.keyprovider.KeyPairProvider;
+import org.apache.sshd.core.CoreModuleProperties;
+import org.apache.sshd.scp.server.ScpCommandFactory;
 import org.apache.sshd.server.SshServer;
 import org.apache.sshd.server.forward.Accep
[...truncated]
DIFF>>>

Test class `org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest` (source, may be truncated):
<<<TEST
/*
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
package org.apache.karaf.jaas.blueprint.jasypt.handler;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.Arrays;
import java.util.Collection;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.jar.JarInputStream;

import junit.framework.TestCase;
import org.apache.felix.connect.PojoServiceRegistryFactoryImpl;
import org.apache.felix.connect.launch.BundleDescriptor;
import org.apache.felix.connect.launch.ClasspathScanner;
import org.apache.felix.connect.launch.PojoServiceRegistry;
import org.apache.felix.connect.launch.PojoServiceRegistryFactory;
import org.apache.karaf.jaas.blueprint.jasypt.handler.beans.Bean;
import org.apache.karaf.util.StreamUtils;
import org.jasypt.encryption.pbe.StandardPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.EnvironmentStringPBEConfig;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.ops4j.pax.tinybundles.core.TinyBundle;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.Constants;
import org.osgi.framework.Filter;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceReference;
import org.osgi.util.tracker.ServiceTracker;

import static org.ops4j.pax.tinybundles.core.TinyBundles.bundle;

public class EncryptablePropertyPlaceholderTest extends TestCase {

    public static final long DEFAULT_TIMEOUT = 30000;

    private BundleContext bundleContext;

    @Before
    public void setUp() throws Exception {

        StandardPBEStringEncryptor enc = new StandardPBEStringEncryptor();
        EnvironmentStringPBEConfig env = new EnvironmentStringPBEConfig();
        env.setAlgorithm("PBEWithMD5AndDES");
        env.setPassword("password");
        enc.setConfig(env);
        String val = enc.encrypt("bar");
        System.setProperty("foo", val);

        System.setProperty("org.bundles.framework.storage", "target/bundles/" + System.currentTimeMillis());
        System.setProperty("karaf.name", "root");

        List<BundleDescriptor> bundles = new ClasspathScanner().scanForBundles("(Bundle-SymbolicName=*)");
        bundles.add(getBundleDescriptor(
                "target/jasypt.jar",
            
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 23. orchestrator · llm_call

- time: 2026-11-07T14:57:10.705Z
- latency: 4.037 s

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
- n_code_files = 7: number of changed code files in the diff
- n_dirs = 3: number of distinct folders those files are in
- lines_added = 31: added lines in the diff
- lines_removed = 24: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 205: number of candidate test classes
- shortlist_size = 19: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.0210526: mean relevance used over the shortlisted tests
- rel_max = 0.1: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.159037: highest history score over all candidates
- hist_mean_shortlist = 0.0293427: mean history score over the shortlisted tests

Changed files (7):
- client/src/main/java/org/apache/karaf/client/Main.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java
- shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java
- shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java
- shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.audit.util.FastDateFormatTest | 0.000 | 1.000 | 0.000 | 0.004
- org.apache.karaf.shell.ssh.SshUtilsTest | 0.159 | 1.000 | 0.100 | 0.078
- org.apache.karaf.itests.examples.JpaExampleTest | 0.093 | 0.313 | 0.000 | 7.782
- org.apache.karaf.itests.ssh.SshKeyFormatTest | 0.000 | 1.000 | 0.100 | 0.54
- org.apache.karaf.itests.examples.JdbcExampleTest | 0.069 | 0.132 | 0.000 | 10.701
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 1.000 | 0.000 | 0.029
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.052 | 0.693 | 0.100 | 0.32
- org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest | 0.000 | 1.000 | 0.000 | 0.271
- org.apache.karaf.itests.examples.ServletExampleTest | 0.041 | 0.707 | 0.000 | 58.216
- org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest | 0.000 | 1.000 | 0.000 | 0.683
- org.apache.karaf.itests.examples.HttpResourceExampleTest | 0.031 | 0.585 | 0.000 | 2.369
- org.apache.karaf.itests.examples.RestExampleTest | 0.031 | 0.591 | 0.000 | 80.073
- org.apache.karaf.specs.locator.OsgiLocatorTest | 0.000 | 1.000 | 0.000 | 1.004
- org.apache.karaf.deployer.spring.SpringDeploymentListenerTest | 0.000 | 0.998 | 0.000 | 0.582
- org.apache.karaf.itests.examples.SoapExampleTest | 0.031 | 0.752 | 0.000 | 24.923
- org.apache.karaf.itests.examples.WebSocketExampleTest | 0.031 | 0.662 | 0.000 | 13.615
- org.apache.karaf.main.lock.MySQLJDBCLockTest | 0.000 | 0.980 | 0.000 | 0.033
- org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest | 0.021 | 0.558 | 0.100 | 34.715
- org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest | 0.000 | 0.900 | 0.000 | 1.063

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
{"action": "final", "w": 0.7, "confidence": 0.8, "reason": "The change involves a small number of files and folders, and the relevance signal is weak, with no shortlisted tests having a relevance >= 0.5. The history signal is also informative with a high recent failure density."}
```

## 24. orchestrator · decision

- time: 2026-11-07T14:57:10.722Z
- latency: —

```json
{
  "w": 0.7,
  "confidence": 0.8,
  "source": "agent",
  "reason": "The change involves a small number of files and folders, and the relevance signal is weak, with no shortlisted tests having a relevance >= 0.5. The history signal is also informative with a high recent failure density.",
  "tool_calls": 0
}
```

## 25. pipeline · state

- time: 2026-11-07T14:57:10.961Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```

## 26. pipeline · state

- time: 2026-11-07T14:57:10.980Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T14:57:10.997Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.shell.ssh.KnownHostsManagerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T14:57:11.104Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T14:57:11.120Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T14:57:11.136Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T14:57:11.245Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T14:57:11.261Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T14:57:11.279Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T14:57:11.388Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T14:57:11.407Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T14:57:11.427Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T14:57:11.532Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T14:57:11.552Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T14:57:11.570Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T14:57:11.622Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 41. explainer · explanation

- time: 2026-11-07T14:57:17.198Z
- latency: 5.560 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 9,
    "n_candidates": 205,
    "n_selected": 28,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 12,
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
        null
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 24.923,
    "budget_s": 41.344,
    "remaining_budget_at_turn_s": 3.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 63.064
  },
  "justification": "Skipping it is risky: it has a low relevance of 0.0 because it does not appear to interact with the changed code in Main.java or Activator.java. It needs 24.923 s but only 3.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: client/src/main/java/org/apache/karaf/client/Main.java",
    "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
    "duration_s: 24.923",
    "remaining_budget_at_turn_s: 3.203"
  ],
  "ok": true,
  "error": null
}
```

## 42. explainer · explanation

- time: 2026-11-07T14:57:22.648Z
- latency: 5.435 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 10,
    "n_candidates": 205,
    "n_selected": 28,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 4,
      "failure_rate": 0.041237113402061855,
      "last_failure_distance": 12,
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
        null
      ]
    },
    "history_score": 0.041,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 58.216,
    "budget_s": 41.344,
    "remaining_budget_at_turn_s": 3.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 96.357
  },
  "justification": "Skipping it is risky: it has a relevance of 0.0 because it does not appear to interact with the changed code in Main.java or Activator.java, and it needs 58.216 s but only 3.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: client/src/main/java/org/apache/karaf/client/Main.java",
    "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
    "duration_s: 58.216",
    "remaining_budget_at_turn_s: 3.203"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T14:57:26.802Z
- latency: 4.139 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 11,
    "n_candidates": 205,
    "n_selected": 28,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 20,
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
        null
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the SSH client configuration or properties.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 34.715,
    "budget_s": 41.344,
    "remaining_budget_at_turn_s": 3.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 72.856
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not appear to interact with the SSH client configuration or properties, and it needs 34.715 s but only 3.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "duration_s: 34.715",
    "remaining_budget_at_turn_s: 3.203"
  ],
  "ok": true,
  "error": null
}
```

## 44. explainer · explanation

- time: 2026-11-07T14:57:31.257Z
- latency: 4.441 s

```json
{
  "test": "org.apache.karaf.itests.examples.WarExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.WarExampleTest",
    "rank_by_value": 12,
    "n_candidates": 205,
    "n_selected": 28,
    "history": {
      "test": "org.apache.karaf.itests.examples.WarExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 15,
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
        null
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 5.198,
    "budget_s": 41.344,
    "remaining_budget_at_turn_s": 3.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 43.339
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 5.198 s but only 3.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 5.198",
    "remaining_budget_at_turn_s: 3.203"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T14:57:35.583Z
- latency: 4.313 s

```json
{
  "test": "org.apache.karaf.itests.WebTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.WebTest",
    "rank_by_value": 13,
    "n_candidates": 205,
    "n_selected": 28,
    "history": {
      "test": "org.apache.karaf.itests.WebTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 15,
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
        null
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 6.387,
    "budget_s": 41.344,
    "remaining_budget_at_turn_s": 3.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 44.528
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 6.387 s but only 3.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 6.387",
    "remaining_budget_at_turn_s: 3.203"
  ],
  "ok": true,
  "error": null
}
```

## 46. pipeline · state

- time: 2026-11-07T14:57:35.657Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 47. explainer · explanation

- time: 2026-11-07T14:57:42.416Z
- latency: 6.741 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 10,
    "n_candidates": 205,
    "n_selected": 20,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 4,
      "failure_rate": 0.041237113402061855,
      "last_failure_distance": 12,
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
        null
      ]
    },
    "history_score": 0.041,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 58.216,
    "budget_s": 82.687,
    "remaining_budget_at_turn_s": 19.623,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 121.28
  },
  "justification": "Skipping it is reasonable: its relevance is 0.0 because it does not appear to interact with the changed code in Main.java or Activator.java, and it has a failure rate of 0.041237113402061855 over 97 runs. It needs 58.216 s but only 19.623 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: client/src/main/java/org/apache/karaf/client/Main.java",
    "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
    "failures: 4 of 97 runs",
    "duration_s: 58.216",
    "remaining_budget_at_turn_s: 19.623"
  ],
  "ok": true,
  "error": null
}
```

## 48. explainer · explanation

- time: 2026-11-07T14:57:47.771Z
- latency: 5.338 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 11,
    "n_candidates": 205,
    "n_selected": 20,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 2,
      "failure_rate": 0.020618556701030927,
      "last_failure_distance": 20,
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
        null
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the SSH client configuration or properties.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 34.715,
    "budget_s": 82.687,
    "remaining_budget_at_turn_s": 19.623,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 97.779
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not appear to interact with the SSH client configuration or properties, and it has a failure rate of 0.0206. It needs 34.715 s but only 19.623 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "history_score: 0.021",
    "failures: 2 of 97 runs",
    "duration_s: 34.715",
    "remaining_budget_at_turn_s: 19.623"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T14:57:52.264Z
- latency: 4.474 s

```json
{
  "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "rank_by_value": 14,
    "n_candidates": 205,
    "n_selected": 20,
    "history": {
      "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
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
        null
      ]
    },
    "history_score": 0.015,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 11.267,
    "budget_s": 82.687,
    "remaining_budget_at_turn_s": 8.038,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 85.916
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 11.267 s but only 8.038 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 11.267",
    "remaining_budget_at_turn_s: 8.038"
  ],
  "ok": true,
  "error": null
}
```

## 50. explainer · explanation

- time: 2026-11-07T14:57:56.325Z
- latency: 4.045 s

```json
{
  "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "rank_by_value": 16,
    "n_candidates": 205,
    "n_selected": 20,
    "history": {
      "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
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
        null
      ]
    },
    "history_score": 0.015,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 11.55,
    "budget_s": 82.687,
    "remaining_budget_at_turn_s": 0.078,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 94.159
  },
  "justification": "Skipping it is risky: it has a failure rate of 0.0104 and its duration of 11.55 s exceeds the remaining budget of 0.078 s.",
  "cited_facts": [
    "failure_rate: 0.010416666666666666",
    "duration_s: 11.55",
    "remaining_budget_at_turn_s: 0.078"
  ],
  "ok": true,
  "error": null
}
```

## 51. explainer · explanation

- time: 2026-11-07T14:58:13.712Z
- latency: 17.368 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 17,
    "n_candidates": 205,
    "n_selected": 20,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 12,
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
        null
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with the SSH client or related components that were modified in the code change.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 80.073,
    "budget_s": 82.687,
    "remaining_budget_at_turn_s": 0.078,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 162.682
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 52. pipeline · state

- time: 2026-11-07T14:58:13.786Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest"
  ]
}
```

## 53. explainer · explanation

- time: 2026-11-07T14:58:18.185Z
- latency: 4.380 s

```json
{
  "test": "org.apache.karaf.itests.WebTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.WebTest",
    "rank_by_value": 13,
    "n_candidates": 205,
    "n_selected": 43,
    "history": {
      "test": "org.apache.karaf.itests.WebTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 15,
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
        null
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 6.387,
    "budget_s": 165.375,
    "remaining_budget_at_turn_s": 4.182,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 167.58
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 97 runs, indicating potential instability. It needs 6.387 s but only 4.182 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 6.387",
    "remaining_budget_at_turn_s: 4.182"
  ],
  "ok": true,
  "error": null
}
```

## 54. explainer · explanation

- time: 2026-11-07T14:58:22.686Z
- latency: 4.486 s

```json
{
  "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "rank_by_value": 14,
    "n_candidates": 205,
    "n_selected": 43,
    "history": {
      "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
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
        null
      ]
    },
    "history_score": 0.015,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 11.267,
    "budget_s": 165.375,
    "remaining_budget_at_turn_s": 4.182,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 172.46
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 11.267 s but only 4.182 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 11.267",
    "remaining_budget_at_turn_s: 4.182"
  ],
  "ok": true,
  "error": null
}
```

## 55. explainer · explanation

- time: 2026-11-07T14:58:26.966Z
- latency: 4.266 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.FeatureTest",
    "rank_by_value": 15,
    "n_candidates": 205,
    "n_selected": 43,
    "history": {
      "test": "org.apache.karaf.itests.FeatureTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 100,
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
        null
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 7.96,
    "budget_s": 165.375,
    "remaining_budget_at_turn_s": 4.182,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 169.153
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential issues. It needs 7.96 s but only 4.182 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 7.96",
    "remaining_budget_at_turn_s: 4.182"
  ],
  "ok": true,
  "error": null
}
```

## 56. explainer · explanation

- time: 2026-11-07T14:58:31.406Z
- latency: 4.426 s

```json
{
  "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "rank_by_value": 16,
    "n_candidates": 205,
    "n_selected": 43,
    "history": {
      "test": "org.apache.karaf.itests.features.Spring3FeaturesTest",
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
        null
      ]
    },
    "history_score": 0.015,
    "relevance_used": 0.0,
    "relevance_reason": null,
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 11.55,
    "budget_s": 165.375,
    "remaining_budget_at_turn_s": 4.182,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 172.743
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 11.55 s but only 4.182 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 11.55",
    "remaining_budget_at_turn_s: 4.182"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T14:58:48.794Z
- latency: 17.369 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 17,
    "n_candidates": 205,
    "n_selected": 43,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 12,
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
        null
      ]
    },
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with the SSH client or related components that were modified in the code change.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/SshUtilsTest.java"
    ],
    "duration_s": 80.073,
    "budget_s": 165.375,
    "remaining_budget_at_turn_s": 4.182,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 241.266
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```
