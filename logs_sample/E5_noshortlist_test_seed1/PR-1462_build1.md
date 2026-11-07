# Trace of PR-1462_build1

Run: `E5_noshortlist_test_seed1` · events: 138

## 1. pipeline · state

- time: 2026-11-07T18:00:00.293Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 130,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T18:00:00.393Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 130
}
```

## 3. pipeline · state

- time: 2026-11-07T18:00:00.398Z
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

- time: 2026-11-07T18:00:04.769Z
- latency: 3.869 s

```json
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1599,
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

Test class `org.apache.karaf.audit.logger.EventLoggerTest` (source, may be truncated):
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
package org.apache.karaf.audit.logger;

import org.apache.karaf.audit.Event;
import org.apache.karaf.audit.EventLayout;
import org.apache.karaf.audit.EventLogger;
import org.apache.karaf.audit.MapEvent;
import org.apache.karaf.audit.layout.GelfLayout;
import org.apache.karaf.audit.layout.Rfc3164Layout;
import org.apache.karaf.audit.layout.Rfc5424Layout;
import org.junit.Test;

import javax.management.ObjectName;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TimeZone;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class EventLoggerTest {

    private static final String INVOKE = "invoke";
    private static final String[] INVOKE_SIG = new String[] {ObjectName.class.getName(), String.class.getName(), Object[].class.getName(), String[].class.getName()};

    @Test
    public void testUdp() throws Exception {
        Map<String, Object> map = new HashMap<>();
        map.put("type", Event.TYPE_JMX);
        map.put("subtype", INVOKE);
        map.put("method", INVOKE);
        map.put("signature", INVOKE_SIG);
        map.put("params", new Object[] { new ObjectName("org.apache.karaf.Mbean:type=foo"), "myMethod", new Object[] { String.class.getName() }, new String[] { "the-param "}});
        Event event = new MapEvent(map, 1510902000000L);

        int port = getNewPort();

        DatagramSocket socket = new DatagramSocket(port);
        List<DatagramPacket> packets = new ArrayList<>();
        new Thread(() -> {
            try {
                DatagramPacket dp = new DatagramPacket(new byte[1024], 1024);
               
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.audit.logger.EventLoggerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:04.778Z
- latency: 2.976 s

```json
{
  "test": "org.apache.karaf.audit.util.FastDateFormatTest",
  "attempt": 0,
  "cached": true,
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

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:07.677Z
- latency: 2.892 s

```json
{
  "test": "org.apache.karaf.bundle.command.ListServicesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1335,
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

Test class `org.apache.karaf.bundle.command.ListServicesTest` (source, may be truncated):
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
package org.apache.karaf.bundle.command;

import java.util.Arrays;

import org.apache.karaf.bundle.core.internal.BundleServiceImpl;
import org.junit.Test;
import org.osgi.framework.BundleContext;

public class ListServicesTest {

    private BundleContext bundleContext;
    private Services listServices;

    public ListServicesTest() {
        listServices = new Services();
        bundleContext = new TestBundleFactory().createBundleContext();
        listServices.context = null;
        listServices.setBundleContext(bundleContext);
        listServices.setBundleService(new BundleServiceImpl(bundleContext));
    }
    
    @Test
    public void listAllShort() throws Exception {
        System.out.println("listAllShort");
        listServices.execute();
    }

    
    @Test
    public void listAllLong() throws Exception {
        System.out.println("listAllLong");
        listServices.ids = Arrays.asList("1", "2");
        listServices.execute();
    }

    @Test
    public void listAllLongServiceUse() throws Exception {
        System.out.println("listAllLongServicesUse");
        listServices.ids = Arrays.asList("1", "2");
        listServices.inUse = true;
        listServices.execute();
    }


}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.bundle.command.ListServicesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.bundle.command.ListServicesTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, client configuration, or the changes made in the provided diff.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:10.615Z
- latency: 2.928 s

```json
{
  "test": "org.apache.karaf.bundle.command.bundletree.TreeTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1535,
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

Test class `org.apache.karaf.bundle.command.bundletree.TreeTest` (source, may be truncated):
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
package org.apache.karaf.bundle.command.bundletree;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.Set;

import org.junit.Test;

/**
 * Test cases for {@link org.apache.karaf.bundle.command.bundletree.Tree}
 * and {@link org.apache.karaf.bundle.command.bundletree.Node}
 */
public class TreeTest {

    @Test
    public void writeTreeWithOneChild() throws IOException {
        Tree<String> tree = new Tree<>("root");
        tree.addChild("child");

        BufferedReader reader = read(tree);

        assertEquals("root"     , reader.readLine());
        assertEquals("+- child" , reader.readLine());
    }

    @Test
    public void writeTreeWithOneChildAndNodeConverter() throws IOException {
        Tree<String> tree = new Tree<>("root");
        tree.addChild("child");

        StringWriter writer = new StringWriter();
        tree.write(new PrintWriter(writer), node -> "my " + node.getValue());

        BufferedReader reader = new BufferedReader(new StringReader(writer.getBuffer().toString()));

        assertEquals("my root"     , reader.readLine());
        assertEquals("+- my child" , reader.readLine());
    }

    @Test
    public void writeTreeWithChildAndGrandChild() throws IOException {
        Tree<String> tree = new Tree<>("root");
        Node<String> node = tree.addChild("child");
        node.addChild("grandchild");

        BufferedReader reader = read(tree);

        assertEquals("root"            , reader.readLine());
        assertEquals("+- child"        , reader.readLine());
        assertEquals("   +- grandchild", reader.readLine());
    }

    @Test
    public void writeTreeWithTwoChildrenAndOneGrandchild() throws IOException {
        Tree<String> tree = new Tree<>("root");
        Node<String> child = tree.addChild("child1");
        child.addChild("grandchild");
        tree.addChild("child2");

        BufferedReader reader = read(tree);

        
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.bundle.command.bundletree.TreeTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.bundle.command.bundletree.TreeTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code related to SSH client properties or configurations.",
  "confidence": 1
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:13.238Z
- latency: 2.611 s

```json
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1374,
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

Test class `org.apache.karaf.bundle.core.internal.MavenConfigServiceTest` (source, may be truncated):
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
package org.apache.karaf.bundle.core.internal;

import java.util.Hashtable;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class MavenConfigServiceTest {

    @Test
    public void testLocalRepoEmpty() throws Exception {
        Hashtable<String, Object> config = new Hashtable<>();
        assertEquals(null, MavenConfigService.getLocalRepoFromConfig(config));
    }

    @Test
    public void testLocalRepoExplicit() throws Exception {
        Hashtable<String, Object> config = new Hashtable<>();
        config.put("org.ops4j.pax.url.mvn.localRepository", "foo/bar");
        assertEquals("foo/bar", MavenConfigService.getLocalRepoFromConfig(config));
    }

    @Test
    public void testLocalRepoFromSettings() throws Exception {
        Hashtable<String, Object> config = new Hashtable<>();
        config.put("org.ops4j.pax.url.mvn.settings", getClass().getResource("/settings.xml").getPath());
        assertEquals("foo/bar", MavenConfigService.getLocalRepoFromConfig(config));
    }

    @Test
    public void testLocalRepoFromSettingsNs() throws Exception {
        Hashtable<String, Object> config = new Hashtable<>();
        config.put("org.ops4j.pax.url.mvn.settings", getClass().getResource("/settings2.xml").getPath());
        assertEquals("foo/bar", MavenConfigService.getLocalRepoFromConfig(config));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change.",
  "confidence": 1
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:15.790Z
- latency: 2.540 s

```json
{
  "test": "org.apache.karaf.client.ClientConfigTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1275,
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
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:18.766Z
- latency: 2.969 s

```json
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1505,
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
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:21.757Z
- latency: 2.982 s

```json
{
  "test": "org.apache.karaf.config.command.UpdateCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1546,
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
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:21.764Z
- latency: 2.546 s

```json
{
  "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
  "attempt": 0,
  "cached": true,
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

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:24.847Z
- latency: 3.076 s

```json
{
  "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1546,
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

Test class `org.apache.karaf.config.core.impl.JsonConfigInstallerTest` (source, may be truncated):
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
package org.apache.karaf.config.core.impl;

import java.io.File;
import java.util.Hashtable;

import org.apache.karaf.util.config.ConfigurationPID;
import org.junit.Test;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

import static org.easymock.EasyMock.anyObject;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.mock;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;

public class JsonConfigInstallerTest {

    public static final String[] a = {"a1", "a2", "a3"};

    public static final String[] b = {"b1", "b2", "b3"};

    public static final String[] c = {"c1", "c2", "c3"};

    @Test
    public void KARAF_7097_update_required() throws Exception {
        final String filename = "/org.example.Arrays~update_required.json";
        final String pid = ConfigurationPID.parseFilename(filename).getPid();
        final String path = getClass().getResource(filename).getPath();
        final File artifact = new File(path);

        final Hashtable<String, Object> properties = new Hashtable<>();
        properties.put("a", a);
        properties.put("b", b);
        properties.put("c", c);
        final Configuration configuration = mock(Configuration.class);
        expect(configuration.getPid()).andReturn(pid);
        expect(configuration.getProperties()).andReturn(properties);
        configuration.update(anyObject());

        final ConfigurationAdmin configurationAdmin = mock(ConfigurationAdmin.class);
        expect(configurationAdmin.listConfigurations(String.format("(felix.fileinstall.filename=%s)", artifact.toURI()))).andReturn(new Configuration[]{configuration});
        expect(configurationAdmin.getConfiguration(pid, null)).andReturn(configuration);

        replay(configuration, configurationAdmin);

        final JsonConfigInstaller installer = new JsonConfigInstaller(configurationAdmin);
        installer.install(artifact);

        verify(configuration, configurationAdmin);
    }

    @Test
    public void KARAF_7097_no_update_required() throws Exception {
        final String filename = "/org.example.Arrays~no_update_required.json";
      
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:27.846Z
- latency: 2.991 s

```json
{
  "test": "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1402,
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

Test class `org.apache.karaf.config.core.impl.KarafConfigurationPluginTest` (source, may be truncated):
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
package org.apache.karaf.config.core.impl;

import org.junit.Assert;
import org.junit.Test;
import org.osgi.framework.Constants;

import java.util.Dictionary;
import java.util.Hashtable;

public class KarafConfigurationPluginTest {

    @Test
    public void testSystemProperty() throws Exception {
        System.setProperty("org.apache.karaf.shell.sshPort", "8102");
        KarafConfigurationPlugin plugin = new KarafConfigurationPlugin();
        Dictionary<String, Object> properties = new Hashtable<>();
        properties.put(Constants.SERVICE_PID, "org.apache.karaf.shell");
        properties.put("foo", "bar");
        properties.put("sshPort", 8101);
        plugin.modifyConfiguration(null, properties);

        Assert.assertEquals(8102, properties.get("sshPort"));
        Assert.assertEquals("bar", properties.get("foo"));
    }

    @Test
    public void testAppending() throws Exception {
        System.setProperty("org.apache.karaf.features.repositories", "${repositories},third");
        KarafConfigurationPlugin plugin = new KarafConfigurationPlugin();
        Dictionary<String, Object> properties = new Hashtable<>();
        properties.put(Constants.SERVICE_PID, "org.apache.karaf.features");
        properties.put("repositories", "first,second");
        properties.put("foo", "bar");
        plugin.modifyConfiguration(null, properties);

        Assert.assertEquals("first,second,third", properties.get("repositories"));
        Assert.assertEquals("bar", properties.get("foo"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:30.990Z
- latency: 3.137 s

```json
{
  "test": "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1523,
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

Test class `org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest` (source, may be truncated):
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
package org.apache.karaf.deployer.blueprint;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Iterator;
import java.util.Set;
import java.util.jar.JarInputStream;
import java.util.zip.ZipEntry;

import javax.xml.transform.dom.DOMSource;

import junit.framework.TestCase;

public class BlueprintDeploymentListenerTest extends TestCase {
	
	private static final String BLUEPRINT_ENTRY = "OSGI-INF/blueprint/";

    public void testPackagesExtraction() throws Exception {
        BlueprintDeploymentListener l = new BlueprintDeploymentListener();
        File f = new File(getClass().getClassLoader().getResource("test.xml").toURI());
        Set<String> pkgs = BlueprintTransformer.analyze(new DOMSource(BlueprintTransformer.parse(f.toURL())));
        assertNotNull(pkgs);
        assertEquals(1, pkgs.size());
        Iterator<String> it = pkgs.iterator();
        assertEquals("org.apache.aries.blueprint.sample", it.next());
    }

    public void testCustomManifest() throws Exception {
        File f = File.createTempFile("smx", ".jar");
        try {
            OutputStream os = new FileOutputStream(f);
            BlueprintTransformer.transform(getClass().getClassLoader().getResource("test.xml"), os);
            os.close();
            InputStream is = new FileInputStream(f);
            JarInputStream jar = new JarInputStream(is);
            jar.getManifest().write(System.err);
            is.close();
        } finally {
            f.delete();
        }
    }

    // KARAF-1617
    public void testAppendDescriptorFileExtension() throws Exception {
    	final String expectedFileName = "test-fileextension";
        File f = File.createTempFile("smx", ".jar");
        try {
        	ZipEntry zipEntry = null;
            OutputStream os = new FileOutputStream(f);
			BlueprintTransformer.transform(getClass().getClassLoader().getResource(expectedFileName), os);
            os.close();
            InputStream is = new FileInputStream(f);
            JarInputStream jar = new JarInputStream(is);
            while(true) {
                zipEntry = jar.getNextEntr
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:34.470Z
- latency: 3.470 s

```json
{
  "test": "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1609,
  "completion_tokens": 73
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

Test class `org.apache.karaf.deployer.kar.KarArtifactInstallerTest` (source, may be truncated):
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
package org.apache.karaf.deployer.kar;

import static org.easymock.EasyMock.*;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.net.URI;
import java.util.Collections;
import java.util.List;

import org.apache.karaf.kar.KarService;
import org.junit.Before;
import org.junit.Test;

public class KarArtifactInstallerTest {
	private KarArtifactInstaller karArtifactInstaller;
	private KarService karService;

	private URI goodKarFile;
	private URI zipFileWithKarafManifest;
	private URI zipFileWithoutKarafManifest;
	private URI badZipFile;
	
	@Before
	public void setUp() throws Exception {
		karService = createMock(KarService.class);

		karArtifactInstaller = new KarArtifactInstaller();

		karArtifactInstaller.setKarService(karService);
		
		goodKarFile = getClass().getClassLoader().getResource("goodKarFile.kar").toURI();
		zipFileWithKarafManifest = getClass().getClassLoader().getResource("karFileAsZip.zip").toURI();
		zipFileWithoutKarafManifest = getClass().getClassLoader().getResource("karFileAsZipNoManifest.zip").toURI();
		badZipFile = getClass().getClassLoader().getResource("badZipFile.zip").toURI();
	}

	@Test
	public void shouldHandleKarFile() throws Exception {
		assertTrue(karArtifactInstaller.canHandle(new File(goodKarFile)));
	}
	
	@Test
	public void shouldHandleZipFileWithKarafManifest() throws Exception {
		assertTrue(karArtifactInstaller.canHandle(new File(zipFileWithKarafManifest)));
	}

	@Test
	public void shouldIgnoreZipFileWithoutKarafManifest() throws Exception { 		
		assertFalse(karArtifactInstaller.canHandle(new File(zipFileWithoutKarafManifest)));
	}

	@Test
	public void shouldIgnoreBadZipFile() throws Exception { 		
		assertFalse(karArtifactInstaller.canHandle(new File(badZipFile)));
	}

    /**
     * This is test for KARAF-5533. Issue comes from fact that internally KAR service process file in it's own way.
     *
     * Because of that artifact installer must follow the same logic of service it calls, as returned list of installed.
     * KAR files is not list of full file names, but files with stripped extensions.
     *
     * @throws Exception Any exception cause
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.deployer.kar.KarArtifactInstallerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, heartbeats, or timeouts, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:34.478Z
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

- time: 2026-11-07T18:00:37.141Z
- latency: 2.655 s

```json
{
  "test": "org.apache.karaf.event.command.EventDisplayCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1289,
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
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:39.859Z
- latency: 2.706 s

```json
{
  "test": "org.apache.karaf.event.command.EventPrinterTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1459,
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

Test class `org.apache.karaf.event.command.EventPrinterTest` (source, may be truncated):
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

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;

import org.apache.karaf.event.command.EventPrinter;
import org.junit.Test;
import org.osgi.service.event.Event;

public class EventPrinterTest {
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm");

    @Test
    public void testPrint() throws UnsupportedEncodingException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(baos);
        new EventPrinter(out, false).accept(event());
        String result = baos.toString("utf-8");
        assertThat(result, equalTo("<date> - myTopic\n"));
    }
    
    @Test
    public void testPrintVerbose() throws UnsupportedEncodingException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(baos);
        new EventPrinter(out, true).accept(event());
        String result = baos.toString("utf-8");
        assertThat(result, equalTo("<date> - myTopic\n" 
            + "a: b\n"
            + "c: [d, e]\n\n"));
    }

    private Event event() {
        HashMap<String, Object> props = new HashMap<>();
        props.put("a", "b");
        props.put("c", new String[]{"d", "e"});
        Date date;
        try {
            date = df.parse("<date>");
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
        props.put("timestamp",  date.getTime());
        return new Event("myTopic", props);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.command.EventPrinterTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.command.EventPrinterTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:42.688Z
- latency: 2.822 s

```json
{
  "test": "org.apache.karaf.event.command.EventSendCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1568,
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

Test class `org.apache.karaf.event.command.EventSendCommandTest` (source, may be truncated):
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

import static org.easymock.EasyMock.capture;
import static org.easymock.EasyMock.expectLastCall;
import static org.easymock.EasyMock.mock;
import static org.easymock.EasyMock.newCapture;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertThat;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.easymock.Capture;
import org.junit.Test;
import org.osgi.service.event.Event;
import org.osgi.service.event.EventAdmin;

public class EventSendCommandTest {

    @Test
    public void testExecute() throws Exception {
        EventSendCommand send = new EventSendCommand();
        send.eventAdmin = mock(EventAdmin.class);
        Capture<Event> eventCapture = newCapture();
        send.eventAdmin.sendEvent(capture(eventCapture));
        expectLastCall();

        replay(send.eventAdmin);
        send.topic = "myTopic";
        send.properties = Collections.singletonList("a=b");
        send.execute();
        verify(send.eventAdmin);
        
        Event event = eventCapture.getValue();
        assertThat(event.getTopic(), equalTo("myTopic"));
        assertThat(event.getProperty("a"), equalTo("b"));
    }
    
    @Test
    public void testParse() {
        List<String> propList = Arrays.asList("a=b","b=c");
        Map<String, String> expectedMap = new HashMap<>();
        expectedMap.put("a", "b");
        expectedMap.put("b", "c");
        Map<String, String> props = EventSendCommand.parse(propList);
        assertThat(props.size(), equalTo(2));
        assertThat(props.get("a"), equalTo("b"));
        assertThat(props.get("b"), equalTo("c"));
    }
    
    @Test
    public void testParseNull() {
        Map<String, String> props = EventSendCommand.parse(null);
        assertNotNull(props);
        assertThat(props.size(), equalTo(0));
    }
    
    @Test(expected=IllegalArgumentException.class)
    public void testParseNoKeyValue() {
        EventSendCommand.parse(Coll
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.command.EventSendCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.command.EventSendCommandTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:45.378Z
- latency: 2.679 s

```json
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1434,
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
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:48.148Z
- latency: 2.759 s

```json
{
  "test": "org.apache.karaf.event.service.EventCollectorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1515,
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

Test class `org.apache.karaf.event.service.EventCollectorTest` (source, may be truncated):
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
package org.apache.karaf.event.service;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

import java.util.HashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;
import java.util.stream.IntStream;

import org.junit.Test;
import org.osgi.service.event.Event;

public class EventCollectorTest {

    @Test
    public void testHandleEvent() throws Exception {
        EventCollector collector = new EventCollector();
        assertThat(collector.getEvents().count(), equalTo(0l));
        collector.handleEvent(event("myTopic"));
        assertThat(collector.getEvents().count(), equalTo(1l));
        assertThat(collector.getEvents().findFirst().get().getTopic(), equalTo("myTopic"));
        
    }
    
    @Test
    public void testLimit() {
        EventCollector collector = new EventCollector();
        collector.handleEvent(event("first"));
        IntStream.rangeClosed(1, 99).forEach(c -> collector.handleEvent(event("myTopic")));
        assertThat(collector.getEvents().count(), equalTo(100l));
        collector.handleEvent(event("last"));
        assertThat(collector.getEvents().count(), equalTo(100l));
        assertTrue(collector.getEvents().noneMatch(event -> event.getTopic().endsWith("first")));
        assertTrue(collector.getEvents().anyMatch(event -> event.getTopic().endsWith("last")));
    }

    @Test
    public void testAddRemoveConsumer() {
        final AtomicInteger count = new AtomicInteger();
        Consumer<Event> countingConsumer = event -> count.incrementAndGet();
        EventCollector collector = new EventCollector();
        collector.handleEvent(event("myTopic"));
        collector.addConsumer(countingConsumer);
        assertThat(count.get(), equalTo(1));

        collector.handleEvent(event("another"));
        assertThat(count.get(), equalTo(2));

        collector.removeConsumer(countingConsumer);
        collector.handleEvent(event("and/another"));
        assertThat(count.get(), equalTo(2));
    }

    private Event event(String topic) {
        return new Event(topic, new HashMap<>());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.service.EventCollectorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.service.EventCollectorTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 23. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:50.904Z
- latency: 2.748 s

```json
{
  "test": "org.apache.karaf.event.service.TopicPredicateTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1344,
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

Test class `org.apache.karaf.event.service.TopicPredicateTest` (source, may be truncated):
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
package org.apache.karaf.event.service;

import static org.apache.karaf.event.service.TopicPredicate.matchTopic;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.HashMap;
import java.util.function.Predicate;

import org.junit.Test;
import org.osgi.service.event.Event;

public class TopicPredicateTest {

    @Test
    public void testMatchAll() {
        Predicate<Event> matcher = matchTopic("*");
        assertTrue(matcher.test(event("myTopic")));
        assertTrue(matcher.test(event("my/other")));
    }
     
    @Test
    public void testMatchSpecific() {
        Predicate<Event> matcher = matchTopic("myTopic");
        assertTrue(matcher.test(event("myTopic")));
        assertFalse(matcher.test(event("myTopic/test")));
        assertFalse(matcher.test(event("my/other")));
    }
    
    @Test
    public void testMatchSubTopics() {
        Predicate<Event> matcher = matchTopic("myTopic*");
        assertTrue(matcher.test(event("myTopic")));
        assertTrue(matcher.test(event("myTopic/test")));
        assertFalse(matcher.test(event("my/other")));
    }

    private Event event(String topic) {
        return new Event(topic, new HashMap<String, String>());
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.event.service.TopicPredicateTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.event.service.TopicPredicateTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 24. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:53.994Z
- latency: 3.080 s

```json
{
  "test": "org.apache.karaf.features.AppendTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1535,
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

Test class `org.apache.karaf.features.AppendTest` (source, may be truncated):
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
package org.apache.karaf.features;

import static org.easymock.EasyMock.eq;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.expectLastCall;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Properties;

import org.apache.karaf.features.internal.service.FeatureConfigInstaller;
import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.easymock.Capture;
import org.easymock.EasyMock;
import org.easymock.IMocksControl;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

public class AppendTest {

    private IMocksControl c;
    private Feature feature;
    private ConfigurationAdmin admin;
    private FeatureConfigInstaller installer;
    
    @Before
    public void before() throws Exception {
        System.setProperty("karaf.data", "data");
        System.setProperty("karaf.etc", "target");
        RepositoryImpl r = new RepositoryImpl(getClass().getResource("internal/service/f08.xml").toURI());
        Feature[] features = r.getFeatures();
        feature = features[0];
        checkFeature(feature);
        c = EasyMock.createControl();
        admin = c.createMock(ConfigurationAdmin.class);
        installer = new FeatureConfigInstaller(admin);
    }

    @Test
    public void testNoChange() throws Exception {
        Hashtable<String, Object> original = new Hashtable<>();
        original.put("javax.servlet.context.tempdir", "bar");
        expectConfig(admin, original);

        c.replay();
        installer.installFeatureConfigs(feature);
        c.verify();
    }

    @Test
    public void testAppendWhenFileExists() throws Exception {
        testAppendInternal(true);
    }
    
    @Test
    public void testAppendWhenNoFileExists() throws Exception {
        testAppendInternal(false);
    }

    private void testAppendInternal(boolean cfgFil
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.AppendTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.AppendTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 0.9
}
```

## 25. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:56.659Z
- latency: 2.657 s

```json
{
  "test": "org.apache.karaf.features.ConditionalTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1302,
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

Test class `org.apache.karaf.features.ConditionalTest` (source, may be truncated):
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
package org.apache.karaf.features;

import static org.hamcrest.Matchers.contains;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;

import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.junit.Test;


public class ConditionalTest {

    @Test
    public void testLoad() throws Exception {
        RepositoryImpl r = new RepositoryImpl(getClass().getResource("internal/service/f06.xml").toURI());
        Feature[] features = r.getFeatures();
        assertEquals(1, features.length);
        Feature feature = features[0];

        assertEquals(2,feature.getConditional().size());

        Conditional conditional1 = feature.getConditional().get(0);
        assertThat(conditional1.getCondition(), contains("http"));
        assertEquals(1, conditional1.getBundles().size());

        Conditional conditional2 = feature.getConditional().get(1);
        assertThat(conditional2.getCondition(), contains("req:osgi.ee;filter:=\"(&(osgi.ee=JavaSE)(!(version>=1.7)))\""));
    }
    
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.ConditionalTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.ConditionalTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 26. semantic_analyzer · llm_call

- time: 2026-11-07T18:00:59.725Z
- latency: 3.057 s

```json
{
  "test": "org.apache.karaf.features.FeaturesServiceTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1557,
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

Test class `org.apache.karaf.features.FeaturesServiceTest` (source, may be truncated):
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
package org.apache.karaf.features;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.concurrent.CopyOnWriteArraySet;

import org.apache.felix.resolver.ResolverImpl;
import org.apache.karaf.features.internal.resolver.Slf4jResolverLog;
import org.apache.karaf.features.internal.service.BundleInstallSupport;
import org.apache.karaf.features.internal.service.BundleInstallSupport.FrameworkInfo;
import org.apache.karaf.features.internal.service.FeaturesServiceConfig;
import org.apache.karaf.features.internal.service.FeaturesServiceImpl;
import org.apache.karaf.features.internal.service.StateStorage;
import org.apache.karaf.features.internal.util.MultiException;
import org.easymock.EasyMock;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.osgi.service.resolver.Resolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.easymock.EasyMock.expect;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

public class FeaturesServiceTest extends TestBase {
    private static final String FEATURE_WITH_INVALID_BUNDLE = "<features name='test' xmlns='http://karaf.apache.org/xmlns/features/v1.0.0'>"
            + "  <feature name='f1'><bundle>%s</bundle><bundle>zfs:unknown</bundle></feature>"
            + "  <feature name='f2'><bundle>%s</bundle></feature>"
            + "</features>";

    File dataFile;
    Logger logger = LoggerFactory.getLogger(FeaturesServiceTest.class);
    Resolver resolver = new ResolverImpl(new Slf4jResolverLog(logger));

    @Before
    public void setUp() throws IOException {
        dataFile = File.createTempFile("features", null, null);
    }
    
    private URI createTempRepo(String repoContent, Object ... variables) throws IOException {
        File tmp = File.createTempFile("karaf", ".feature");
        PrintWriter pw = new PrintWriter(n
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.FeaturesServiceTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.FeaturesServiceTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the SSH client or related components that were modified in the code change.",
  "confidence": 0.8
}
```

## 27. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:02.620Z
- latency: 2.886 s

```json
{
  "test": "org.apache.karaf.features.RepositoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1556,
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

Test class `org.apache.karaf.features.RepositoryTest` (source, may be truncated):
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
package org.apache.karaf.features;

import java.net.URI;

import junit.framework.TestCase;
import org.apache.karaf.features.internal.resolver.FeatureResource;
import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.osgi.resource.Resource;


public class RepositoryTest extends TestCase {

    public void testLoad() throws Exception {
        RepositoryImpl r = new RepositoryImpl(getClass().getResource("repo1.xml").toURI());
        // Check repo
        URI[] repos = r.getRepositories();
        assertNotNull(repos);
        assertEquals(1, repos.length);
        assertEquals(URI.create("urn:r1"), repos[0]);
        // Check features
        Feature[] features = r.getFeatures();
        assertNotNull(features);
        assertEquals(3, features.length);
        assertNotNull(features[0]);
        assertEquals("http://karaf.apache.org/xmlns/features/v1.1.0", features[0].getNamespace());
        assertEquals("f1", features[0].getName());
        assertNotNull(features[0].getConfigurations());
        assertEquals(1, features[0].getConfigurations().size());
        assertNotNull(features[0].getConfigurations().get(0).getName());
        assertEquals("c1", features[0].getConfigurations().get(0).getName());
        assertEquals(1, features[0].getConfigurations().get(0).getProperties().size());
        assertEquals("v", features[0].getConfigurations().get(0).getProperties().get("k"));
        assertNotNull(features[0].getDependencies());
        assertEquals(0, features[0].getDependencies().size());
        assertNotNull(features[0].getBundles());
        assertEquals(2, features[0].getBundles().size());
        assertEquals("b1", features[0].getBundles().get(0).getLocation());
        assertEquals("b2", features[0].getBundles().get(1).getLocation());
        assertNotNull(features[1]);
        assertEquals("f2", features[1].getName());
        assertNotNull(features[1].getConfigurations());
        assertEquals(0, features[1].getConfigurations().size());
        assertNotNull(features[1].getDependencies());
        assertEquals(1, features[1].getDependencies().size());
        assertEquals("f1" + org.apache.karaf.features.internal.model.Feature.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.RepositoryTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.RepositoryTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 28. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:05.592Z
- latency: 2.965 s

```json
{
  "test": "org.apache.karaf.features.command.ListFeaturesCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1507,
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

Test class `org.apache.karaf.features.command.ListFeaturesCommandTest` (source, may be truncated):
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
package org.apache.karaf.features.command;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeatureState;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.Repository;
import org.easymock.EasyMock;
import org.junit.Test;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

public class ListFeaturesCommandTest {

    @Test
    public void testHiddenFeatures() throws Exception {

        FeaturesService service = EasyMock.createMock(FeaturesService.class);
        Repository repo = EasyMock.createMock(Repository.class);
        Feature feature = EasyMock.createMock(Feature.class);

        EasyMock.expect(service.listRepositories()).andReturn(new Repository[] { repo });
        EasyMock.expect(repo.getFeatures()).andReturn(new Feature[] { feature });
        EasyMock.expect(feature.isHidden()).andReturn(true);
        EasyMock.expect(feature.isBlacklisted()).andReturn(false);

        EasyMock.replay(service, repo, feature);

        ListFeaturesCommand command = new ListFeaturesCommand();
        command.setFeaturesService(service);
        command.noFormat = true;

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(baos);
        System.setOut(out);

        command.execute();

        out.flush();
        assertFalse(baos.toString().contains("feature"));
        EasyMock.verify(service, repo, feature);
    }

    @Test
    public void testShowHiddenFeatures() throws Exception {

        FeaturesService service = EasyMock.createMock(FeaturesService.class);
        Repository repo = EasyMock.createMock(Repository.class);
        Feature feature = EasyMock.createMock(Feature.class);

        EasyMock.expect(service.listRepositories()).andReturn(new Repository[] { repo });
        EasyMock.expect(repo.getFeatures()).andReturn(new Feature[] { feature });
        EasyMock.expect(feature.isHidden()).andReturn(true).anyTimes();
        EasyMock.expect(feature.isBlacklisted()).andReturn(false).anyTimes();
        EasyMock.expect(feature.getName()).and
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.command.ListFeaturesCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.command.ListFeaturesCommandTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 29. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:08.579Z
- latency: 2.980 s

```json
{
  "test": "org.apache.karaf.features.extension.BundleWiresTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1567,
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

Test class `org.apache.karaf.features.extension.BundleWiresTest` (source, may be truncated):
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
package org.apache.karaf.features.extension;

import static org.easymock.EasyMock.expect;
import static org.junit.Assert.assertEquals;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.Map.Entry;
import java.util.stream.Collectors;
import java.util.stream.LongStream;

import org.easymock.EasyMock;
import org.easymock.IMocksControl;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.Constants;
import org.osgi.framework.namespace.HostNamespace;
import org.osgi.framework.namespace.PackageNamespace;
import org.osgi.framework.wiring.BundleCapability;
import org.osgi.framework.wiring.BundleRequirement;
import org.osgi.framework.wiring.BundleRevision;
import org.osgi.framework.wiring.BundleWire;
import org.osgi.framework.wiring.BundleWiring;
import org.osgi.resource.Namespace;

public class BundleWiresTest {

    private static final Path BASE_PATH = new File("target/bundles").toPath();
    private static final String targetBundleVersion = "1.0.1";
    private static final int targetBundleId = 2;
    private static final String packageFilter = "(&(osgi.wiring.package=org.osgi.framework)(version>=1.6.0)(!(version>=2.0.0)))";
    private IMocksControl c;

    @Before
    public void init() {
        c = EasyMock.createControl();
    }

    @Test
    public void testFromBundle() throws IOException {
        BundleWire wire = packageWire(packageFilter, bundleCap(targetBundleId, targetBundleVersion, true ));
        Bundle bundle = wiredBundle(Arrays.asList(wire));
        c.replay();
        BundleWires bwires = new BundleWires(bundle);
        bwires.save(BASE_PATH);
        c.verify();
        Iterator<String> lines = Files.lines(new File("target/bundles/1").toPath()).iterator();
        Assert.assertEquals(PackageNamespace.PACKAGE_NAMESPACE + "; " + packageFilter, lines.next());
        Assert.assertEquals(targetBundleId + "; version=" + targetBundleVersion, lines.next());
        bwires.delete(BASE_PATH);
    }
    
    @Test
    public v
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.extension.BundleWiresTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.extension.BundleWiresTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 30. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:11.777Z
- latency: 3.190 s

```json
{
  "test": "org.apache.karaf.features.extension.StoredWiringResolverTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1574,
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

Test class `org.apache.karaf.features.extension.StoredWiringResolverTest` (source, may be truncated):
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
package org.apache.karaf.features.extension;

import org.easymock.EasyMock;
import org.easymock.IMocksControl;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.Constants;
import org.osgi.framework.namespace.IdentityNamespace;
import org.osgi.framework.namespace.PackageNamespace;
import org.osgi.framework.wiring.*;
import org.osgi.resource.Capability;
import org.osgi.resource.Namespace;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.easymock.EasyMock.expect;
import static org.junit.Assert.assertEquals;

public class StoredWiringResolverTest {
    private static final String TEST_RESOURCES_WIRINGS = "target/test-classes/wirings/";

    private static final int EXPECTED_STOCK_WIRINGS = 3;
    private static final String PACKAGE_FILTER = "(&(osgi.wiring.package=org.osgi.framework)(version>=1.6.0)(!(version>=2.0.0)))";

    private IMocksControl c;

    private StoredWiringResolver wiringResolver;

    @Before
    public void init() {
        c = EasyMock.createControl();

        wiringResolver = new StoredWiringResolver(new File(TEST_RESOURCES_WIRINGS).toPath());
        wiringResolver.load();
    }

    @After
    public void cleanup() {
        new File(TEST_RESOURCES_WIRINGS + "25").delete();
    }

    @Test
    public void load() {
        Assert.assertEquals(EXPECTED_STOCK_WIRINGS, wiringResolver.wiring.size());

        Assert.assertTrue(wiringResolver.wiring.containsKey(1L));
        Assert.assertTrue(wiringResolver.wiring.containsKey(5L));
        Assert.assertTrue(wiringResolver.wiring.containsKey(9L));
    }

    @Test
    public void filterMatches() {
        List<BundleCapability> candidates = new ArrayList<>();

        long sourceBundleId = 1L;
        long targetBundleId = 2L;
        String targetBundleVersion = "1.0.1";

        BundleCapability candidate1 = mockBundleCapability(targetBundleId, targetBundleVersion);
        candidates.add(candidate1);

        BundleCapability candidate2 = mockBundleCapability(targetB
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.extension.StoredWiringResolverTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.extension.StoredWiringResolverTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 31. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:14.419Z
- latency: 2.634 s

```json
{
  "test": "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1278,
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

Test class `org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.download.impl;

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import static junit.framework.TestCase.assertEquals;

public class DownloadManagerHelperTest {

  @Test
  public void testSetExtraProtocols(){
    assertEquals("^(jar|war|war-i|warref|webbundle|wrap|spring|blueprint):.*$", DownloadManagerHelper.getIgnoredProtocolPattern().toString());

    List<String> extraProtocols = new ArrayList<>();
    extraProtocols.add( "extra1" );
    extraProtocols.add( "extra2" );
    DownloadManagerHelper.setExtraProtocols( extraProtocols );

    assertEquals("^(jar|war|war-i|warref|webbundle|wrap|spring|blueprint|extra1|extra2):.*$", DownloadManagerHelper.getIgnoredProtocolPattern().toString());
  }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code in the provided diff.",
  "confidence": 1
}
```

## 32. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:17.059Z
- latency: 2.629 s

```json
{
  "test": "org.apache.karaf.features.internal.model.ConfigTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1296,
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

Test class `org.apache.karaf.features.internal.model.ConfigTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.model;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ConfigTest {

    @Test
    public void testTrim() {
        Config config = new Config();
        config.setName("my.config");
        config.setValue("    # my comment\n" +
                        "    my.key = my.value\n");

        assertEquals("my.value", config.getProperties().getProperty("my.key"));
    }

    @Test
    public void testInterpolation() {
        Config config = new Config();
        config.setName("my.config");
        config.setValue("    # my comment\n" +
                        "    my.nb = 2\n" +
                        "    my.key.1 = my.value.1\n" +
                        "    my.key.2 = my.value.2\n" +
                        "    my.key.3 = ab${my.key.${my.nb}}");

        assertEquals("abmy.value.2", config.getProperties().getProperty("my.key.3"));
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.model.ConfigTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.model.ConfigTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 33. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:20.015Z
- latency: 2.949 s

```json
{
  "test": "org.apache.karaf.features.internal.model.JsonTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1592,
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

Test class `org.apache.karaf.features.internal.model.JsonTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.model;

import org.junit.Assert;
import org.junit.Test;

public class JsonTest {

    @Test
    public void testUnmarshall() throws Exception {
        Assert.assertTrue(JacksonUtil.isJson(this.getClass().getResourceAsStream("/org/apache/karaf/features/repo.json")));

        Features features = JacksonUtil.unmarshal(this.getClass().getResourceAsStream("/org/apache/karaf/features/repo.json"));

        Assert.assertEquals("test", features.getName());

        Assert.assertEquals("mvn:org.apache.karaf/test/1.0-SNAPSHOT", features.getRepository().get(0));

        Assert.assertEquals("test-feature", features.getFeature().get(0).getName());
        Assert.assertEquals("1.0.0.SNAPSHOT", features.getFeature().get(0).getVersion());
        Assert.assertEquals("This is test feature", features.getFeature().get(0).getDescription());
        Assert.assertEquals("obr", features.getFeature().get(0).getResolver());
        Assert.assertEquals("auto", features.getFeature().get(0).getInstall());
        Assert.assertEquals(30, features.getFeature().get(0).getStartLevel());
        Assert.assertEquals(false, features.getFeature().get(0).isHidden());

        Assert.assertEquals("inner-feature", features.getFeature().get(0).getFeature().get(0).getName());
        Assert.assertEquals("[1,2)", features.getFeature().get(0).getFeature().get(0).getVersion());

        Assert.assertEquals("mvn:org.apache.karaf/test-bundle/1.0-SNAPSHOT", features.getFeature().get(0).getBundle().get(0).getLocation());
        Assert.assertEquals(40, features.getFeature().get(0).getBundle().get(0).getStartLevel());
        Assert.assertEquals(true, features.getFeature().get(0).getBundle().get(0).isDependency());
        Assert.assertEquals(true, features.getFeature().get(0).getBundle().get(0).isStart());

        Assert.assertEquals("test-config", features.getFeature().get(0).getConfig().get(0).getName());
        Assert.assertEquals(false, features.getFeature().get(0).getConfig().get(0).isAppend());
        Assert.assertEquals(false, features.getFeature().get(0).getConfig().get(0).isExternal());
        Assert.assertEquals(false, features.getFeature().get(0)
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.model.JsonTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.model.JsonTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 34. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:22.967Z
- latency: 2.939 s

```json
{
  "test": "org.apache.karaf.features.internal.osgi.ActivatorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1548,
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

Test class `org.apache.karaf.features.internal.osgi.ActivatorTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.osgi;

import static org.easymock.EasyMock.anyString;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.niceMock;
import static org.easymock.EasyMock.replay;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;

import java.util.Dictionary;
import java.util.Hashtable;

import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

public class ActivatorTest {

  private Activator activator;
  private ConfigurationAdmin configurationAdmin;
  private BundleContext bundleContext;

  @Before
  public void setup() throws Exception {
    activator = new TestActivator();

    configurationAdmin = niceMock(ConfigurationAdmin.class);
    Configuration featuresConfig = niceMock(Configuration.class);
    Dictionary<String, Object> properties = buildTestProperties();
    expect(featuresConfig.getProperties()).andReturn(properties);
    expect(configurationAdmin.getConfiguration(Activator.FEATURES_SERVICE_CONFIG)).andReturn(featuresConfig);

    bundleContext = niceMock(BundleContext.class);
    Bundle bundle = niceMock(Bundle.class);
    expect(bundle.getResource(anyString())).andReturn(null);
    expect(bundleContext.getBundle()).andReturn(bundle);

    replay(bundleContext, bundle, configurationAdmin, featuresConfig);
  }

  private Dictionary<String, Object> buildTestProperties() {
    Dictionary<String, Object> properties = new Hashtable<>();
    properties.put("key1", "value1");
    properties.put("key2", "value2");

    return properties;
  }

  @Test
  public void testStart() throws Exception {
    activator.start(bundleContext);

    Dictionary<String, ?> configuration = ((TestActivator) activator).getConfiguration();
    assertThat(configuration.get("key1"), is("value1"));
    assertThat(configuration.get("key2"), is("value2"));
  }

  /**
   * Overwrite #getTrackedService which could otherwise not be mocked.
   * Overwrite #doStart to avoid full start up of the Activator.
   * Overwrite #getConfiguratio
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.osgi.ActivatorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.osgi.ActivatorTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 35. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:26.287Z
- latency: 3.309 s

```json
{
  "test": "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1618,
  "completion_tokens": 70
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

Test class `org.apache.karaf.features.internal.region.FeaturesDependenciesTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.region;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.felix.resolver.ResolverImpl;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.internal.resolver.Slf4jResolverLog;
import org.apache.karaf.features.internal.service.Deployer;
import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.apache.karaf.features.internal.support.TestDownloadManager;
import org.junit.Test;
import org.osgi.framework.namespace.IdentityNamespace;
import org.osgi.resource.Capability;
import org.osgi.resource.Resource;
import org.osgi.resource.Wire;
import org.osgi.service.resolver.Resolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.apache.karaf.features.internal.util.MapUtils.addToMapSet;
import static org.junit.Assert.assertEquals;

public class FeaturesDependenciesTest {

    Logger logger = LoggerFactory.getLogger(FeaturesDependenciesTest.class);
    Resolver resolver = new ResolverImpl(new Slf4jResolverLog(logger));

    @Test
    public void testFeatureDependency1() throws Exception {
        doTestFeatureDependency(
                new String[] { "f1" },
                new String[] { "a1/1.0.0", "b/2.0.0" }
        );
    }

    @Test
    public void testFeatureDependency1b() throws Exception {
        doTestFeatureDependency(
                new String[] { "f1", "dep/[1.0,2.0)"},
                new String[] { "a1/1.0.0", "b/1.0.0" }
        );
    }

    @Test
    public void testFeatureDependency2() throws Exception {
        doTestFeatureDependency(
                new String[] { "f2" },
                new String[] { "a1/1.0.0", "b/2.0.0" }
        );
    }

    @Test
    public void testFeatureDependency2b() throws Exception {
        doTestFeatureDependency(
                new String[] { "f2", "dep/[1.0,2.0)"},
                new String[] { "a1/1.0.0", "b/1.0.0" }
        );
    }

    @Test
    public void testFeatureDependen
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.region.FeaturesDependenciesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, heartbeats, or timeouts, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 36. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:29.359Z
- latency: 3.062 s

```json
{
  "test": "org.apache.karaf.features.internal.region.SubsystemTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1557,
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

Test class `org.apache.karaf.features.internal.region.SubsystemTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.region;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.felix.resolver.ResolverImpl;
import org.apache.karaf.features.BundleInfo;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.internal.model.Bundle;
import org.apache.karaf.features.internal.resolver.Slf4jResolverLog;
import org.apache.karaf.features.internal.service.Deployer;
import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.apache.karaf.features.internal.support.TestDownloadManager;
import org.junit.Test;
import org.osgi.framework.namespace.IdentityNamespace;
import org.osgi.resource.Capability;
import org.osgi.resource.Resource;
import org.osgi.resource.Wire;
import org.osgi.service.resolver.Resolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.apache.karaf.features.internal.util.MapUtils.addToMapSet;
import static org.junit.Assert.assertEquals;

public class SubsystemTest {

    Logger logger = LoggerFactory.getLogger(SubsystemTest.class);
    Resolver resolver = new ResolverImpl(new Slf4jResolverLog(logger));

    @Test
    public void test1() throws Exception {
        RepositoryImpl repo = new RepositoryImpl(getClass().getResource("data1/features.xml").toURI());

        Map<String, Set<String>> features = new HashMap<>();
        addToMapSet(features, "root", "f1");
        addToMapSet(features, "root/apps1", "f2");

        Map<String, Set<String>> expected = new HashMap<>();
        addToMapSet(expected, "root", "a/1.0.0");
        addToMapSet(expected, "root", "c/1.0.0");
        addToMapSet(expected, "root/apps1", "b/1.0.0");

        SubsystemResolver resolver = new SubsystemResolver(this.resolver, new TestDownloadManager(getClass(), "data1"));
        resolver.prepare(partitionByName(repo.getFeatures()),
                         features,
                         Collections.emptyMap());
        resolver.resolve(FeaturesService.DEFAULT_FEATURE_R
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.region.SubsystemTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.region.SubsystemTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 37. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:32.304Z
- latency: 2.936 s

```json
{
  "test": "org.apache.karaf.features.internal.repository.RepositoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1535,
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

Test class `org.apache.karaf.features.internal.repository.RepositoryTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.repository;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.util.zip.GZIPOutputStream;

import org.apache.felix.utils.repository.BaseRepository;
import org.apache.karaf.util.StreamUtils;
import org.junit.Test;
import org.osgi.resource.Resource;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.osgi.framework.namespace.BundleNamespace.BUNDLE_NAMESPACE;
import static org.osgi.framework.namespace.IdentityNamespace.IDENTITY_NAMESPACE;
import static org.osgi.framework.namespace.PackageNamespace.PACKAGE_NAMESPACE;

public class RepositoryTest {

    @Test
    public void testXml() throws Exception {
        URL url = getClass().getResource("repo.xml");
        XmlRepository repo = new XmlRepository(url.toExternalForm(), 0, false);
        verify(repo);
    }

    @Test
    public void testJson() throws Exception {
        URL url = getClass().getResource("repo.json");
        JsonRepository repo = new JsonRepository(url.toExternalForm(), 0, false);
        verify(repo);
    }

    @Test
    public void testXmlGzip() throws Exception {
        URL url = getClass().getResource("repo.xml");
        url = gzip(url);
        XmlRepository repo = new XmlRepository(url.toExternalForm(), 0, false);
        verify(repo);
    }

    @Test
    public void testJsonGzip() throws Exception {
        URL url = getClass().getResource("repo.json");
        url = gzip(url);
        JsonRepository repo = new JsonRepository(url.toExternalForm(), 0, false);
        verify(repo);
    }

    private void verify(BaseRepository repo) {
        assertNotNull(repo.getResources());
        assertEquals(1, repo.getResources().size());
        Resource resource = repo.getResources().get(0);
        assertNotNull(resource);
        assertEquals(1, resource.getCapabilities(IDENTITY_NAMESPACE).size());
        assertEquals(1, resource.getCapabilities(BUNDLE_NAMESPACE).size());
        assertEquals(1, resource.getCapabilities(PACKAGE_NAMESPACE).size());
        assertEq
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.repository.RepositoryTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.repository.RepositoryTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 38. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:35.298Z
- latency: 2.983 s

```json
{
  "test": "org.apache.karaf.features.internal.service.BlacklistTest",
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

Test class `org.apache.karaf.features.internal.service.BlacklistTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashSet;
import java.util.stream.Stream;

import org.apache.karaf.features.BundleInfo;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeaturesService;
import org.junit.Test;

import static org.junit.Assert.assertTrue;

public class BlacklistTest {

    @Test
    public void testBlacklistFeatureWithRange() throws IOException {
        Stream<Feature> features = blacklistWith("spring;range=\"[2,3)\"");
        assertTrue(features.noneMatch(f -> f.getId().equals("spring/2.5.6.SEC02") && !f.isBlacklisted()));
    }

    @Test
    public void testBlacklistFeatureWithVersion() throws IOException {
        Stream<Feature> features = blacklistWith("spring;range=2.5.6.SEC02");
        assertTrue(features.noneMatch(f -> f.getId().equals("spring/2.5.6.SEC02") && !f.isBlacklisted()));
    }

    @Test
    public void testBlacklistFeatureWithoutVersion() throws IOException {
        Stream<Feature> features = blacklistWith("spring");
        assertTrue(features.noneMatch(f -> f.getId().startsWith("spring/") && !f.isBlacklisted()));
    }

    @Test
    public void testBlacklistBundle() throws IOException {
        String blacklisted = "mvn:org.apache.servicemix.bundles/org.apache.servicemix.bundles.jasypt/1.7_1";
        Stream<Feature> features = blacklistWith(blacklisted);
        Stream<BundleInfo> bundles = features.flatMap(f -> f.getBundles().stream());
        assertTrue(bundles.noneMatch(b -> b.getLocation().equals(blacklisted) && !b.isBlacklisted()));
    }

    @Test
    public void testBlacklistLoad() throws URISyntaxException {
        Blacklist blacklist = new Blacklist(getClass().getResource("blacklist.txt").toExternalForm());
        RepositoryImpl repo = new RepositoryImpl(getClass().getResource("f02.xml").toURI(), true);
        Stream<Feature> features = Arrays.stream(repo.getFeatures());
        FeaturesProcessorImpl processor = new FeaturesProcessorImpl(n
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.BlacklistTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.BlacklistTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 39. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:38.790Z
- latency: 3.483 s

```json
{
  "test": "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1603,
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

Test class `org.apache.karaf.features.internal.service.BootFeaturesInstallerTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.karaf.features.FeaturesService.Option;
import org.apache.karaf.features.TestBase;
import org.easymock.Capture;
import org.junit.Assert;
import org.junit.Test;

import static java.util.Arrays.asList;
import static org.easymock.EasyMock.capture;
import static org.easymock.EasyMock.createMock;
import static org.easymock.EasyMock.createStrictMock;
import static org.easymock.EasyMock.eq;
import static org.easymock.EasyMock.expectLastCall;
import static org.easymock.EasyMock.newCapture;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;

public class BootFeaturesInstallerTest extends TestBase {

    private static final String INEXISTANT_REPO = "mvn:inexistent/features/1.0/xml/features";

    @Test
    public void testParser() {
        BootFeaturesInstaller installer = new BootFeaturesInstaller(null, null, new String[0], "", false);
        Assert.assertEquals(asList(setOf("test1", "test2"), setOf("test3")), installer.parseBootFeatures(" ( test1 , test2 ) , test3 "));
        Assert.assertEquals(Collections.singletonList(setOf("test1", "test2", "test3")), installer.parseBootFeatures(" test1 , test2, test3"));
        Assert.assertEquals(asList(setOf("test1"), setOf("test2"), setOf("test3")), installer.parseBootFeatures("(test1), (test2), test3"));
    }
    
    @Test
    public void testDefaultBootFeatures() throws Exception  {
        FeaturesServiceImpl impl = createMock(FeaturesServiceImpl.class);

        Capture<Set<String>> featuresCapture = newCapture();
        impl.installFeatures(capture(featuresCapture), eq(EnumSet.of(Option.NoFailOnFeatureNotFound)));
        expectLastCall();

        impl.bootDone();
        expectLastCall();

        replay(impl);
        BootFeaturesInstaller bootFeatures = new BootFeaturesInstaller(null, impl, new String[0], "config,standard,region", false);
        bootFeatures.installB
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, heartbeats, or timeouts, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 40. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:41.920Z
- latency: 3.122 s

```json
{
  "test": "org.apache.karaf.features.internal.service.DeployerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1562,
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

Test class `org.apache.karaf.features.internal.service.DeployerTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.jar.Manifest;

import org.apache.felix.resolver.ResolverImpl;
import org.apache.felix.utils.version.VersionRange;
import org.apache.karaf.features.BundleInfo;
import org.apache.karaf.features.DeploymentEvent;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeatureEvent;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.internal.resolver.Slf4jResolverLog;
import org.apache.karaf.features.internal.support.TestBundle;
import org.apache.karaf.features.internal.support.TestDownloadManager;
import org.easymock.EasyMock;
import org.easymock.IAnswer;
import org.easymock.IArgumentMatcher;
import org.easymock.IMocksControl;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleException;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.resource.Resource;
import org.osgi.resource.Wire;
import org.osgi.service.resolver.Resolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.apache.karaf.features.FeaturesService.*;
import static org.apache.karaf.features.internal.util.MapUtils.addToMapSet;
import static org.easymock.EasyMock.anyInt;
import static org.junit.Assert.fail;

public class DeployerTest {

    private static final Logger LOGGER = LoggerFactory.getLogger(DeployerTest.class);
    private Resolver resolver = new ResolverImpl(new Slf4jResolverLog(LOGGER));

    @Test
    public void testInstallSimpleFeature() throws Exception {
        IMocksControl c = EasyMock.createControl();
        String dataDir = "data1";

        TestDownloadManager manager = new TestDownloadManager(getClass(), dataDir);

        RepositoryImpl repo = new RepositoryImpl(getClass().getResource(dataDir + "/features.xml").toURI());
        Feature f100 = repo.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.DeployerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.DeployerTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 41. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:44.918Z
- latency: 2.990 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1548,
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

Test class `org.apache.karaf.features.internal.service.FeaturesProcessorTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.FileWriter;
import java.net.URI;
import java.util.Properties;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;

import org.apache.felix.utils.manifest.Clause;
import org.apache.felix.utils.version.VersionRange;
import org.apache.karaf.features.BundleInfo;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.internal.model.Bundle;
import org.apache.karaf.features.internal.model.processing.BundleReplacements;
import org.apache.karaf.features.internal.model.processing.FeatureReplacements;
import org.apache.karaf.features.internal.model.processing.FeaturesProcessing;
import org.apache.karaf.features.internal.model.processing.ObjectFactory;
import org.apache.karaf.features.internal.model.processing.OverrideBundleDependency;
import org.apache.karaf.util.maven.Parser;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.nullValue;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

public class FeaturesProcessorTest {

    public static Logger LOG = LoggerFactory.getLogger(FeaturesProcessorTest.class);

    @Test
    public void jaxbModelForProcessor() throws Exception {
        JAXBContext jaxb = JAXBContext.newInstance(ObjectFactory.class);
        FeaturesProcessing fp = (FeaturesProcessing) jaxb.createUnmarshaller().unmarshal(getClass().getResourceAsStream("/org/apache/karaf/features/internal/service/org.apache.karaf.features.xml"));
        assertThat(fp.getFeatureReplacements().getReplacements().get(0).getFeature().getName(), equalTo("pax-jsf-resources-support"));

        Marshaller marshaller = jaxb.createMarshaller();
        marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, Boolean.TRUE);
        marshaller.marshal(fp, System.out);
    }

    @Test
    public void versionRanges() {
        LOG.info(new VersionRange("1", false).toString());
        LOG.info(new VersionRange("[2,3)", true).toString());
    }

    @Test
    public void mavenURIs()
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.FeaturesProcessorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 42. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:47.956Z
- latency: 3.030 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1544,
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

Test class `org.apache.karaf.features.internal.service.FeaturesServiceImplTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Field;
import java.net.*;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;

import org.apache.felix.resolver.ResolverImpl;
import org.apache.karaf.features.Feature;
import org.apache.karaf.features.FeatureState;
import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.TestBase;
import org.apache.karaf.features.FeaturesService.Option;
import org.apache.karaf.features.internal.download.DownloadManager;
import org.apache.karaf.features.internal.resolver.Slf4jResolverLog;
import org.apache.karaf.features.internal.service.BundleInstallSupport.FrameworkInfo;
import org.apache.karaf.features.internal.support.TestDownloadManager;
import org.easymock.Capture;
import org.easymock.EasyMock;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.Version;
import org.osgi.framework.startlevel.BundleStartLevel;
import org.osgi.framework.wiring.BundleRevision;
import org.osgi.service.resolver.Resolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.easymock.EasyMock.anyObject;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.expectLastCall;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;

/**
 * Test cases for {@link org.apache.karaf.features.internal.service.FeaturesServiceImpl}
 */
public class FeaturesServiceImplTest extends TestBase {

    Logger logger = LoggerFactory.getLogger(FeaturesServiceImplTest.class);
    Resolver resolver = new ResolverImpl(new Slf4jResolverLog(logger));
    File dataFile;

    @Before
    public void setUp() throws IOException {
        dataFile = File.createTempFile("features", null, null);
        URL.setURLStreamHandlerFactory(protocol -> protocol.e
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.FeaturesServiceImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 43. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:50.961Z
- latency: 2.997 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeaturesValidationTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1561,
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

Test class `org.apache.karaf.features.internal.service.FeaturesValidationTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.net.URI;

import org.apache.karaf.features.Feature;
import org.apache.karaf.features.Library;
import org.apache.karaf.features.Repository;
import org.junit.Test;

public class FeaturesValidationTest {

    @Test
    public void testNs10() throws Exception {
        Repository features = unmarshalAndValidate("f02.xml");
        assertNotNull(features);
    }

    @Test
    public void testNs10NoName() throws Exception {
        Repository features = unmarshalAndValidate("f03.xml");
        assertNotNull(features);
    }

    @Test
    public void testNs11() throws Exception {
        Repository features = unmarshalAndValidate("f04.xml");;
        assertNotNull(features);
    }

    @Test
    public void testNs11NoName() throws Exception {
        try {
            unmarshalAndValidate("f05.xml");
            fail("Validation should have failed");
        } catch (Exception e) {
            // ok
        }
    }

    @Test
    public void testNs12Unmarshall() throws Exception {
        Repository features = unmarshalAndValidate("f06.xml");
        assertNotNull(features);
    }

    @Test
    public void testNs13() throws Exception {
        Repository features = unmarshalAndValidate("f07.xml");
        assertNotNull(features);
        Feature f0 = features.getFeatures()[0];
        Feature f1 = features.getFeatures()[1];
        assertEquals("2.5.6.SEC02", f0.getVersion());
        assertTrue(f1.isHidden());
        assertNotNull(f1.getLibraries());
        assertEquals(1, f0.getLibraries().size());
        Library lib = f0.getLibraries().get(0);
        assertEquals("my-library", lib.getLocation());
        assertEquals(Library.TYPE_ENDORSED, lib.getType());
        assertFalse(lib.isExport());
        assertTrue(lib.isDelegate());
    }

    private Repository unmarshalAndValidate(String path) throws Exception {
        URI uri = getClass().getResource(path).toURI();
        return 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.FeaturesValidationTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.FeaturesValidationTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 44. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:54.053Z
- latency: 3.073 s

```json
{
  "test": "org.apache.karaf.features.internal.service.LocationPatternTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1649,
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

Test class `org.apache.karaf.features.internal.service.LocationPatternTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.net.MalformedURLException;

import org.apache.karaf.features.LocationPattern;
import org.junit.Test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class LocationPatternTest {

    @Test
    public void matchingNonMavenUris() throws MalformedURLException {
        assertTrue(new LocationPattern("file:1").matches("file:1"));
        assertFalse(new LocationPattern("file:1").matches("file:2"));
        assertFalse(new LocationPattern("file:*").matches(null));
        assertTrue(new LocationPattern("http://*").matches("http://a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q.txt"));
        assertTrue(new LocationPattern("file:/tmp/x*.txt").matches("file:/tmp/x1.txt"));
        assertTrue(new LocationPattern("file:/tmp/x$2*.txt").matches("file:/tmp/x$24.txt"));
        assertTrue(new LocationPattern("file:/tmp/x^2*.txt").matches("file:/tmp/x^24.txt"));
    }

    @Test
    public void correctMvnLocationPatterns() {
        boolean exception = false;
        for (String p : new String[] {
                "mvn:groupId/artifactId",
                "mvn:groupId/artifactId/1",
                "mvn:groupId/artifactId/1/t",
                "mvn:groupId/artifactId/1/t/c",
                "mvn:groupId/*",
                "mvn:*/*",
                "mvn:*/*/[0,*)/*/*",
                "mvn:g/a/[1,2)",
                "mvn:g/a/[1,*)",
                "mvn:groupId/artifactId/[1.0.0,1.0.0.0)",
                "mvn:groupId/artifactId/[1.0,1.0.0.0)",
                "mvn:groupId/artifactId/[1,1.0.0.0)",
        }) {
            try {
                new LocationPattern(p);
            } catch (IllegalArgumentException ignored) {
                exception |= true;
            }
        }
        assertFalse("We should not fail for correct mvn: URIs", exception);
    }

    @Test
    public void incorrectMvnLocationPatterns() {
        boolean exception = true;
        for (String p : new String[] {
                "mvn:onlyGroupId",
//                "mvn:groupId/artifactId/wrongVersion",
                "mvn:groupId/artifactId/[1.2,2",
                "mvn:groupId/artifactId/
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.LocationPatternTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.LocationPatternTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 45. semantic_analyzer · llm_call

- time: 2026-11-07T18:01:57.030Z
- latency: 2.967 s

```json
{
  "test": "org.apache.karaf.features.internal.service.OverridesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1653,
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

Test class `org.apache.karaf.features.internal.service.OverridesTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import org.apache.felix.utils.manifest.Clause;
import org.apache.felix.utils.manifest.Parser;
import org.apache.felix.utils.resource.ResourceBuilder;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.BundleException;
import org.osgi.resource.Resource;

import static org.apache.karaf.features.internal.resolver.ResourceUtils.getUri;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class OverridesTest {

    private String bsn = "bsn";
    private Resource b100;
    private Resource b101;
    private Resource b102;
    private Resource b110;
    private Resource c100;
    private Resource c101;
    private Resource c110;

    @Before
    public void setUp() throws BundleException {
        b100 = resource("karaf-100.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.0.0")
                .build();

        b101 = resource("karaf-101.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.0.1")
                .build();

        b102 = resource("karaf-102.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.0.2")
                .build();

        b110 = resource("karaf-110.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.1.0")
                .build();

        c100 = resource("karafc-100.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.0.0")
                .set("Bundle-Vendor", "Apache")
                .build();

        c101 = resource("karafc-101.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.0.1")
                .set("Bundle-Vendor", "NotApache")
                .build();

        c110 = resource("karafc-110.jar")
                .set("Bundle-SymbolicName", bsn)
                .set("Bundle-Version", "1.1.0"
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.OverridesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.OverridesTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH client configuration or properties.",
  "confidence": 1
}
```

## 46. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:00.002Z
- latency: 2.963 s

```json
{
  "test": "org.apache.karaf.features.internal.service.StateStorageTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1456,
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

Test class `org.apache.karaf.features.internal.service.StateStorageTest` (source, may be truncated):
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
package org.apache.karaf.features.internal.service;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class StateStorageTest {

    @Test
    public void testStoreLoad() throws Exception {

        State oldState = new State();
        oldState.bootDone.set(true);
        oldState.bundleChecksums.put(4l, 32794l);
        oldState.requirements.put("bar", Collections.singleton("f1"));
        oldState.managedBundles.put("reg", Collections.singleton(32l));
        oldState.managedBundles.put("reg2", new HashSet<>(Arrays.asList(24l, 43l)));
        oldState.repositories.add("repo");

        TestStorage storage = new TestStorage();

        storage.save(oldState);

        System.out.println(storage.baos.toString());

        State newState = new State();
        storage.load(newState);

        assertEquals(oldState.bootDone.get(), newState.bootDone.get());
        assertEquals(oldState.bundleChecksums, newState.bundleChecksums);
        assertEquals(oldState.requirements, newState.requirements);
        assertEquals(oldState.managedBundles, newState.managedBundles);
        assertEquals(oldState.repositories, newState.repositories);
    }

    static class TestStorage extends StateStorage {
        ByteArrayOutputStream baos;

        @Override
        protected InputStream getInputStream() throws IOException {
            if (baos != null) {
                return new ByteArrayInputStream(baos.toByteArray());
            }
            return null;
        }

        @Override
        protected OutputStream getOutputStream() throws IOException {
            baos = new ByteArrayOutputStream();
            return baos;
        }
    }


}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.StateStorageTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.StateStorageTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 47. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:02.965Z
- latency: 2.955 s

```json
{
  "test": "org.apache.karaf.features.management.codec.JmxFeatureTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1530,
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

Test class `org.apache.karaf.features.management.codec.JmxFeatureTest` (source, may be truncated):
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
package org.apache.karaf.features.management.codec;

import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_BLACKLISTED;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_BUNDLES;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_CONFIGURATIONFILES;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_CONFIGURATIONS;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_CONFIG_PID;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_DEPENDENCIES;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_INSTALLED;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_NAME;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_REQUIRED;
import static org.apache.karaf.features.management.FeaturesServiceMBean.FEATURE_VERSION;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;

import org.apache.karaf.features.internal.model.Bundle;
import org.apache.karaf.features.internal.model.Config;
import org.apache.karaf.features.internal.model.ConfigFile;
import org.apache.karaf.features.internal.model.Dependency;
import org.apache.karaf.features.internal.model.Feature;
import org.junit.Test;

public class JmxFeatureTest {

    @Test
    public void testJmxFeatureCompositeData() throws Exception {
        Feature feature = new Feature();
        feature.setName("test-feature");
        feature.setVersion("1.0.0");
        feature.setBlacklisted(true);

        Dependency dependency = new Dependency();
        dependency.setName("test-dependent-feature");
        dependency.setVersion("1.0.0");
        feature.getFeature().add(dependency);

        Bundle bundle = new Bundle();
        bundle.setLocation("mvn:org.test/test/1.0.0");
        feature.getBundle().add(bundle);

        Config config = new Config();
        config.setName(FEATURE_CONFIG_PID);
       
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.management.codec.JmxFeatureTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.management.codec.JmxFeatureTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to the changes made in Main.java and Activator.java.",
  "confidence": 1
}
```

## 48. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:06.024Z
- latency: 3.051 s

```json
{
  "test": "org.apache.karaf.features.management.codec.JmxRepositoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1560,
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

Test class `org.apache.karaf.features.management.codec.JmxRepositoryTest` (source, may be truncated):
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
package org.apache.karaf.features.management.codec;

import static org.apache.karaf.features.management.FeaturesServiceMBean.REPOSITORY_BLACKLISTED;
import static org.apache.karaf.features.management.FeaturesServiceMBean.REPOSITORY_FEATURES;
import static org.apache.karaf.features.management.FeaturesServiceMBean.REPOSITORY_NAME;
import static org.apache.karaf.features.management.FeaturesServiceMBean.REPOSITORY_REPOSITORIES;
import static org.apache.karaf.features.management.FeaturesServiceMBean.REPOSITORY_URI;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.net.URI;

import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;

import org.apache.karaf.features.Repository;
import org.apache.karaf.features.internal.model.Feature;
import org.apache.karaf.features.internal.model.Features;
import org.apache.karaf.features.internal.service.RepositoryImpl;
import org.junit.Test;

public class JmxRepositoryTest {

    @Test
    public void testJmxRepositoryCompositeData() throws Exception {
        Features features = new Features();
        features.setName("test-1.0.0");
        features.getRepository().add("mvn:org.test/test-dependency/1.0.0/xml/features");
        features.getFeature().add(new Feature("test-feature", "1.0.0"));

        URI uri = new URI("mvn:org.test/test/1.0.0/xml/features");
        Repository repository = new RepositoryImpl(uri, features, true);

        JmxRepository jmxRepository = new JmxRepository(repository);
        CompositeData compositeData = jmxRepository.asCompositeData();

        assertEquals("test-1.0.0", compositeData.get(REPOSITORY_NAME));
        assertEquals(uri.toString(), compositeData.get(REPOSITORY_URI));
        assertTrue((Boolean) compositeData.get(REPOSITORY_BLACKLISTED));

        String[] repositoryUris = (String[]) compositeData.get(REPOSITORY_REPOSITORIES);
        assertEquals(1, repositoryUris.length);
        assertEquals("mvn:org.test/test-dependency/1.0.0/xml/features", repositoryUris[0]);

        TabularData repositoryFeatures = (TabularData) compositeData.get(REPOSITORY_FEA
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.management.codec.JmxRepositoryTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.management.codec.JmxRepositoryTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 49. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:08.620Z
- latency: 2.588 s

```json
{
  "test": "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1252,
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

Test class `org.apache.karaf.http.core.internal.HttpMBeanImplTest` (source, may be truncated):
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
package org.apache.karaf.http.core.internal;

import java.lang.management.ManagementFactory;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.openmbean.TabularData;

import org.junit.Test;

public class HttpMBeanImplTest {

    @Test
    public void testRegisterMBean() throws Exception {
        HttpMBeanImpl httpMBean = new HttpMBeanImpl(new ServletServiceImpl(new ServletEventHandler()), new ProxyServiceImpl(null, null, null));
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        mbeanServer.registerMBean(httpMBean, new ObjectName("org.apache.karaf:type=http,name=root"));
        
        TabularData data = httpMBean.getServlets();
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.http.core.internal.HttpMBeanImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 50. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:11.787Z
- latency: 3.153 s

```json
{
  "test": "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1554,
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

Test class `org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest` (source, may be truncated):
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
package org.apache.karaf.http.core.internal.proxy;

import org.junit.Assert;
import org.junit.Test;

public class BalancingPoliciesTest {

    private static final String proxyTo = "A,B,C";

    @Test
    public void testSingleHost() throws Exception {
        String[] proxyTos = "A".split(",");
        Assert.assertEquals(1, proxyTos.length);
        Assert.assertEquals("A", proxyTos[0]);
    }

    @Test
    public void testRandomBalancingPolicy() throws Exception {
        RandomBalancingPolicy balancingPolicy = new RandomBalancingPolicy();
        String selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("First call: " + selected);
        Assert.assertTrue(selected.equals("A") || selected.equals("B") || selected.equals("C"));
        selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("Second call: " + selected);
        Assert.assertTrue(selected.equals("A") || selected.equals("B") || selected.equals("C"));
        selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("Third call: " + selected);
        Assert.assertTrue(selected.equals("A") || selected.equals("B") || selected.equals("C"));
        selected = balancingPolicy.selectHost("A".split(","));
        System.out.println("Single host: " + selected);
        Assert.assertEquals("A", selected);
    }

    @Test
    public void testRoundRobinBalancingPolicy() throws Exception {
        RoundRobinBalancingPolicy balancingPolicy = new RoundRobinBalancingPolicy();
        String selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("First call: " + selected);
        Assert.assertEquals("A", selected);
        selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("Second call: " + selected);
        Assert.assertEquals("B", selected);
        selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("Third call: " + selected);
        Assert.assertEquals("C", selected);
        selected = balancingPolicy.selectHost(proxyTo.split(","));
        System.out.println("Fourth call: " + selected);
        Assert.assert
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 51. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:14.581Z
- latency: 2.787 s

```json
{
  "test": "org.apache.karaf.instance.command.CreateCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1482,
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

Test class `org.apache.karaf.instance.command.CreateCommandTest` (source, may be truncated):
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
package org.apache.karaf.instance.command;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

import junit.framework.TestCase;

import org.apache.karaf.instance.core.InstanceService;
import org.apache.karaf.instance.core.InstanceSettings;
import org.easymock.EasyMock;

public class CreateCommandTest extends TestCase {

    public void testCreateCommandExecute() throws Exception {
        InstanceService instanceService = EasyMock.createMock(InstanceService.class);
        EasyMock.replay(instanceService);
        
        CreateCommand cc = new CreateCommand();
        cc.setInstanceService(instanceService);
        cc.sshPort = 9941;
        cc.rmiRegistryPort = 1122;
        cc.rmiServerPort = 44444;
        cc.location = "top";
        cc.javaOpts = "foo";
        cc.features = new ArrayList<>(Arrays.asList("abc", "def"));
        cc.featureURLs = new ArrayList<>(Collections.singletonList("http://something"));
        cc.instance = "myInstance";
        cc.verbose = true;

        // Create the features config file used
        System.setProperty("karaf.etc", "target/etc");
        File cfgFile = new File("target/etc/" + CreateCommand.FEATURES_SERVICE_CONFIG_FILE);
        cfgFile.getParentFile().mkdirs();
        cfgFile.createNewFile();

        
        EasyMock.verify(instanceService); // check precondition
        EasyMock.reset(instanceService);
        InstanceSettings expectedIS =
            new InstanceSettings(9941, 1122, 44444, "top", "foo", Collections.singletonList("http://something"), Arrays.asList("abc", "def"));
        EasyMock.expect(instanceService.createInstance("myInstance", expectedIS, true)).andReturn(null);
        EasyMock.replay(instanceService);
        
        cc.doExecute();
        EasyMock.verify(instanceService);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.command.CreateCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.command.CreateCommandTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client configuration.",
  "confidence": 1
}
```

## 52. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:17.310Z
- latency: 2.718 s

```json
{
  "test": "org.apache.karaf.instance.core.InstanceSettingsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1485,
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

Test class `org.apache.karaf.instance.core.InstanceSettingsTest` (source, may be truncated):
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
package org.apache.karaf.instance.core;

import java.util.Collections;
import java.util.List;

import junit.framework.TestCase;

import org.junit.Assert;

public class InstanceSettingsTest extends TestCase {
    public void testInstanceSettings() {
        InstanceSettings is =
            new InstanceSettings(1, 1, 1, null, null, Collections.emptyList(), Collections.singletonList("hi"));
        assertEquals(1, is.getSshPort());
        assertEquals(1, is.getRmiRegistryPort());
        assertEquals(1, is.getRmiServerPort());
        Assert.assertNull(is.getLocation());
        assertEquals(Collections.singletonList("hi"), is.getFeatures());
        assertEquals(0, is.getFeatureURLs().size());
    }
    
    public void testEqualsHashCode() {
        testEqualsHashCode(1, 1, 1, "top", "foo", Collections.emptyList(), Collections.singletonList("hi"));
        testEqualsHashCode(0, 0, 0, null, null, null, null);
    }

    private void testEqualsHashCode(int sshPort, int rmiRegistryPort, int rmiServerPort, String location, String javaOpts, List<String> featureURLs, List<String> features) {
        InstanceSettings is = new InstanceSettings(sshPort, rmiRegistryPort, rmiServerPort, location, javaOpts, featureURLs, features);
        InstanceSettings is2 = new InstanceSettings(sshPort, rmiRegistryPort, rmiServerPort, location, javaOpts, featureURLs, features);
        assertEquals(is, is2);
        assertEquals(is.hashCode(), is2.hashCode());
    }
    
    public void testEqualsHashCode2() {
        InstanceSettings is = new InstanceSettings(1, 1, 1, "top", "foo", Collections.emptyList(),
            Collections.singletonList("hi"));
        Assert.assertNotEquals(null, is);
        Assert.assertNotEquals(is, new Object());
        assertEquals(is, is);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.core.InstanceSettingsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.core.InstanceSettingsTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 53. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:17.317Z
- latency: 2.785 s

```json
{
  "test": "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1551,
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

Test class `org.apache.karaf.instance.core.internal.InstanceServiceImplTest` (source, may be truncated):
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
package org.apache.karaf.instance.core.internal;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

import org.apache.karaf.instance.core.Instance;
import org.apache.karaf.instance.core.InstanceSettings;
import org.junit.BeforeClass;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;
import org.junit.rules.TestName;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

public class InstanceServiceImplTest {

    @Rule
    public TestName name = new TestName();

    @Rule
    public TemporaryFolder tempFolder = new TemporaryFolder();

    @BeforeClass
    public static void setUpClass() throws Exception {
        String buildDirectory = ClassLoader.getSystemResource("etc/startup.properties").getFile()
                .replace("startup.properties", "");
        System.setProperty("karaf.etc", buildDirectory);
    }

    @Test
    public void testHandleFeatures() throws Exception {
        InstanceServiceImpl as = new InstanceServiceImpl();

        File f = tempFolder.newFile(getName() + ".test");
        Properties p = new Properties();
        p.put("featuresBoot", "abc,def ");
        p.put("featuresRepositories", "somescheme://xyz");
        try (OutputStream os = new FileOutputStream(f)) {
            p.store(os, "Test comment");
        }

        InstanceSettings s = new InstanceSettings(8122, 1122, 44444, null, null, null,
            Collections.singletonList("test"));
        as.addFeaturesFromSettings(f, s);

        Properties p2 = new Properties();
        try (InputStream is = new FileInputStream(f)) {
            p2.load(is);
        }
        assertEquals(2, p2.size());
        assertEquals("abc,def,test", p2.get("featuresBoot"));
        assertEquals("somescheme://xyz", p2.get("featuresRepositories"));
    }

    @Test
    public void testConfigurationFiles() throws Exception {
      
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.core.internal.InstanceServiceImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 54. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:20.425Z
- latency: 3.100 s

```json
{
  "test": "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1578,
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

Test class `org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest` (source, may be truncated):
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
package org.apache.karaf.instance.core.management.internal;

import java.util.Arrays;
import java.util.Collections;

import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;

import junit.framework.TestCase;

import org.apache.karaf.instance.core.Instance;
import org.apache.karaf.instance.core.InstanceService;
import org.apache.karaf.instance.core.InstanceSettings;
import org.apache.karaf.instance.core.InstancesMBean;
import org.apache.karaf.instance.core.internal.InstancesMBeanImpl;
import org.easymock.EasyMock;
import org.junit.Assert;

public class InstanceServiceMBeanImplTest extends TestCase {

    public void testCreateInstance() throws Exception {
        final InstanceSettings instanceSettings = new InstanceSettings(123, 456,789, "somewhere", "someopts",
                Collections.emptyList(), Arrays.asList("webconsole", "funfeat"), "localhost");
        
        final Instance inst = EasyMock.createMock(Instance.class);
        EasyMock.expect(inst.getPid()).andReturn(42);
        EasyMock.replay(inst);

        org.apache.karaf.instance.core.InstanceService instanceService = EasyMock.createMock(org.apache.karaf.instance.core.InstanceService.class);
        EasyMock.expect(instanceService.createInstance("t1", instanceSettings, false)).andReturn(inst);
        EasyMock.replay(instanceService);
        
        InstancesMBeanImpl ab = new InstancesMBeanImpl(instanceService);
        assertEquals(42, ab.createInstance("t1", 123, 456, 789, "somewhere", "someopts", " webconsole,  funfeat", ""));
    }
    
    public void testCreateInstance2() throws Exception {
        final InstanceSettings instanceSettings = new InstanceSettings(0, 0, 0, null, null,
                Collections.emptyList(), Collections.emptyList(), "localhost");
        
        InstanceService instanceService = EasyMock.createMock(InstanceService.class);
        EasyMock.expect(instanceService.createInstance("t1", instanceSettings, false)).andReturn(null);
        EasyMock.replay(instanceService);
        
        InstancesMBean ab = new InstancesMBeanImpl(instanceService);
        assertEquals(-1, ab.createInstance("t1", 0, 0, 0, "", "", "", "")
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
  "relevance": 0,
  "reason": "The test class does not interact with the SSH client or related classes that were modified in the code change.",
  "confidence": 1
}
```

## 55. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:23.656Z
- latency: 3.224 s

```json
{
  "test": "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1572,
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

Test class `org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest` (source, may be truncated):
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
package org.apache.karaf.instance.core.management.internal;

import java.util.Collection;
import java.util.Collections;

import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;

import junit.framework.TestCase;

import org.apache.karaf.instance.core.Instance;
import org.apache.karaf.instance.core.internal.InstanceToTableMapper;
import org.easymock.EasyMock;
import org.junit.Assert;

public class InstanceToTableMapperTest extends TestCase {
    public void testJMXInstance() throws Exception {
        Instance instance = EasyMock.createMock(Instance.class);
        EasyMock.expect(instance.getPid()).andReturn(1712);
        EasyMock.expect(instance.getName()).andReturn("MyInstance");
        EasyMock.expect(instance.isRoot()).andReturn(false);
        EasyMock.expect(instance.getSshPort()).andReturn(0);
        EasyMock.expect(instance.getSshHost()).andReturn("0.0.0.0");
        EasyMock.expect(instance.getRmiRegistryPort()).andReturn(0);
        EasyMock.expect(instance.getRmiRegistryHost()).andReturn("0.0.0.0");
        EasyMock.expect(instance.getRmiServerPort()).andReturn(0);
        EasyMock.expect(instance.getRmiServerHost()).andReturn("0.0.0.0");
        EasyMock.expect(instance.getState()).andThrow(new Exception("gotcha"));
        EasyMock.expect(instance.getLocation()).andReturn("somewhere");
        EasyMock.expect(instance.getJavaOpts()).andReturn("someopts");
        EasyMock.replay(instance);
        
        TabularData td = InstanceToTableMapper.tableFrom(Collections.singletonList(instance));
        Collection<?> keys = (Collection<?>) td.keySet().iterator().next();
        Assert.assertEquals("MyInstance", keys.iterator().next());
        
        CompositeData cd = td.get(keys.toArray());
        Assert.assertEquals(1712, cd.get("Pid"));
        Assert.assertEquals("MyInstance", cd.get("Name"));
        Assert.assertEquals(false, cd.get("Is Root"));
        Assert.assertEquals(0, cd.get("SSH Port"));
        Assert.assertEquals("0.0.0.0", cd.get("SSH Host"));
        Assert.assertEquals(0, cd.get("RMI Registry Port"));
        Assert.assertEquals("0.0.0.0", cd.get("RMI Registry Host"));
        Assert.a
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 56. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:26.718Z
- latency: 3.053 s

```json
{
  "test": "org.apache.karaf.instance.main.ExecuteTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1498,
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

Test class `org.apache.karaf.instance.main.ExecuteTest` (source, may be truncated):
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
package org.apache.karaf.instance.main;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.PrintStream;
import java.io.IOException;
import java.util.Properties;

import junit.framework.TestCase;

public class ExecuteTest extends TestCase {
    private String userDir;
    
    @Override
    protected void setUp() throws Exception {
        super.setUp();
        Execute.exitAllowed = false;
        userDir = System.getProperty("user.dir");
    }

    @Override
    protected void tearDown() throws Exception {
        super.tearDown();
        Execute.exitAllowed = true;
        System.setProperty("user.dir", userDir);
    }

    public void testListCommands() throws Exception {
        PrintStream oldOut = System.out;
        
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream capturedOut = new PrintStream(baos); 
        System.setOut(capturedOut);

        try {
            Execute.main(new String [] {});            
        } catch (RuntimeException re) {
            assertEquals("0", re.getMessage());

            String s = new String(baos.toByteArray());            
            assertTrue(s.contains("list"));
            assertTrue(s.contains("create"));
            assertTrue(s.contains("destroy"));
        } finally {
            System.setOut(oldOut);
        }
    }
    
    public void testNonexistingCommand() throws Exception {
        try {
            Execute.main(new String [] {"bheuaark"});
        } catch (RuntimeException re) {
            assertEquals("-1", re.getMessage());
        }
    }
    
    public void testNoStorageFile() throws Exception {
        PrintStream oldErr = System.err;
        
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream capturedErr = new PrintStream(baos); 
        System.setErr(capturedErr);

        try {
            Execute.main(new String [] {"create"});            
        } catch (RuntimeException re) {
            assertEquals("-2", re.getMessage());
            
            String s = new String(baos.toByteArray());            
            assertTrue(s.contains("karaf.instances"));
            assertTrue(s.contain
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.instance.main.ExecuteTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.instance.main.ExecuteTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 57. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:26.726Z
- latency: 3.148 s

```json
{
  "test": "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
  "attempt": 0,
  "cached": true,
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

## 58. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:26.734Z
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

## 59. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:29.936Z
- latency: 3.194 s

```json
{
  "test": "org.apache.karaf.jaas.command.ManageRealmCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1599,
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

Test class `org.apache.karaf.jaas.command.ManageRealmCommandTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.jaas.command;

import java.util.Arrays;
import java.util.Collections;
import java.util.Properties;

import org.apache.karaf.jaas.config.impl.Config;
import org.apache.karaf.jaas.config.impl.Module;
import org.apache.karaf.shell.api.console.Session;
import org.easymock.Capture;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;

import static org.easymock.EasyMock.anyObject;
import static org.easymock.EasyMock.capture;
import static org.easymock.EasyMock.createMock;
import static org.easymock.EasyMock.eq;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.newCapture;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class ManageRealmCommandTest {

    @Test
    public void testSelectByIndex() throws Exception {
        ManageRealmCommand cmd = new ManageRealmCommand();

        // set up two realms, each containing 1 module

        Config realm1 = newConfigNamed("realm1");
        realm1.setModules(new Module[] { newModuleNamed("module1") });

        Config realm2 = newConfigNamed("realm2");
        realm2.setModules(new Module[] { newModuleNamed("module2") });

        Config[] realms = { realm1, realm2 };

        doVerifyIndex(cmd, 1, realms);
        doVerifyIndex(cmd, 2, realms);
    }

    @Test
    public void testRealmAdd() throws Exception {
        RealmAddCommand cmd = new RealmAddCommand();
        cmd.setRealmname("myDummyRealm");

        // prepare mocks
        Session session = createMock(Session.class);
        BundleContext bundleContext = createMock(BundleContext.class);
        Bundle bundle = createMock(Bundle.class);

        // prepare command
        cmd.setContext(bundleContext);
        cmd.setSession(session);

        Object[] mocks = { session, bundleContext, bundle };

        expect(bundleContext.registerService(anyObject(Class.class),
            (Object)anyObject(), anyObject())).andReturn(null).anyTimes();

        replay(mocks);
        cmd.execute();
        verify(mocks);
    }

    @T
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.command.ManageRealmCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.command.ManageRealmCommandTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 60. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:33.030Z
- latency: 3.086 s

```json
{
  "test": "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1295,
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

Test class `org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest` (source, may be truncated):
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
package org.apache.karaf.jaas.jasypt.impl;

import java.util.HashMap;
import java.util.Map;

import junit.framework.TestCase;
import org.apache.karaf.jaas.modules.EncryptionService;

/**
 * Test <code>JasyptEncryption</code>.
 */
public class JasyptEncryptionTest extends TestCase {
    
    private JasyptEncryption encryption;
    
    /*
     * (non-Javadoc)
     * @see junit.framework.TestCase#setUp()
     */
    public void setUp() {
        Map<String,String> props = new HashMap<>();
        props.put(EncryptionService.ALGORITHM, "MD5");
        this.encryption = new JasyptEncryption(props);
    }
    
    /**
     * <p>
     * Test <code>checkPassword()</p> method.
     * </p>
     * 
     * @throws Exception in case of test error.
     */
    public void testCheckPassword() throws Exception {
        String password = this.encryption.encryptPassword("test");
        
        assertEquals(true, this.encryption.checkPassword("test", password));
    }
    
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 61. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:36.076Z
- latency: 3.038 s

```json
{
  "test": "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1424,
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

Test class `org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.audit;

import org.apache.karaf.jaas.boot.principal.ClientPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.junit.Assert;
import org.junit.Test;

import javax.security.auth.Subject;
import java.nio.file.attribute.UserPrincipal;
import java.util.HashMap;
import java.util.Map;

public class AbstractAuditLoginModuleTest {

    @Test
    public void getPrincipalInfo() {
        LogAuditLoginModule module = new LogAuditLoginModule();
        Map<String, String> options = new HashMap<>();
        options.put("logger", "test");
        Subject subject = new Subject();
        subject.getPrincipals().add(new ClientPrincipal("ssh", "/127.0.0.1"));
        subject.getPrincipals().add(new ClientPrincipal("ssh", "/127.0.0.2"));
        subject.getPrincipals().add((UserPrincipal) () -> "noexist");
        module.initialize(subject, new NamePasswordCallbackHandler("myuser", "mypassword"), null, options);
        Assert.assertEquals("ssh(/127.0.0.1), ssh(/127.0.0.2)", module.getPrincipalInfo());
    }

    @Test
    public void getPrincipalInfoEmpty() {
        LogAuditLoginModule module = new LogAuditLoginModule();
        Map<String, String> options = new HashMap<>();
        options.put("logger", "test");
        Subject subject = new Subject();
        module.initialize(subject, new NamePasswordCallbackHandler("myuser", "mypassword"), null, options);
        Assert.assertEquals("no client principals found", module.getPrincipalInfo());
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 62. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:39.240Z
- latency: 3.156 s

```json
{
  "test": "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1527,
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

Test class `org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.jdbc;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;

import javax.security.auth.Subject;
import javax.sql.DataSource;

import org.apache.derby.jdbc.EmbeddedDataSource;
import org.apache.karaf.jaas.boot.principal.GroupPrincipal;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.easymock.EasyMock;
import org.junit.Before;
import org.junit.Test;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceReference;

import static org.easymock.EasyMock.expect;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

public class JdbcLoginModuleTest {

    private EmbeddedDataSource dataSource;
    private Map<String, Object> options;

    @SuppressWarnings("unchecked")
    @Before
    public void setUp() throws Exception {
        System.setProperty("derby.stream.error.file", "target/derby.log");

        // Create datasource
        dataSource = new EmbeddedDataSource();
        dataSource.setDatabaseName("memory:db");
        dataSource.setCreateDatabase("create");

        // Delete tables
        try (Connection connection = dataSource.getConnection()) {
            connection.setAutoCommit(true);
            try (Statement statement = connection.createStatement()) {
                    statement.execute("drop table USERS");
            } catch (SQLException e) {
                // Ignore
            }
            try (Statement statement = connection.createStatement()) {
                statement.execute("drop table ROLES");
            } catch (SQLException e) {
                // Ignore
            }
            try (Statement statement = connection.createStatement()) {
                statement.execute("create table USERS (USERNAME VARCHAR(32) PRIMARY KEY, PASSWORD VARCHAR(32))");
                statement.execute("create table ROLES (USERNAME VARCHAR(32), ROLE VARCHAR(1024))");
            }
            connection.commit();
        }

        BundleContext context = EasyMock.createMock(BundleContext.class);
        ServiceReference<DataSource> reference = 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client configuration and properties.",
  "confidence": 1
}
```

## 63. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:42.524Z
- latency: 3.276 s

```json
{
  "test": "org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1544,
  "completion_tokens": 70
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

Test class `org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.krb5;

import org.apache.directory.api.ldap.model.constants.SupportedSaslMechanisms;
import org.apache.directory.api.ldap.model.entry.DefaultEntry;
import org.apache.directory.api.ldap.model.entry.Entry;
import org.apache.directory.api.ldap.model.exception.LdapException;
import org.apache.directory.ldap.client.api.Krb5LoginConfiguration;
import org.apache.directory.server.annotations.CreateKdcServer;
import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.annotations.SaslMechanism;
import org.apache.directory.server.core.annotations.ApplyLdifs;
import org.apache.directory.server.core.annotations.ContextEntry;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreateIndex;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.directory.server.core.kerberos.KeyDerivationInterceptor;
import org.apache.directory.server.kerberos.kdc.KerberosTestUtils;
import org.apache.directory.server.kerberos.shared.crypto.encryption.KerberosKeyFactory;
import org.apache.directory.server.kerberos.shared.keytab.Keytab;
import org.apache.directory.server.kerberos.shared.keytab.KeytabEntry;
import org.apache.directory.server.ldap.handlers.sasl.cramMD5.CramMd5MechanismHandler;
import org.apache.directory.server.ldap.handlers.sasl.digestMD5.DigestMd5MechanismHandler;
import org.apache.directory.server.ldap.handlers.sasl.gssapi.GssapiMechanismHandler;
import org.apache.directory.server.ldap.handlers.sasl.ntlm.NtlmMechanismHandler;
import org.apache.directory.server.ldap.handlers.sasl.plain.PlainMechanismHandler;
import org.apache.directory.server.protocol.shared.transport.TcpTransport;
import org.apache.directory.server.protocol.shared.transport.Transport;
import org.apache.directory.shared.kerberos.KerberosTime;
import org.apache.directory.shared.kerberos.KerberosUtils;
import org.apache.directory.shared.kerberos.codec.types.EncryptionType;
import org.apache.directory.shared.kerberos.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.krb5.Krb5LoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 64. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:45.451Z
- latency: 2.919 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1445,
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

Test class `org.apache.karaf.jaas.modules.ldap.BadReferenceTest` (source, may be truncated):
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

import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;

import java.io.File;
import java.io.IOException;
import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.felix.utils.properties.Properties;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;

@RunWith(FrameworkRunner.class)
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "BadReferenceTest-class",
    partitions = {@CreatePartition(name = "example", suffix = "dc=example,dc=com")})
@ApplyLdifFiles(
    "org/apache/karaf/jaas/modules/ldap/example.com_badref.ldif"
)
public class BadReferenceTest extends LdapCacheTest {

    @Before
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldap_badref.properties",
                  LdapLoginModuleTest::replacePort);
    }

    @After
    public void tearDown() {
        LDAPCache.clear();
    }

    @Override
    protected Properties ldapLoginModuleOptions() throws IOException {
        String basedir = System.getProperty("basedir");
        if (basedir == null) {
            basedir = new File(".").getCanonicalPath();
        }
        File file = new File(basedir + "/target/test-classes/org/apache/karaf/jaas/modules/ldap/ldap_badref.properties");
        return new Properties(file);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.BadReferenceTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
  "relevance": 0,
  "reason": "The test class is focused on LDAP authentication and does not involve changes related to SSH client properties or configurations.",
  "confidence": 1
}
```

## 65. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:48.791Z
- latency: 3.332 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1595,
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

Test class `org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.ldap;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.security.auth.Subject;
import javax.security.auth.login.LoginException;
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
import org.apache.karaf.jaas.modules.NamePubkeyCallbackHandler;
import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;
import org.apache.log4j.Level;
import org.hamcrest.Matchers;
import static org.hamcrest.Matchers.containsInAnyOrder;
import org.junit.After;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(FrameworkRunner.class)
@CreateLdapServer(transports = {
    @CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapPubkeyLoginModuleTest-class",
        partitions = {
            @CreatePartition(name = "example", suffix = "dc=example,dc=com")})
@ApplyLdifFiles(
        "org/apache/karaf/jaas/modules/ldap/example.com_pubkey.ldif"
)
public class LDAPPubkeyLoginModuleTest extends AbstractLdapTestUnit {

    private static final String LDAP_PROPERTIES_FILE = "org/apache/karaf/jaas/modules/ldap/ldap_pubkey.properties";

    @Before
    public void updatePort() throws Exception {
        ldapProps(LDAP_PROPERTIES_FILE, LdapLoginModuleTest::replacePort);
    }

    public static String replacePort(String line) {
        return line.replaceAll("portno", "" + getLdapServer().getPort());
    }

    @After
    public void tearDown() {
        LDAPCache.clear();
    }

    @Test
  
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 66. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:52.128Z
- latency: 3.329 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1571,
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
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSHD and Karaf client configurations.",
  "confidence": 1
}
```

## 67. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:55.444Z
- latency: 3.308 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1578,
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

Test class `org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest` (source, may be truncated):
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

import javax.security.auth.Subject;

import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith ( FrameworkRunner.class )
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapCaseInsensitiveDNTest-class",
 partitions = { @CreatePartition(name = "example", suffix = "dc=example,dc=com") })
@ApplyLdifFiles(
   "org/apache/karaf/jaas/modules/ldap/example.com.ldif"
)
public class LdapCaseInsensitiveDNTest extends LdapLoginModuleTest {
    
    @Before
    @Override
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldapCaseInsensitiveDN.properties", 
                  LdapLoginModuleTest::replacePort);
    }
    
    @Test
    public void testCaseInsensitiveDN() throws Exception {
        Properties options = ldapLoginModuleOptions();
        LDAPLoginModule module = new LDAPLoginModule();
        Subject subject = new Subject();
        module.initialize(subject, new NamePasswordCallbackHandler("admin", "admin123"), null, options);

        assertEquals("Precondition", 0, subject.getPrincipals().size());
        assertTrue(module.login());
        assertTrue(module.commit());

        assertEquals(2, subject.getPrincipals().size());
        assertThat(names(subject.getPrincipals(UserPrincipal.class)), contains
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSHD and Karaf client configurations.",
  "confidence": 1
}
```

## 68. semantic_analyzer · llm_call

- time: 2026-11-07T18:02:58.731Z
- latency: 3.280 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1577,
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

Test class `org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest` (source, may be truncated):
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

import org.apache.directory.server.core.integ.AbstractLdapTestUnit;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.apache.log4j.Level;
import org.hamcrest.Matchers;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import javax.security.auth.Subject;
import javax.security.auth.login.LoginException;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

@RunWith(FrameworkRunner.class)
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapLoginModuleTest-class",
        partitions = {@CreatePartition(name = "example", suffix = "dc=example,dc=com")})
@ApplyLdifFiles(
        "org/apache/karaf/jaas/modules/ldap/example.com.ldif"
)
public class LdapLoginModuleTest extends AbstractLdapTestUnit {

    @Before
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldap.properties",
                                   LdapLoginModuleTest::replacePort);
    }

    public static String replacePort(String line) {
        return line.replaceAll("portno", "" + getLdapServer().getPort());
    }
    
    @After
    public void tearDown() {
        LDAPCache.clear();
    }

    @Test
    public void testAdminLogin() throws Exception {
        Properties options = ldapLoginModuleOptions();
        LDAPLoginModule m
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 69. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:01.838Z
- latency: 3.096 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1341,
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

Test class `org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest` (source, may be truncated):
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

import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;

import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.junit.Before;
import org.junit.runner.RunWith;

@RunWith ( FrameworkRunner.class )
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapLoginModuleWithEscapesTest-class",
 partitions = { @CreatePartition(name = "example", suffix = "dc=example,dc=com") })
@ApplyLdifFiles(
   "org/apache/karaf/jaas/modules/ldap/example.com_with_escapes.ldif"
)
public class LdapLoginModuleWithEscapesTest extends LdapLoginModuleTest {
    
    @Before
    @Override
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldap.properties", 
                  LdapLoginModuleTest::replacePort);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 70. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:04.991Z
- latency: 3.145 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1599,
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

Test class `org.apache.karaf.jaas.modules.ldap.LdapPoolingTest` (source, may be truncated):
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

import java.io.FileInputStream;
import java.io.IOException;
import java.net.Socket;
import java.security.KeyStore;
import java.security.SecureRandom;
import java.util.Hashtable;
import javax.naming.directory.InitialDirContext;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;

import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.directory.server.core.integ.AbstractLdapTestUnit;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;

@RunWith ( FrameworkRunner.class )
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAPS", ssl = true)},
 keyStore = "src/test/resources/org/apache/karaf/jaas/modules/ldap/ldaps.jks", certificatePassword = "123456")
@CreateDS(name = "LdapPoolingTest-class",
 partitions = { @CreatePartition(name = "example", suffix = "dc=example,dc=com") })
@ApplyLdifFiles(
   "org/apache/karaf/jaas/modules/ldap/example.com.ldif"
)
public class LdapPoolingTest extends AbstractLdapTestUnit {

    private SSLContext sslContext;

    @Before
    public void keystore() throws Exception {
        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
        ks.load(new FileInputStream("src/test/resources/org/apache/karaf/jaas/modules/ldap/ldaps.jks"), "123456".toCharArray());
        kmf.init(ks, "123456".toCharArray());
        tmf.init(ks);

        String javaVendor = System.getProperty("java.vendor");
        if (javaVendor.contains("IBM")) {
        	sslContext = SSLContext.getInstance("SSL_TLSv2","IBMJSSE2");
        } else {
            sslContext = SSLContext.getInstance("TLSv1.2");
        }
        sslContext.init(kmf.getKeyManagers(), tmf
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 71. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:08.369Z
- latency: 3.371 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1599,
  "completion_tokens": 70
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

Test class `org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest` (source, may be truncated):
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

import static org.apache.karaf.jaas.modules.ldap.LdapPropsUpdater.ldapProps;

import java.io.File;
import java.io.IOException;

import org.apache.directory.api.ldap.model.constants.SchemaConstants;
import org.apache.directory.api.ldap.model.message.ModifyRequest;
import org.apache.directory.api.ldap.model.message.ModifyRequestImpl;
import org.apache.directory.api.ldap.model.name.Dn;
import org.apache.directory.ldap.client.api.LdapConnection;
import org.apache.directory.ldap.client.api.LdapNetworkConnection;
import org.apache.directory.server.core.integ.FrameworkRunner;
import org.apache.directory.server.annotations.CreateLdapServer;
import org.apache.directory.server.annotations.CreateTransport;
import org.apache.directory.server.core.annotations.ApplyLdifFiles;
import org.apache.directory.server.core.annotations.CreateDS;
import org.apache.directory.server.core.annotations.CreatePartition;
import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest;
import org.junit.Before;
import org.junit.runner.RunWith;

@RunWith ( FrameworkRunner.class )
@CreateLdapServer(transports = {@CreateTransport(protocol = "LDAP")})
@CreateDS(name = "LdapSpecialCharsInPasswordTest-class",
 partitions = { @CreatePartition(name = "example", suffix = "dc=example,dc=com") })
@ApplyLdifFiles(
   "org/apache/karaf/jaas/modules/ldap/example.com.ldif"
)
public class LdapSpecialCharsInPasswordTest extends LdapLoginModuleTest {
    
    private static final String NEW_CONNECTION_PASSWORD = "#a&b{>c=<12~d%";
    
    @Before
    @Override
    public void updatePort() throws Exception {
        ldapProps("org/apache/karaf/jaas/modules/ldap/ldap_special_char_in_password.properties", 
                  LdapLoginModuleTest::replacePort);
    }

    protected Properties ldapLoginModuleOptions() throws IOException {
        String basedir = System.getProperty("basedir");
        if (basedir == null) {
            basedir = new File(".").getCanonicalPath();
        }
        File file = new File(basedir + "/target/test-classes/org/apache/karaf/jaas/modules/ldap/ldap_special_char_in_password.properties");
        return new Properties(file);
    }
    
    @Before
    public void changeAdminPassword() throws Exception {
        LdapConnection connection = new LdapNetworkConnection( "localhost", getLdap
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 72. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:11.562Z
- latency: 3.185 s

```json
{
  "test": "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1594,
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

Test class `org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.properties;

import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.GroupPrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class PropertiesBackingEngineTest {
    private File f;

    @Before
    public void start() throws IOException {
        f = File.createTempFile(getClass().getName(), ".tmp");
    }

    @Test
    public void testUserRoles() throws IOException {
        Properties p = new Properties(f);

        PropertiesBackingEngine engine = new PropertiesBackingEngine(p);
        engine.addUser("a", "aa");
        engine.addUser("b", "bb");

        engine.addRole("a", "role1");
        engine.addRole("a", "role2");
        
        UserPrincipal upa = getUser(engine, "a");
        Assert.assertThat(names(engine.listRoles(upa)), containsInAnyOrder("role1", "role2"));

        engine.addGroup("a", "g");
        engine.addGroupRole("g", "role2");
        engine.addGroupRole("g", "role3");
        engine.addGroup("b", "g");
        engine.addGroup("b", "g2");
        engine.addGroupRole("g2", "role4");

        Assert.assertThat(names(engine.listUsers()), containsInAnyOrder("a", "b"));
        Assert.assertThat(names(engine.listRoles(upa)), containsInAnyOrder("role1", "role2", "role3"));

        checkLoading();

        assertNotNull(engine.lookupUser("a"));
        assertEquals("a", engine.lookupUser("a").getName());

        // removing some stuff
        UserPrincipal upb = getUser(engine, "b");
        assertEquals(1, engine.listGroups(upa).size());
        assertEquals(2, engine.listGroups(upb).size());

        GroupPrincipal gp = engine.listGroups(upa).iterator().next();
        engine.dele
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 73. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:14.741Z
- latency: 3.170 s

```json
{
  "test": "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1532,
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

Test class `org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.properties;

import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.junit.Assert.assertThat;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.security.auth.Subject;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.callback.UnsupportedCallbackException;
import javax.security.auth.login.FailedLoginException;
import javax.security.auth.login.LoginException;

import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.GroupPrincipal;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePasswordCallbackHandler;
import org.junit.Assert;
import org.junit.Test;

public class PropertiesLoginModuleTest {

    @Test
    public void testBasicLogin() throws Exception {
        File f = File.createTempFile(getClass().getName(), ".tmp");
        try {
            Properties p = new Properties(f);
            PropertiesBackingEngine pbe = new PropertiesBackingEngine(p);
            pbe.addUser("abc", "xyz");
            pbe.addRole("abc", "myrole");
            pbe.addUser("pqr", "abc");

            PropertiesLoginModule module = new PropertiesLoginModule();
            Map<String, String> options = new HashMap<>();
            options.put(PropertiesLoginModule.USER_FILE, f.getAbsolutePath());
            Subject subject = new Subject();
            module.initialize(subject, new NamePasswordCallbackHandler("abc", "xyz"), null, options);

            Assert.assertEquals("Precondition", 0, subject.getPrincipals().size());
            Assert.assertTrue(module.login());
            Assert.assertTrue(module.commit());

            Assert.assertEquals(2, subject.getPrincipals().size());

            assertThat(names(subject.getPrincipals(UserPrincipal.class)), containsInAnyOrder("abc"));
            assertThat(names(subject.getPrincipals(RolePrincipal.class)), containsInAnyOrder("myrole"));

            Assert.assertTrue(mod
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client configuration and properties.",
  "confidence": 1
}
```

## 74. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:18.313Z
- latency: 3.562 s

```json
{
  "test": "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 2058,
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

Test class `org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.publickey;

import static org.apache.karaf.jaas.modules.PrincipalHelper.names;
import static org.hamcrest.Matchers.isIn;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.security.AlgorithmParameters;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.DSAPublicKeySpec;
import java.security.spec.ECGenParameterSpec;
import java.security.spec.ECParameterSpec;
import java.security.spec.ECPoint;
import java.security.spec.ECPublicKeySpec;
import java.security.spec.KeySpec;
import java.security.spec.RSAPublicKeySpec;

import javax.security.auth.Subject;
import javax.security.auth.login.FailedLoginException;

import org.apache.felix.utils.properties.Properties;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.jaas.boot.principal.UserPrincipal;
import org.apache.karaf.jaas.modules.NamePubkeyCallbackHandler;
import org.junit.Test;

public class PublicKeyLoginModuleTest {

    private static final String PK_PROPERTIES_FILE = "org/apache/karaf/jaas/modules/publickey/pubkey.properties";

    @Test
    public void testRSALogin() throws Exception {
        Properties options = getLoginModuleOptions();
        PublickeyLoginModule module = new PublickeyLoginModule();
        Subject subject = new Subject();

        String knownModulus = "2504227846033126752625313329217708474924890377669312098933267135871562327792150810915433595733"
            + "979130785790337621243914845149325143098632580183245971502051291613503136182182218708721890923769091345704"
            + "119963221758691543226829294312457492456071842409242817598014777158790065648435489978774648853589909638928"
            + "448069481622573966178879417253888452317622624006445863588961367514293886664167742695648199055900918338245"
            + "701727653606086096756173044470526840851957391900922886984556493506186438991284463663361749451775578708454"
            + "0181594148839238901052763862484299588887844606103377160953183624788815045644521767391398467190125279747";

        // Generate a PublicKey using the known values
        BigInteger modulus = new Big
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 75. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:21.636Z
- latency: 3.312 s

```json
{
  "test": "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1550,
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

Test class `org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest` (source, may be truncated):
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
package org.apache.karaf.jaas.modules.syncope;

import static org.hamcrest.Matchers.contains;
import static org.junit.Assert.assertThat;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.junit.Test;

public class SyncopeLoginModuleTest {

    @Test
    public void testRolesExtractionSyncope1() throws Exception {
        String syncopeResponse = read("syncope1Response.xml");
        SyncopeLoginModule syncopeLoginModule = new SyncopeLoginModule();
        List<String> roles = syncopeLoginModule.extractingRolesSyncope1(syncopeResponse);
        assertThat(roles, contains("admin", "another"));
    }

    @Test
    public void testRolesExtractionSyncope2() throws Exception {
        String syncopeResponse = read("syncope2Response.json");
        SyncopeLoginModule syncopeLoginModule = new SyncopeLoginModule();
        Map<String, String> options = Collections.singletonMap(SyncopeLoginModule.USE_ROLES_FOR_SYNCOPE2, "true");
        syncopeLoginModule.initialize(null, null, Collections.emptyMap(), options);
        List<String> roles = syncopeLoginModule.extractingRolesSyncope2(syncopeResponse);
        assertThat(roles, contains("admin", "another"));
    }

    @Test
    public void testGroupsExtractionSyncope2() throws Exception {
        String syncopeResponse = read("syncope2Response.json");
        SyncopeLoginModule syncopeLoginModule = new SyncopeLoginModule();
        List<String> roles = syncopeLoginModule.extractingRolesSyncope2(syncopeResponse);
        assertThat(roles, contains("manager"));
    }

    private String read(String resourceName) throws URISyntaxException, IOException {
        URI response = this.getClass().getResource(resourceName).toURI();
        return Files.lines(Paths.get(response), StandardCharsets.UTF_8)
            .collect(Collectors.joining("\n"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 76. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:24.739Z
- latency: 3.092 s

```json
{
  "test": "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1477,
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

Test class `org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest` (source, may be truncated):
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
package org.apache.karaf.jaas.spring_security_crypto.impl;

import java.util.HashMap;
import java.util.Map;

import org.apache.karaf.jaas.modules.EncryptionService;

/**
 * Test <code>SpringSecurityCryptoEncryption</code>.
 */
public class SpringSecurityCryptoEncryptionTest {

    @org.junit.Test
    public void testCheckPasswordPBKDF12() throws Exception {
        performTest("pbkdf2", EncryptionService.ENCODING_BASE64);
        performTest("pbkdf2", EncryptionService.ENCODING_HEXADECIMAL);
        performTest("pbkdf2", null);
    }

    @org.junit.Test
    public void testCheckPasswordBCrypt() throws Exception {
        performTest("bcrypt", EncryptionService.ENCODING_BASE64);
        performTest("bcrypt", EncryptionService.ENCODING_HEXADECIMAL);
        performTest("bcrypt", null);
    }

    @org.junit.Test
    public void testCheckPasswordSCrypt() throws Exception {
        performTest("scrypt", EncryptionService.ENCODING_BASE64);
        performTest("scrypt", EncryptionService.ENCODING_HEXADECIMAL);
        performTest("scrypt", null);
    }

    @org.junit.Test
    public void testCheckPasswordArgon2() throws Exception {
        performTest("argon2", EncryptionService.ENCODING_BASE64);
        performTest("argon2", EncryptionService.ENCODING_HEXADECIMAL);
    }

    private void performTest(String algorithm, String encoding) throws Exception {
        Map<String,String> props = new HashMap<>();
        props.put(EncryptionService.ALGORITHM, algorithm);
        props.put(EncryptionService.ENCODING, encoding);
        SpringSecurityCryptoEncryption encryption = new SpringSecurityCryptoEncryption(props);
        String password = encryption.encryptPassword("test");
        org.junit.Assert.assertEquals(true, encryption.checkPassword("test", password));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 77. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:27.680Z
- latency: 2.931 s

```json
{
  "test": "org.apache.karaf.jpm.ProcessTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1542,
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

Test class `org.apache.karaf.jpm.ProcessTest` (source, may be truncated):
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
package org.apache.karaf.jpm;

import java.io.File;

import junit.framework.TestCase;

import org.apache.karaf.jpm.impl.ProcessBuilderFactoryImpl;
import org.apache.karaf.jpm.impl.ScriptUtils;

public class ProcessTest extends TestCase {

    public void testCreate() throws Exception {
        String javaPath = new File(System.getProperty("java.home"), ScriptUtils.isWindows() ? "bin\\java.exe" : "bin/java").getCanonicalPath();
        System.err.println(javaPath);
        StringBuilder command = new StringBuilder();
        command.append("\"").append(javaPath).append("\"");
        command.append(" -Dprop=\"key\"");
        command.append(" -classpath ");
        String clRes = getClass().getName().replace('.', '/') + ".class";
        String str = getClass().getClassLoader().getResource(clRes).toString();
        str = str.substring("file:".length(), str.indexOf(clRes));
        command.append(str);
        command.append(" ");
        command.append(MainTest.class.getName());
        command.append(" ");
        command.append(60000); // process sleep time
        command.append(" ");
        command.append(11000); // shutdown sleep time, to have the SIGKILL get triggered
        System.err.println("Executing: " + command.toString());

        ProcessBuilder builder = new ProcessBuilderFactoryImpl().newBuilder();
        org.apache.karaf.jpm.Process p = builder.command(command.toString()).start();
        assertNotNull(p);
        System.err.println("Process: " + p.getPid());
        assertNotNull(p.getPid());
        Thread.sleep(1000);
        System.err.println("Running: " + p.isRunning());
        assertTrue(p.isRunning());
        System.err.println("Destroying");
        p.destroy();
        Thread.sleep(1000);
        System.err.println("Running: " + p.isRunning());
        assertFalse(p.isRunning());
    }

    /*
     * When the process creation fails, no error is reported by the script
     * 
    public void testFailure() throws Exception {
        ProcessBuilder builder = ProcessBuilderFactory.newInstance().newBuilder();
        Process p = builder.command("ec").start();
        fail("An exception should have been thrown");
    }
    */
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.jpm.ProcessTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.jpm.ProcessTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 0.9
}
```

## 78. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:30.697Z
- latency: 3.001 s

```json
{
  "test": "org.apache.karaf.kar.internal.KarTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1587,
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

Test class `org.apache.karaf.kar.internal.KarTest` (source, may be truncated):
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
package org.apache.karaf.kar.internal;

import org.junit.Assert;
import org.junit.Test;

import java.io.File;
import java.io.FileOutputStream;
import java.net.URI;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class KarTest {

    @Test
    public void karExtractTest() throws Exception {
        File base = new File("target/test");
        base.mkdirs();

        Kar kar = new Kar(new URI("https://repo1.maven.org/maven2/org/apache/karaf/features/framework/4.2.2/framework-4.2.2.kar"));
        File repoDir = new File("target/test/framework-repo");
        repoDir.mkdirs();
        File resourcesDir = new File("target/test/framework-resources");
        resourcesDir.mkdirs();

        kar.extract(repoDir, resourcesDir);

        File[] repoDirFiles = repoDir.listFiles();
        Assert.assertEquals(1, repoDirFiles.length);
        Assert.assertEquals("org", repoDirFiles[0].getName());
        File[] resourceDirFiles = resourcesDir.listFiles();
        Assert.assertEquals(6, resourceDirFiles.length);
    }

    @Test
    public void badKarExtractTest() throws Exception {
        File base = new File("target/test");
        base.mkdirs();
        File badKarFile = new File(base,"bad.kar");
        ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(badKarFile));
        ZipEntry entry = new ZipEntry("../../../../foo.bar");
        zos.putNextEntry(entry);

        byte[] data = "Test Data".getBytes();
        zos.write(data, 0, data.length);
        zos.closeEntry();
        zos.close();

        Kar kar = new Kar(new URI("file:target/test/bad.kar"));
        File repoDir = new File("target/test/repo");
        repoDir.mkdirs();
        File resourceDir = new File("target/test/resources");
        resourceDir.mkdirs();
        kar.extract(repoDir, resourceDir);

        File[] repoDirFiles = repoDir.listFiles();
        Assert.assertEquals(0, repoDirFiles.length);
        File[] resourceDirFiles = resourceDir.listFiles();
        Assert.assertEquals(0, resourceDirFiles.length);

        badKarFile.delete();
    }

    @Test
    public void badEncodedKarExtractTest() throws Exception {
        File base = new File("tar
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.kar.internal.KarTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.kar.internal.KarTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 79. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:34.006Z
- latency: 3.300 s

```json
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1575,
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

Test class `org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest` (source, may be truncated):
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
package org.apache.karaf.log.core.internal;

import org.junit.Test;

import java.util.Dictionary;
import java.util.Hashtable;

import static org.hamcrest.Matchers.hasEntry;
import static org.junit.Assert.assertThat;

public class LogServiceLog4j2ImplTest {

    private static final String ROOT_LOGGER = "log4j.rootLogger";

    private static final String LOGGER_PREFIX = "log4j2.logger.";

    private static final String NAME_SUFFIX = ".name";

    private static final String LEVEL_SUFFIX = ".level";

    @Test
    public void testLoggerNameWithNumbers() {
        final String name = "some_logger_name";
        final String logger = "org.ops4j.pax.web";
        final String level = "WARN";

        final Dictionary<String, Object> config = new Hashtable<>();
        config.put(ROOT_LOGGER, "INFO");
        config.put(LOGGER_PREFIX + name + NAME_SUFFIX, logger);
        config.put(LOGGER_PREFIX + name + LEVEL_SUFFIX, level);

        final LogServiceInternal logServiceInternal = new LogServiceLog4j2Impl(config);

        assertThat(logServiceInternal.getLevel(logger), hasEntry(logger, level));
    }

    @Test
    public void testSetLevelForLoggerNameWithNumbers() {
        final String logger = "org.ops4j.pax.web";
        final String level = "WARN";

        final Dictionary<String, Object> config = new Hashtable<>();
        config.put(ROOT_LOGGER, "INFO");
        final LogServiceInternal logServiceInternal = new LogServiceLog4j2Impl(config);

        logServiceInternal.setLevel(logger, level);

        assertThat(logServiceInternal.getLevel(logger), hasEntry(logger, level));
    }

    @Test
    public void testUpdateLevelForLoggerNameWithNumbers() {
        final String name = "some_logger_name";
        final String logger = "org.ops4j.pax.web";

        final Dictionary<String, Object> config = new Hashtable<>();
        config.put(ROOT_LOGGER, "INFO");
        config.put(LOGGER_PREFIX + name + NAME_SUFFIX, logger);
        config.put(LOGGER_PREFIX + name + LEVEL_SUFFIX, "WARN");
        final LogServiceInternal logServiceInternal = new LogServiceLog4j2Impl(config);

        final String newLevel = "TRACE";
        logServiceInternal.setLevel(logger, n
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 80. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:37.227Z
- latency: 3.214 s

```json
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1556,
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

Test class `org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest` (source, may be truncated):
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
package org.apache.karaf.log.core.internal;

import org.junit.Test;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.ByteArrayInputStream;
import java.io.StringWriter;

import static org.junit.Assert.assertEquals;

public class LogServiceLog4j2XmlImplTest {

    @Test
    public void testInsertIndentedTabs() throws Exception {
        String xml = "<Configuration>\n" +
                "\t<Loggers>\n" +
                "\t</Loggers>\n" +
                "</Configuration>";

        String out = insertIndented(xml, false);
        assertEquals(
                "<Configuration>\n" +
                        "\t<Loggers>\n" +
                        "\t\t<Logger/>\n" +
                        "\t</Loggers>\n" +
                        "</Configuration>", out);
        out = insertIndented(xml, true);
        assertEquals(
                "<Configuration>\n" +
                        "\t<Loggers>\n" +
                        "\t\t<Logger/>\n" +
                        "\t</Loggers>\n" +
                        "</Configuration>", out);
    }

    @Test
    public void testInsertIndentedSpaces() throws Exception {
        String xml = "<Configuration>\n" +
                "  <Loggers>\n" +
                "  </Loggers>\n" +
                "</Configuration>";

        String out = insertIndented(xml, false);
        assertEquals(
                "<Configuration>\n" +
                        "  <Loggers>\n" +
                        "    <Logger/>\n" +
                        "  </Loggers>\n" +
                        "</Configuration>", out);
        out = insertIndented(xml, true);
        assertEquals(
                "<Configuration>\n" +
                        "  <Loggers>\n" +
                        "    <Logger/>\n" +
                        "  </Loggers>\n" +
                        "</Configuration>", out);
    }

    @Test
    public void testInsertIndentedTabsWithRoot() throws Exception {
        String xml = "<Configu
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 81. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:40.234Z
- latency: 2.999 s

```json
{
  "test": "org.apache.karaf.log.core.internal.SetLogLevelTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1526,
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

Test class `org.apache.karaf.log.core.internal.SetLogLevelTest` (source, may be truncated):
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
package org.apache.karaf.log.core.internal;

import java.util.Hashtable;

import junit.framework.TestCase;

import org.apache.karaf.log.core.LogMBean;
import org.apache.karaf.log.core.LogService;
import org.easymock.EasyMock;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

/**
 * Test cases for {@link org.apache.karaf.log.command.SetLogLevel}
 */
@SuppressWarnings("unchecked")
public class SetLogLevelTest extends TestCase {
    
    private static final String ROOT_LOGGER = "log4j.rootLogger";
    private static final String PACKAGE_LOGGER = "log4j.logger.org.apache.karaf.test";
    
    private LogService logService;
    private LogMBean logMBean;
    @SuppressWarnings("rawtypes")
    private Hashtable properties;

    @Override
    protected void setUp() throws Exception {
        super.setUp();

        properties = new Hashtable<String, String>();
        properties.put(ROOT_LOGGER, "info");

        final Configuration configuration = EasyMock.createMock(Configuration.class);
        EasyMock.expect(configuration.getProcessedProperties(null)).andReturn(properties);
        configuration.update(properties);        
        ConfigurationAdmin configAdmin = EasyMock.createMock(ConfigurationAdmin.class);
        EasyMock.expect(configAdmin.getConfiguration(LogServiceImpl.CONFIGURATION_PID, null)).andReturn(configuration);
        logService = new LogServiceImpl(configAdmin, 100);
        logMBean = new LogMBeanImpl(logService);
        EasyMock.replay(configAdmin);
        EasyMock.replay(configuration);
    }
    
    @Override
    protected void tearDown() throws Exception {
        super.tearDown();
    }
    
    public void testInvalidLogLevel() throws Exception {
        try {
            logMBean.setLevel("INVALID");
            fail("Exception expected");
        } catch(IllegalArgumentException e) {
            // Expected
        }
    }
    
    public void testSetLogLevel() throws Exception {
        logMBean.setLevel("org.apache.karaf.test", "INFO");
        assertEquals("INFO", properties.get(PACKAGE_LOGGER));
    }
    
    public void testSetRootLogLevel() throws Exception {
        logMBean.setLevel(
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.log.core.internal.SetLogLevelTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.log.core.internal.SetLogLevelTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 82. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:40.241Z
- latency: 2.578 s

```json
{
  "test": "org.apache.karaf.main.MainLockingTest",
  "attempt": 0,
  "cached": true,
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

## 83. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:43.200Z
- latency: 2.952 s

```json
{
  "test": "org.apache.karaf.main.MainStartTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1503,
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

Test class `org.apache.karaf.main.MainStartTest` (source, may be truncated):
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

import java.io.File;

import org.junit.After;
import org.junit.Assert;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.launch.Framework;

public class MainStartTest {

    private Main main;

    @After
    public void tearDown() throws Exception {
        if(main != null){
            main.destroy();
        }

		System.clearProperty("karaf.home");
		System.clearProperty("karaf.data");
		System.clearProperty("karaf.log");
    }

    @Test
    public void testAutoStart() throws Exception {
        File basedir = new File(getClass().getClassLoader().getResource("foo").getPath()).getParentFile();
        File home = new File(basedir, "test-karaf-home");
        // generate an unique folder name to avoid conflict with folder created by other unit tests (KARAF-2558)
        File data = new File(home, "data" + System.currentTimeMillis());
		File log = new File(home, "log" + System.currentTimeMillis());

		String[] args = new String[0];
		System.setProperty("karaf.home", home.toString());
		System.setProperty("karaf.data", data.toString());
		System.setProperty("karaf.log", log.toString());

		main = new Main(args);
		main.launch();
		Framework framework = main.getFramework();
		Bundle[] bundles = framework.getBundleContext().getBundles();
		Assert.assertEquals(3, bundles.length);
		
		// Give the framework some time to start the bundles
		Thread.sleep(1000);

		Bundle bundle1 = framework.getBundleContext().getBundle("mvn:org.apache.aries.blueprint/org.apache.aries.blueprint.api/1.0.0");
		Assert.assertEquals(Bundle.ACTIVE, bundle1.getState());

		Bundle bundle2 = framework.getBundleContext().getBundle("pax-url-mvn.jar");
		Assert.assertEquals(Bundle.ACTIVE, bundle2.getState());
	}

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.MainStartTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.MainStartTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 0.8
}
```

## 84. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:46.290Z
- latency: 3.082 s

```json
{
  "test": "org.apache.karaf.main.MainTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1552,
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

Test class `org.apache.karaf.main.MainTest` (source, may be truncated):
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

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;

import static java.util.Arrays.asList;
import static org.apache.karaf.main.ConfigProperties.PROP_KARAF_BASE;
import static org.apache.karaf.main.ConfigProperties.PROP_KARAF_HOME;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

public class MainTest {
    @Rule
    public final TemporaryFolder temporaryFolder = new TemporaryFolder();

    /**
     * Ensures "clean" arg is supported by karaf main.
     *
     * Impl note: since it is the first part of the main we just call launch but skip the execution thanks to ConfigProperties hack.
     */
    @Test
    public void ensureDataCanBeDelete() throws Exception {
        final Path data = temporaryFolder.getRoot().toPath().resolve("data");
        final Path child = data.resolve("child1").resolve("child2");
        Files.createDirectories(child);
        final Path foo = child.resolve("foo.txt");
        Files.write(foo, new byte[0]);

        // here foo exists
        assertTrue(Files.exists(foo));

        final Main main = new Main(new String[]{"clean"});
        assertTrue(Files.exists(foo));

        final Path base = new File(getClass().getClassLoader().getResource("foo").getPath()).toPath().getParent().resolve("test-karaf-home");
        final Collection<String> props = asList(PROP_KARAF_HOME, PROP_KARAF_BASE);
        System.setProperty("org.osgi.framework.startlevel.beginning", "0");
        System.setProperty("karaf.framework", "test");
        System.setProperty("karaf.framework.test", "test");
        System.setProperty("karaf.data", data.toString());
        props.forEach(k -> System.setProperty(k, base.normalize().toAbsolutePath().toString()));
        main.setConfig(new ConfigProperties() { // just to test clean phase, not the rest
            @Override
            public void performInit() throws Exception {
                throw new EagerExit();
            }
        });
        try {
          
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.MainTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.MainTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 0.8
}
```

## 85. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:49.368Z
- latency: 3.071 s

```json
{
  "test": "org.apache.karaf.main.lock.DefaultJDBCLockTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1520,
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

Test class `org.apache.karaf.main.lock.DefaultJDBCLockTest` (source, may be truncated):
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
import java.sql.SQLException;
import java.util.logging.Level;

import org.apache.felix.utils.properties.Properties;

import org.junit.Before;
import org.junit.Test;


public class DefaultJDBCLockTest extends BaseJDBCLockTest {
    
    @Before
    @Override
    public void setUp() throws Exception {
        password = "root";
        driver = "org.apache.derby.jdbc.ClientDriver";
        url = "jdbc:derby://127.0.0.1:1527/test";
        
        super.setUp();
    }
    
    DefaultJDBCLock createLock(Properties props) {
        return new DefaultJDBCLock(props) {
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + ";create=true", url);
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
    public void createConnectionShouldConcatinateOptionsCorrect() throws SQLException {
        props.put("karaf.lock.jdbc.url", this.url + ";dataEncryption=false");
        
        lock = new DefaultJDBCLock(props) {
            @Override
            boolean schemaExists() {
                return true;
            }

            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + ";create=true", url);
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
{"test": "org.apache.karaf.main.lock.DefaultJDBCLockTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.lock.DefaultJDBCLockTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 86. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:52.531Z
- latency: 3.152 s

```json
{
  "test": "org.apache.karaf.main.lock.DerbyJDBCLockTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1517,
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

Test class `org.apache.karaf.main.lock.DerbyJDBCLockTest` (source, may be truncated):
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


public class DerbyJDBCLockTest extends BaseJDBCLockTest {
    
    @Before
    @Override
    public void setUp() throws Exception {
        password = "root";
        driver = "org.apache.derby.jdbc.ClientDriver";
        url = "jdbc:derby://127.0.0.1:1527/test";
        
        super.setUp();
    }
    
    DerbyJDBCLock createLock(Properties props) {
        return new DerbyJDBCLock(props) {
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + ";create=true", url);
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
        props.put("karaf.lock.jdbc.url", this.url + ";dataEncryption=false");
        
        lock = new DerbyJDBCLock(props) {
            @Override
            boolean schemaExists() {
                return true;
            }
            
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url + ";create=true", url);
                assertEquals(this.user, username);
                assertEquals(this.password, password);
                return connection;
            }

            @Override
            long getCurrentTimeMillis() {
                return 1;
            }
        };
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.lock.DerbyJDBCLockTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.lock.DerbyJDBCLockTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 87. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:52.539Z
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

## 88. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:55.674Z
- latency: 3.127 s

```json
{
  "test": "org.apache.karaf.main.lock.OracleJDBCLockTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1555,
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

Test class `org.apache.karaf.main.lock.OracleJDBCLockTest` (source, may be truncated):
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

import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.reset;
import static org.easymock.EasyMock.verify;
import static org.junit.Assert.*;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.logging.Level;

import org.apache.felix.utils.properties.Properties;

import org.junit.Before;
import org.junit.Test;


public class OracleJDBCLockTest extends BaseJDBCLockTest {

    @Before
    @Override
    public void setUp() throws Exception {
        password = "root";
        driver = "oracle.jdbc.driver.OracleDriver";
        url = "jdbc:oracle:thin:@172.16.16.132:1521:XE";
        momentDatatype = "NUMBER(20)";

        super.setUp();
    }

    OracleJDBCLock createLock(Properties props) {
        return new OracleJDBCLock(props) {
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url, url);
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
    @Override
    public void lockShouldReturnTrueItTheTableIsNotLocked() throws Exception {
        initShouldNotCreateTheSchemaIfItAlreadyExists();
        reset(connection, metaData, statement, preparedStatement, resultSet);

        expect(connection.isClosed()).andReturn(false);
        expect(connection.prepareStatement("SELECT * FROM " + tableName + " FOR UPDATE")).andReturn(preparedStatement);
        preparedStatement.setQueryTimeout(10);
        expect(preparedStatement.execute()).andReturn(true);
        preparedStatement.close();
        expect(connection.isClosed()).andReturn(false);
        expect(connection.prepareStatement("SELECT COUNT(*) FROM " + t
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.lock.OracleJDBCLockTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.lock.OracleJDBCLockTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 89. semantic_analyzer · llm_call

- time: 2026-11-07T18:03:58.809Z
- latency: 3.125 s

```json
{
  "test": "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1520,
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

Test class `org.apache.karaf.main.lock.PostgreSQLJDBCLockTest` (source, may be truncated):
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

import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.logging.Level;

import org.apache.felix.utils.properties.Properties;

import static org.easymock.EasyMock.*;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;


public class PostgreSQLJDBCLockTest extends BaseJDBCLockTest {

    @Before
    @Override
    public void setUp() throws Exception {
        password = "secret";
        driver = "org.postgresql.Driver";
        url = "jdbc:postgresql://127.0.0.1:5432/test";

        super.setUp();
    }

    DefaultJDBCLock createLock(Properties props) {
        return new PostgreSQLJDBCLock(props) {
            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url, url);
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
        props.put("karaf.lock.jdbc.url", this.url + ";dataEncryption=false");

        lock = new PostgreSQLJDBCLock(props) {
            @Override
            boolean schemaExists() {
                return true;
            }

            @Override
            Connection doCreateConnection(String driver, String url, String username, String password) {
                assertEquals(this.driver, driver);
                assertEquals(this.url, url);
                assertEquals(this.user, username);
                assertEquals(this.password, password);
                return connection;
            }

            @Override
            long getCurrentTimeMillis() {
            
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 90. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:01.962Z
- latency: 3.144 s

```json
{
  "test": "org.apache.karaf.management.KarafMBeanServerGuardTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1564,
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

Test class `org.apache.karaf.management.KarafMBeanServerGuardTest` (source, may be truncated):
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
package org.apache.karaf.management;

import junit.framework.TestCase;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.util.jaas.JaasHelper;
import org.easymock.EasyMock;
import org.osgi.framework.Constants;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

import javax.management.*;
import javax.security.auth.Subject;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.login.LoginException;
import javax.security.auth.spi.LoginModule;
import java.io.IOException;
import java.lang.reflect.Method;
import java.security.Principal;
import java.security.PrivilegedAction;
import java.util.*;

public class KarafMBeanServerGuardTest extends TestCase {

    public void testRequiredRolesMethodNameOnly() throws Exception {
        Dictionary<String, Object> configuration = new Hashtable<>();
        configuration.put("doit", "master");
        configuration.put("fryit", "editor,viewer");
        ConfigurationAdmin ca = getMockConfigAdmin(configuration);

        KarafMBeanServerGuard guard = new KarafMBeanServerGuard();
        guard.setConfigAdmin(ca);

        ObjectName on = ObjectName.getInstance("foo.bar:type=Test");
        assertEquals(Collections.singletonList("master"),
                guard.getRequiredRoles(on, "doit", new Object[]{}, new String[]{}));
        assertEquals(Arrays.asList("editor", "viewer"),
                guard.getRequiredRoles(on, "fryit", new Object[]{"blah"}, new String[]{"java.lang.String"}));
    }

    @SuppressWarnings("unchecked")
    public void testRequiredRolesMethodNameEmpty() throws Exception {
        Dictionary<String, Object> conf1 = new Hashtable<>();
        conf1.put("doit", "");
        conf1.put("fryit", "editor, viewer");
        conf1.put(Constants.SERVICE_PID, "jmx.acl.foo.bar.Test");
        Dictionary<String, Object> conf2 = new Hashtable<>();
        conf2.put("doit", "editor");
        conf2.put(Constants.SERVICE_PID, "jmx.acl.foo.bar");
        ConfigurationAdmin ca = getMockConfigAdmin2(conf1, conf2);

        KarafMBeanServerGuard guard = new KarafMBeanServerGuard
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.management.KarafMBeanServerGuardTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.management.KarafMBeanServerGuardTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 91. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:05.193Z
- latency: 3.223 s

```json
{
  "test": "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1603,
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

Test class `org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase` (source, may be truncated):
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
package org.apache.karaf.management.internal;

import junit.framework.TestCase;
import org.apache.karaf.management.KarafMBeanServerGuard;
import org.easymock.EasyMock;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;
import java.io.IOException;
import java.util.*;

public class JMXSecurityMBeanImplTestCase extends TestCase {

    public void testMBeanServerAccessors() throws Exception {
        MBeanServer mbs = EasyMock.createMock(MBeanServer.class);
        EasyMock.replay(mbs);

        JMXSecurityMBeanImpl mb = new JMXSecurityMBeanImpl();
        mb.setMBeanServer(mbs);
        assertSame(mbs, mb.getMBeanServer());
    }

    public void testCanInvokeMBean() throws Exception {
        MBeanServer mbs = EasyMock.createMock(MBeanServer.class);
        EasyMock.replay(mbs);

        String objectName = "foo.bar.testing:type=SomeMBean";
        KarafMBeanServerGuard testGuard = EasyMock.createMock(KarafMBeanServerGuard.class);
        EasyMock.expect(testGuard.canInvoke(null, mbs, new ObjectName(objectName))).andReturn(true);
        EasyMock.replay(testGuard);

        JMXSecurityMBeanImpl mb = new JMXSecurityMBeanImpl();
        mb.setMBeanServer(mbs);
        mb.setGuard(testGuard);
        assertTrue(mb.canInvoke(objectName));
    }

    public void testCanInvokeMBean2() throws Exception {
        MBeanServer mbs = EasyMock.createMock(MBeanServer.class);
        EasyMock.replay(mbs);

        String objectName = "foo.bar.testing:type=SomeMBean";
        KarafMBeanServerGuard testGuard = EasyMock.createMock(KarafMBeanServerGuard.class);
        EasyMock.expect(testGuard.canInvoke(null, mbs, new ObjectName(objectName))).andReturn(false);
        EasyMock.replay(testGuard);

        JMXSecurityMBeanImpl mb = new JMXSecurityMBeanImpl();
        mb.setMBeanServer(mbs);
        mb.setGuard(testGuard);
        assertFalse(mb.canInvoke(objectName));
    }

    public void testCanInvokeMBeanThrowsException() throws Exception {
        try {
            MBean
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
  "relevance": 0,
  "reason": "The test class does not interact with the SSH client or related classes that were modified in the code change.",
  "confidence": 1
}
```

## 92. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:08.218Z
- latency: 3.017 s

```json
{
  "test": "org.apache.karaf.maven.SettingsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1590,
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

Test class `org.apache.karaf.maven.SettingsTest` (source, may be truncated):
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
package org.apache.karaf.maven;

import java.io.IOException;

import org.apache.maven.settings.Server;
import org.apache.maven.settings.Settings;
import org.apache.maven.settings.io.DefaultSettingsWriter;
import org.junit.Test;
import org.sonatype.plexus.components.cipher.DefaultPlexusCipher;
import org.sonatype.plexus.components.cipher.PBECipher;

public class SettingsTest {

    @Test
    public void readAndWriteSettings() throws IOException {
        Settings settings = new Settings();
        Server s = new Server();
        s.setId("id");
        s.setUsername("admin");
        s.setPassword("admin");
        settings.getServers().add(s);

        new DefaultSettingsWriter().write(System.out, null, settings);
    }

    @Test
    public void encryptMavenPassword() throws Exception {
        // non-master password ('mvn -ep admin')
        DefaultPlexusCipher plexusCipher = new DefaultPlexusCipher();
        System.out.println(plexusCipher.encrypt("admin", "admin"));

        // master password (`mvn -emp admin`)
        PBECipher cipher = new PBECipher();
        System.out.println(cipher.encrypt64("admin","settings.security"));
    }

    @Test
    public void decryptMavenPassword() throws Exception {
        // non-master password ('mvn -ep admin')
        DefaultPlexusCipher plexusCipher = new DefaultPlexusCipher();
        System.out.println(plexusCipher.decrypt("{EhjazkVpkMoHjAgaUKX+UxeXn9lsJGHst2uFKmhNZ8U=}", "admin"));
        System.out.println(plexusCipher.decrypt("{oWE12FbirwYHNit93TAMA+OC/GJge2r9FuzI8kOuHlA=}", "settings.security"));

        // master password (`mvn -emp admin`)
        PBECipher cipher = new PBECipher();
        System.out.println(cipher.decrypt64("EhjazkVpkMoHjAgaUKX+UxeXn9lsJGHst2uFKmhNZ8U=","admin"));
        System.out.println(cipher.decrypt64("oWE12FbirwYHNit93TAMA+OC/GJge2r9FuzI8kOuHlA=","settings.security"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.maven.SettingsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.maven.SettingsTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 93. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:11.211Z
- latency: 2.985 s

```json
{
  "test": "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1449,
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

Test class `org.apache.karaf.maven.command.MavenConfigurationSupportTest` (source, may be truncated):
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
package org.apache.karaf.maven.command;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Dictionary;
import java.util.regex.Pattern;

import org.junit.Test;
import shaded.org.apache.commons.io.FileUtils;

import static org.junit.Assert.assertTrue;

public class MavenConfigurationSupportTest {

    @Test
    public void sequenceFiles() throws IOException {
        File dataDir = new File("target/data");
        FileUtils.deleteDirectory(dataDir);
        dataDir.mkdirs();

        MavenConfigurationSupport support = new MavenConfigurationSupport() {
            @Override
            protected void doAction(String prefix, Dictionary<String, Object> config) throws Exception { }
        };

        File newFile = support.nextSequenceFile(dataDir, Pattern.compile("file-(\\d+).txt"), "file-%04d.txt");
        assertTrue(Pattern.compile("^file-\\d+\\.txt$").matcher(newFile.getName()).matches());

        try (FileWriter fw = new FileWriter(new File(dataDir, "file-abcd.txt"))) {
            fw.write("~");
        }
        newFile = support.nextSequenceFile(dataDir, Pattern.compile("file-(\\d+).txt"), "file-%04d.txt");
        assertTrue(Pattern.compile("^file-\\d+\\.txt$").matcher(newFile.getName()).matches());

        try (FileWriter fw = new FileWriter(new File(dataDir, "file-0004.txt"))) {
            fw.write("~");
        }
        newFile = support.nextSequenceFile(dataDir, Pattern.compile("file-(\\d+).txt"), "file-%04d.txt");
        assertTrue(Pattern.compile("^file-\\d+\\.txt$").matcher(newFile.getName()).matches());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.maven.command.MavenConfigurationSupportTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 94. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:14.163Z
- latency: 2.944 s

```json
{
  "test": "org.apache.karaf.maven.core.MavenRepositoryURLTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1655,
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

Test class `org.apache.karaf.maven.core.MavenRepositoryURLTest` (source, may be truncated):
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
package org.apache.karaf.maven.core;

import java.net.MalformedURLException;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class MavenRepositoryURLTest {

    @Test
    public void uris() throws MalformedURLException {
        String uri1, uri2;
        MavenRepositoryURL mavenURI;

        uri1 = "http://localhost/@id=id1@snapshots@update=interval:42@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@snapshots@update=interval:42";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));

        uri1 = "http://localhost/@id=id1@snapshots@checksum=fail@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@snapshots@checksum=fail";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));

        uri1 = "http://localhost/@id=id1@snapshots@noreleases@update=interval:42@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@noreleases@snapshots@snapshotsUpdate=interval:42";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));

        uri1 = "http://localhost/@id=id1@update=interval:42@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@releasesUpdate=interval:42";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));

        uri1 = "http://localhost/@id=id1@snapshots@noreleases@checksum=fail@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@noreleases@snapshots@snapshotsChecksum=fail";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));

        uri1 = "http://localhost/@id=id1@checksum=fail@_from=" + MavenRepositoryURL.FROM.SETTINGS;
        uri2 = "http://localhost/@id=id1@releasesChecksum=fail";
        mavenURI = new MavenRepositoryURL(uri1);
        assertThat(mavenURI.asRepositorySpec(), equalTo(uri2));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.maven.core.MavenRepositoryURLTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.maven.core.MavenRepositoryURLTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change in the provided diff.",
  "confidence": 1
}
```

## 95. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:14.171Z
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

## 96. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:16.928Z
- latency: 2.749 s

```json
{
  "test": "org.apache.karaf.packages.core.internal.ImportDetailsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1221,
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

Test class `org.apache.karaf.packages.core.internal.ImportDetailsTest` (source, may be truncated):
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
package org.apache.karaf.packages.core.internal;

import org.junit.Assert;
import org.junit.Test;

public class ImportDetailsTest {

    @Test
    public void testGetPackageName() {
        String filter = "(&(osgi.wiring.package=org.mypackage)(version>=1.9.0)(!(version>=2.0.0)))";
        ImportDetails details = new ImportDetails(filter);
        Assert.assertEquals("org.mypackage", details.name);
        Assert.assertEquals("1.9.0", details.minVersion);
        Assert.assertEquals("2.0.0", details.maxVersion);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.packages.core.internal.ImportDetailsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.packages.core.internal.ImportDetailsTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code related to SSHD or Karaf client configurations.",
  "confidence": 1
}
```

## 97. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:20.087Z
- latency: 3.150 s

```json
{
  "test": "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1610,
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

Test class `org.apache.karaf.packages.core.internal.filter.FilterParserTest` (source, may be truncated):
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
package org.apache.karaf.packages.core.internal.filter;


import org.apache.karaf.packages.core.internal.filter.AndExpression;
import org.apache.karaf.packages.core.internal.filter.Expression;
import org.apache.karaf.packages.core.internal.filter.FilterParser;
import org.apache.karaf.packages.core.internal.filter.NotExpression;
import org.apache.karaf.packages.core.internal.filter.SimpleItem;
import org.apache.karaf.packages.core.internal.filter.SimpleItem.FilterType;
import org.junit.Assert;
import org.junit.Test;

public class FilterParserTest {
    @Test
    public void testSimpleItem() {
        Expression expr = new FilterParser().parse(" (a= b)");
        SimpleItem item = (SimpleItem) expr;
        checkItem(item, "a", FilterType.equal, "b");
    }

    private void checkItem(Expression expr, String expectedAttr, FilterType expectedFilterType, String expectedValue) {
        if (!(expr instanceof SimpleItem)) {
            Assert.fail("SimpleItem expected");
        }
        SimpleItem item = (SimpleItem)expr;
        Assert.assertEquals(expectedAttr, item.attr);
        Assert.assertEquals(expectedFilterType, item.filterType);
        Assert.assertEquals(expectedValue, item.value);
    }
    
    @Test
    public void testNotSimpleItem() {
        NotExpression not = (NotExpression) new FilterParser().parse("(!(a=b))");
        checkItem(not.expression, "a", FilterType.equal, "b");
    }
    
    @Test
    public void testPackageImport() {
        AndExpression expr = (AndExpression) new FilterParser().parse("(&(osgi.wiring.package=org.mypackage)(version>=1.9.0)(!(version>=2.0.0)))");
        Assert.assertEquals(3, expr.expressions.length);
        checkItem(expr.expressions[0], "osgi.wiring.package", FilterType.equal, "org.mypackage");
        checkItem(expr.expressions[1], "version", FilterType.gt, "1.9.0");
        NotExpression notVersion = (NotExpression)expr.expressions[2];
        checkItem(notVersion.expression, "version", FilterType.gt, "2.0.0");
    }
    
    @Test
    public void testPackageImportNoVersions() {
        Expression expr = new FilterParser().parse("(osgi.wiring.package=org.mypackage)");
        checkItem(expr, "osgi.wiring.p
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.packages.core.internal.filter.FilterParserTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 98. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:23.189Z
- latency: 3.095 s

```json
{
  "test": "org.apache.karaf.profile.assembly.BuilderTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1549,
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

Test class `org.apache.karaf.profile.assembly.BuilderTest` (source, may be truncated):
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
package org.apache.karaf.profile.assembly;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

import org.junit.Test;
import org.osgi.framework.Constants;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class BuilderTest {

    @Test
    public void testCyclicRepos() throws Exception {
        Path workDir = Paths.get("target/distrib");
        recursiveDelete(workDir);

        // Create dummy etc/config.properties file
        Path config = workDir.resolve("etc/config.properties");
        Files.createDirectories(config.getParent());
        try (BufferedWriter w = Files.newBufferedWriter(config)) {
            w.write(Constants.FRAMEWORK_SYSTEMPACKAGES + "= org.osgi.dto");
            w.newLine();
            w.write(Constants.FRAMEWORK_SYSTEMCAPABILITIES + "= ");
            w.newLine();
        }

        Path mvnRepo = Paths.get("target/test-classes/repo");
        Builder builder = Builder.newInstance()
                .repositories(Builder.Stage.Startup, true, "mvn:foo/baz/1.0/xml/features")
                .homeDirectory(workDir)
                .localRepository(mvnRepo.toString());
        try {
            builder.generateAssembly();
        } catch (Exception e) {
            e.printStackTrace();
            throw e;
        }
    }

    @Test
    public void testPidsToExtract() {
        String pidsToExtract = "\n" +
                "                        !jmx.acl.*,\n" +
                "                        !org.apache.karaf.command.acl.*,\n" +
                "                        *\n" +
                "                    ";
        List<String> p2e = Arrays.asList(pidsToExtract.split(","));
        Builder builder = Builder.newInstance().pidsToExtract(p2e);
        assertThat(builder.getPidsToExtract().get(0), equalTo("!jmx.acl.*"));
        assertThat(builder.getPidsToExtract().get(1), equalTo("!org.apache.karaf.command.acl.*"));
        assertThat(builder.getPidsToExtract().get(2), equalTo("*")
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.profile.assembly.BuilderTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.profile.assembly.BuilderTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 99. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:26.045Z
- latency: 2.849 s

```json
{
  "test": "org.apache.karaf.profile.impl.ProfilesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1584,
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

Test class `org.apache.karaf.profile.impl.ProfilesTest` (source, may be truncated):
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
package org.apache.karaf.profile.impl;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

import org.apache.karaf.profile.Profile;
import org.apache.karaf.profile.ProfileBuilder;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.nullValue;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class ProfilesTest {

    public static Logger LOG = LoggerFactory.getLogger(ProfilesTest.class);

    @Test
    public void testProfilesApi() throws IOException {
        ProfileBuilder builder = ProfileBuilder.Factory.create("my-simple-profile");
        builder.addParents(Collections.emptyList());
        builder.addAttribute("attr1", "val1");
        builder.addBundle("mvn:commons-everything/commons-everything/42");
        builder.addBlacklistedBundle("mvn:commons-banned/commons-banned/[42,52)");
        builder.addConfiguration("my.pid", "a1", "v1${profile:my.pid2/a2}");
        builder.addConfiguration("my.pid", "a2", "v1${profile:my.pid2/a3}");
        builder.addFeature("feature1");
        builder.addBlacklistedFeature("f34tu4e");
        builder.addFileConfiguration("my.pid2.txt", "hello!".getBytes(StandardCharsets.UTF_8));
        builder.addFileConfiguration("my.pid2.cfg", "a2=v2".getBytes(StandardCharsets.UTF_8));
        builder.addRepository("mvn:my/repository/1/xml/features");
        builder.addBlacklistedRepository("mvn:my/repository/[0,1)/xml/features");
        builder.setOptionals(Arrays.asList("mvn:g/a/1", "mvn:g/a/2"));
        builder.setOverrides(Arrays.asList("mvn:g/a/4", "mvn:g/a/3"));
        Profile profile = builder.getProfile();
        LOG.info("Profile: {}", profile.toString());
        LOG.info("Config: {}", profile.getConfig());
        LOG.info("Libraries: {}", profile.getLibraries());
        LOG.info("System: {}", prof
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.profile.impl.ProfilesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.profile.impl.ProfilesTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 100. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:28.610Z
- latency: 2.558 s

```json
{
  "test": "org.apache.karaf.service.command.ListServiceNamesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1179,
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

Test class `org.apache.karaf.service.command.ListServiceNamesTest` (source, may be truncated):
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
package org.apache.karaf.service.command;
import org.junit.Test;

public class ListServiceNamesTest {

    public ListServiceNamesTest() {
        
    }
    
    @Test
    public void listAll() throws Exception {
        ListServices listServices = new ListServices();
        listServices.setBundleContext(new TestBundleFactory().createBundleContext());
        listServices.onlyNames = true;
        listServices.execute();
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.command.ListServiceNamesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.command.ListServiceNamesTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 101. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:31.029Z
- latency: 2.410 s

```json
{
  "test": "org.apache.karaf.service.command.ListServicesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1168,
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

Test class `org.apache.karaf.service.command.ListServicesTest` (source, may be truncated):
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
package org.apache.karaf.service.command;

import org.junit.Test;

public class ListServicesTest {

    public ListServicesTest() {
        
    }
    
    @Test
    public void listAll() throws Exception {
        ListServices listServices = new ListServices();
        listServices.setBundleContext(new TestBundleFactory().createBundleContext());
        listServices.execute();
    }
    

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.command.ListServicesTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.command.ListServicesTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 102. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:33.493Z
- latency: 2.453 s

```json
{
  "test": "org.apache.karaf.service.command.ObjectClassMatcherTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1288,
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

Test class `org.apache.karaf.service.command.ObjectClassMatcherTest` (source, may be truncated):
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
package org.apache.karaf.service.command;

import org.junit.Assert;
import org.junit.Test;

public class ObjectClassMatcherTest {

    @Test
    public void testGetShortName() {
        Assert.assertEquals("TestClass", ObjectClassMatcher.getShortName("org.apache.TestClass"));
        Assert.assertEquals("", ObjectClassMatcher.getShortName("test."));
        Assert.assertEquals("TestClass", ObjectClassMatcher.getShortName("TestClass"));
    }

    @Test
    public void testMatchesName() {
        Assert.assertTrue(ObjectClassMatcher.matchesName("org.apache.TestClass", "TestClass"));
        Assert.assertTrue(ObjectClassMatcher.matchesName("TestClass", "TestClass"));
    }

    @Test
    public void testMatchesAtLeastOneName() {
        Assert.assertTrue(ObjectClassMatcher.matchesAtLeastOneName(new String[]{"other", "org.apache.TestClass"}, "TestClass"));
        Assert.assertFalse(ObjectClassMatcher.matchesAtLeastOneName(new String[]{"TestClass2"}, "TestClass"));
    }

    
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.command.ObjectClassMatcherTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.command.ObjectClassMatcherTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code in the provided diff.",
  "confidence": 1
}
```

## 103. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:36.502Z
- latency: 3.001 s

```json
{
  "test": "org.apache.karaf.service.guard.impl.ActivatorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1518,
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

Test class `org.apache.karaf.service.guard.impl.ActivatorTest` (source, may be truncated):
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
package org.apache.karaf.service.guard.impl;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import org.easymock.EasyMock;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.hooks.service.EventListenerHook;
import org.osgi.framework.hooks.service.FindHook;

import java.util.Dictionary;
import java.util.Properties;

public class ActivatorTest {

    @SuppressWarnings("unchecked")
    @Test
    public void testStartActivator() throws Exception {
        // keep the old properties. Note that the Properties 'copy constructor' new Properties(props)
        // doesn't actually copy, hence the awkward setup here...
        Properties oldProps = new Properties();
        oldProps.putAll(System.getProperties());

        try {
            System.setProperty(GuardProxyCatalog.KARAF_SECURED_SERVICES_SYSPROP, "(foo=bar)");
            Bundle b = EasyMock.createMock(Bundle.class);
            EasyMock.expect(b.getBundleId()).andReturn(768L).anyTimes();
            EasyMock.replay(b);

            BundleContext bc = EasyMock.createNiceMock(BundleContext.class);
            EasyMock.expect(bc.getBundle()).andReturn(b).anyTimes();
            EasyMock.expect(bc.createFilter(EasyMock.anyObject(String.class))).andAnswer(
                    () -> FrameworkUtil.createFilter((String) EasyMock.getCurrentArguments()[0])).anyTimes();

            EasyMock.expect(bc.registerService(
                    EasyMock.eq(EventListenerHook.class), EasyMock.isA(EventListenerHook.class), EasyMock.isNull(Dictionary.class)))
                    .andReturn(null);
            EasyMock.expect(bc.registerService(
                    EasyMock.eq(FindHook.class), EasyMock.isA(FindHook.class), EasyMock.isNull(Dictionary.class)))
                    .andReturn(null);

            EasyMock.replay(bc);

            Activator a = new Activator();
            a.start(bc);

            assertNotNull(a.guardProxyCatalog);
            assertNotNull(a.guardingEventHook);
            assertNotNull(a.guardingFindHook);

            EasyMock.verify(bc);
     
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.guard.impl.ActivatorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.guard.impl.ActivatorTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 104. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:39.423Z
- latency: 2.909 s

```json
{
  "test": "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1522,
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

Test class `org.apache.karaf.service.guard.impl.GuardProxyCatalogTest` (source, may be truncated):
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
package org.apache.karaf.service.guard.impl;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;
import java.security.Principal;
import java.security.PrivilegedAction;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.LinkedHashMap;
import java.util.Map;

import javax.security.auth.Subject;

import org.apache.aries.proxy.ProxyManager;
import org.apache.aries.proxy.impl.AsmProxyManager;
import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.apache.karaf.service.guard.impl.GuardProxyCatalog.CreateProxyRunnable;
import org.apache.karaf.service.guard.impl.GuardProxyCatalog.ServiceRegistrationHolder;
import org.easymock.EasyMock;
import org.easymock.IAnswer;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.Constants;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceFactory;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;
import org.osgi.framework.ServiceRegistration;
import org.osgi.framework.wiring.BundleWiring;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

public class GuardProxyCatalogTest {
    // Some assertions fail when run under a code coverage tool, they are skipped when this is set to true
    private static final boolean runningUnderCoverage = false; // set to false before committing any changes

    @Test
    public void testGuardProxyCatalog() throws Exception {
        Bundle b = EasyMock.createMock(Bundle.class);
        EasyMock.expect(b.getBundleId()).and
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 105. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:42.644Z
- latency: 3.209 s

```json
{
  "test": "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1544,
  "completion_tokens": 70
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

Test class `org.apache.karaf.service.guard.impl.GuardingEventHookTest` (source, may be truncated):
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
package org.apache.karaf.service.guard.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.io.IOException;
import java.util.Collection;
import java.util.Collections;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;

import org.easymock.EasyMock;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.Constants;
import org.osgi.framework.Filter;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;
import org.osgi.framework.hooks.service.ListenerHook.ListenerInfo;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

public class GuardingEventHookTest {
    @SuppressWarnings("unchecked")
    @Test
    public void testEventHookEvents() throws Exception {
        BundleContext frameworkBC = mockBundleContext(0L);

        Dictionary<String, Object> config = new Hashtable<>();
        config.put("service.guard", "(service.id=*)");
        BundleContext hookBC = mockConfigAdminBundleContext(frameworkBC, config);
        GuardProxyCatalog gpc = new GuardProxyCatalog(hookBC);

        Filter serviceFilter = FrameworkUtil.createFilter("(foo=bar)");
        GuardingEventHook geh = new GuardingEventHook(hookBC, gpc, serviceFilter);

        Dictionary<String, Object> props = new Hashtable<>();
        props.put(Constants.SERVICE_ID, 13L);
        ServiceReference<?> sref = mockServiceReference(props);

        BundleContext client1BC = mockBundleContext(123L);
        Map<BundleContext, Collection<ListenerInfo>> listeners = new HashMap<>();
        listeners.put(client1BC, Collections.emptyList());

        // Send the event. It should have no effect because the service doens't match the filter
        assertEquals("Precondition", 0, gpc.proxyMap.size());
        geh.event(new ServiceEvent(ServiceEvent.REGISTERED, sref), listeners);
        assertEquals("No proxy should have been created becau
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.guard.impl.GuardingEventHookTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code related to the `Duration` class or the `CoreModuleProperties` class.",
  "confidence": 1
}
```

## 106. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:45.677Z
- latency: 3.025 s

```json
{
  "test": "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1561,
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

Test class `org.apache.karaf.service.guard.impl.GuardingFindHookTest` (source, may be truncated):
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
package org.apache.karaf.service.guard.impl;

import static org.junit.Assert.assertEquals;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Dictionary;
import java.util.Hashtable;

import org.easymock.EasyMock;
import org.junit.Test;
import org.osgi.framework.Bundle;
import org.osgi.framework.BundleContext;
import org.osgi.framework.Constants;
import org.osgi.framework.Filter;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;
import org.osgi.service.cm.Configuration;
import org.osgi.service.cm.ConfigurationAdmin;

public class GuardingFindHookTest {
    @SuppressWarnings("unchecked")
    @Test
    public void testFindHook() throws Exception {
        Dictionary<String, Object> config = new Hashtable<>();
        config.put("service.guard", "(|(moo=foo)(foo=*))");

        BundleContext hookBC = mockConfigAdminBundleContext(config);
        GuardProxyCatalog gpc = new GuardProxyCatalog(hookBC);

        Filter serviceFilter = FrameworkUtil.createFilter("(foo=*)");
        GuardingFindHook gfh = new GuardingFindHook(hookBC, gpc, serviceFilter);

        BundleContext clientBC = mockBundleContext(31L);

        Dictionary<String, Object> props = new Hashtable<>();
        props.put(Constants.SERVICE_ID, 16L);
        props.put("moo", "foo");
        ServiceReference<?> sref = mockServiceReference(props);

        Collection<ServiceReference<?>> refs = new ArrayList<>();
        refs.add(sref);

        assertEquals("Precondition", 0, gpc.proxyMap.size());
        gfh.find(clientBC, null, null, true, refs);
        assertEquals("The service doesn't match the filter so should have no effect", 0, gpc.proxyMap.size());
        assertEquals("The service doesn't match the filter so should be presented to the client",
                Collections.singletonList(sref), refs);

        long service2ID = 17L;
        Dictionary<String, Object> props2 = new Hashtable<>();
        props2.put(Constants.SERVICE_ID, service2ID);
        props2.put("foo", new Object());
 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.guard.impl.GuardingFindHookTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code related to SSHD or Karaf client configuration.",
  "confidence": 1
}
```

## 107. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:48.606Z
- latency: 2.917 s

```json
{
  "test": "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1572,
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

Test class `org.apache.karaf.service.guard.tools.ACLConfigurationParserTest` (source, may be truncated):
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
package org.apache.karaf.service.guard.tools;

import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.List;

import org.apache.karaf.service.guard.tools.ACLConfigurationParser.Specificity;
import org.junit.Test;

public class ACLConfigurationParserTest {
    @Test
    public void testParseRoles() {
        assertEquals(Collections.singletonList("some_role"),
                ACLConfigurationParser.parseRoles(" some_role   "));
        assertEquals(Arrays.asList("a","b","C"),
                ACLConfigurationParser.parseRoles("a,b,C"));
        assertEquals(Collections.emptyList(),
                ACLConfigurationParser.parseRoles("# test comment"));
    }

    @Test
    public void testGetRolesForInvocation() {
        Dictionary<String, Object> config = new Hashtable<>();
        config.put("foo", "r1, r2");
        config.put("bar(java.lang.String, int)[/aa/,/42/]", "ra");
        config.put("bar(java.lang.String, int)[/bb/,/42/]", "rb");
        config.put("bar(java.lang.String, int)[\"cc\", \"17\"]", "rc");
        config.put("bar(java.lang.String, int)", "rd");
        config.put("bar(java.lang.String)", "re");
        config.put("bar", "rf");
        config.put("ba*", "rg #Wildcard");

        List<String> roles1 = new ArrayList<>();
        assertEquals(Specificity.NAME_MATCH,
                ACLConfigurationParser.getRolesForInvocation("foo", new Object [] {}, new String [] {}, config, roles1));
        assertEquals(Arrays.asList("r1", "r2"), roles1);

        List<String> roles2 = new ArrayList<>();
        assertEquals(Specificity.NAME_MATCH,
                ACLConfigurationParser.getRolesForInvocation("foo", new Object [] {"test"}, new String [] {"java.lang.String"}, config, roles2));
        assertEquals(Arrays.asList("r1", "r2"), roles2);

        List<String> roles3 = new ArrayList<>();
        assertEquals(Specificity.NO_MATCH,
                ACLConfigurationParser.getRolesForInvocation("test", new Object [] {}, new String [] {}, config, roles3));
        assertEquals(0, roles3.size());

        List
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code related to SSH client configuration or properties.",
  "confidence": 1
}
```

## 108. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:51.363Z
- latency: 2.748 s

```json
{
  "test": "org.apache.karaf.shell.commands.impl.InfoTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1317,
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

Test class `org.apache.karaf.shell.commands.impl.InfoTest` (source, may be truncated):
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
package org.apache.karaf.shell.commands.impl;

import junit.framework.TestCase;

import org.apache.karaf.shell.commands.impl.InfoAction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InfoTest extends TestCase {

    private static final transient Logger LOGGER = LoggerFactory.getLogger(TestCase.class);

    public void testUptime() throws Exception {
        InfoAction infoAction = new InfoAction();
        // uptime 30 seconds
        assertEquals("30.000 seconds", infoAction.printDuration(30 * 1000));
        // uptime 2 minutes
        assertEquals("2 minutes", infoAction.printDuration(2 * 60 * 1000));
        // uptime 2 hours
        assertEquals("2 hours", infoAction.printDuration(2 * 3600 * 1000));
        // update 2 days and 2 hours
        assertEquals("2 days 2 hours", infoAction.printDuration(50 * 3600 * 1000));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.commands.impl.InfoTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.commands.impl.InfoTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 109. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:53.881Z
- latency: 2.510 s

```json
{
  "test": "org.apache.karaf.shell.commands.impl.ThreadsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1276,
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

Test class `org.apache.karaf.shell.commands.impl.ThreadsTest` (source, may be truncated):
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
package org.apache.karaf.shell.commands.impl;

import org.junit.Test;

/**
 * These are not real tests as they do no assertions. They simply help to see how the layout will look like.
 */
public class ThreadsTest {
    @Test
    public void testThreadlist() throws Exception {
        ThreadsAction action = new ThreadsAction();
        action.list = true;
        action.execute();
    }
    
    @Test
    public void testThreadInfo() throws Exception {
        ThreadsAction action = new ThreadsAction();
        action.id = 1L;
        action.execute();
    }

    @Test
    public void testThreadTree() throws Exception {
        ThreadsAction action = new ThreadsAction();
        action.tree = true;
        action.execute();
    }

    @Test
    public void testThreadDump() throws Exception {
        ThreadsAction action = new ThreadsAction();
        action.execute();
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.commands.impl.ThreadsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.commands.impl.ThreadsTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 110. semantic_analyzer · llm_call

- time: 2026-11-07T18:04:56.948Z
- latency: 3.058 s

```json
{
  "test": "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1574,
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
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 111. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:00.444Z
- latency: 3.484 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1738,
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

Test class `org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest` (source, may be truncated):
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
package org.apache.karaf.shell.impl.console.commands.help.wikidoc;

import java.io.IOException;
import java.io.StringReader;

import org.easymock.EasyMock;
import org.junit.Test;

public class WikiParserTest {

	private static final String TESTDOC =
		"h1. myTestdoc\n" +
		"\n" +
		"Some text\n" +
		"* enumeration\n" +
		"* enumeration - with additional text\n" +
		" some text [a link] some more text\n" +
		"# a comment in between\n" +
		"h1 is no heading\n" +
		"some **bold** text\n" +
		"and a line for KARAF-6650 h\n";
	
	private static final String HEADINGCASES = 
		"h1.\n" +
		"hf.";

	@Test
	public void parseTestDoc() throws IOException {
		WikiVisitor visitor = EasyMock.createStrictMock(WikiVisitor.class);
		visitor.startPara(0);
		visitor.heading(1, "myTestdoc");
		visitor.endPara();
		visitor.startPara(0);
		visitor.endPara();
		visitor.startPara(0);
		visitor.text("Some text");
		visitor.endPara();
		visitor.startPara(0);
		visitor.enumeration("enumeration");
		visitor.endPara();
		visitor.startPara(0);
		visitor.enumeration("enumeration");
		visitor.text("- wit");
		visitor.text("h additional text");
		visitor.endPara();
		visitor.startPara(1);
		visitor.text("some text ");
		visitor.link("a link", "");
		visitor.text(" some more text");
		visitor.endPara();
		visitor.startPara(0);
		visitor.text("h1 is no heading");
		visitor.endPara();
		visitor.startPara(0);
		visitor.text("some ");
		visitor.bold(true);
		visitor.text("bold");
		visitor.bold(false);
		visitor.text(" text");
		visitor.endPara();
		visitor.startPara(0);
		visitor.text("and a line for KARAF-6650 ");
		visitor.text("h");
		visitor.endPara();

		EasyMock.replay(visitor);
		WikiParser parser = new WikiParser(visitor);
		parser.parse(new StringReader(TESTDOC));
		EasyMock.verify(visitor);
	}
	
	@Test
	public void parseHeadingSpecialCases() throws IOException {
		WikiVisitor visitor = EasyMock.createStrictMock(WikiVisitor.class);
		visitor.startPara(0);
		EasyMock.expectLastCall();
		visitor.heading(1, "");
		visitor.endPara();
		visitor.startPara(0);
		visitor.text("hf.");
		visitor.endPara();
		
		EasyMock.replay(visitor);
		WikiParser parser = new WikiParser(visitor);
		parser.parse(
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 112. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:03.359Z
- latency: 2.908 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1558,
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

Test class `org.apache.karaf.shell.impl.console.parsing.ParsingTest` (source, may be truncated):
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
package org.apache.karaf.shell.impl.console.parsing;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.felix.gogo.runtime.threadio.ThreadIOImpl;
import org.apache.karaf.shell.api.action.Action;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Parsing;
import org.apache.karaf.shell.api.console.CommandLine;
import org.apache.karaf.shell.api.console.Parser;
import org.apache.karaf.shell.api.console.Session;
import org.apache.karaf.shell.impl.action.command.ActionCommand;
import org.apache.karaf.shell.impl.action.command.ManagerImpl;
import org.apache.karaf.shell.impl.console.HeadlessSessionImpl;
import org.apache.karaf.shell.impl.console.SessionFactoryImpl;
import org.apache.karaf.shell.support.parsing.CommandLineImpl;
import org.apache.karaf.shell.support.parsing.DefaultParser;
import org.apache.karaf.shell.support.parsing.GogoParser;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ParsingTest {

    @Test
    public void testDefaultParser() {
        String command = " foo  bar (a +  b) ; another command ";
        String subCmd = " foo  bar (a +  b) ";
        DefaultParser parser = new DefaultParser();
        CommandLine line = parser.parse(null, command, command.length());
        assertEquals(3, line.getArguments().length);
        assertEquals("foo", line.getArguments()[0]);
        assertEquals("bar", line.getArguments()[1]);
        assertEquals("(a +  b)", line.getArguments()[2]);
        assertEquals(subCmd, line.getBuffer());

    }

    @Test
    public void testCommandLineParser() {

        SessionFactoryImpl sessionFactory = new SessionFactoryImpl(new ThreadIOImpl());
        ManagerImpl manager = new ManagerImpl(sessionFactory, sessionFactory);
        sessionFactory.getRegistry().register(new ActionCommand(manager, FooCommand.class));
        sessionFactory.getRegistry().register(new ActionCommand(manager, AnotherCommand.class));
        sessionFactory.getRegistry().register(new CustomParser());
        Session session = new HeadlessSessionI
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.impl.console.parsing.ParsingTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH client configuration or properties.",
  "confidence": 1
}
```

## 113. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:03.366Z
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

## 114. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:03.374Z
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

## 115. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:06.172Z
- latency: 2.791 s

```json
{
  "test": "org.apache.karaf.shell.ssh.KnownHostsManagerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1442,
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

Test class `org.apache.karaf.shell.ssh.KnownHostsManagerTest` (source, may be truncated):
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

import java.io.File;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;

import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

public class KnownHostsManagerTest {

	private static String ALGORITHM;
	private static int KEY_SIZE;

	@BeforeClass
	public static void init() throws IOException {
		// test key algorithm and size as configured...
		ALGORITHM = "RSA";
		KEY_SIZE = 4096;
	}

	private PublicKey createPubKey() throws NoSuchAlgorithmException {
		KeyPairGenerator gen = KeyPairGenerator.getInstance(ALGORITHM);
		gen.initialize(KEY_SIZE);
		KeyPair keyPair = gen.generateKeyPair();
		return keyPair.getPublic();
	}
	
	@Test
	public void testStoreAndRetrieve() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException {
		SocketAddress address = new InetSocketAddress("localhost", 1001);
		File hostsFile = File.createTempFile("hosts", "");
		KnownHostsManager manager = new KnownHostsManager(hostsFile);

		PublicKey foundKey1 = manager.getKnownKey(address, ALGORITHM);
		Assert.assertNull(foundKey1);
		
		PublicKey serverKey = createPubKey();
		manager.storeKeyForHost(address, serverKey);
		PublicKey foundKey2 = manager.getKnownKey(address, ALGORITHM);
		Assert.assertEquals(serverKey, foundKey2);
	}
	
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.ssh.KnownHostsManagerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.ssh.KnownHostsManagerTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 116. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:09.292Z
- latency: 3.112 s

```json
{
  "test": "org.apache.karaf.shell.ssh.ServerKeyVerifierImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1605,
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

Test class `org.apache.karaf.shell.ssh.ServerKeyVerifierImplTest` (source, may be truncated):
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
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;

import org.easymock.EasyMock;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

public class ServerKeyVerifierImplTest {

	private static final InetSocketAddress LOCALHOST = new InetSocketAddress("localhost", 1001);
	private static String ALGORITHM;
	private static int KEY_SIZE;

	@BeforeClass
	public static void init() throws IOException {
		// test key algorithm and size as configured...
		ALGORITHM = "RSA";
		KEY_SIZE = 4096;
	}

	private PublicKey createPubKey() throws NoSuchAlgorithmException {
		KeyPairGenerator gen = KeyPairGenerator.getInstance(ALGORITHM);
		gen.initialize(KEY_SIZE);
		KeyPair keyPair = gen.generateKeyPair();
		return keyPair.getPublic();
	}
	
	@Test
	public void testNewKey() throws NoSuchAlgorithmException, InvalidKeySpecException {
		SocketAddress address = LOCALHOST;
		PublicKey validServerKey = createPubKey();
		
		KnownHostsManager knowHostsManager = EasyMock.createMock(KnownHostsManager.class);
		EasyMock.expect(knowHostsManager.getKnownKey(address, ALGORITHM)).andReturn(null);
		knowHostsManager.storeKeyForHost(address, validServerKey);
		EasyMock.expectLastCall();
		EasyMock.replay(knowHostsManager);

		ServerKeyVerifierImpl verifier = new ServerKeyVerifierImpl(knowHostsManager, true);		
		boolean verified = verifier.verifyServerKey(null, address, validServerKey);
		Assert.assertTrue("Key should be verified as the key is new", verified);
	}
	
	@Test
	public void testKnownAndCorrectKey() throws NoSuchAlgorithmException, InvalidKeySpecException {
		SocketAddress address = LOCALHOST;
		PublicKey validServerKey = createPubKey();
		
		KnownHostsManager knowHostsManager = EasyMock.createMock(KnownHostsManager.class);
		EasyMock.expect(knowHostsManager.getKnownKey(address, ALGORITHM)).andReturn(validServerKey);
		EasyMock.replay(knowHostsManager);

		ServerKeyVerifierImpl veri
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.ssh.ServerKeyVerifierImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.ssh.ServerKeyVerifierImplTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 117. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:12.694Z
- latency: 3.396 s

```json
{
  "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1614,
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
        String ciphers = "aes128-ctr,arcfour128,aes128-cbc,3des-cbc,blowfish-cbc";

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
        String kexAlgorithms = "diffie-hellman-group-exchange-sha256,ecdh-sha2-nistp521,ecdh-sha2-nistp38
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

## 118. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:16.184Z
- latency: 3.481 s

```json
{
  "test": "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1592,
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

Test class `org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest` (source, may be truncated):
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
package org.apache.karaf.shell.ssh.keygenerator;

import static org.junit.Assert.fail;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyPair;
import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.ECPublicKey;
import java.security.interfaces.RSAPrivateCrtKey;
import java.security.interfaces.RSAPublicKey;
import java.util.List;

import org.apache.sshd.common.config.keys.KeyUtils;
import org.apache.sshd.server.keyprovider.SimpleGeneratorHostKeyProvider;
import org.junit.Assert;
import org.junit.Test;

public class OpenSSHGeneratorKeyFileProviderTest {

    @Test
    public void writeSshKey() throws Exception {
        File privateKeyTemp = File.createTempFile(this.getClass().getCanonicalName(), ".priv");
        privateKeyTemp.deleteOnExit();
        File publicKeyTemp = File.createTempFile(this.getClass().getCanonicalName(), ".pub");
        publicKeyTemp.deleteOnExit();

        KeyPair kp = new OpenSSHKeyPairGenerator(KeyUtils.RSA_ALGORITHM, 1024).generate();
        new PemWriter(privateKeyTemp.toPath(), publicKeyTemp.toPath()).writeKeyPair(KeyUtils.RSA_ALGORITHM, kp);

        OpenSSHKeyPairProvider prov =
            new OpenSSHKeyPairProvider(privateKeyTemp.toPath(), publicKeyTemp.toPath(), KeyUtils.RSA_ALGORITHM, 1024, null);
        KeyPair keys = prov.loadKeys(null).iterator().next();
        Assert.assertNotNull(keys);
        Assert.assertTrue("Loaded key is not RSA Key", keys.getPrivate() instanceof RSAPrivateCrtKey);
        Assert.assertTrue("Loaded key is not RSA Key", keys.getPublic() instanceof RSAPublicKey);
    }

    @Test
    public void convertSimpleKey() throws Exception {
        File privateKeyTemp = File.createTempFile(this.getClass().getCanonicalName(), ".priv");
        privateKeyTemp.deleteOnExit();
        File publicKeyTemp = File.createTempFile(this.getClass().getCanonicalName(), ".pub");
        publicKeyTemp.deleteOnExit();

        SimpleGeneratorHostKeyProvider simpleGenerator = new SimpleGeneratorHostKeyProvider(privateKeyTemp.toPath());
        simpleGenerator.setKeySize(2048);
        simpleGenerator.setAlgorithm("DS
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 0.9
}
```

## 119. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:19.175Z
- latency: 2.983 s

```json
{
  "test": "org.apache.karaf.shell.support.ShellUtilTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1701,
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

Test class `org.apache.karaf.shell.support.ShellUtilTest` (source, may be truncated):
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
package org.apache.karaf.shell.support;

import static org.junit.Assert.assertEquals;

import java.util.AbstractList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;

import org.junit.Test;

public class ShellUtilTest {

    @Test
    public void testGetValueStringWithCustomCollection() {
        List<Integer> data = new AbstractList<Integer>() {

            int[] values = new int[15];
            int size = 0;

            @Override
            public boolean add(Integer e) {
                values[size] = e;
                size++;
                return true;
            }

            @Override
            public Integer get(int index) {
                if ( index >= size ) throw new IndexOutOfBoundsException();
                return values[index];
            }

            @Override
            public int size() {
                return size;
            }

            @Override
            public String toString() {
                return "Custom" + super.toString();
            }
        };
        data.add(5);
        assertEquals("[5]", ShellUtil.getValueString(data));
    }

    @Test
    public void testGetValueString() {
        Object data;
        data = "Hello World";
        assertEquals("Hello World", ShellUtil.getValueString(data));

        data = new int[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1, 2, 3, 5, 7, 9]", ShellUtil.getValueString(data));

        data = new short[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1, 2, 3, 5, 7, 9]", ShellUtil.getValueString(data));

        data = new long[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1, 2, 3, 5, 7, 9]", ShellUtil.getValueString(data));

        data = new byte[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1, 2, 3, 5, 7, 9]", ShellUtil.getValueString(data));

        data = new float[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1.0, 2.0, 3.0, 5.0, 7.0, 9.0]",
                ShellUtil.getValueString(data));

        data = new double[] { 1, 2, 3, 5, 7, 9 };
        assertEquals("[1.0, 2.0, 3.0, 5.0, 7.0, 9.0]",
                ShellUtil.getValueString(data));

        data = new boolean[] { true, true, false };
        assertEquals("[t
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.support.ShellUtilTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.support.ShellUtilTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 120. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:22.085Z
- latency: 2.902 s

```json
{
  "test": "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1236,
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

Test class `org.apache.karaf.shell.support.ansi.AnsiSplitterTest` (source, may be truncated):
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
package org.apache.karaf.shell.support.ansi;

import java.io.IOException;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class AnsiSplitterTest {

    @Test
    public void testWindow() throws IOException {
        String text = "\u001B[1mThis is bold.\u001B[22m";
        assertEquals("\u001B[1mis\u001B[0m", AnsiSplitter.substring(text, 5, 7, 4));
        assertEquals(13, AnsiSplitter.length(text, 4));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.support.ansi.AnsiSplitterTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 121. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:25.111Z
- latency: 3.018 s

```json
{
  "test": "org.apache.karaf.shell.support.table.ShellTableTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1569,
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

Test class `org.apache.karaf.shell.support.table.ShellTableTest` (source, may be truncated):
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
package org.apache.karaf.shell.support.table;

import static org.junit.Assert.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.PrintStream;

import org.apache.felix.gogo.runtime.threadio.ThreadIOImpl;
import org.apache.felix.service.threadio.ThreadIO;
import org.apache.karaf.shell.support.ansi.SimpleAnsi;
import org.junit.Test;

public class ShellTableTest {

    @Test
    public void testLongValueFull() {
        ShellTable table = new ShellTable().forceAscii();
        table.separator("|");
        table.column("col1");
        table.column("col2").maxSize(-1);
        table.addRow().addContent("my first column value", "my second column value is quite long");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        table.print(new PrintStream(baos), false);
        assertEquals(String.format("%s%n","my first column value\tmy second column value is quite long"), baos.toString());
    }

    @Test
    public void testLongValueCut() {
        ShellTable table = new ShellTable().forceAscii();
        table.separator("|");
        table.column("col1");
        table.column("col2").maxSize(-1);
        table.addRow().addContent("my first column value", "my second column value is quite long");
        table.size(50);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        table.print(new PrintStream(baos), false);
        assertEquals(String.format("%s%n","my first column value\tmy second column value is q"), baos.toString());
    }

    @Test
    public void testLongValueMultiline() {
        ShellTable table = new ShellTable().forceAscii();
        table.separator("|");
        table.column("col1");
        table.column("col2").maxSize(-1).wrap();
        table.addRow().addContent("my first column value", "my second column value is quite long");
        table.size(50);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        table.print(new PrintStream(baos), false);
        assertEquals(String.format("%1$s\n%2$s%n","my first column value\tmy second column value is",
                "                     \tquite long"), baos.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.support.table.ShellTableTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.support.table.ShellTableTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 122. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:28.228Z
- latency: 3.108 s

```json
{
  "test": "org.apache.karaf.shell.tabletest.ShellTableTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1577,
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

Test class `org.apache.karaf.shell.tabletest.ShellTableTest` (source, may be truncated):
<<<TEST
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.apache.karaf.shell.tabletest;

import java.io.PrintStream;
import java.io.StringWriter;

import junit.framework.Assert;

import org.apache.commons.io.output.WriterOutputStream;
import org.apache.karaf.shell.table.Col;
import org.apache.karaf.shell.table.Row;
import org.apache.karaf.shell.table.ShellTable;
import org.junit.Test;

public class ShellTableTest {

    @Test
    public void testTable() {
        ShellTable table = new ShellTable();
        table.column(new Col("id").alignRight().maxSize(5));
        table.column(new Col("Name").maxSize(20));
        table.column(new Col("Centered").alignCenter());

        table.addRow().addContent(1, "Test", "Description");
        table.addRow().addContent(20, "My name", "Description");

        Row row = table.addRow();
        row.addContent(123456789);
        row.addContent("A very long text that should be cut");
        row.addContent("A very long text that should not be cut");

        StringWriter writer = new StringWriter();
        PrintStream out = new PrintStream(new WriterOutputStream(writer));
        table.print(out, true);
        out.flush();
        String expected = 
                "   id | Name                 |                Centered                \n" + 
                "----------------------------------------------------------------------\n" + 
                "    1 | Test                 |               Description              \n" + 
                "   20 | My name              |               Description              \n" + 
                "12345 | A very long text tha | A very long text that should not be cut\n";
        Assert.assertEquals(expected, getString(writer));
    }

    @Test
    public void testGrow() {
        ShellTable table = new ShellTable().size(10);
        table.column(new Col("1"));
        table.column(new Col("2"));

        table.addRow().addContent("1", "2");

        StringWriter writer = new StringWriter();
        PrintStream out = new PrintStream(new WriterOutputStream(writer));
        table.print(out, true);
        out.flush();
        String expected = 
                "1      | 2\n" + 
        		"----------\n" + 
        		"1      | 2\
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.shell.tabletest.ShellTableTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.shell.tabletest.ShellTableTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSH client properties and configurations.",
  "confidence": 1
}
```

## 123. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:28.235Z
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

## 124. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:30.909Z
- latency: 2.667 s

```json
{
  "test": "org.apache.karaf.system.internal.SystemServiceImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1341,
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

Test class `org.apache.karaf.system.internal.SystemServiceImplTest` (source, may be truncated):
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
package org.apache.karaf.system.internal;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;

import org.apache.felix.utils.properties.Properties;
import org.easymock.EasyMock;
import org.junit.Assert;
import org.junit.Test;
import org.osgi.framework.BundleContext;

/**
 * Implementation of the system service.
 */

public class SystemServiceImplTest {

    private static final String NEW_NAME = "newName";

    @Test
    public void testSetName() throws URISyntaxException, IOException {
        SystemServiceImpl system = new SystemServiceImpl();
        BundleContext bundleContext = EasyMock.createMock(BundleContext.class);
        URL propUrl = this.getClass().getClassLoader().getResource("etc/system.properties");
        File propfile = new File(propUrl.toURI());        
        EasyMock.expect(bundleContext.getProperty("karaf.etc")).andReturn(propfile.getParentFile().getParent() + "/etc");
        EasyMock.replay(bundleContext);
        system.setBundleContext(bundleContext);
        system.setName(NEW_NAME);
        EasyMock.verify(bundleContext);
        Properties props = new Properties(propfile);
        String nameAfter = props.getProperty("karaf.name");
        Assert.assertEquals(NEW_NAME, nameAfter);
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.system.internal.SystemServiceImplTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.system.internal.SystemServiceImplTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 125. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:33.674Z
- latency: 2.754 s

```json
{
  "test": "org.apache.karaf.tooling.VerifyMojoTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1305,
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

Test class `org.apache.karaf.tooling.VerifyMojoTest` (source, may be truncated):
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
package org.apache.karaf.tooling;

import org.apache.karaf.tooling.VerifyMojo;
import org.junit.Test;

import java.util.Arrays;
import java.util.regex.Pattern;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class VerifyMojoTest {

    @Test
    public void testFeaturePattern() {
        Pattern pattern = VerifyMojo.getPattern(Arrays.asList("foobiz", "!foo*", "bar", "!ba*", "*"));
        assertTrue(pattern.matcher("foobiz/1.0").matches());
        assertFalse(pattern.matcher("foobaz/1.0").matches());
        assertTrue(pattern.matcher("bar/1.0").matches());
        assertFalse(pattern.matcher("baz/1.0").matches());
        assertTrue(pattern.matcher("biz/1.0").matches());

        pattern = VerifyMojo.getPattern(Arrays.asList("!hibernate", " *"));
        assertTrue(pattern.matcher("framework/4.2.0.SNAPSHOT").matches());
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tooling.VerifyMojoTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tooling.VerifyMojoTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in `Main.java` or `Activator.java`.",
  "confidence": 1
}
```

## 126. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:36.955Z
- latency: 3.271 s

```json
{
  "test": "org.apache.karaf.tooling.features.BundleToArtifactTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1540,
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

Test class `org.apache.karaf.tooling.features.BundleToArtifactTest` (source, may be truncated):
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


package org.apache.karaf.tooling.features;

import java.lang.reflect.Field;
import java.util.HashMap;

import org.apache.karaf.tooling.utils.MojoSupport;
import org.apache.maven.artifact.Artifact;
import org.apache.maven.artifact.factory.DefaultArtifactFactory;
import org.apache.maven.artifact.handler.manager.ArtifactHandlerManager;
import org.apache.maven.artifact.handler.manager.DefaultArtifactHandlerManager;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugin.MojoFailureException;
import org.junit.Assert;
import org.junit.Test;


public class BundleToArtifactTest extends MojoSupport {

    @SuppressWarnings("rawtypes")
	public BundleToArtifactTest() throws NoSuchFieldException, IllegalAccessException {
        factory = new DefaultArtifactFactory();
        ArtifactHandlerManager artifactHandlerManager = new DefaultArtifactHandlerManager();
        Field f = factory.getClass().getDeclaredField("artifactHandlerManager");
        f.setAccessible(true);
        f.set(factory, artifactHandlerManager);
        f.setAccessible(false);

        f = artifactHandlerManager.getClass().getDeclaredField("artifactHandlers");
        f.setAccessible(true);
        f.set(artifactHandlerManager, new HashMap());
        f.setAccessible(false);
    }

    public void execute() throws MojoExecutionException, MojoFailureException {
    }
    
    @Test
    public void testSimpleURL() throws Exception {
        Artifact artifact = resourceToArtifact("mvn:org.foo/bar/1.0/kar", false);
        assert artifact.getGroupId().equals("org.foo");
        assert artifact.getArtifactId().equals("bar");
        assert artifact.getBaseVersion().equals("1.0");
        assert artifact.getType().equals("kar");
        assert artifact.getRepository() == null;
        assert artifact.getClassifier() == null;
    }

    @Test
    public void testURLWithClassifier() throws Exception {
        Artifact artifact = resourceToArtifact("mvn:org.foo/bar/1.0/kar/type", false);
        Assert.assertEquals("org.foo", artifact.getGroupId());
        Assert.assertEquals("bar", artifact.getArtifactId());
        Assert.assertEquals("1.0", artifact.getBaseVersion());
 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tooling.features.BundleToArtifactTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tooling.features.BundleToArtifactTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, heartbeats, or timeouts, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 127. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:39.976Z
- latency: 3.013 s

```json
{
  "test": "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1457,
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

Test class `org.apache.karaf.tooling.features.GenerateDescriptorMojoTest` (source, may be truncated):
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

package org.apache.karaf.tooling.features;

import static org.junit.Assert.*;

import java.io.ByteArrayOutputStream;
import java.net.URL;
import java.util.List;

import javax.xml.bind.JAXBException;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.stream.XMLStreamException;

import org.apache.karaf.features.FeaturesNamespaces;
import org.apache.karaf.features.internal.model.Features;
import org.apache.karaf.features.internal.model.Feature;
import org.apache.karaf.features.internal.model.JaxbUtil;
import org.junit.Test;
import org.xml.sax.SAXException;

public class GenerateDescriptorMojoTest {

    @Test
    public void testReadXml100() throws JAXBException, SAXException, ParserConfigurationException, XMLStreamException {

        URL url = getClass().getClassLoader().getResource("input-features-1.0.0.xml");

        Features featuresRoot = JaxbUtil.unmarshal(url.toExternalForm(), false);

        assertEquals(featuresRoot.getRepository().size(), 1);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        JaxbUtil.marshal(featuresRoot, baos);

        String text = new String(baos.toByteArray());

        assertTrue(text.contains("repository"));

        assertTrue(text.contains(FeaturesNamespaces.URI_CURRENT));
    }

    @Test
    public void testReadXml1() throws Exception {

        URL url = getClass().getClassLoader().getResource("input-features-1.1.0.xml");

        Features featuresRoot = JaxbUtil.unmarshal(url.toExternalForm(), false);

        List<Feature> featuresList = featuresRoot.getFeature();

        assertEquals(featuresList.size(), 1);

        Feature feature = featuresList.get(0);

        assertEquals(feature.getInstall(), "auto");
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to SSH, client configuration, or the changes made in the provided diff.",
  "confidence": 1
}
```

## 128. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:44.915Z
- latency: 4.932 s

```json
{
  "test": "org.apache.karaf.tooling.features.ManifestUtilsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1667,
  "completion_tokens": 115
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

Test class `org.apache.karaf.tooling.features.ManifestUtilsTest` (source, may be truncated):
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
package org.apache.karaf.tooling.features;

import static org.apache.karaf.tooling.utils.ManifestUtils.matches;

import junit.framework.TestCase;

import org.apache.felix.utils.manifest.Attribute;
import org.apache.felix.utils.manifest.Clause;
import org.apache.felix.utils.manifest.Directive;
import org.apache.karaf.tooling.utils.ManifestUtils;
import org.osgi.framework.Constants;

/**
 * Test cased for {@link org.apache.karaf.tooling.utils.ManifestUtils}
 */
public class ManifestUtilsTest extends TestCase {

    public void testIsOptional() {
    	Directive[] directive = new Directive[0];
    	Attribute[] attribute = new Attribute[0];
        Clause clause = new Clause("org.apache.karaf.test", directive, attribute);
        assertFalse(ManifestUtils.isOptional(clause));

        directive = new Directive[1];
        directive[0] = new Directive("resolution", "mandatory");
        clause = new Clause("org.apache.karaf.test", directive, attribute);
        
        assertFalse(ManifestUtils.isOptional(clause));

        directive[0] = new Directive("resolution", "optional");
        clause = new Clause("org.apache.karaf.test", directive, attribute);
        assertTrue(ManifestUtils.isOptional(clause));
    }

    public void testMatches() {
        assertFalse(matches(clause("org.apache.karaf.dev"), clause("org.apache.karaf.test")));
        assertTrue(matches(clause("org.apache.karaf.test"), clause("org.apache.karaf.test")));

        assertFalse(matches(clause("org.apache.karaf.test", "1.2.0"), clause("org.apache.karaf.test", "[1.1.0, 1.1.0]")));
        assertTrue(matches(clause("org.apache.karaf.test", "1.1.0"), clause("org.apache.karaf.test", "[1.1.0, 1.1.0]")));

        // a single version means >= 1.0.0, so 1.1.O should be a match
        assertTrue(matches(clause("org.apache.karaf.test", "1.0.0"), clause("org.apache.karaf.test", "1.1.0")));
        assertTrue(matches(clause("org.apache.karaf.test", "1.0.0"), clause("org.apache.karaf.test")));

        assertFalse(matches(clause("org.apache.karaf.test", "[1.1.0, 1.2.0)"), clause("org.apache.karaf.test", "[1.0.0, 1.0.0]")));
        assertFalse(matches(clause("org.apache.karaf.test", "[1.1.0, 1.2.0)"), c
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tooling.features.ManifestUtilsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tooling.features.ManifestUtilsTest",
  "relevance": 0,
  "reason": "The test class does not involve any classes or methods that are directly related to the changes made in the code. The changes are in the `Main.java` and `Activator.java` files, which are part of the Karaf client and SSH shell components, respectively. The test class is focused on testing utility methods for manifest handling, which is not affected by the changes.",
  "confidence": 1
}
```

## 129. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:48.166Z
- latency: 3.244 s

```json
{
  "test": "org.apache.karaf.tooling.features.MavenUtilTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1800,
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

Test class `org.apache.karaf.tooling.features.MavenUtilTest` (source, may be truncated):
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
package org.apache.karaf.tooling.features;

import org.apache.karaf.tooling.utils.Dependency31Helper;
import org.junit.Test;

import static org.apache.karaf.tooling.utils.MavenUtil.aetherToMvn;
import static org.apache.karaf.tooling.utils.MavenUtil.mvnToAether;
import static org.junit.Assert.assertEquals;

public class MavenUtilTest {

    @Test
    public void testMvnToAether() throws Exception {
        assertEquals("org.foo:org.foo.bar:1.0-SNAPSHOT", mvnToAether("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT"));
        assertEquals("org.foo:org.foo.bar:kar:1.0-SNAPSHOT", mvnToAether("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/kar"));
        assertEquals("org.foo:org.foo.bar:xml:features:1.0-SNAPSHOT", mvnToAether("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/xml/features"));
        assertEquals("org.foo:org.foo.bar:1.0-SNAPSHOT", mvnToAether("wrap:mvn:org.foo/org.foo.bar/1.0-SNAPSHOT"));
        assertEquals("org.foo:org.foo.bar:kar:1.0-SNAPSHOT", mvnToAether("wrap:mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/kar"));
        assertEquals("org.foo:org.foo.bar:xml:features:1.0-SNAPSHOT", mvnToAether("wrap:mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/xml/features"));
    }

    @Test
    public void testAetherToMvn() throws Exception {
        assertEquals("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT", aetherToMvn("org.foo:org.foo.bar:1.0-SNAPSHOT"));
        assertEquals("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/kar", aetherToMvn("org.foo:org.foo.bar:kar:1.0-SNAPSHOT"));
        assertEquals("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/xml/features", aetherToMvn("org.foo:org.foo.bar:xml:features:1.0-SNAPSHOT"));
    }

    @Test
    public void testPathFromMvnEclipse() throws Exception {
        Dependency31Helper helper = new Dependency31Helper(null, null, null);
        assertEquals("org/foo/org.foo.bar/1.0-SNAPSHOT/org.foo.bar-1.0-SNAPSHOT.jar", helper.pathFromMaven("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT"));
        assertEquals("org/foo/org.foo.bar/1.0-SNAPSHOT/org.foo.bar-1.0-SNAPSHOT.kar", helper.pathFromMaven("mvn:org.foo/org.foo.bar/1.0-SNAPSHOT/kar"));
        assertEquals("org/foo/org.foo.bar/1.0-SNAPSHOT/org.foo.bar-1.0-SNAPSHOT-features.xml", helper.pathFromMaven("mvn:org.foo/org.foo.bar/1.0-SNAP
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tooling.features.MavenUtilTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tooling.features.MavenUtilTest",
  "relevance": 0,
  "reason": "The test class does not involve any code related to the changes made in Main.java and Activator.java.",
  "confidence": 1
}
```

## 130. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:51.398Z
- latency: 3.216 s

```json
{
  "test": "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1562,
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

Test class `org.apache.karaf.tools.utils.KarafPropertiesEditorTest` (source, may be truncated):
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

package org.apache.karaf.tools.utils;

import com.google.common.io.Resources;
import org.apache.karaf.tools.utils.model.KarafPropertyEdits;
import org.apache.karaf.tools.utils.model.io.stax.KarafPropertyInstructionsModelStaxReader;
import org.junit.Test;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

/**
 * Test the property editing system.
 * See src/test/resources/.../test-edit.xml.
 */
public class KarafPropertiesEditorTest {
    private static final String ETC_TO_START_WITH = "../../main/src/test/resources/test-karaf-home/etc/";

    @Test
    public void onceOver() throws Exception {
        KarafPropertyInstructionsModelStaxReader kipmsr = new KarafPropertyInstructionsModelStaxReader();
        URL editsUrl = Resources.getResource(KarafPropertiesEditorTest.class, "test-edits.xml");
        KarafPropertyEdits edits;
        try (InputStream editsStream = Resources.asByteSource(editsUrl).openStream()) {
            edits = kipmsr.read(editsStream, true);
        }

        Path path = FileSystems.getDefault().getPath("target");
        Path outputEtc = Files.createTempDirectory(path, "test-etc");
        outputEtc.toFile().deleteOnExit();

        KarafPropertiesEditor editor = new KarafPropertiesEditor();
        editor.setInputEtc(new File(ETC_TO_START_WITH))
                .setOutputEtc(outputEtc.toFile())
                .setEdits(edits);
        editor.run();

        File resultConfigProps = new File(outputEtc.toFile(), "config.properties");
        Properties properties = new Properties();
        try (InputStream resultInputStream = new FileInputStream(resultConfigProps)) {
            properties.load(resultInputStream);
        }
        assertEquals("equinox", properties.getProperty("karaf.framework"));
        assertEquals("prepended,root,toor", properties.getProperty("karaf.name"));

        resultConfigProps = new File(outputEtc.toFile(), "jre.properties");
        try (InputStream
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.tools.utils.KarafPropertiesEditorTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the changed code in Main.java or Activator.java.",
  "confidence": 0.8
}
```

## 131. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:53.852Z
- latency: 2.445 s

```json
{
  "test": "org.apache.karaf.util.BundleUtilsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1221,
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

Test class `org.apache.karaf.util.BundleUtilsTest` (source, may be truncated):
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
package org.apache.karaf.util;

import org.apache.karaf.util.bundles.BundleUtils;
import org.junit.Test;

import java.io.File;
import java.io.FileInputStream;

public class BundleUtilsTest {

    @Test
    public void testJavaxMail() throws Exception {
        String url = getClass().getClassLoader().getResource("com/sun/mail/util/ASCIIUtility.class").toString();
        url = url.substring("jar:file:".length(), url.indexOf("!/"));
        File file = new File(url);
        BundleUtils.fixBundleWithUpdateLocation(new FileInputStream(file), "mvn:javax.mail/mail/1.4.7");
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.util.BundleUtilsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.util.BundleUtilsTest",
  "relevance": 0,
  "reason": "The test class does not involve any of the changed code in the provided diff.",
  "confidence": 1
}
```

## 132. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:56.867Z
- latency: 3.007 s

```json
{
  "test": "org.apache.karaf.util.config.ConfigurationPIDTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1520,
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

Test class `org.apache.karaf.util.config.ConfigurationPIDTest` (source, may be truncated):
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
package org.apache.karaf.util.config;

import org.junit.Assert;
import org.junit.Test;

public class ConfigurationPIDTest {

    @Test
    public void testR7FactoryPID() {
        final String pid = "org.apache.karaf.test.my.factory~Foo";
        final ConfigurationPID configurationPID = ConfigurationPID.parsePid(pid);
        Assert.assertEquals(pid, configurationPID.getPid());
        Assert.assertEquals("org.apache.karaf.test.my.factory", configurationPID.getFactoryPid());
        Assert.assertEquals("Foo", configurationPID.getName());
        Assert.assertTrue(configurationPID.isFactory());
        Assert.assertTrue(configurationPID.isR7());
    }

    @Test
    public void testNonR7FactoryPID() {
        final String pid = "org.apache.karaf.test.my.factory-Foo";
        final ConfigurationPID configurationPID = ConfigurationPID.parsePid(pid);
        Assert.assertEquals(pid, configurationPID.getPid());
        Assert.assertEquals("org.apache.karaf.test.my.factory", configurationPID.getFactoryPid());
        Assert.assertEquals("Foo", configurationPID.getName());
        Assert.assertTrue(configurationPID.isFactory());
        Assert.assertFalse(configurationPID.isR7());
    }

    @Test
    public void testR7FactoryPIDFromFilenameWithCfgExtension() {
        final String filename = "org.apache.karaf.test.my.factory~Foo.cfg";
        final ConfigurationPID configurationPID = ConfigurationPID.parseFilename(filename);
        Assert.assertEquals("org.apache.karaf.test.my.factory", configurationPID.getFactoryPid());
        Assert.assertEquals("Foo", configurationPID.getName());
        Assert.assertTrue(configurationPID.isFactory());
        Assert.assertTrue(configurationPID.isR7());
    }

    @Test
    public void testR7FactoryPIDFromFilenameWithConfigExtension() {
        final String filename = "org.apache.karaf.test.my.factory~Foo.config";
        final ConfigurationPID configurationPID = ConfigurationPID.parseFilename(filename);
        Assert.assertEquals("org.apache.karaf.test.my.factory", configurationPID.getFactoryPid());
        Assert.assertEquals("Foo", configurationPID.getName());
        Assert.assertTrue(configurationPID.isR7());
     
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.util.config.ConfigurationPIDTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.util.config.ConfigurationPIDTest",
  "relevance": 0,
  "reason": "The test class does not involve any changes related to the code change, which primarily affects SSHD and Karaf client configurations.",
  "confidence": 1
}
```

## 133. semantic_analyzer · llm_call

- time: 2026-11-07T18:05:59.670Z
- latency: 2.792 s

```json
{
  "test": "org.apache.karaf.webconsole.instance.InstancePluginTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1528,
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

Test class `org.apache.karaf.webconsole.instance.InstancePluginTest` (source, may be truncated):
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
package org.apache.karaf.webconsole.instance;

import java.io.ByteArrayOutputStream;
import java.io.PrintWriter;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import junit.framework.TestCase;

import org.apache.karaf.instance.core.Instance;
import org.apache.karaf.instance.core.InstanceService;
import org.apache.karaf.instance.core.InstanceSettings;
import org.easymock.EasyMock;

public class InstancePluginTest extends TestCase {
    public void testParseStringList() throws Exception {
        assertEquals(Arrays.asList("a", "b"), testParseStringList(" a ,b"));
        assertEquals(Collections.emptyList(), testParseStringList(null));
        assertEquals(Collections.singletonList("hello"), testParseStringList("hello"));
        assertEquals(Collections.singletonList("b"), testParseStringList(",b,"));
    }
    
    @SuppressWarnings("unchecked")
    private List<String> testParseStringList(String s) throws Exception {
        InstancePlugin ap = new InstancePlugin();
        Method m = ap.getClass().getDeclaredMethod("parseStringList", String.class);
        m.setAccessible(true);
        return (List<String>) m.invoke(ap, s);
    }
    
    public void testDoPostCreate() throws Exception {
        InstanceSettings instanceSettings =
            new InstanceSettings(123, 456, 789,  null, null, Collections.singletonList("http://someURL"), Arrays.asList("abc", "def"));
        InstanceService instanceService = EasyMock.createMock(InstanceService.class);
        EasyMock.expect(instanceService.createInstance("instance1", instanceSettings, false)).andReturn(null);
        EasyMock.expect(instanceService.getInstances()).andReturn(new Instance[]{}).anyTimes();
        EasyMock.replay(instanceService);
        
        InstancePlugin ap = new InstancePlugin();
        ap.setInstanceService(instanceService);

        final Map<String, String> params = new HashMap<>();
        params.put("action", "create");
        params.put("name", "instance1");
        params.
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.webconsole.instance.InstancePluginTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.webconsole.instance.InstancePluginTest",
  "relevance": 0,
  "reason": "The test class does not interact with the changed code in Main.java or Activator.java.",
  "confidence": 1
}
```

## 134. orchestrator · llm_call

- time: 2026-11-07T18:06:02.892Z
- latency: 3.003 s

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

Relevance source for this build: llm_all_individual

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

## 135. orchestrator · decision

- time: 2026-11-07T18:06:02.928Z
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

## 136. pipeline · state

- time: 2026-11-07T18:06:03.328Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system (no shortlist)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 137. pipeline · state

- time: 2026-11-07T18:06:03.370Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system (no shortlist)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 138. pipeline · state

- time: 2026-11-07T18:06:03.410Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system (no shortlist)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.jpm.ProcessTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
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
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.event.service.TopicPredicateTest"
  ]
}
```
