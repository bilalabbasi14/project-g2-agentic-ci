# Trace of PR-1626_build2

Run: `E3_test_seed1` · events: 58

## 1. pipeline · state

- time: 2026-11-07T15:15:58.619Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 202,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T15:15:58.708Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 202
}
```

## 3. pipeline · state

- time: 2026-11-07T15:15:58.713Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.InstanceTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.itests.examples.ServletExampleTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jpm.ProcessTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:01.664Z
- latency: 2.892 s

```json
{
  "test": "org.apache.karaf.itests.FelixHttpTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1379,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.FelixHttpTest` (source, may be truncated):
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
package org.apache.karaf.itests;

import org.junit.Before;
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
public class FelixHttpTest extends BaseTest {

    @Before
    public void setup() throws Exception {
        installAndAssertFeature("felix-http");
    }

    @Test
    public void testHttpService() throws Exception {
        waitForService("(objectClass=org.osgi.service.http.HttpService)", 5000);

        installBundle("mvn:org.apache.karaf.examples/karaf-servlet-example-registration/" + System.getProperty("karaf.version"), true);

        URL url = new URL("http://localhost:8181/servlet-example");
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

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.FelixHttpTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.FelixHttpTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:04.019Z
- latency: 2.347 s

```json
{
  "test": "org.apache.karaf.itests.InstanceTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1528,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.InstanceTest` (source, may be truncated):
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

import org.apache.commons.compress.archivers.tar.TarArchiveInputStream;
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipFile;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import javax.management.MBeanServer;
import javax.management.MBeanServerConnection;
import javax.management.ObjectName;
import javax.management.openmbean.TabularData;
import java.io.FileInputStream;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;
import java.util.zip.GZIPInputStream;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class InstanceTest extends BaseTest {

    @Test
    public void createDestroyCommand() throws Exception {
        System.out.println(executeCommand("instance:create itest1"));
        assertContains("itest1", executeCommand("instance:list"));
        System.out.println(executeCommand("instance:destroy itest1"));
        assertContainsNot("itest1", executeCommand("instance:list"));
    }

    @Test
    public void createDestroyViaMBean() throws Exception {
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        ObjectName name = new ObjectName("org.apache.karaf:type=instance,name=root");
        int oldNum = getInstancesNum(mbeanServer, name);
        mbeanServer.invoke(name, "createInstance", new Object[]{"itest2", 0, 0, 0, null, null, null, null},
                new String[]{"java.lang.String", "int", "int", "int", "java.lang.String", "java.lang.String", "java.lang.String", "java.lang.String"});
        Assert.assertEquals(oldNum + 1, getInstancesNum(mbeanServer, name));
        mbeanServer.invoke(name, "destroyInstance", new Object[]{"itest2"}, new String[]{"java.lang.String"});
        Assert.assertEquals(oldNum, getInstancesNum(mbeanServer, name));
    }

    @Test
    public void createStartStopDestroyCommand() throws Exception {
 
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.InstanceTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.InstanceTest",
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the new PackageCommand class.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:06.531Z
- latency: 2.504 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1554,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
		assertEquals("data1", config.getProperties().get("test1").toString());
	}

	private void checkInitialValuesFromFelixConfigAdmin() throws IOException,
			InvalidSyntaxException {
		Configuration config = readConfig();
		assertNotNull("The configuration is null", config);
		assertEquals("data1", config.getProperties().get("test1").toString());
		assertEquals("data2", config.getProperties().get("test2").toString());
	}

	private void checkEditByFactoryPid() throws IOExce
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
  "relevance": 0,
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:08.848Z
- latency: 2.309 s

```json
{
  "test": "org.apache.karaf.main.MainTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1508,
  "completion_tokens": 51
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:11.287Z
- latency: 2.430 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1555,
  "completion_tokens": 53
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.JmsTest` (source, may be truncated):
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

import java.lang.management.ManagementFactory;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.MavenUtils;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import javax.management.MBeanServer;
import javax.management.ObjectName;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class JmsTest extends BaseTest {

    @Configuration
    public Option[] config() {
        String version = MavenUtils.getArtifactVersion("org.apache.karaf", "apache-karaf");
        List<Option> options = new LinkedList<>(Arrays.asList(super.config()));
        options.add(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", "featuresRepositories",
                "mvn:org.apache.karaf.features/framework/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/spring/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/spring-legacy/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/enterprise/" + version + "/xml/features, " +
                        "mvn:org.apache.karaf.features/standard/" + version + "/xml/features, " +
                        "mvn:org.apache.activemq/activemq-karaf/" + System.getProperty("activemq.version") + "/xml/features"));
        return options.toArray(new Option[options.size()]);
    }

    @Test(timeout = 60000)
    public void testCommands() throws Exception {
        System.out.println("== Installing ActiveMQ");
        featureService.installFeature("aries-blueprint");
        featureService.installFeature("activemq-broker-noweb");

        System.out.println("== Installing JMS feature");
        featureService.installFeature("jms");
        featureService.installFeature("pax-jms-activemq");

        System.out.println("== Creating JMS ConnectionFactory");
        executeCommand("jms:create test");
        Thread.sleep(2000);
        String output = executeCommand("jms:connectionfactories");
        System.out.println(
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.JmsTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.JmsTest",
  "relevance": 0,
  "reason": "The test class does not interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:13.720Z
- latency: 2.425 s

```json
{
  "test": "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1518,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "relevance": 0,
  "reason": "The test class does not interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:16.226Z
- latency: 2.496 s

```json
{
  "test": "org.apache.karaf.itests.XATest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1581,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not appear to interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:18.594Z
- latency: 2.360 s

```json
{
  "test": "org.apache.karaf.profile.assembly.BuilderTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1505,
  "completion_tokens": 53
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:20.888Z
- latency: 2.284 s

```json
{
  "test": "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1260,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:23.392Z
- latency: 2.494 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1588,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:25.893Z
- latency: 2.490 s

```json
{
  "test": "org.apache.karaf.itests.LogTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1531,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not interact with the code that was added in the PackageCommand.java file.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:28.291Z
- latency: 2.390 s

```json
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1453,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the code in PackageCommand.java.",
  "confidence": 1
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:30.587Z
- latency: 2.288 s

```json
{
  "test": "org.apache.karaf.instance.main.ExecuteTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1454,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not appear to interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:32.974Z
- latency: 2.380 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1508,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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

import org.apache.karaf.features.FeaturesService;
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
import java.util.EnumSet;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class ServletExampleTest extends BaseTest {

    private void setup() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-servlet-example-features/" + System.getProperty("karaf.version") + "/xml");
        installAndAssertFeature("http");
        installAndAssertFeature("http-whiteboard");
        installAndAssertFeature("pax-web-karaf");
        featureService.installFeature("pax-web-jsp", EnumSet.noneOf(FeaturesService.Option.class));
        installAndAssertFeature("pax-web-jsp");
    }

    private void verify() throws Exception {
        String command = executeCommand("web:servlet-list");
        while (!command.contains("servlet-example")) {
            Thread.sleep(200);
            command = executeCommand("web:servlet-list");
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
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:35.358Z
- latency: 2.377 s

```json
{
  "test": "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1507,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the newly added PackageCommand class.",
  "confidence": 1
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:37.901Z
- latency: 2.535 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1494,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:40.528Z
- latency: 2.618 s

```json
{
  "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1658,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest` (source, may be truncated):
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
 * This test exercises the Shell Command ACL for the bundle scope commands as defined in
 * /framework/src/main/resources/resources/etc/org.apache.karaf.command.acl.bundle.cfg
 */
@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class BundleSshCommandSecurityTest extends SshCommandTestBase {
    private static int counter = 0;
    


    @Test
    public void testBundleCommandSecurityViaSsh() throws Exception {
        String manageruser = "man" + System.nanoTime() + "_" + counter++;
        String vieweruser = "view" + System.nanoTime() + "_" + counter++;

        addUsers(manageruser, vieweruser);

        assertCommand(vieweruser, "bundle:refresh 999", Result.NOT_FOUND);
        assertCommand(manageruser, "bundle:refresh -f 999", Result.NO_CREDENTIALS);
        assertCommand(manageruser, "bundle:refresh 999", Result.OK);
        assertCommand("karaf", "bundle:refresh -f 999", Result.OK);
        assertCommand("karaf", "bundle:refresh 999", Result.OK);

        assertCommand(vieweruser, "bundle:restart 999", Result.NOT_FOUND);
        assertCommand(manageruser, "bundle:restart -f 999", Result.NO_CREDENTIALS);
        assertCommand(manageruser, "bundle:restart 999", Result.OK);
        assertCommand("karaf", "bundle:restart -f 999", Result.OK);
        assertCommand("karaf", "bundle:restart 999", Result.OK);

        assertCommand(vieweruser, "bundle:start 999", Result.NOT_FOUND);
        assertCommand(manageruser, "bundle:start -f 999", Result.NO_CREDENTIALS);
        assertCommand(manageruser, "bundle:start 999", Result.OK);
        assertCommand("karaf", "bundle:start -f 999", Result.OK);
        assertCommand("karaf", "bundle:start 999", Result.OK);

        assertCommand(vieweruser, "bundle:stop 999", Result.NOT_FOUND);
        assertCommand(manageruser, "bundle:stop -f 999", Result.NO_CREDENTIALS);
        assertCommand(manageruser, "bundle:stop 999", Result.OK);
        assertCommand("karaf", "bundle:stop -f 999", Result.OK);
        assertCommand("karaf", "bundle:stop 999", Result.OK);

        assertCommand(vieweruser, "bundle:uninstall 999", Result.NOT_FOUND);
        assertCommand(manageruser, "bundle:uninstall -f 999",
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
  "relevance": 0,
  "reason": "The test class does not interact with the PackageCommand or any related functionality.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:42.900Z
- latency: 2.362 s

```json
{
  "test": "org.apache.karaf.jpm.ProcessTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1498,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "relevance": 0,
  "reason": "The test class does not interact with the code changes made in PackageCommand.java.",
  "confidence": 1
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:45.518Z
- latency: 2.610 s

```json
{
  "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1455,
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
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest` (source, may be truncated):
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

import org.junit.Assert;
import org.junit.Test;

/**
 * This test exercises the Shell Command ACL for the feature scope commands as defined in
 * /framework/src/main/resources/resources/etc/org.apache.karaf.command.acl.feature.cfg
 */
public class FeatureSshCommandSecurityTest extends SshCommandTestBase {
    
    
    
    @Test
    public void testFeatureCommandSecurityViaSsh() throws Exception {
        String vieweruser = "viewer" + System.nanoTime() + "_features";
        String feature = "wrapper";

        addViewer(vieweruser);

        String r = assertCommand(vieweruser, "feature:list -i --no-format", Result.OK);
        Assert.assertFalse("Precondition failed, this test uses the " + feature + " subsystem to test features with...",
                r.contains(feature));

        assertCommand(vieweruser, "feature:install -r " + feature, Result.NOT_FOUND);
        String r2 = assertCommand("karaf", "feature:list -i --no-format", Result.OK);
        Assert.assertFalse(feature + " features should not have been installed, as viewer doesn't have credentials",
                r2.contains(feature));

        assertCommand("karaf", "feature:install -r " + feature, Result.OK);
        String r3 = assertCommand(vieweruser, "feature:list -i --no-format", Result.OK);
        Assert.assertTrue(feature + " feature should have been installed by 'karaf' user",
                r3.contains(feature));

        assertCommand(vieweruser, "feature:uninstall -r " + feature, Result.NOT_FOUND);
        String r4 = assertCommand("karaf", "feature:list -i --no-format", Result.OK);
        Assert.assertTrue(feature + " feature should still be there, as viewer doesn't have credentials",
                r4.contains(feature));

        assertCommand("karaf", "feature:uninstall -r " + feature, Result.OK);
        String r5 = assertCommand(vieweruser, "feature:list -i --no-format", Result.OK);
        Assert.assertFalse(feature + " feature should have been uninstalled",
                r5.contains(feature));
    }
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
  "confidence": 1
}
```

## 23. semantic_analyzer · llm_call

- time: 2026-11-07T15:16:48.591Z
- latency: 3.066 s

```json
{
  "test": "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1488,
  "completion_tokens": 80
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
new file mode 100644
--- /dev/null
+++ b/instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
@@ -0,0 +1,143 @@
+/*
+ * Licensed to the Apache Software Foundation (ASF) under one or more
+ * contributor license agreements.  See the NOTICE file distributed with
+ * this work for additional information regarding copyright ownership.
+ * The ASF licenses this file to You under the Apache License, Version 2.0
+ * (the "License"); you may not use this file except in compliance with
+ * the License.  You may obtain a copy of the License at
+ *
+ *      http://www.apache.org/licenses/LICENSE-2.0
+ *
+ * Unless required by applicable law or agreed to in writing, software
+ * distributed under the License is distributed on an "AS IS" BASIS,
+ * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+ * See the License for the specific language governing permissions and
+ * limitations under the License.
+ */
+package org.apache.karaf.instance.command;
+
+import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
+import org.apache.commons.compress.archivers.tar.TarArchiveOutputStream;
+import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
+import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream;
+import org.apache.karaf.instance.command.completers.InstanceCompleter;
+import org.apache.karaf.instance.core.Instance;
+import org.apache.karaf.shell.api.action.Argument;
+import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
+import org.apache.karaf.shell.api.action.lifecycle.Service;
+
+import java.io.BufferedOutputStream;
+import java.io.FileOutputStream;
+import java.io.IOException;
+import java.io.OutputStream;
+import java.nio.file.*;
+import java.nio.file.attribute.BasicFileAttributes;
+import java.util.zip.ZipOutputStream;
+
+@Command(scope = "instance", name = "package", description = "Create a .zip or .tar.gz archive of the instance.")
+@Service
+public class PackageCommand extends InstanceCommandSupport {
+
+    @Argument(index = 0, name = "name", description = "The name of the container instance", required = true)
+    @Completion(InstanceCompleter.class)
+    private String name;
+    @Argument(index = 1, name = "destination", description = "Destination path for the archive", required = true)
+    private String destination;
+
+    protected Object doExecute() throws Exception {
+        Instance instance = getInstanceService().getInstance(name);
+        Path location = Paths.get(instance.getLocation());
+
+        Path destinationPath = Paths.get(destination);
+        if (destination.endsWith(".zip")) {
+            createZip(location, destinationPath);
+        } else {
+            createTarGz(location, destinationPath);
+        }
+
+        retu
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
  "reason": "The test class is related to JAAS (Java Authentication and Authorization Service) and properties-based login modules, which is unrelated to the code change that introduces a new command for packaging instances.",
  "confidence": 1
}
```

## 24. orchestrator · llm_call

- time: 2026-11-07T15:16:51.611Z
- latency: 2.880 s

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
- lines_added = 233: added lines in the diff
- lines_removed = 8: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 202: number of candidate test classes
- shortlist_size = 20: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.01: mean relevance used over the shortlisted tests
- rel_max = 0.2: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.1: highest history score over all candidates
- hist_mean_shortlist = 0.0183228: mean history score over the shortlisted tests

Changed files (3):
- instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java
- itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java
- manual/src/main/asciidoc/user-guide/instances.adoc

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.itests.FelixHttpTest | 0.100 | 0.262 | 0.000 | 2.012
- org.apache.karaf.itests.InstanceTest | 0.000 | 1.000 | 0.200 | 30.095
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.067 | 0.376 | 0.000 | 2.231
- org.apache.karaf.main.MainTest | 0.000 | 0.751 | 0.000 | 0.032
- org.apache.karaf.itests.JmsTest | 0.040 | 0.453 | 0.000 | 54.386
- org.apache.karaf.tools.utils.KarafPropertiesEditorTest | 0.000 | 0.748 | 0.000 | 0.194
- org.apache.karaf.itests.XATest | 0.040 | 0.320 | 0.000 | 27.53
- org.apache.karaf.profile.assembly.BuilderTest | 0.000 | 0.748 | 0.000 | 1.597
- org.apache.karaf.config.core.impl.ConfigMBeanImplTest | 0.000 | 0.724 | 0.000 | 0.044
- org.apache.karaf.itests.examples.JmsExampleTest | 0.040 | 0.371 | 0.000 | 14.779
- org.apache.karaf.itests.LogTest | 0.020 | 0.289 | 0.000 | 2.859
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 0.701 | 0.000 | 0.038
- org.apache.karaf.instance.main.ExecuteTest | 0.000 | 0.689 | 0.000 | 0.105
- org.apache.karaf.itests.examples.ServletExampleTest | 0.017 | 0.228 | 0.000 | 71.536
- org.apache.karaf.instance.core.internal.InstanceServiceImplTest | 0.000 | 0.665 | 0.000 | 1.381
- org.apache.karaf.itests.examples.SoapExampleTest | 0.017 | 0.278 | 0.000 | 32.557
- org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest | 0.013 | 0.105 | 0.000 | 19.732
- org.apache.karaf.jpm.ProcessTest | 0.000 | 0.653 | 0.000 | 13.404
- org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest | 0.013 | 0.142 | 0.000 | 9.103
- org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest | 0.000 | 0.614 | 0.000 | 1.738

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
{"action": "final", "w": 0.7, "confidence": 0.8, "reason": "High relevance signal from specific changed files and low history failure rate."}
```

## 25. orchestrator · decision

- time: 2026-11-07T15:16:51.629Z
- latency: —

```json
{
  "w": 0.7,
  "confidence": 0.8,
  "source": "agent",
  "reason": "High relevance signal from specific changed files and low history failure rate.",
  "tool_calls": 0
}
```

## 26. pipeline · state

- time: 2026-11-07T15:16:51.866Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T15:16:51.883Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T15:16:51.903Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.BundleTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.WrapperTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.itests.examples.SoapExampleTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T15:16:52.008Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T15:16:52.028Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T15:16:52.047Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.spring_security_crypto.impl.SpringSecurityCryptoEncryptionTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T15:16:52.150Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T15:16:52.170Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T15:16:52.186Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.itests.features.Spring52FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T15:16:52.299Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T15:16:52.318Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T15:16:52.338Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.InstanceTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.itests.features.Spring52FeaturesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T15:16:52.458Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T15:16:52.478Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T15:16:52.496Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.itests.features.Spring52FeaturesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 41. pipeline · state

- time: 2026-11-07T15:16:52.550Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest"
  ]
}
```

## 42. explainer · explanation

- time: 2026-11-07T15:16:57.130Z
- latency: 4.564 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.JmsTest",
    "rank_by_value": 7,
    "n_candidates": 202,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.JmsTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 4,
      "failure_rate": 0.04,
      "last_failure_distance": 55,
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
    "history_score": 0.04,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the newly added PackageCommand class.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 54.386,
    "budget_s": 58.693,
    "remaining_budget_at_turn_s": 9.203,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 103.876
  },
  "justification": "Skipping it is reasonable: its relevance is 0.0 because it does not interact with the newly added PackageCommand class, and it only needs 54.386 s while 9.203 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "changed_files: instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
    "duration_s: 54.386",
    "remaining_budget_at_turn_s: 9.203"
  ],
  "ok": true,
  "error": null
}
```

## 43. explainer · explanation

- time: 2026-11-07T15:17:10.369Z
- latency: 13.220 s

```json
{
  "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "rank_by_value": 9,
    "n_candidates": 202,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.013,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 9.103,
    "budget_s": 58.693,
    "remaining_budget_at_turn_s": 5.052,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 62.744
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 44. explainer · explanation

- time: 2026-11-07T15:17:14.559Z
- latency: 4.170 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.FeatureTest",
    "rank_by_value": 10,
    "n_candidates": 202,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.FeatureTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 88,
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 8.954,
    "budget_s": 58.693,
    "remaining_budget_at_turn_s": 5.052,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 62.595
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 100 runs. It needs 8.954 s but only 5.052 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 100 runs",
    "duration_s: 8.954",
    "remaining_budget_at_turn_s: 5.052"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T15:17:28.406Z
- latency: 13.828 s

```json
{
  "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "rank_by_value": 11,
    "n_candidates": 202,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.013,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the PackageCommand or any related functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 19.732,
    "budget_s": 58.693,
    "remaining_budget_at_turn_s": 5.052,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 73.373
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 46. explainer · explanation

- time: 2026-11-07T15:17:42.344Z
- latency: 13.915 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 12,
    "n_candidates": 202,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.017,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 32.557,
    "budget_s": 58.693,
    "remaining_budget_at_turn_s": 5.052,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 86.198
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 47. pipeline · state

- time: 2026-11-07T15:17:42.417Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:17:46.126Z
- latency: 3.691 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.FeatureTest",
    "rank_by_value": 10,
    "n_candidates": 202,
    "n_selected": 23,
    "history": {
      "test": "org.apache.karaf.itests.FeatureTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 88,
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 8.954,
    "budget_s": 117.386,
    "remaining_budget_at_turn_s": 0.256,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 126.084
  },
  "justification": "Skipping it is risky: it has a failure rate of 0.01 and its duration of 8.954 s exceeds the remaining budget of 0.256 s.",
  "cited_facts": [
    "failures: 1 of 100 runs",
    "failure_rate: 0.01",
    "duration_s: 8.954",
    "remaining_budget_at_turn_s: 0.256"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T15:17:59.522Z
- latency: 13.376 s

```json
{
  "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "rank_by_value": 11,
    "n_candidates": 202,
    "n_selected": 23,
    "history": {
      "test": "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.013,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the PackageCommand or any related functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 19.732,
    "budget_s": 117.386,
    "remaining_budget_at_turn_s": 0.256,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 136.862
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 50. explainer · explanation

- time: 2026-11-07T15:18:12.258Z
- latency: 12.711 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 12,
    "n_candidates": 202,
    "n_selected": 23,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.017,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 32.557,
    "budget_s": 117.386,
    "remaining_budget_at_turn_s": 0.256,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 149.687
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 51. explainer · explanation

- time: 2026-11-07T15:18:24.638Z
- latency: 12.359 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JpaExampleTest",
    "rank_by_value": 13,
    "n_candidates": 202,
    "n_selected": 23,
    "history": {
      "test": "org.apache.karaf.itests.examples.JpaExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 31.461,
    "budget_s": 117.386,
    "remaining_budget_at_turn_s": 0.256,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 148.591
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 52. explainer · explanation

- time: 2026-11-07T15:18:37.187Z
- latency: 12.532 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 14,
    "n_candidates": 202,
    "n_selected": 23,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.017,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 71.536,
    "budget_s": 117.386,
    "remaining_budget_at_turn_s": 0.256,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 188.666
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 53. pipeline · state

- time: 2026-11-07T15:18:37.265Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.SoapExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.itests.features.Spring52FeaturesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest"
  ]
}
```

## 54. explainer · explanation

- time: 2026-11-07T15:18:51.158Z
- latency: 13.872 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 14,
    "n_candidates": 202,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
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
    "history_score": 0.017,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `PackageCommand` class or its functionality.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 71.536,
    "budget_s": 234.772,
    "remaining_budget_at_turn_s": 24.938,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 281.37
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 55. explainer · explanation

- time: 2026-11-07T15:19:01.847Z
- latency: 10.666 s

```json
{
  "test": "org.apache.karaf.itests.InstanceTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.InstanceTest",
    "rank_by_value": 15,
    "n_candidates": 202,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.InstanceTest",
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
    "relevance_used": 0.2,
    "relevance_reason": "The test class does not directly interact with the new PackageCommand class.",
    "changed_files": [
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 30.095,
    "budget_s": 234.772,
    "remaining_budget_at_turn_s": 24.938,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 239.929
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 56. explainer · explanation

- time: 2026-11-07T15:19:05.133Z
- latency: 3.269 s

```json
{
  "test": "org.apache.karaf.bundle.command.ListServicesTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.bundle.command.ListServicesTest",
    "rank_by_value": 65,
    "n_candidates": 202,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.bundle.command.ListServicesTest",
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 0.063,
    "budget_s": 234.772,
    "remaining_budget_at_turn_s": 0.005,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 234.83
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.063 s, which is less than the remaining budget of 0.005 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.063",
    "remaining_budget_at_turn_s: 0.005"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T15:19:08.413Z
- latency: 3.266 s

```json
{
  "test": "org.apache.karaf.client.ClientConfigTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.client.ClientConfigTest",
    "rank_by_value": 68,
    "n_candidates": 202,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.client.ClientConfigTest",
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 0.022,
    "budget_s": 234.772,
    "remaining_budget_at_turn_s": 0.001,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 234.793
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.022 s, which is negligible compared to the remaining budget of 0.001 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.022",
    "remaining_budget_at_turn_s: 0.001"
  ],
  "ok": true,
  "error": null
}
```

## 58. explainer · explanation

- time: 2026-11-07T15:19:11.746Z
- latency: 3.314 s

```json
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.config.command.EditCommandTest",
    "rank_by_value": 69,
    "n_candidates": 202,
    "n_selected": 27,
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
      "instance/src/main/java/org/apache/karaf/instance/command/PackageCommand.java",
      "itests/test/src/test/java/org/apache/karaf/itests/InstanceTest.java",
      "manual/src/main/asciidoc/user-guide/instances.adoc"
    ],
    "duration_s": 0.008,
    "budget_s": 234.772,
    "remaining_budget_at_turn_s": 0.001,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 234.779
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.008 s, which is negligible compared to the remaining budget of 0.001 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.008",
    "remaining_budget_at_turn_s: 0.001"
  ],
  "ok": true,
  "error": null
}
```
