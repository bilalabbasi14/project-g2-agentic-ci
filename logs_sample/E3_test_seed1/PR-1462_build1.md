# Trace of PR-1462_build1

Run: `E3_test_seed1` · events: 49

## 1. pipeline · state

- time: 2026-11-07T14:56:34.286Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 130,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T14:56:34.374Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 130
}
```

## 3. pipeline · state

- time: 2026-11-07T14:56:34.378Z
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

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:37.388Z
- latency: 2.976 s

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

- time: 2026-11-07T14:56:39.977Z
- latency: 2.578 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1572,
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

Test class `org.apache.karaf.main.MainLockingTest` (source, may be truncated):
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
package org.apache.karaf.main;

import static org.ops4j.pax.tinybundles.core.TinyBundles.withBnd;

import java.io.File;
import java.io.IOException;

import org.apache.karaf.main.util.Utils;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.ops4j.pax.tinybundles.core.TinyBundles;
import org.osgi.framework.Bundle;
import org.osgi.framework.Constants;
import org.osgi.framework.launch.Framework;
import org.osgi.framework.startlevel.FrameworkStartLevel;

public class MainLockingTest {
    private File home;

    private File data;
    private File log;

    @Before
    public void setUp() throws IOException {
        File basedir = new File(getClass().getClassLoader().getResource("foo").getPath()).getParentFile();
        home = new File(basedir, "test-karaf-home");
        data = new File(home, "data" + System.currentTimeMillis());
        log = new File(home, "log" + System.currentTimeMillis());

        Utils.deleteDirectory(data);

        System.setProperty("karaf.home", home.toString());
        System.setProperty("karaf.data", data.toString());
        System.setProperty("karaf.log", log.toString());
        System.setProperty("karaf.framework.factory", "org.apache.felix.framework.FrameworkFactory");

        System.setProperty("karaf.lock", "true");
        System.setProperty("karaf.lock.delay", "1000");
        System.setProperty("karaf.lock.class", "org.apache.karaf.main.MockLock");
    }

    @After
    public void tearDown() {
        home = null;
        data = null;
        log = null;

        System.clearProperty("karaf.home");
        System.clearProperty("karaf.data");
        System.clearProperty("karaf.log");
        System.clearProperty("karaf.framework.factory");

        System.clearProperty("karaf.lock");
        System.clearProperty("karaf.lock.delay");
        System.clearProperty("karaf.lock.lostThreshold");
        System.clearProperty("karaf.lock.class");

        System.clearProperty("karaf.pid.file");
    }

    @Test
    public void testLostMasterLock() throws Exception {
        String[] args = new String[0];
        Main main = new Main(args);
        main.launch();
  
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.MainLockingTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:42.955Z
- latency: 2.971 s

```json
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
  "attempt": 0,
  "cached": false,
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

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:45.647Z
- latency: 2.685 s

