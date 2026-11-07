# Trace of PR-1501_build3

Run: `E3_test_seed1` · events: 57

## 1. pipeline · state

- time: 2026-11-07T15:00:58.622Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 206,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T15:00:58.723Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 206
}
```

## 3. pipeline · state

- time: 2026-11-07T15:00:58.728Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.examples.RestExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.763Z
- latency: 3.128 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1487,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
[...truncated]
DIFF>>>

Test class `org.apache.karaf.features.internal.service.FeatureConfigInstallerTest` (source, may be truncated):
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

import org.junit.Test;

import static org.junit.Assert.assertEquals;

import java.io.File;

public class FeatureConfigInstallerTest {
    
    private void substEqual(final String src, final String subst) {
        assertEquals(FeatureConfigInstaller.substFinalName(src), subst);
    }

    @Test
    public void testSubstFinalName() {
        final String karafBase = "/tmp/karaf.base";
        final String karafEtc = karafBase + "/etc";
        final String foo = "/foo";
        
        System.setProperty("karaf.base", karafBase);
        System.setProperty("karaf.etc", karafEtc);
        System.setProperty("foo", foo);
        
        substEqual("etc/test.cfg", karafBase + File.separator + "etc/test.cfg");
        substEqual("/etc/test.cfg", karafBase + File.separator + "/etc/test.cfg");
        substEqual("${karaf.etc}/test.cfg", karafEtc + "/test.cfg");
        substEqual("${karaf.base}/etc/test.cfg", karafBase + "/etc/test.cfg");
        substEqual("etc/${foo}/test.cfg", karafBase + File.separator + "etc/" + foo + "/test.cfg");
        substEqual("${foo}/test.cfg", foo + "/test.cfg");
        substEqual("etc${bar}/${bar}test.cfg", karafBase + File.separator + "etc/test.cfg");
        substEqual("${bar}/etc/test.cfg${bar}", karafBase + File.separator + "/etc/test.cfg");
        substEqual("${karaf.base}${bar}/etc/test.cfg", karafBase + "/etc/test.cfg");
        substEqual("etc${}/${foo}/test.cfg", karafBase + File.separator + "etc//test.cfg");
        substEqual("${foo}${bar}/${bar}${foo}", foo + "/" + foo);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the code changes made in FeatureConfigInstaller.java.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.770Z
- latency: 2.124 s

```json
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1322,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.SystemShutdownTest` (source, may be truncated):
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

import javax.management.MBeanServer;
import javax.management.ObjectName;

import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import java.lang.management.ManagementFactory;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class SystemShutdownTest extends BaseTest {

    @Test
    public void shutdownCommand() {
        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
        Assert.assertEquals("", result);
    }

    @Test
    public void haltAlias() {
        String result = executeCommand("halt", new RolePrincipal("admin"));
        Assert.assertEquals("", result);
    }

    @Test
    public void shutdownViaMBean() throws Exception {
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
        Assert.assertNotNull(result);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.SystemShutdownTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or its methods.",
  "confidence": 1
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.778Z
- latency: 2.758 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1644,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "relevance": 0,
  "reason": "The test class does not involve file operations or configuration management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.785Z
- latency: 2.648 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1604,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not involve file operations or configuration management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.792Z
- latency: 2.558 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1569,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not involve any of the changed code in the provided diff.",
  "confidence": 1
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.799Z
- latency: 2.433 s

```json
{
  "test": "org.apache.karaf.instance.main.ExecuteTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1496,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not appear to interact with the changed code in FeatureConfigInstaller.java.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.807Z
- latency: 2.525 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1403,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.815Z
- latency: 2.479 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1537,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.JMXSecurityTest` (source, may be truncated):
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
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

import javax.management.Attribute;
import javax.management.AttributeNotFoundException;
import javax.management.InstanceNotFoundException;
import javax.management.InvalidAttributeValueException;
import javax.management.MBeanException;
import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.ReflectionException;
import javax.management.openmbean.CompositeData;
import javax.management.openmbean.CompositeDataSupport;
import javax.management.openmbean.CompositeType;
import javax.management.openmbean.OpenType;
import javax.management.openmbean.SimpleType;
import javax.management.openmbean.TabularData;
import javax.management.openmbean.TabularDataSupport;
import javax.management.openmbean.TabularType;
import javax.management.remote.JMXConnector;

import org.apache.karaf.jaas.boot.principal.RolePrincipal;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.service.cm.ConfigurationAdmin;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class JMXSecurityTest extends BaseTest {

    private static AtomicInteger counter = new AtomicInteger(0);

    @Configuration
    public Option[] config() {
        List<Option> options = new ArrayList<>(Arrays.asList(super.config()));

        // Add some extra options used by this test...
        options.addAll(Arrays.asList(
            editConfigurationFilePut("etc/jmx.acl.org.apache.karaf.service.cfg", "getServices()", "admin"),
            editConfigurationFilePut("etc/jmx.acl.org.apache.karaf.service.cfg", "getS
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.JMXSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or its methods.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.824Z
- latency: 2.756 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1576,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not involve file operations or system shutdown commands, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.832Z
- latency: 2.552 s

```json
{
  "test": "org.apache.karaf.itests.examples.HttpResourceExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1472,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.839Z
- latency: 2.456 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1443,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class is related to LDAP authentication and does not involve file operations or configuration updates.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.847Z
- latency: 2.695 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1586,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the code changes made in the diff.",
  "confidence": 1
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.853Z
- latency: 2.942 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1593,
  "completion_tokens": 76
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not involve any file operations or handling of IOExceptions, which are directly related to the changes in FeatureConfigInstaller.java.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.860Z
- latency: 2.602 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1546,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.867Z
- latency: 2.307 s

```json
{
  "test": "org.apache.karaf.main.MainTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1550,
  "completion_tokens": 55
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "relevance": 0,
  "reason": "The test class does not appear to interact with the changed code in FeatureConfigInstaller.java.",
  "confidence": 1
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.874Z
- latency: 2.747 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1536,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.881Z
- latency: 2.827 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1575,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not involve any code related to file operations or configuration management, which are the primary changes in the provided code diff.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T15:00:58.888Z
- latency: 2.640 s

```json
{
  "test": "org.apache.karaf.itests.examples.WebSocketExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1548,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the files modified in the code change.",
  "confidence": 1
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T15:01:02.129Z
- latency: 3.234 s

```json
{
  "test": "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1447,
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
diff --git a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
--- a/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
+++ b/features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
@@ -331,7 +331,9 @@ protected void updateStorage(ConfigId cid, TypedProperties props, boolean append
                 } else {
                     props.save(tmpCfgFile);
                 }
-                tmpCfgFile.renameTo(cfgFile);
+                if (!tmpCfgFile.renameTo(cfgFile)) {
+                    throw new IOException("Can't rename file from " + tmpCfgFile.getName() + " to " + cfgFile.getName());
+                }
             } else {
                 updateExistingConfig(props, append, cfgFile, jsonFormat);
             }
diff --git a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
--- a/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
+++ b/itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
@@ -17,6 +17,7 @@
 import javax.management.ObjectName;
 
 import org.apache.karaf.jaas.boot.principal.RolePrincipal;
+import org.junit.Assert;
 import org.junit.Test;
 import org.junit.runner.RunWith;
 import org.ops4j.pax.exam.junit.PaxExam;
@@ -30,20 +31,23 @@
 public class SystemShutdownTest extends BaseTest {
 
     @Test
-    public void shutdownCommand() throws Exception {
-        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
+    public void shutdownCommand() {
+        String result = executeCommand("system:shutdown -f", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
-    public void haltAlias() throws Exception {
-        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
+    public void haltAlias() {
+        String result = executeCommand("halt", new RolePrincipal("admin"));
+        Assert.assertEquals("", result);
     }
 
     @Test
     public void shutdownViaMBean() throws Exception {
         MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
         ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
-        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Object result = mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
+        Assert.assertNotNull(result);
     }
 
 }
diff --git a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
--- a/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
+++ b/obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java
@@ -159,6 +159,10
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
  "reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the provided code diff.",
  "confidence": 1
}
```

## 23. orchestrator · llm_call

- time: 2026-11-07T15:01:04.944Z
- latency: 2.695 s

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
- n_code_files = 3: number of changed code files in the diff
- n_dirs = 3: number of distinct folders those files are in
- lines_added = 16: added lines in the diff
- lines_removed = 6: removed lines in the diff
- recent_failure_density = 0.4: share of the last 10 history builds with at least one failing test
- n_candidates = 206: number of candidate test classes
- shortlist_size = 19: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0: mean relevance used over the shortlisted tests
- rel_max = 0: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.168204: highest history score over all candidates
- hist_mean_shortlist = 0.0284341: mean history score over the shortlisted tests

Changed files (3):
- features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java
- itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java
- obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.features.internal.service.FeatureConfigInstallerTest | 0.000 | 1.000 | 0.000 | 0.003
- org.apache.karaf.itests.SystemShutdownTest | 0.168 | 1.000 | 0.000 | 395.824
- org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest | 0.080 | 0.191 | 0.000 | 35.082
- org.apache.karaf.itests.examples.JpaExampleTest | 0.052 | 0.280 | 0.000 | 34.141
- org.apache.karaf.jaas.modules.ldap.LdapCacheTest | 0.010 | 1.000 | 0.000 | 0.683
- org.apache.karaf.instance.main.ExecuteTest | 0.000 | 0.825 | 0.000 | 0.027
- org.apache.karaf.itests.examples.JdbcExampleTest | 0.043 | 0.186 | 0.000 | 10.988
- org.apache.karaf.itests.JMXSecurityTest | 0.033 | 0.266 | 0.000 | 15.947
- org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest | 0.000 | 0.812 | 0.000 | 0.147
- org.apache.karaf.itests.examples.HttpResourceExampleTest | 0.031 | 0.108 | 0.000 | 2.927
- org.apache.karaf.jaas.modules.ldap.BadReferenceTest | 0.000 | 0.795 | 0.000 | 0.655
- org.apache.karaf.itests.examples.RestExampleTest | 0.031 | 0.088 | 0.000 | 83.333
- org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest | 0.000 | 0.793 | 0.000 | 0.173
- org.apache.karaf.itests.examples.ServletExampleTest | 0.031 | 0.110 | 0.000 | 61.19
- org.apache.karaf.main.MainTest | 0.000 | 0.791 | 0.000 | 0.021
- org.apache.karaf.itests.examples.SoapExampleTest | 0.031 | 0.112 | 0.000 | 27.849
- org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest | 0.000 | 0.733 | 0.000 | 0.503
- org.apache.karaf.itests.examples.WebSocketExampleTest | 0.031 | 0.075 | 0.000 | 13.272
- org.apache.karaf.maven.command.MavenConfigurationSupportTest | 0.000 | 0.723 | 0.000 | 0.015

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

- time: 2026-11-07T15:01:04.960Z
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

- time: 2026-11-07T15:01:05.164Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest"
  ]
}
```

## 26. pipeline · state

- time: 2026-11-07T15:01:05.180Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.itests.WrapperTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.BundleTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T15:01:05.197Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.itests.WrapperTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.BundleTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.shell.ssh.KnownHostsManagerTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.itests.examples.BlueprintExampleTest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.itests.ssh.JaasSshCommandSecurityTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T15:01:05.289Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T15:01:05.304Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T15:01:05.320Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T15:01:05.412Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T15:01:05.428Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T15:01:05.443Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T15:01:05.536Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T15:01:05.552Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T15:01:05.567Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T15:01:05.674Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T15:01:05.694Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T15:01:05.714Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T15:01:05.770Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 41. explainer · explanation

- time: 2026-11-07T15:01:19.537Z
- latency: 13.742 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 8,
    "n_candidates": 206,
    "n_selected": 19,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 2,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0
      ]
    },
    "history_score": 0.08,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not involve file operations or configuration management, which are the primary changes in the provided code diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 35.082,
    "budget_s": 63.174,
    "remaining_budget_at_turn_s": 0.32,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 97.936
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 42. explainer · explanation

- time: 2026-11-07T15:01:22.854Z
- latency: 3.302 s

```json
{
  "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
    "rank_by_value": 9,
    "n_candidates": 206,
    "n_selected": 19,
    "history": {
      "test": "org.apache.karaf.shell.ssh.SshUtilsTest",
      "history_builds": 100,
      "runs": 99,
      "failures": 1,
      "failure_rate": 0.010101010101010102,
      "last_failure_distance": 48,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 1.63,
    "budget_s": 63.174,
    "remaining_budget_at_turn_s": 0.32,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 64.484
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and its duration of 1.63 s exceeds the remaining budget of 0.32 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 1.63",
    "remaining_budget_at_turn_s: 0.32"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T15:01:27.055Z
- latency: 4.183 s

```json
{
  "test": "org.apache.karaf.itests.LogTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.LogTest",
    "rank_by_value": 10,
    "n_candidates": 206,
    "n_selected": 19,
    "history": {
      "test": "org.apache.karaf.itests.LogTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 91,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 2.737,
    "budget_s": 63.174,
    "remaining_budget_at_turn_s": 0.32,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 65.591
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 2.737 s but only 0.32 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 2.737",
    "remaining_budget_at_turn_s: 0.32"
  ],
  "ok": true,
  "error": null
}
```

## 44. explainer · explanation

- time: 2026-11-07T15:01:38.999Z
- latency: 11.921 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 11,
    "n_candidates": 206,
    "n_selected": 19,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 59,
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
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 27.849,
    "budget_s": 63.174,
    "remaining_budget_at_turn_s": 0.32,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 90.703
  },
  "justification": "Skipping it is reasonable: it has a relevance of 0.0 because it does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff. It only took 27.849 s, which was well within the remaining budget of 0.32 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
    "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
    "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java",
    "duration_s: 27.849",
    "remaining_budget_at_turn_s: 0.32"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T15:01:51.630Z
- latency: 12.614 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.JMXSecurityTest",
    "rank_by_value": 12,
    "n_candidates": 206,
    "n_selected": 19,
    "history": {
      "test": "org.apache.karaf.itests.JMXSecurityTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 3,
      "recent_outcomes": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0
      ]
    },
    "history_score": 0.033,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or its methods.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 15.947,
    "budget_s": 63.174,
    "remaining_budget_at_turn_s": 0.32,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 78.801
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 46. pipeline · state

- time: 2026-11-07T15:01:51.710Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.audit.util.FastDateFormatTest"
  ]
}
```

## 47. explainer · explanation

- time: 2026-11-07T15:02:03.619Z
- latency: 11.886 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 11,
    "n_candidates": 206,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 59,
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
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 27.849,
    "budget_s": 126.349,
    "remaining_budget_at_turn_s": 24.046,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 130.152
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:02:17.565Z
- latency: 13.922 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 14,
    "n_candidates": 206,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 59,
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
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the changes made in the code diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 61.19,
    "budget_s": 126.349,
    "remaining_budget_at_turn_s": 2.559,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 184.98
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 49. explainer · explanation

- time: 2026-11-07T15:02:21.751Z
- latency: 4.163 s

```json
{
  "test": "org.apache.karaf.itests.WebTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.WebTest",
    "rank_by_value": 15,
    "n_candidates": 206,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.WebTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 62,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 7.064,
    "budget_s": 126.349,
    "remaining_budget_at_turn_s": 2.559,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 130.854
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 97 runs. It needs 7.064 s but only 2.559 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 7.064",
    "remaining_budget_at_turn_s: 2.559"
  ],
  "ok": true,
  "error": null
}
```

## 50. explainer · explanation

- time: 2026-11-07T15:02:34.573Z
- latency: 12.799 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 16,
    "n_candidates": 206,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 59,
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
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the code changes made in the diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 83.333,
    "budget_s": 126.349,
    "remaining_budget_at_turn_s": 2.559,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 207.123
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 51. explainer · explanation

- time: 2026-11-07T15:02:39.028Z
- latency: 4.440 s

```json
{
  "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "rank_by_value": 17,
    "n_candidates": 206,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.features.Spring43FeaturesTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 53,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 11.271,
    "budget_s": 126.349,
    "remaining_budget_at_turn_s": 2.559,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 135.061
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential instability. It needs 11.271 s but only 2.559 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 11.271",
    "remaining_budget_at_turn_s: 2.559"
  ],
  "ok": true,
  "error": null
}
```

## 52. pipeline · state

- time: 2026-11-07T15:02:39.111Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.WebSocketExampleTest",
    "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.WarExampleTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.itests.WebTest",
    "org.apache.karaf.itests.features.Spring43FeaturesTest",
    "org.apache.karaf.itests.features.Spring3FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 53. explainer · explanation

- time: 2026-11-07T15:02:50.939Z
- latency: 11.803 s

```json
{
  "test": "org.apache.karaf.itests.examples.RestExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.RestExampleTest",
    "rank_by_value": 16,
    "n_candidates": 206,
    "n_selected": 40,
    "history": {
      "test": "org.apache.karaf.itests.examples.RestExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 3,
      "failure_rate": 0.030927835051546393,
      "last_failure_distance": 59,
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
    "history_score": 0.031,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or any of the code changes made in the diff.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 83.333,
    "budget_s": 252.697,
    "remaining_budget_at_turn_s": 32.804,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 303.226
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 54. explainer · explanation

- time: 2026-11-07T15:02:55.214Z
- latency: 4.257 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JmsExampleTest",
    "rank_by_value": 19,
    "n_candidates": 206,
    "n_selected": 40,
    "history": {
      "test": "org.apache.karaf.itests.examples.JmsExampleTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 87,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 12.729,
    "budget_s": 252.697,
    "remaining_budget_at_turn_s": 9.759,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 255.667
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 97 runs. It needs 12.729 s but only 9.759 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 97 runs",
    "duration_s: 12.729",
    "remaining_budget_at_turn_s: 9.759"
  ],
  "ok": true,
  "error": null
}
```

## 55. explainer · explanation

- time: 2026-11-07T15:02:59.671Z
- latency: 4.442 s

```json
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.SystemShutdownTest",
    "rank_by_value": 20,
    "n_candidates": 206,
    "n_selected": 40,
    "history": {
      "test": "org.apache.karaf.itests.SystemShutdownTest",
      "history_builds": 100,
      "runs": 97,
      "failures": 1,
      "failure_rate": 0.010309278350515464,
      "last_failure_distance": 1,
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
        1
      ]
    },
    "history_score": 0.168,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `FeatureConfigInstaller` class or its methods.",
    "changed_files": [
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 395.824,
    "budget_s": 252.697,
    "remaining_budget_at_turn_s": 9.759,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 638.762
  },
  "justification": "Skipping it is risky: it has a failure rate of 0.0103 and its duration is 395.824 s, which exceeds the remaining budget of 9.759 s.",
  "cited_facts": [
    "failures: 1 of 97 runs",
    "failure_rate: 0.010309278350515464",
    "duration_s: 395.824",
    "remaining_budget_at_turn_s: 9.759"
  ],
  "ok": true,
  "error": null
}
```

## 56. explainer · explanation

- time: 2026-11-07T15:03:02.972Z
- latency: 3.284 s

```json
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.config.command.EditCommandTest",
    "rank_by_value": 68,
    "n_candidates": 206,
    "n_selected": 40,
    "history": {
      "test": "org.apache.karaf.config.command.EditCommandTest",
      "history_builds": 100,
      "runs": 100,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 0.003,
    "budget_s": 252.697,
    "remaining_budget_at_turn_s": 0.001,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 252.699
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.003 s, which is negligible compared to the remaining budget of 0.001 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.003",
    "remaining_budget_at_turn_s: 0.001"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T15:03:06.341Z
- latency: 3.350 s

```json
{
  "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "rank_by_value": 70,
    "n_candidates": 206,
    "n_selected": 40,
    "history": {
      "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
      "history_builds": 100,
      "runs": 100,
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
      "features/core/src/main/java/org/apache/karaf/features/internal/service/FeatureConfigInstaller.java",
      "itests/test/src/test/java/org/apache/karaf/itests/SystemShutdownTest.java",
      "obr/src/main/java/org/apache/karaf/obr/command/util/FileUtil.java"
    ],
    "duration_s": 0.047,
    "budget_s": 252.697,
    "remaining_budget_at_turn_s": 0.001,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 252.743
  },
  "justification": "Skipping it is risky: it has no relevance and its duration is 0.047 s, which is less than the remaining budget of 0.001 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.047",
    "remaining_budget_at_turn_s: 0.001"
  ],
  "ok": true,
  "error": null
}
```
