# Trace of PR-1536_build2

Run: `E3_test_seed1` · events: 58

## 1. pipeline · state

- time: 2026-11-07T15:03:12.672Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 212,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T15:03:12.756Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 212
}
```

## 3. pipeline · state

- time: 2026-11-07T15:03:12.760Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.JmsExampleTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:15.930Z
- latency: 3.097 s

```json
{
  "test": "org.apache.karaf.itests.XATest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1609,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with logging configuration or services.",
  "confidence": 0.8
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:18.379Z
- latency: 2.439 s

```json
{
  "test": "org.apache.karaf.itests.examples.LogAppenderExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1252,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
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
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the LogServiceImpl or LogServiceLogbackXmlImpl classes.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:18.390Z
- latency: 3.354 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1590,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not appear to interact with logging or configuration settings, which are the primary focus of the code change.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:21.001Z
- latency: 2.600 s

```json
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1540,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not cover the new LogServiceLogbackXmlImpl class or its methods.",
  "confidence": 1
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:23.641Z
- latency: 2.632 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1582,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "relevance": 0.2,
  "reason": "The test class does not appear to interact with the LogService or its implementations.",
  "confidence": 0.8
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:26.425Z
- latency: 2.777 s

```json
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1512,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest` (source, may be truncated):
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

public class LogServiceLogbackXmlTest {

    @Test
    public void testInsertIndentedTabs() throws Exception {
        String xml = "<configuration>\n" +
                "</configuration>";

        String out = insertIndented(xml);
        assertEquals(
                "<configuration>\n" +
                        "\t<logger/>\n" +
                        "</configuration>", out);
    }

    @Test
    public void testInsertIndentedSpaces() throws Exception {
        //this one tests with one logger already added, because with no loggers there is no indentation to decide by and the function will choose tab
        String xml = "<configuration>\n" +
                "  <logger/>\n" +
                "</configuration>";

        String out = insertIndented(xml);
        assertEquals(
                "<configuration>\n" +
                        "  <logger/>\n" +
                        "  <logger/>\n" +
                        "</configuration>", out);
    }

    @Test
    public void testInsertIndentedTabsWithRoot() throws Exception {
        String xml = "<configuration>\n" +
                "\t<root/>\n" +
                "</configuration>";

        String out = insertIndented(xml);
        assertEquals(
                "<configuration>\n" +
                        "\t<root/>\n" +
                        "\t<logger/>\n" +
                        "</configuration>", out);
    }

    @Test
    public void testInsertIndentedSpacesWithRoot() throws Exception {
        String xml = "<configuration>\n" +
                "  <root/>\n" +
                "</configuration>";

        String out = insertIndented(xml);
        assertEquals(
                "<configuration>\n" +
                        "  <root/>\n" +
      
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
  "relevance": 0.2,
  "reason": "The test class does not directly test the new LogServiceLogbackXmlImpl class or its methods.",
  "confidence": 0.8
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:26.433Z
- latency: 2.359 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1583,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not appear to interact with logging configurations or services.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:28.956Z
- latency: 2.514 s

```json
{
  "test": "org.apache.karaf.main.util.BootstrapLogManagerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1415,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.main.util.BootstrapLogManagerTest` (source, may be truncated):
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
package org.apache.karaf.main.util;

import java.io.File;
import java.util.logging.Handler;

import org.apache.felix.utils.properties.Properties;
import org.junit.Assert;
import org.junit.Test;

public class BootstrapLogManagerTest {
	
	private Properties getConfigProperties() {
		Properties configProps = new Properties();
		configProps.put("karaf.log", "target/log");
		return configProps;
	}
	
	@Test
	public void testGetLogManagerNoProperties() {
		BootstrapLogManager.setProperties(getConfigProperties());
		try {
			BootstrapLogManager.getDefaultHandler();
		} catch (IllegalStateException e) {
			Assert.assertEquals("Properties must be set before calling getDefaultHandler", e.getMessage());
		}
	}
	
	@Test
	public void testGetLogManager() {
		new File("target/log/karaf.log").delete();
		BootstrapLogManager.setProperties(getConfigProperties());
		Handler handler = BootstrapLogManager.getDefaultHandler();
		Assert.assertNotNull(handler);
		assertExists("target/log/karaf.log");
	}
	
	@Test
	public void testGetLogManagerFromPaxLoggingConfig() {
		new File("target/test.log").delete();
		Properties configProps = getConfigProperties();
		BootstrapLogManager.setProperties(configProps, "src/test/resources/org.ops4j.pax.logging.cfg");
		Handler handler = BootstrapLogManager.getDefaultHandler();
		Assert.assertNotNull(handler);
		assertExists("target/test.log");
	}
	
	private void assertExists(String path) {
		Assert.assertTrue("File should exist at " + path, new File(path).exists());
	}
}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.main.util.BootstrapLogManagerTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.main.util.BootstrapLogManagerTest",
  "relevance": 0.1,
  "reason": "The test class does not directly interact with the LogServiceImpl or LogServiceLogbackXmlImpl classes.",
  "confidence": 0.8
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:28.964Z
- latency: 1.949 s

```json
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1289,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
    public void shutdownCommand() throws Exception {
        System.out.println(executeCommand("system:shutdown -f", new RolePrincipal("admin")));
    }

    @Test
    public void haltAlias() throws Exception {
        System.out.println(executeAlias("halt", new RolePrincipal("admin")));
    }

    @Test
    public void shutdownViaMBean() throws Exception {
        MBeanServer mbeanServer = ManagementFactory.getPlatformMBeanServer();
        ObjectName name = new ObjectName("org.apache.karaf:type=system,name=root");
        mbeanServer.invoke(name, "halt", new Object[]{}, new String[]{});
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
  "reason": "The test class does not interact with logging configurations or services.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:32.112Z
- latency: 3.141 s

```json
{
  "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1588,
  "completion_tokens": 78
}
```

**prompt**

```text
You help decide which regression tests to run for a code change.
Rate how likely it is that the test class below exercises the changed code,
so that it could fail because of this change.

Code change (unified diff, may be truncated):
<<<DIFF
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest` (source, may be truncated):
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
package org.apache.karaf.itests.mavenresolver;

import static org.junit.Assert.assertEquals;
import static org.ops4j.pax.exam.CoreOptions.composite;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.debugConfiguration;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.replaceConfigurationFile;

import java.io.File;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Test shows that without <code>org.ops4j.pax.url.mvn.requireConfigAdminConfig=true</code>,
 * there are two instances of MavenResolver service being published.
 */
@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class MavenResolverRegisteredBeforeConfigAdminTest extends KarafMinimalMonitoredTestSupport {

    public static Logger LOG = LoggerFactory.getLogger(MavenResolverRegisteredBeforeConfigAdminTest.class);

    @Configuration
    public Option[] config() throws Exception {
        return new Option[] {
        composite(super.baseConfig()),
        composite(editConfigurationFilePut("etc/org.apache.karaf.features.cfg", new File("target/test-classes/etc/org.apache.karaf.features.cfg"))),
        // etc/config.properties which doesn't have org.ops4j.pax.url.mvn.requireConfigAdminConfig=true
        replaceConfigurationFile("etc/config.properties", new File("target/test-classes/etc/config.properties")),
        // threaded=false, so we don't get:
        // java.io.IOException: Cannot bind to URL [rmi://:1099/karaf-root]: javax.naming.ServiceUnavailableException
        editConfigurationFilePut("etc/org.apache.karaf.management.cfg", "threaded", "false")
        };
    }

    @Test
    public void mavenResolverAvailable() throws Exception {
        long count = numberOfServiceEventsFor("org.ops4j.pax.url.mvn.MavenResolver");
        assertEquals("The
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the LogService or Logback configuration, which are the primary changes in the provided code diff.",
  "confidence": 0.8
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:34.692Z
- latency: 2.572 s

```json
{
  "test": "org.apache.karaf.itests.examples.CamelExampleTest",
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.examples.CamelExampleTest` (source, may be truncated):
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

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

import static org.junit.Assert.assertEquals;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class CamelExampleTest extends BaseTest {

    public void setup() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-camel-example-features/" + System.getProperty("karaf.version") + "/xml");
    }

    @Test(timeout = 60000)
    public void testJavaDSL() throws Exception {
        setup();
        installAndAssertFeature("karaf-camel-example-java");
        verify();
    }

    @Test(timeout = 60000)
    public void testBlueprintDSL() throws Exception {
        setup();
        installAndAssertFeature("karaf-camel-example-blueprint");
        verify();
    }

    public void verify() throws Exception {
        String output = executeCommand("camel:route-list");
        while (!output.contains("Started")) {
            Thread.sleep(500);
            output = executeCommand("camel:route-list");
        }
        System.out.println(output);

        URL url = new URL("http://localhost:9090/example");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setDoOutput(true);
        connection.setDoInput(true);

        PrintWriter writer = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
        writer.println("{ \"notification\": { \"type\": \"email\", \"to\": \"<email>\", \"message\": \"this is a test\" }}");
        writer.flush();
        writer.close();

        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String line;
        StringBuilder buffer = new StringBuilder();
        while ((line = reader
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.CamelExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.CamelExampleTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with logging configurations or services.",
  "confidence": 0.8
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:37.433Z
- latency: 2.733 s

```json
{
  "test": "org.apache.karaf.log.core.internal.SetLogLevelTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1510,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the new Logback XML configuration handling introduced in the code change.",
  "confidence": 0.8
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:40.079Z
- latency: 2.639 s

```json
{
  "test": "org.apache.karaf.itests.JavaSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1564,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.JavaSecurityTest` (source, may be truncated):
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

import org.apache.karaf.bundle.core.BundleInfo;
import org.apache.karaf.bundle.core.BundleService;
import org.apache.karaf.bundle.core.BundleState;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.MavenUtils;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.framework.Bundle;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.*;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;
import static org.ops4j.pax.exam.CoreOptions.maven;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.*;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class JavaSecurityTest extends BaseTest {

    @Configuration
    public Option[] config() {
        String version = MavenUtils.getArtifactVersion("org.apache.felix", "org.apache.felix.framework.security");
        String url = maven("org.apache.felix", "org.apache.felix.framework.security", version).getURL();
        Path temp;
        try {
            temp = Files.createTempFile("org.apache.felix.framework.security-" + version + "-", ".jar");
            System.setProperty("java.protocol.handler.pkgs", "org.ops4j.pax.url");
            try (InputStream is = new URL(url).openStream()) {
                Files.copy(is, temp, StandardCopyOption.REPLACE_EXISTING);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


        List<Option> options = new ArrayList<>(Arrays.asList(super.config()));
        // Add some extra options used by this test...
        options.addAll(Arrays.asList(
            editConfigurationFilePut("etc/system.properties", "java.security.policy", "${karaf.etc}/all.policy"),
            editConfigurationFilePut("etc/system.properties", "org.osgi.framework.security", "osgi"),
            editConfigurationFilePut("etc/system.properties", "org.osgi.framework.trust.repositories", "${karaf.etc}/trustStore.ks"),
            editConfigurationFilePut("etc/startup.properties", "mvn:org.apache.felix/org.apache.felix.framework.security/" + version
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.JavaSecurityTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.JavaSecurityTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with logging or configuration files, which are the primary focus of the code change.",
  "confidence": 1
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:40.089Z
- latency: 2.243 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "attempt": 0,
  "cached": true,
  "prompt_tokens": 1389,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not interact with logging configurations or services.",
  "confidence": 1
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:42.800Z
- latency: 2.703 s

```json
{
  "test": "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1439,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest` (source, may be truncated):
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
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.karaf.options.KarafDistributionOption;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ScrExampleWithEquinoxTest extends BaseTest {

    @Configuration
    public Option[] config() {
        List<Option> config = new LinkedList<>(Arrays.asList(super.config()));
        config.add(KarafDistributionOption.editConfigurationFilePut("etc/config.properties", "karaf.framework", "equinox"));
        return config.toArray(new Option[config.size()]);
    }

    @Test
    public void test() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-scr-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("karaf-scr-example-client");

        String output = executeCommand("scr:info BookingServiceMemoryImpl");
        System.out.println(output);
        assertContains("\"state\":32", output);

        output = executeCommand("scr:info ConsoleClient");
        System.out.println(output);
        assertContains("\"state\":32", output);
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the logging configuration or the LogService implementations.",
  "confidence": 0.8
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:45.382Z
- latency: 2.574 s

```json
{
  "test": "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1555,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class is related to LDAP authentication and does not involve logging or configuration handling.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:47.809Z
- latency: 2.419 s

```json
{
  "test": "org.apache.karaf.itests.EquinoxTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1312,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.EquinoxTest` (source, may be truncated):
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

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.karaf.options.KarafDistributionOption;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class EquinoxTest extends BaseTest {

    @Configuration
    public Option[] config() {
        List<Option> config = new LinkedList<>(Arrays.asList(super.config()));
        config.add(KarafDistributionOption.editConfigurationFilePut("etc/config.properties", "karaf.framework", "equinox"));
        return config.toArray(new Option[config.size()]);
    }

    @Test
    public void simpleTest() throws Exception {
        assertContains("org.eclipse.osgi", executeCommand("shell:info"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.EquinoxTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.EquinoxTest",
  "relevance": 0,
  "reason": "The test class does not appear to interact with the LogServiceImpl or LogServiceLogbackXmlImpl classes.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:50.433Z
- latency: 2.615 s

```json
{
  "test": "org.apache.karaf.itests.ExternalConfigTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1532,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.ExternalConfigTest` (source, may be truncated):
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

import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;
import org.osgi.service.cm.Configuration;

import java.io.BufferedWriter;
import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static java.nio.file.StandardOpenOption.CREATE;
import static java.nio.file.StandardOpenOption.TRUNCATE_EXISTING;
import static java.nio.file.StandardOpenOption.WRITE;
import static org.junit.Assert.*;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ExternalConfigTest extends BaseTest {

    @Test
    public void externalConfigTest() throws Exception {
        Path dir = Paths.get(System.getProperty("karaf.base"), "system/org/foo/bar/1.0-SNAPSHOT");
        Files.createDirectories(dir);
        
        writeTo(dir.resolve("bar-1.0-SNAPSHOT.properties"), //
                "key=value");

        writeTo(dir.resolve("bar-1.0-SNAPSHOT-features.xml"), // 
                "<features name='org.foo'>\n" +
                "  <feature name='bar' version='1.0-SNAPSHOT'>\n" +
                "    <config name='org.foo' external='true'>\n" +
                "      mvn:org.foo/bar/1.0-SNAPSHOT/properties" +
                "    </config>\n" +
                "  </feature>\n" +
                "</features>\n");

        Configuration[] cfgs = configurationAdmin.listConfigurations("(service.pid=org.foo)");
        assertNull(cfgs);

        featureService.addRepository(URI.create("mvn:org.foo/bar/1.0-SNAPSHOT/xml/features"), true);

        cfgs = configurationAdmin.listConfigurations("(service.pid=org.foo)");
        assertNotNull(cfgs);
        assertEquals(1, cfgs.length);
        assertEquals("value", cfgs[0].getProcessedProperties(null).get("key"));
    }

    private void writeTo(Path file, String content) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(file, CREATE, TRUNCATE_EXISTING, WRITE)) {
            w.write(content);
        }
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.ExternalConfigTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.ExternalConfigTest",
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the LogServiceImpl or LogServiceLogbackXmlImpl classes.",
  "confidence": 0.8
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:52.838Z
- latency: 2.394 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1523,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not appear to interact with logging configuration or LogService implementations.",
  "confidence": 1
}
```

## 23. semantic_analyzer · llm_call

- time: 2026-11-07T15:03:55.605Z
- latency: 2.759 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1616,
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
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
--- a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
@@ -59,6 +59,14 @@ else if (config.get("org.ops4j.pax.logging.log4j2.config.file") != null) {
                 throw new IllegalStateException("Unsupported Log4j2 configuration type: " + file);
             }
         }
+        else if (config.get("org.ops4j.pax.logging.logback.config.file") != null) {
+            String file = config.get("org.ops4j.pax.logging.logback.config.file").toString();
+            if (file.endsWith(".xml")) {
+                return new LogServiceLogbackXmlImpl(file);
+            } else {
+                throw new IllegalStateException("Unsupported Logback configuration type: " + file);
+            }
+        }
         else {
             throw new IllegalStateException("Unrecognized configuration");
         }
diff --git a/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
new file mode 100644
--- /dev/null
+++ b/log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
@@ -0,0 +1,258 @@
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
+package org.apache.karaf.log.core.internal;
+
+import org.apache.karaf.log.core.Level;
+import org.w3c.dom.Document;
+import org.w3c.dom.Element;
+import org.w3c.dom.Node;
+import org.w3c.dom.NodeList;
+import org.xml.sax.InputSource;
+import org.xml.sax.SAXException;
+
+import javax.xml.XMLConstants;
+import javax.xml.parsers.DocumentBuilder;
+import javax.xml.parsers.DocumentBuilderFactory;
+import javax.xml.parsers.ParserConfigurationException;
+import javax.xml.transform.Transformer;
+import javax.xml.transform.TransformerFactory;
+import javax.xml.transform.dom.DOMSource;
+import javax.xml.transform.stream.StreamResult;
+import java.io.IOException;
+import java.io.InputStream;
+import java.io.OutputStream;
+import java.nio.file.Files;
+import java.nio.file.Path;
+impor
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
  "reason": "The test class does not appear to interact with logging or configuration settings, which are the primary areas affected by the code change.",
  "confidence": 1
}
```

## 24. orchestrator · llm_call

- time: 2026-11-07T15:03:58.753Z
- latency: 2.955 s

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
- n_code_files = 4: number of changed code files in the diff
- n_dirs = 3: number of distinct folders those files are in
- lines_added = 397: added lines in the diff
- lines_removed = 0: removed lines in the diff
- recent_failure_density = 0.1: share of the last 10 history builds with at least one failing test
- n_candidates = 212: number of candidate test classes
- shortlist_size = 20: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.075: mean relevance used over the shortlisted tests
- rel_max = 0.2: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.0877193: highest history score over all candidates
- hist_mean_shortlist = 0.0168443: mean history score over the shortlisted tests

Changed files (4):
- log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java
- log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java
- log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java
- manual/src/main/asciidoc/user-guide/log.adoc

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.itests.XATest | 0.088 | 0.540 | 0.100 | 31.652
- org.apache.karaf.itests.examples.LogAppenderExampleTest | 0.000 | 1.000 | 0.200 | 1.081
- org.apache.karaf.itests.examples.JpaExampleTest | 0.073 | 0.333 | 0.000 | 34.772
- org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest | 0.000 | 1.000 | 0.000 | 0.057
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.042 | 0.709 | 0.200 | 0.455
- org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest | 0.000 | 1.000 | 0.200 | 0.371
- org.apache.karaf.itests.JmsTest | 0.021 | 0.610 | 0.000 | 57.567
- org.apache.karaf.main.util.BootstrapLogManagerTest | 0.000 | 1.000 | 0.100 | 0.002
- org.apache.karaf.itests.SystemShutdownTest | 0.021 | 0.276 | 0.000 | 34.484
- org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest | 0.000 | 0.939 | 0.100 | 9.993
- org.apache.karaf.itests.examples.CamelExampleTest | 0.021 | 0.288 | 0.100 | 39.115
- org.apache.karaf.log.core.internal.SetLogLevelTest | 0.000 | 0.882 | 0.200 | 0.082
- org.apache.karaf.itests.JavaSecurityTest | 0.000 | 0.877 | 0.000 | 0.248
- org.apache.karaf.itests.examples.JdbcExampleTest | 0.021 | 0.427 | 0.000 | 12.566
- org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest | 0.000 | 0.831 | 0.100 | 1.947
- org.apache.karaf.jaas.modules.ldap.LdapCacheTest | 0.020 | 0.252 | 0.000 | 0.815
- org.apache.karaf.itests.EquinoxTest | 0.000 | 0.801 | 0.000 | 1.582
- org.apache.karaf.itests.ExternalConfigTest | 0.010 | 0.595 | 0.200 | 0.529
- org.apache.karaf.itests.JMXSecurityTest | 0.010 | 0.498 | 0.000 | 16.351
- org.apache.karaf.itests.examples.JmsExampleTest | 0.010 | 0.761 | 0.000 | 13.065

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
{"action": "final", "w": 0.3, "confidence": 0.8, "reason": "Low relevance signal and weak history indicate a need to trust relevance more."}
```

## 25. orchestrator · decision

- time: 2026-11-07T15:03:58.773Z
- latency: —

```json
{
  "w": 0.3,
  "confidence": 0.8,
  "source": "agent",
  "reason": "Low relevance signal and weak history indicate a need to trust relevance more.",
  "tool_calls": 0
}
```

## 26. pipeline · state

- time: 2026-11-07T15:03:59.030Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.util.JsonReaderTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T15:03:59.051Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.util.JsonReaderTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T15:03:59.069Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.features.FeatureTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.util.JsonReaderTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.PackageTest",
    "org.apache.karaf.itests.JndiTest",
    "org.apache.karaf.shell.ssh.keygenerator.OpenSSHGeneratorKeyFileProviderTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.itests.examples.BlueprintExampleTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.itests.ObrTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.itests.examples.CdiExampleTest",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.BundleTest",
    "org.apache.karaf.itests.WrapperTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T15:03:59.162Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T15:03:59.178Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.main.lock.StatementsTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T15:03:59.194Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T15:03:59.301Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.main.lock.StatementsTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T15:03:59.317Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T15:03:59.334Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T15:03:59.432Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T15:03:59.449Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T15:03:59.465Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.main.lock.StatementsTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T15:03:59.559Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T15:03:59.576Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T15:03:59.592Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 41. pipeline · state

- time: 2026-11-07T15:03:59.638Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 42. explainer · explanation

- time: 2026-11-07T15:04:12.793Z
- latency: 13.136 s

```json
{
  "test": "org.apache.karaf.itests.examples.JpaExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JpaExampleTest",
    "rank_by_value": 10,
    "n_candidates": 212,
    "n_selected": 25,
    "history": {
      "test": "org.apache.karaf.itests.examples.JpaExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 7,
      "failure_rate": 0.07291666666666667,
      "last_failure_distance": 14,
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
    "history_score": 0.073,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with logging or configuration settings, which are the primary focus of the code change.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 34.772,
    "budget_s": 59.176,
    "remaining_budget_at_turn_s": 23.626,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 70.322
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 43. explainer · explanation

- time: 2026-11-07T15:04:27.298Z
- latency: 14.488 s

```json
{
  "test": "org.apache.karaf.itests.examples.CamelExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.CamelExampleTest",
    "rank_by_value": 11,
    "n_candidates": 212,
    "n_selected": 25,
    "history": {
      "test": "org.apache.karaf.itests.examples.CamelExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 39.115,
    "budget_s": 59.176,
    "remaining_budget_at_turn_s": 23.626,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 74.665
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 44. explainer · explanation

- time: 2026-11-07T15:04:40.233Z
- latency: 12.917 s

```json
{
  "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "rank_by_value": 15,
    "n_candidates": 212,
    "n_selected": 25,
    "history": {
      "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
      "history_builds": 100,
      "runs": 96,
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
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the LogService or Logback configuration, which are the primary changes in the provided code diff.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 9.993,
    "budget_s": 59.176,
    "remaining_budget_at_turn_s": 6.783,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 62.386
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 45. explainer · explanation

- time: 2026-11-07T15:04:52.474Z
- latency: 12.222 s

```json
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.SystemShutdownTest",
    "rank_by_value": 16,
    "n_candidates": 212,
    "n_selected": 25,
    "history": {
      "test": "org.apache.karaf.itests.SystemShutdownTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 34.484,
    "budget_s": 59.176,
    "remaining_budget_at_turn_s": 6.783,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 86.877
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 46. explainer · explanation

- time: 2026-11-07T15:05:05.442Z
- latency: 12.948 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JmsExampleTest",
    "rank_by_value": 17,
    "n_candidates": 212,
    "n_selected": 25,
    "history": {
      "test": "org.apache.karaf.itests.examples.JmsExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
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
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with logging or configuration settings, which are the primary areas affected by the code change.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 13.065,
    "budget_s": 59.176,
    "remaining_budget_at_turn_s": 6.783,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 65.458
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 47. pipeline · state

- time: 2026-11-07T15:05:05.536Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest"
  ]
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:05:09.570Z
- latency: 4.019 s

```json
{
  "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
    "rank_by_value": 14,
    "n_candidates": 212,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.JdbcExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 12.566,
    "budget_s": 118.353,
    "remaining_budget_at_turn_s": 4.639,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 126.28
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 because it does not interact with logging configurations or services, and it only needs 12.566 s but only 4.639 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 12.566",
    "remaining_budget_at_turn_s: 4.639"
  ],
  "ok": true,
  "error": null
}
```

## 49. explainer · explanation

- time: 2026-11-07T15:05:22.705Z
- latency: 13.113 s

```json
{
  "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "rank_by_value": 15,
    "n_candidates": 212,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
      "history_builds": 100,
      "runs": 96,
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
    "relevance_used": 0.1,
    "relevance_reason": "The test class does not appear to interact with the LogService or Logback configuration, which are the primary changes in the provided code diff.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 9.993,
    "budget_s": 118.353,
    "remaining_budget_at_turn_s": 4.639,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 123.707
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 50. explainer · explanation

- time: 2026-11-07T15:05:35.747Z
- latency: 13.017 s

```json
{
  "test": "org.apache.karaf.itests.SystemShutdownTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.SystemShutdownTest",
    "rank_by_value": 16,
    "n_candidates": 212,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.SystemShutdownTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
        0,
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 34.484,
    "budget_s": 118.353,
    "remaining_budget_at_turn_s": 4.639,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 148.198
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 51. explainer · explanation

- time: 2026-11-07T15:05:48.602Z
- latency: 12.836 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JmsExampleTest",
    "rank_by_value": 17,
    "n_candidates": 212,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.examples.JmsExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
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
        0
      ]
    },
    "history_score": 0.01,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with logging or configuration settings, which are the primary areas affected by the code change.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 13.065,
    "budget_s": 118.353,
    "remaining_budget_at_turn_s": 4.639,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 126.779
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 52. explainer · explanation

- time: 2026-11-07T15:05:52.672Z
- latency: 4.058 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.JmsTest",
    "rank_by_value": 18,
    "n_candidates": 212,
    "n_selected": 26,
    "history": {
      "test": "org.apache.karaf.itests.JmsTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 57.567,
    "budget_s": 118.353,
    "remaining_budget_at_turn_s": 4.639,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 171.281
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 because it does not appear to interact with logging configurations or services, and it only needs 57.567 s but only 4.639 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 57.567",
    "remaining_budget_at_turn_s: 4.639"
  ],
  "ok": true,
  "error": null
}
```

## 53. pipeline · state

- time: 2026-11-07T15:05:52.753Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.log.core.internal.LogServiceLogbackXmlTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JpaExampleTest",
    "org.apache.karaf.itests.examples.CamelExampleTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.shell.ssh.SshUtilsTest",
    "org.apache.karaf.itests.examples.JdbcExampleTest",
    "org.apache.karaf.itests.mavenresolver.MavenResolverRegisteredBeforeConfigAdminTest",
    "org.apache.karaf.itests.SystemShutdownTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.main.MainLockingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest"
  ]
}
```

## 54. explainer · explanation

- time: 2026-11-07T15:05:56.765Z
- latency: 3.996 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.JmsTest",
    "rank_by_value": 18,
    "n_candidates": 212,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.itests.JmsTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 2,
      "failure_rate": 0.020833333333333332,
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
        0
      ]
    },
    "history_score": 0.021,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not appear to interact with logging configurations or services.",
    "changed_files": [
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 57.567,
    "budget_s": 236.706,
    "remaining_budget_at_turn_s": 52.884,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 241.389
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 because it does not appear to interact with logging configurations or services, and it only needs 57.567 s, which fits within the remaining budget of 52.884 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 57.567",
    "remaining_budget_at_turn_s: 52.884"
  ],
  "ok": true,
  "error": null
}
```

## 55. explainer · explanation

- time: 2026-11-07T15:06:01.360Z
- latency: 4.581 s

```json
{
  "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
    "rank_by_value": 21,
    "n_candidates": 212,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.itests.ssh.ConfigSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 51,
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
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 44.779,
    "budget_s": 236.706,
    "remaining_budget_at_turn_s": 11.306,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 270.179
  },
  "justification": "Skipping it is risky: it has a failure rate of 0.0104 and its duration of 44.779 s exceeds the remaining budget of 11.306 s.",
  "cited_facts": [
    "failures: 1 of 96 runs",
    "failure_rate: 0.010416666666666666",
    "duration_s: 44.779",
    "remaining_budget_at_turn_s: 11.306"
  ],
  "ok": true,
  "error": null
}
```

## 56. explainer · explanation

- time: 2026-11-07T15:06:13.685Z
- latency: 12.307 s

```json
{
  "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
    "rank_by_value": 22,
    "n_candidates": 212,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.itests.examples.ConfigExampleTest",
      "history_builds": 100,
      "runs": 96,
      "failures": 1,
      "failure_rate": 0.010416666666666666,
      "last_failure_distance": 23,
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
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 60.988,
    "budget_s": 236.706,
    "remaining_budget_at_turn_s": 11.306,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 286.388
  },
  "justification": "Skipping it is risky: it has a low relevance score of 0.0 and has failed once in 96 runs, indicating potential issues. It needs 60.988 s but only 11.306 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 96 runs",
    "duration_s: 60.988",
    "remaining_budget_at_turn_s: 11.306"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T15:06:26.384Z
- latency: 12.682 s

```json
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "rank_by_value": 70,
    "n_candidates": 212,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
      "history_builds": 100,
      "runs": 98,
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
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 0.111,
    "budget_s": 236.706,
    "remaining_budget_at_turn_s": 0.005,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 236.812
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 58. explainer · explanation

- time: 2026-11-07T15:06:29.724Z
- latency: 3.326 s

```json
{
  "test": "org.apache.karaf.config.command.EditCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.config.command.EditCommandTest",
    "rank_by_value": 72,
    "n_candidates": 212,
    "n_selected": 47,
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
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceImpl.java",
      "log/src/main/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlImpl.java",
      "log/src/test/java/org/apache/karaf/log/core/internal/LogServiceLogbackXmlTest.java",
      "manual/src/main/asciidoc/user-guide/log.adoc"
    ],
    "duration_s": 0.088,
    "budget_s": 236.706,
    "remaining_budget_at_turn_s": 0.005,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 236.789
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.088 s, which is less than the remaining budget of 0.005 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.088",
    "remaining_budget_at_turn_s: 0.005"
  ],
  "ok": true,
  "error": null
}
```