```json
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "attempt": 0,
  "cached": false,
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

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:48.024Z
- latency: 2.370 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
  "attempt": 0,
  "cached": false,
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

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:50.849Z
- latency: 2.817 s

```json
{
  "test": "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
  "attempt": 0,
  "cached": false,
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

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:53.810Z
- latency: 2.951 s

```json
{
  "test": "org.apache.karaf.specs.locator.OsgiLocatorTest",
  "attempt": 0,
  "cached": false,
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

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:56.497Z
- latency: 2.680 s

```json
{
  "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
  "attempt": 0,
  "cached": false,
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

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T14:56:59.652Z
- latency: 3.148 s

```json
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1609,
  "completion_tokens": 74
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

Test class `org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest` (source, may be truncated):
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

import junit.framework.TestCase;
import org.apache.felix.connect.PojoServiceRegistryFactoryImpl;
import org.apache.felix.connect.launch.BundleDescriptor;
import org.apache.felix.connect.launch.ClasspathScanner;
import org.apache.felix.connect.launch.PojoServiceRegistry;
import org.apache.felix.connect.launch.PojoServiceRegistryFactory;
import org.apache.karaf.util.StreamUtils;
import org.jasypt.encryption.pbe.StandardPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.EnvironmentStringPBEConfig;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.ops4j.pax.tinybundles.core.TinyBundle;
import org.osgi.framework.*;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;
import org.osgi.util.tracker.ServiceTracker;

import java.io.*;
import java.util.*;
import java.util.jar.JarInputStream;

import static org.ops4j.pax.tinybundles.core.TinyBundles.bundle;

public class EncryptableConfigAdminPropertyPlaceholderTest extends TestCase {

    public static final long DEFAULT_TIMEOUT = 30000;

    private BundleContext bundleContext;
    private ConfigurationAdmin configAdmin;
    private EnvironmentStringPBEConfig env;
    private StandardPBEStringEncryptor enc;
    private String encryptedValue;

    @Before
    public void setUp() throws Exception {

        // Configure Jasypt
        enc = new StandardPBEStringEncryptor();
        env = new EnvironmentStringPBEConfig();
        env.setAlgorithm("PBEWithMD5AndDES");
        env.setPassword("password");
        enc.setConfig(env);

        System.setProperty("org.osgi.framework.storage", "target/osgi/" + System.currentTimeMillis());
        System.setProperty("karaf.name", "root");

        List<BundleDescriptor> bundles = new ClasspathScanner().scanForBundles("(Bundle-SymbolicName=*)");
        bundles.add(getBundleDescriptor(
                "target/jasypt2.jar",
                bundle().add("OSGI-INF/blueprint/karaf-jaas-jasypt.xml", getClass().getResource("/OSGI-INF/blueprint/karaf-jaas-jasypt.xml"))
                        .set("Manifest-Version", "2")
                        .set("Bundle-ManifestVersion", "2")
                        .set("Bundle-SymbolicName", "jasypt")
                        .set("Bundle-Version", "0.0.0")));
        bundles.add(getBundleDescriptor(
                "t
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:02.584Z
- latency: 2.924 s

```json
{
  "test": "org.apache.karaf.main.lock.MySQLJDBCLockTest",
  "attempt": 0,
  "cached": false,
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

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T14:57:05.141Z
- latency: 2.546 s

```json
{
  "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1304,
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

Test class `org.apache.karaf.config.core.impl.ConfigMBeanImplTest` (source, may be truncated):
<<<TEST
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.karaf.config.core.impl;

import org.junit.Assert;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class ConfigMBeanImplTest {

    @Test(expected = IllegalArgumentException.class)
    public void testInstallWithNonAuthorizePath() throws Exception {
        System.setProperty("karaf.etc", ".");

        ConfigMBeanImpl configMBean = new ConfigMBeanImpl();

        configMBean.install("file:foo.cfg", "../test.cfg", false);
    }

    @Test
    public void testInstall() throws Exception {
        System.setProperty("karaf.etc", "./target/test-classes");

        ConfigMBeanImpl configMBean = new ConfigMBeanImpl();

        configMBean.install("file:./target/test-classes/test.cfg", "foo.cfg", true);

        File output = new File("target/test-classes/foo.cfg");

        Assert.assertTrue(output.exists());

        StringBuilder builder = new StringBuilder();
        BufferedReader reader = new BufferedReader(new FileReader(output));
        String line = null;
        while ((line = reader.readLine()) != null) {
            builder.append(line).append("\n");
        }
        Assert.assertTrue(builder.toString().contains("foo=bar"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 15. orchestrator · llm_call

- time: 2026-11-07T14:57:08.030Z
- latency: 2.769 s

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
- n_code_files = 6: number of changed code files in the diff
- n_dirs = 3: number of distinct folders those files are in
- lines_added = 29: added lines in the diff
- lines_removed = 21: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 130: number of candidate test classes
- shortlist_size = 11: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.00909091: mean relevance used over the shortlisted tests
- rel_max = 0.1: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
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
- org.apache.karaf.audit.util.FastDateFormatTest | 0.000 | 1.000 | 0.000 | 0.004
- org.apache.karaf.main.MainLockingTest | 0.010 | 0.762 | 0.100 | 23.461
- org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest | 0.000 | 1.000 | 0.000 | 1.127
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 1.000 | 0.000 | 0.03
- org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest | 0.000 | 1.000 | 0.000 | 0.272
- org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest | 0.000 | 1.000 | 0.000 | 0.864
- org.apache.karaf.specs.locator.OsgiLocatorTest | 0.000 | 1.000 | 0.000 | 1.005
- org.apache.karaf.deployer.spring.SpringDeploymentListenerTest | 0.000 | 0.999 | 0.000 | 0.595
- org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest | 0.000 | 0.995 | 0.000 | 0.09
- org.apache.karaf.main.lock.MySQLJDBCLockTest | 0.000 | 0.985 | 0.000 | 0.047
- org.apache.karaf.config.core.impl.ConfigMBeanImplTest | 0.000 | 0.927 | 0.000 | 0.048

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
{"action": "final", "w": 0.2, "confidence": 0.8, "reason": "Low relevance signal and weak history indicate a need to trust relevance more."}
```

## 16. orchestrator · decision

- time: 2026-11-07T14:57:08.051Z
- latency: —

```json
{
  "w": 0.2,
  "confidence": 0.8,
  "source": "agent",
  "reason": "Low relevance signal and weak history indicate a need to trust relevance more.",
  "tool_calls": 0
}
```

## 17. pipeline · state

- time: 2026-11-07T14:57:08.314Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
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

## 18. pipeline · state

- time: 2026-11-07T14:57:08.331Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
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

## 19. pipeline · state

- time: 2026-11-07T14:57:08.348Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
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

## 20. pipeline · state

- time: 2026-11-07T14:57:08.437Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 21. pipeline · state

- time: 2026-11-07T14:57:08.451Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 22. pipeline · state

- time: 2026-11-07T14:57:08.465Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```

## 23. pipeline · state

- time: 2026-11-07T14:57:08.565Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 24. pipeline · state

- time: 2026-11-07T14:57:08.579Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 25. pipeline · state

- time: 2026-11-07T14:57:08.599Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```

## 26. pipeline · state

- time: 2026-11-07T14:57:08.701Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T14:57:08.718Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T14:57:08.735Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T14:57:08.833Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T14:57:08.850Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T14:57:08.864Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T14:57:08.903Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 33. explainer · explanation

- time: 2026-11-07T14:57:26.843Z
- latency: 17.916 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 1,
    "n_candidates": 130,
    "n_selected": 42,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 94,
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
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 23.461,
    "budget_s": 4.886,
    "remaining_budget_at_turn_s": 4.886,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 23.461
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 34. explainer · explanation

- time: 2026-11-07T14:57:30.810Z
- latency: 3.947 s

```json
{
  "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "rank_by_value": 40,
    "n_candidates": 130,
    "n_selected": 42,
    "history": {
      "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
      "history_builds": 100,
      "runs": 90,
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.169,
    "budget_s": 4.886,
    "remaining_budget_at_turn_s": 0.117,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.938
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.169 s, which is very short but still needs 0.117 s of the remaining budget, leaving only 0.048 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.169",
    "remaining_budget_at_turn_s: 0.117"
  ],
  "ok": true,
  "error": null
}
```

## 35. explainer · explanation

- time: 2026-11-07T14:57:35.257Z
- latency: 4.425 s

```json
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "rank_by_value": 45,
    "n_candidates": 130,
    "n_selected": 42,
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.113,
    "budget_s": 4.886,
    "remaining_budget_at_turn_s": 0.035,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.964
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.113 s, which is very short but still needs 4.964 s of the budget to run, leaving only 0.035 s remaining.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.113",
    "remaining_budget_at_turn_s: 0.035",
    "fits_if_budget_s: 4.964"
  ],
  "ok": true,
  "error": null
}
```

## 36. explainer · explanation

- time: 2026-11-07T14:57:38.738Z
- latency: 3.465 s

```json
{
  "test": "org.apache.karaf.bundle.command.ListServicesTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.bundle.command.ListServicesTest",
    "rank_by_value": 47,
    "n_candidates": 130,
    "n_selected": 42,
    "history": {
      "test": "org.apache.karaf.bundle.command.ListServicesTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.062,
    "budget_s": 4.886,
    "remaining_budget_at_turn_s": 0.03,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.918
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.062 s, which is very short but still exceeds the remaining budget of 0.03 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.062",
    "remaining_budget_at_turn_s: 0.03"
  ],
  "ok": true,
  "error": null
}
```

## 37. explainer · explanation

- time: 2026-11-07T14:57:42.176Z
- latency: 3.421 s

```json
{
  "test": "org.apache.karaf.event.service.EventCollectorTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.event.service.EventCollectorTest",
    "rank_by_value": 78,
    "n_candidates": 130,
    "n_selected": 42,
    "history": {
      "test": "org.apache.karaf.event.service.EventCollectorTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.011,
    "budget_s": 4.886,
    "remaining_budget_at_turn_s": 0.003,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.894
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.011 s, which is less than the remaining budget of 0.003 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.011",
    "remaining_budget_at_turn_s: 0.003"
  ],
  "ok": true,
  "error": null
}
```

## 38. pipeline · state

- time: 2026-11-07T14:57:42.240Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest"
  ]
}
```

## 39. explainer · explanation

- time: 2026-11-07T14:57:59.421Z
- latency: 17.163 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 1,
    "n_candidates": 130,
    "n_selected": 62,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 94,
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
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 23.461,
    "budget_s": 9.772,
    "remaining_budget_at_turn_s": 9.772,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 23.461
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 40. explainer · explanation

- time: 2026-11-07T14:58:02.819Z
- latency: 3.385 s

```json
{
  "test": "org.apache.karaf.event.service.EventCollectorTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.event.service.EventCollectorTest",
    "rank_by_value": 78,
    "n_candidates": 130,
    "n_selected": 62,
    "history": {
      "test": "org.apache.karaf.event.service.EventCollectorTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.011,
    "budget_s": 9.772,
    "remaining_budget_at_turn_s": 0.003,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 9.78
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.011 s, which is less than the remaining budget of 0.003 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.011",
    "remaining_budget_at_turn_s: 0.003"
  ],
  "ok": true,
  "error": null
}
```

## 41. explainer · explanation

- time: 2026-11-07T14:58:06.328Z
- latency: 3.495 s

```json
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventTailCommandTest",
    "rank_by_value": 79,
    "n_candidates": 130,
    "n_selected": 62,
    "history": {
      "test": "org.apache.karaf.event.command.EventTailCommandTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.245,
    "budget_s": 9.772,
    "remaining_budget_at_turn_s": 0.003,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 10.014
  },
  "justification": "Skipping it is risky: it has no relevance and its duration is 0.245 s, but only 0.003 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.245",
    "remaining_budget_at_turn_s: 0.003"
  ],
  "ok": true,
  "error": null
}
```

## 42. explainer · explanation

- time: 2026-11-07T14:58:09.752Z
- latency: 3.411 s

```json
{
  "test": "org.apache.karaf.event.command.EventSendCommandTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventSendCommandTest",
    "rank_by_value": 80,
    "n_candidates": 130,
    "n_selected": 62,
    "history": {
      "test": "org.apache.karaf.event.command.EventSendCommandTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.007,
    "budget_s": 9.772,
    "remaining_budget_at_turn_s": 0.003,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 9.776
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.007 s, which is less than the remaining budget of 0.003 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.007",
    "remaining_budget_at_turn_s: 0.003"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T14:58:25.482Z
- latency: 15.706 s

```json
{
  "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "rank_by_value": 83,
    "n_candidates": 130,
    "n_selected": 62,
    "history": {
      "test": "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
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
    "relevance_reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.595,
    "budget_s": 9.772,
    "remaining_budget_at_turn_s": 0.001,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 10.366
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 44. pipeline · state

- time: 2026-11-07T14:58:25.554Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```

## 45. explainer · explanation

- time: 2026-11-07T14:58:31.373Z
- latency: 5.802 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.main.MainLockingTest",
    "rank_by_value": 1,
    "n_candidates": 130,
    "n_selected": 54,
    "history": {
      "test": "org.apache.karaf.main.MainLockingTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 94,
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
    "relevance_reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
    "changed_files": [
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 23.461,
    "budget_s": 19.543,
    "remaining_budget_at_turn_s": 19.543,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 23.461
  },
  "justification": "Skipping it is risky: its relevance is 0.1 because it does not appear to interact with the changed code in Main.java or Activator.java, although it failed once in 100 runs. It needs 23.461 s but the budget was already fully used when it was reached.",
  "cited_facts": [
    "relevance_used: 0.1",
    "changed_files: client/src/main/java/org/apache/karaf/client/Main.java, shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
    "failures: 1 of 100 runs",
    "duration_s: 23.461",
    "remaining_budget_at_turn_s: 19.543"
  ],
  "ok": true,
  "error": null
}
```

## 46. explainer · explanation

- time: 2026-11-07T14:58:34.753Z
- latency: 3.366 s

```json
{
  "test": "org.apache.karaf.event.service.EventCollectorTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.event.service.EventCollectorTest",
    "rank_by_value": 78,
    "n_candidates": 130,
    "n_selected": 54,
    "history": {
      "test": "org.apache.karaf.event.service.EventCollectorTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.011,
    "budget_s": 19.543,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 19.554
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.011 s, which is less than the remaining budget of 0.0 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.011",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 47. explainer · explanation

- time: 2026-11-07T14:58:37.997Z
- latency: 3.225 s

```json
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventTailCommandTest",
    "rank_by_value": 79,
    "n_candidates": 130,
    "n_selected": 54,
    "history": {
      "test": "org.apache.karaf.event.command.EventTailCommandTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.245,
    "budget_s": 19.543,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 19.788
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.245 s, which exceeds the remaining budget of 0.0 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.245",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 48. explainer · explanation

- time: 2026-11-07T14:58:41.417Z
- latency: 3.400 s

```json
{
  "test": "org.apache.karaf.event.command.EventSendCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventSendCommandTest",
    "rank_by_value": 80,
    "n_candidates": 130,
    "n_selected": 54,
    "history": {
      "test": "org.apache.karaf.event.command.EventSendCommandTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.007,
    "budget_s": 19.543,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 19.55
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.007 s, which is less than the remaining budget of 0.0 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.007",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T14:58:44.864Z
- latency: 3.431 s

```json
{
  "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
    "rank_by_value": 82,
    "n_candidates": 130,
    "n_selected": 54,
    "history": {
      "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
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
      "client/src/main/java/org/apache/karaf/client/Main.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/Activator.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/KarafAgentFactory.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshAction.java",
      "shell/ssh/src/main/java/org/apache/karaf/shell/ssh/SshServerAction.java",
      "shell/ssh/src/test/java/org/apache/karaf/shell/ssh/KarafJaasAuthenticatorTest.java"
    ],
    "duration_s": 0.002,
    "budget_s": 19.543,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 19.545
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.002 s, which is negligible compared to the remaining budget of 0.0 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.002",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```
