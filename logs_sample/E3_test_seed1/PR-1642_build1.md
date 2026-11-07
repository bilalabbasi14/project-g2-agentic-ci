# Trace of PR-1642_build1

Run: `E3_test_seed1` · events: 58

## 1. pipeline · state

- time: 2026-11-07T15:19:14.596Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 210,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T15:19:14.691Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 210
}
```

## 3. pipeline · state

- time: 2026-11-07T15:19:14.697Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.itests.LogTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:18.025Z
- latency: 3.262 s

```json
{
  "test": "org.apache.karaf.features.command.ListFeaturesCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1417,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
        EasyMock.expect(repo.getName()).andReturn("repository");
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
        EasyMock.expect(feature.isBlacklisted()).andReturn(
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
  "relevance": 0.2,
  "reason": "The test class does not include any tests that specifically target the changes made in the ListFeaturesCommand class.",
  "confidence": 0.8
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:20.571Z
- latency: 2.539 s

```json
{
  "test": "org.apache.karaf.itests.examples.GraphQLExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1485,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.examples.GraphQLExampleTest` (source, may be truncated):
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

import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.karaf.itests.BaseTest;
import org.apache.karaf.itests.util.SimpleSocket;
import org.eclipse.jetty.websocket.client.ClientUpgradeRequest;
import org.eclipse.jetty.websocket.client.WebSocketClient;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerMethod;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

import static junit.framework.TestCase.assertTrue;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerMethod.class)
public class GraphQLExampleTest extends BaseTest {

    private void setUp() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-graphql-example-features/" + System.getProperty("karaf.version") + "/xml");
        installAndAssertFeature("karaf-graphql-example");
    }

    @Test
    public void testServlet() throws Exception {
        setUp();

        String getBooksQuery = "{ books { name id } }";
        String booksRequestResult = sendGetRequest(getBooksQuery);

        assertContains("\"name\":\"Apache Karaf Cookbook\"", booksRequestResult);
        assertContains("\"id\":\"1\"", booksRequestResult);
        assertContains("\"name\":\"Effective Java\"", booksRequestResult);
        assertContains("\"id\":\"2\"", booksRequestResult);

        String addBookQuery = "mutation { addBook(name:\"Lord of the Rings\" pageCount:100) { id name } }";
        String addBookRequestResult = sendPostRequest(addBookQuery);
        assertContains("id", addBookRequestResult);
        assertContains("Lord of the Rings", addBookRequestResult);

        String getBooksByIdQuery = "{ bookById(id:4) { name } }";
        String getBookByIdRequestResult = sendGetRequest(getBooksByIdQuery);
        assertContains("Lord of the Rings", getBookByIdRequestResult);
    }

    @Test
    public void testCommand() throws Exception {
        setUp();
        String getBooksQuery = "\"{ books { name id } }\"";
        String output = ex
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.itests.examples.GraphQLExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.GraphQLExampleTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of its dependencies.",
  "confidence": 1
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:23.176Z
- latency: 2.594 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1492,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
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

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.ops4j.pax.exam.karaf.options.KarafDistributionOption.editConfigurationFilePut;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.openmbean.TabularData;

import org.apache.karaf.features.FeatureState;
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
        assertFalse(featureListOutput.isEmpty()
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
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the `ListFeaturesCommand` class or its methods.",
  "confidence": 0.8
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:25.583Z
- latency: 2.396 s

```json
{
  "test": "org.apache.karaf.itests.FelixHttpTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1335,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any related classes.",
  "confidence": 1
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:28.209Z
- latency: 2.619 s

```json
{
  "test": "org.apache.karaf.features.command.RepoListCommandTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1452,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
DIFF>>>

Test class `org.apache.karaf.features.command.RepoListCommandTest` (source, may be truncated):
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

import org.apache.karaf.features.FeaturesService;
import org.apache.karaf.features.Repository;
import org.easymock.Capture;
import org.easymock.CaptureType;
import org.easymock.EasyMock;
import org.junit.Test;
import shaded.org.apache.commons.lang3.StringUtils;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.net.URI;

import static org.junit.Assert.*;

public class RepoListCommandTest extends RepositoryCommandTestBase {

    @Test
    public void testListReposAfterReload() throws Exception {
        FeaturesService service = EasyMock.createMock(FeaturesService.class);

        String repoName = "SomeRepository";
        Repository repo = mockRepository(repoName, "1.0.0");
        EasyMock.expect(repo.isBlacklisted()).andReturn(false);

        EasyMock.expect(service.listRepositories()).andReturn(new Repository[]{repo}).anyTimes();
        Capture<URI> uriCapture = Capture.newInstance(CaptureType.ALL);
        service.addRepository(EasyMock.capture(uriCapture));
        EasyMock.expectLastCall().times(1);

        EasyMock.replay(service, repo);

        RepoListCommand repoListCommand = new RepoListCommand();
        repoListCommand.setFeaturesService(service);
        repoListCommand.showBlacklisted = false;
        repoListCommand.noFormat = true;
        repoListCommand.reload = true;

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(baos);
        System.setOut(out);

        repoListCommand.execute();
        out.flush();

        assertEquals(repo.getURI(), uriCapture.getValue());

        String commandOutput = baos.toString();
        assertTrue(commandOutput.contains(repoName + "\t" + repo.getURI()));

        EasyMock.verify(service, repo);
    }

    @Test
    public void testBlacklistedRepositoriesNotShown() throws Exception {
        FeaturesService service = EasyMock.createMock(FeaturesService.class);
        Repository blacklistedRepo = EasyMock.createMock(Repository.class);
        EasyMock.expect(blacklistedRepo.isBlacklisted()).andReturn(true);

        String whitelistedRepoName = "SomeRepository";
        R
[...truncated]
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.features.command.RepoListCommandTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.features.command.RepoListCommandTest",
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the `ListFeaturesCommand` class or its methods.",
  "confidence": 0.8
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:30.970Z
- latency: 2.754 s

```json
{
  "test": "org.apache.karaf.itests.XATest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1537,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not appear to interact with the `ListFeaturesCommand` class or its dependencies.",
  "confidence": 0.8
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:33.680Z
- latency: 2.699 s

```json
{
  "test": "org.apache.karaf.features.internal.region.SubsystemTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1469,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the `ListFeaturesCommand` class or its dependencies.",
  "confidence": 0.8
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:36.359Z
- latency: 2.671 s

```json
{
  "test": "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1510,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:39.020Z
- latency: 2.653 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1511,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:41.538Z
- latency: 2.510 s

```json
{
  "test": "org.apache.karaf.itests.examples.SchedulerExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1227,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 14. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:44.113Z
- latency: 2.568 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1544,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of its dependencies.",
  "confidence": 1
}
```

## 15. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:46.629Z
- latency: 2.508 s

```json
{
  "test": "org.apache.karaf.itests.examples.LogAppenderExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1180,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "relevance": 0,
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 16. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:49.333Z
- latency: 2.695 s

```json
{
  "test": "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1530,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the `ListFeaturesCommand` class or its dependencies.",
  "confidence": 0.9
}
```

## 17. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:51.930Z
- latency: 2.586 s

```json
{
  "test": "org.apache.karaf.itests.examples.HttpResourceExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1404,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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

    @Test(timeout = 600000L)
    public void test() throws Exception {
        addFeaturesRepository("mvn:org.apache.karaf.examples/karaf-http-resource-example-features/" + System.getProperty("karaf.version") + "/xml");

        installAndAssertFeature("pax-web-karaf");
        installAndAssertFeature("karaf-http-resource-example-whiteboard");

        String command = executeCommand("web:servlet-list");
        while (!command.contains("/example/*")) {
            Thread.sleep(200);
            command = executeCommand("web:servlet-list");
        }
        assertContains("ResourceServlet", command);
        assertContains("Whiteboard", command);

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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any related classes.",
  "confidence": 1
}
```

## 18. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:54.523Z
- latency: 2.583 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1451,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
  "confidence": 1
}
```

## 19. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:57.077Z
- latency: 2.543 s

```json
{
  "test": "org.apache.karaf.itests.examples.ScrExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1242,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
DIFF>>>

Test class `org.apache.karaf.itests.examples.ScrExampleTest` (source, may be truncated):
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
public class ScrExampleTest extends BaseTest {

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
{"test": "org.apache.karaf.itests.examples.ScrExampleTest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.itests.examples.ScrExampleTest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 20. semantic_analyzer · llm_call

- time: 2026-11-07T15:19:59.531Z
- latency: 2.448 s

```json
{
  "test": "org.apache.karaf.examples.itests.ExampleWithConfigITest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1235,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
DIFF>>>

Test class `org.apache.karaf.examples.itests.ExampleWithConfigITest` (source, may be truncated):
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

import org.apache.karaf.itests.KarafTestSupport;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.ops4j.pax.exam.Configuration;
import org.ops4j.pax.exam.Option;
import org.ops4j.pax.exam.junit.PaxExam;
import org.ops4j.pax.exam.karaf.options.KarafDistributionOption;
import org.ops4j.pax.exam.spi.reactors.ExamReactorStrategy;
import org.ops4j.pax.exam.spi.reactors.PerClass;

import java.util.stream.Stream;

@RunWith(PaxExam.class)
@ExamReactorStrategy(PerClass.class)
public class ExampleWithConfigITest extends KarafTestSupport {

    @Configuration
    public Option[] config() {
        Option[] options = new Option[]{
                KarafDistributionOption.editConfigurationFilePut("etc/system.properties", "my.system.property", System.getProperty("my.system.property"))
        };
        return Stream.of(super.config(), options).flatMap(Stream::of).toArray(Option[]::new);
    }

    @Test
    public void simpleTest() throws Exception {
        System.out.println("==== System Property in probe bundle: " + System.getProperty("my.system.property"));
        assertContains("foo", System.getProperty("my.system.property"));
    }

}
TEST>>>

Answer with a single JSON object and nothing else:
{"test": "org.apache.karaf.examples.itests.ExampleWithConfigITest", "relevance": <number from 0 to 1>, "reason": "<one short sentence>", "confidence": <number from 0 to 1>}
relevance: 0 = unrelated, 1 = directly tests the changed code.
confidence: how sure you are of the relevance value.
```

**response**

```text
{
  "test": "org.apache.karaf.examples.itests.ExampleWithConfigITest",
  "relevance": 0,
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 21. semantic_analyzer · llm_call

- time: 2026-11-07T15:20:01.716Z
- latency: 2.177 s

```json
{
  "test": "org.apache.karaf.itests.examples.CommandExampleTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1224,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
[...truncated]
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
  "relevance": 0,
  "reason": "The test class does not interact with the `ListFeaturesCommand` class or its functionality.",
  "confidence": 1
}
```

## 22. semantic_analyzer · llm_call

- time: 2026-11-07T15:20:04.305Z
- latency: 2.581 s

```json
{
  "test": "org.apache.karaf.features.internal.model.JsonTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1504,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "relevance": 0.1,
  "reason": "The test class does not appear to interact with the `ListFeaturesCommand` class or its dependencies.",
  "confidence": 0.9
}
```

## 23. semantic_analyzer · llm_call

- time: 2026-11-07T15:20:06.949Z
- latency: 2.637 s

```json
{
  "test": "org.apache.karaf.itests.LogTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1487,
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
diff --git a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
--- a/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
+++ b/features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
@@ -17,14 +17,15 @@
 package org.apache.karaf.features.command;
 
 import java.util.Arrays;
-import java.util.Collections;
 import java.util.Comparator;
 import java.util.List;
 
 import org.apache.karaf.features.Feature;
 import org.apache.karaf.features.FeaturesService;
 import org.apache.karaf.features.Repository;
+import org.apache.karaf.features.command.completers.InstalledRepoNameCompleter;
 import org.apache.karaf.shell.api.action.Command;
+import org.apache.karaf.shell.api.action.Completion;
 import org.apache.karaf.shell.api.action.Option;
 import org.apache.karaf.shell.api.action.lifecycle.Service;
 import org.apache.karaf.shell.support.table.Row;
@@ -49,12 +50,16 @@ public class ListFeaturesCommand extends FeaturesCommandSupport {
     @Option(name = "-o", aliases = {"--ordered"}, description = "Display a list using alphabetical order ", required = false, multiValued = false)
     boolean ordered;
 
+    @Option(name = "--repository", description = "Only list features from that repository", required = false, multiValued = false)
+    @Completion(InstalledRepoNameCompleter.class)
+    String repository;
+
     @Option(name = "--no-format", description = "Disable table rendered output", required = false, multiValued = false)
     boolean noFormat;
 
     protected void doExecute(FeaturesService featuresService) throws Exception {
         boolean needsLegend = false;
-        
+
         ShellTable table = new ShellTable();
         table.column("Name");
         table.column("Version");
@@ -67,43 +72,16 @@ protected void doExecute(FeaturesService featuresService) throws Exception {
         }
         table.emptyTableText(onlyInstalled ? "No features installed" : "No features available");
 
-        List<Repository> repos = Arrays.asList(featuresService.listRepositories());
-        for (Repository r : repos) {
-            List<Feature> features = Arrays.asList(r.getFeatures());
-            if (ordered) {
-                features.sort(new FeatureComparator());
-            }
-            for (Feature f : features) {
-                if (onlyInstalled && !featuresService.isInstalled(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (onlyRequired && !featuresService.isRequired(f)) {
-                    // Filter out not installed features if we only want to see the installed ones
-                    continue;
-                }
-                if (!showBlacklisted && f.isBlacklisted()) {
-                    // Filter out blackli
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
  "reason": "The test class does not interact with the `ListFeaturesCommand` or any of the changes made in the code diff.",
  "confidence": 1
}
```

## 24. orchestrator · llm_call

- time: 2026-11-07T15:20:09.990Z
- latency: 2.888 s

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
- lines_added = 123: added lines in the diff
- lines_removed = 41: removed lines in the diff
- recent_failure_density = 0.3: share of the last 10 history builds with at least one failing test
- n_candidates = 210: number of candidate test classes
- shortlist_size = 20: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.045: mean relevance used over the shortlisted tests
- rel_max = 0.2: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0.402016: highest history score over all candidates
- hist_mean_shortlist = 0.0336339: mean history score over the shortlisted tests

Changed files (3):
- features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java
- features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java
- itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.features.command.ListFeaturesCommandTest | 0.000 | 1.000 | 0.200 | 0.007
- org.apache.karaf.itests.examples.GraphQLExampleTest | 0.402 | 0.162 | 0.000 | 62.407
- org.apache.karaf.itests.FeatureTest | 0.000 | 1.000 | 0.200 | 9.435
- org.apache.karaf.itests.FelixHttpTest | 0.070 | 0.113 | 0.000 | 1.898
- org.apache.karaf.features.command.RepoListCommandTest | 0.000 | 0.508 | 0.100 | 0.062
- org.apache.karaf.itests.XATest | 0.040 | 0.190 | 0.100 | 25.244
- org.apache.karaf.features.internal.region.SubsystemTest | 0.000 | 0.436 | 0.100 | 0.248
- org.apache.karaf.itests.ConfigManagedServiceFactoryTest | 0.040 | 0.065 | 0.000 | 1.27
- org.apache.karaf.itests.JmsTest | 0.040 | 0.169 | 0.000 | 43.895
- org.apache.karaf.itests.examples.SchedulerExampleTest | 0.000 | 0.427 | 0.000 | 2.181
- org.apache.karaf.itests.examples.JmsExampleTest | 0.030 | 0.230 | 0.000 | 15.022
- org.apache.karaf.itests.examples.LogAppenderExampleTest | 0.000 | 0.423 | 0.000 | 1.646
- org.apache.karaf.features.internal.region.FeaturesDependenciesTest | 0.000 | 0.415 | 0.100 | 0.128
- org.apache.karaf.itests.examples.HttpResourceExampleTest | 0.020 | 0.251 | 0.000 | 3.938
- org.apache.karaf.itests.JMXSecurityTest | 0.010 | 0.075 | 0.000 | 16.982
- org.apache.karaf.itests.examples.ScrExampleTest | 0.000 | 0.405 | 0.000 | 2.2
- org.apache.karaf.examples.itests.ExampleWithConfigITest | 0.010 | 0.099 | 0.000 | 1.082
- org.apache.karaf.itests.examples.CommandExampleTest | 0.000 | 0.400 | 0.000 | 1.832
- org.apache.karaf.features.internal.model.JsonTest | 0.000 | 0.395 | 0.100 | 0.091
- org.apache.karaf.itests.LogTest | 0.010 | 0.250 | 0.000 | 3.785

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
{"action": "final", "w": 0.7, "confidence": 0.8, "reason": "High relevance signal from specific changed files and low recent failure density."}
```

## 25. orchestrator · decision

- time: 2026-11-07T15:20:10.007Z
- latency: —

```json
{
  "w": 0.7,
  "confidence": 0.8,
  "source": "agent",
  "reason": "High relevance signal from specific changed files and low recent failure density.",
  "tool_calls": 0
}
```

## 26. pipeline · state

- time: 2026-11-07T15:20:10.230Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.features.command.RepoAddCommandTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.features.command.RepoRemoveCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.command.RepoRefreshCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T15:20:10.247Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.features.command.RepoAddCommandTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.features.command.RepoRemoveCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.command.RepoRefreshCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.examples.itests.ExampleITest",
    "org.apache.karaf.itests.examples.BundleExampleTest",
    "org.apache.karaf.itests.ServiceTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.itests.JaasTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T15:20:10.268Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.features.command.RepoAddCommandTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.packages.command.PackageImportTest",
    "org.apache.karaf.features.command.RepoRemoveCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.util.ParserTest",
    "org.apache.karaf.features.command.RepoRefreshCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.tooling.features.ManifestUtilsTest",
    "org.apache.karaf.tooling.features.AddToRepositoryMojoTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.shell.tabletest.ShellTableTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.bundle.command.bundletree.TreeTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.tooling.VerifyMojoTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.tooling.features.BundleToArtifactTest",
    "org.apache.karaf.tooling.features.MavenUtilTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.service.interceptor.impl.runtime.proxy.AsmProxyFactoryTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.bundle.command.ListServicesTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.ssh.KarafJaasAuthenticatorTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.tooling.features.GenerateDescriptorMojoTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.examples.LogAppenderExampleTest",
    "org.apache.karaf.itests.ExternalConfigTest",
    "org.apache.karaf.itests.OverrideConfigTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.itests.examples.CommandExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.itests.examples.SchedulerExampleTest",
    "org.apache.karaf.itests.SystemTest",
    "org.apache.karaf.profile.assembly.BuilderTest",
    "org.apache.karaf.itests.examples.ScrExampleTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.itests.examples.NamespaceHandlerExampleTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.itests.KarTest",
    "org.apache.karaf.itests.examples.ScrExampleWithEquinoxTest",
    "org.apache.karaf.itests.ConfigTest",
    "org.apache.karaf.itests.EquinoxTest",
    "org.apache.karaf.itests.examples.DeployerExampleTest",
    "org.apache.karaf.itests.JavaSecurityTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.service.guard.impl.GuardProxyCatalogTest",
    "org.apache.karaf.itests.ImportServiceTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T15:20:10.380Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T15:20:10.403Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.main.util.BootstrapLogManagerTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T15:20:10.421Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.itests.ssh.SshKeyFormatTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptableConfigAdminPropertyPlaceholderTest",
    "org.apache.karaf.jaas.blueprint.jasypt.handler.EncryptablePropertyPlaceholderTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.config.command.EditCommandTest"
  ]
}
```

## 32. pipeline · state

- time: 2026-11-07T15:20:10.538Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 33. pipeline · state

- time: 2026-11-07T15:20:10.554Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 34. pipeline · state

- time: 2026-11-07T15:20:10.576Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 35. pipeline · state

- time: 2026-11-07T15:20:10.682Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 36. pipeline · state

- time: 2026-11-07T15:20:10.703Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 37. pipeline · state

- time: 2026-11-07T15:20:10.719Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 38. pipeline · state

- time: 2026-11-07T15:20:10.836Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 39. pipeline · state

- time: 2026-11-07T15:20:10.858Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 40. pipeline · state

- time: 2026-11-07T15:20:10.880Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 41. pipeline · state

- time: 2026-11-07T15:20:10.941Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 42. explainer · explanation

- time: 2026-11-07T15:20:23.488Z
- latency: 12.527 s

```json
{
  "test": "org.apache.karaf.itests.examples.GraphQLExampleTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "rank_by_value": 7,
    "n_candidates": 210,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.examples.GraphQLExampleTest",
      "history_builds": 100,
      "runs": 5,
      "failures": 2,
      "failure_rate": 0.4,
      "last_failure_distance": 1,
      "recent_outcomes": [
        null,
        null,
        null,
        null,
        null,
        null,
        1,
        0,
        0,
        1
      ]
    },
    "history_score": 0.402,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of its dependencies.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 62.407,
    "budget_s": 54.328,
    "remaining_budget_at_turn_s": 50.872,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 65.863
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 43. explainer · explanation

- time: 2026-11-07T15:20:36.958Z
- latency: 13.454 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.JmsTest",
    "rank_by_value": 13,
    "n_candidates": 210,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.JmsTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 4,
      "failure_rate": 0.04,
      "last_failure_distance": 19,
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
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 43.895,
    "budget_s": 54.328,
    "remaining_budget_at_turn_s": 5.338,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 92.885
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 44. explainer · explanation

- time: 2026-11-07T15:20:47.449Z
- latency: 10.471 s

```json
{
  "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "rank_by_value": 15,
    "n_candidates": 210,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 22,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 9.623,
    "budget_s": 54.328,
    "remaining_budget_at_turn_s": 1.553,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 62.398
  },
  "justification": "Skipping it is risky: it has a low relevance of 0.0 and has failed once in 100 runs. It needs 9.623 s but only 1.553 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 100 runs",
    "duration_s: 9.623",
    "remaining_budget_at_turn_s: 1.553"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T15:20:58.592Z
- latency: 11.126 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.FeatureTest",
    "rank_by_value": 16,
    "n_candidates": 210,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.FeatureTest",
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
    "relevance_reason": "The test class does not directly interact with the `ListFeaturesCommand` class or its methods.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 9.435,
    "budget_s": 54.328,
    "remaining_budget_at_turn_s": 1.553,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 62.21
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 46. explainer · explanation

- time: 2026-11-07T15:21:10.280Z
- latency: 11.666 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.itests.JMXSecurityTest",
    "rank_by_value": 17,
    "n_candidates": 210,
    "n_selected": 27,
    "history": {
      "test": "org.apache.karaf.itests.JMXSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 10,
      "recent_outcomes": [
        1,
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
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 16.982,
    "budget_s": 54.328,
    "remaining_budget_at_turn_s": 1.553,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 69.757
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 47. pipeline · state

- time: 2026-11-07T15:21:10.365Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:21:23.674Z
- latency: 13.289 s

```json
{
  "test": "org.apache.karaf.itests.examples.JmsExampleTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.JmsExampleTest",
    "rank_by_value": 12,
    "n_candidates": 210,
    "n_selected": 29,
    "history": {
      "test": "org.apache.karaf.itests.examples.JmsExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 3,
      "failure_rate": 0.03,
      "last_failure_distance": 74,
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
    "history_score": 0.03,
    "relevance_used": 0.0,
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of its dependencies.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 15.022,
    "budget_s": 108.655,
    "remaining_budget_at_turn_s": 12.28,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 111.397
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 49. explainer · explanation

- time: 2026-11-07T15:21:37.284Z
- latency: 13.593 s

```json
{
  "test": "org.apache.karaf.itests.JmsTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.JmsTest",
    "rank_by_value": 13,
    "n_candidates": 210,
    "n_selected": 29,
    "history": {
      "test": "org.apache.karaf.itests.JmsTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 4,
      "failure_rate": 0.04,
      "last_failure_distance": 19,
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
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 43.895,
    "budget_s": 108.655,
    "remaining_budget_at_turn_s": 12.28,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 140.27
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 50. explainer · explanation

- time: 2026-11-07T15:21:41.698Z
- latency: 4.401 s

```json
{
  "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "rank_by_value": 15,
    "n_candidates": 210,
    "n_selected": 29,
    "history": {
      "test": "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 22,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 9.623,
    "budget_s": 108.655,
    "remaining_budget_at_turn_s": 8.495,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 109.783
  },
  "justification": "Skipping it is reasonable: it has a low relevance score of 0.0 and has only failed once in 100 runs. It needs 9.623 s but only 8.495 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "failures: 1 of 100 runs",
    "duration_s: 9.623",
    "remaining_budget_at_turn_s: 8.495"
  ],
  "ok": true,
  "error": null
}
```

## 51. explainer · explanation

- time: 2026-11-07T15:21:52.764Z
- latency: 11.047 s

```json
{
  "test": "org.apache.karaf.itests.FeatureTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.FeatureTest",
    "rank_by_value": 16,
    "n_candidates": 210,
    "n_selected": 29,
    "history": {
      "test": "org.apache.karaf.itests.FeatureTest",
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
    "relevance_reason": "The test class does not directly interact with the `ListFeaturesCommand` class or its methods.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 9.435,
    "budget_s": 108.655,
    "remaining_budget_at_turn_s": 8.495,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 109.595
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 52. explainer · explanation

- time: 2026-11-07T15:22:05.671Z
- latency: 12.890 s

```json
{
  "test": "org.apache.karaf.itests.JMXSecurityTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.itests.JMXSecurityTest",
    "rank_by_value": 17,
    "n_candidates": 210,
    "n_selected": 29,
    "history": {
      "test": "org.apache.karaf.itests.JMXSecurityTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 10,
      "recent_outcomes": [
        1,
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
    "relevance_reason": "The test class does not interact with the `ListFeaturesCommand` or any of the classes it uses.",
    "changed_files": [
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 16.982,
    "budget_s": 108.655,
    "remaining_budget_at_turn_s": 8.495,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 117.142
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 53. pipeline · state

- time: 2026-11-07T15:22:05.745Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.itests.FelixHttpTest",
    "org.apache.karaf.itests.ConfigManagedServiceFactoryTest",
    "org.apache.karaf.features.command.RepoListCommandTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.itests.examples.GraphQLExampleTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.itests.XATest",
    "org.apache.karaf.itests.examples.HttpResourceExampleTest",
    "org.apache.karaf.examples.itests.ExampleWithConfigITest",
    "org.apache.karaf.itests.examples.JmsExampleTest",
    "org.apache.karaf.itests.JmsTest",
    "org.apache.karaf.itests.LogTest",
    "org.apache.karaf.itests.ssh.FeatureSshCommandSecurityTest",
    "org.apache.karaf.itests.FeatureTest",
    "org.apache.karaf.itests.JMXSecurityTest",
    "org.apache.karaf.itests.ssh.BundleSshCommandSecurityTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.jaas.command.ManageRealmCommandTest",
    "org.apache.karaf.jaas.jasypt.impl.JasyptEncryptionTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.config.command.EditCommandTest",
    "org.apache.karaf.packages.core.internal.filter.ExpressionTokenizerTest"
  ]
}
```

## 54. explainer · explanation

- time: 2026-11-07T15:22:18.282Z
- latency: 12.519 s

```json
{
  "test": "org.apache.karaf.itests.examples.SoapExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.SoapExampleTest",
    "rank_by_value": 19,
    "n_candidates": 210,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.examples.SoapExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 21,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 27.436,
    "budget_s": 217.311,
    "remaining_budget_at_turn_s": 3.89,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 240.857
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 55. explainer · explanation

- time: 2026-11-07T15:22:30.703Z
- latency: 12.400 s

```json
{
  "test": "org.apache.karaf.itests.examples.ServletExampleTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.itests.examples.ServletExampleTest",
    "rank_by_value": 20,
    "n_candidates": 210,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.itests.examples.ServletExampleTest",
      "history_builds": 100,
      "runs": 100,
      "failures": 1,
      "failure_rate": 0.01,
      "last_failure_distance": 21,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 71.313,
    "budget_s": 217.311,
    "remaining_budget_at_turn_s": 3.89,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 284.734
  },
  "justification": null,
  "cited_facts": [],
  "ok": false,
  "error": "schema_violation"
}
```

## 56. explainer · explanation

- time: 2026-11-07T15:22:33.929Z
- latency: 3.206 s

```json
{
  "test": "org.apache.karaf.bundle.command.ListServicesTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.bundle.command.ListServicesTest",
    "rank_by_value": 72,
    "n_candidates": 210,
    "n_selected": 33,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 0.061,
    "budget_s": 217.311,
    "remaining_budget_at_turn_s": 0.01,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 217.362
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.061 s, which is less than the remaining budget of 0.01 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.061",
    "remaining_budget_at_turn_s: 0.01"
  ],
  "ok": true,
  "error": null
}
```

## 57. explainer · explanation

- time: 2026-11-07T15:22:37.425Z
- latency: 3.482 s

```json
{
  "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
    "rank_by_value": 74,
    "n_candidates": 210,
    "n_selected": 33,
    "history": {
      "test": "org.apache.karaf.bundle.core.internal.MavenConfigServiceTest",
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 0.106,
    "budget_s": 217.311,
    "remaining_budget_at_turn_s": 0.01,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 217.407
  },
  "justification": "Skipping it is reasonable: it has a relevance score of 0.0 and a very short duration of 0.106 s, which fits within the remaining budget of 0.01 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.106",
    "remaining_budget_at_turn_s: 0.01"
  ],
  "ok": true,
  "error": null
}
```

## 58. explainer · explanation

- time: 2026-11-07T15:22:40.886Z
- latency: 3.447 s

```json
{
  "test": "org.apache.karaf.client.ClientConfigTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.client.ClientConfigTest",
    "rank_by_value": 75,
    "n_candidates": 210,
    "n_selected": 33,
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
      "features/command/src/main/java/org/apache/karaf/features/command/ListFeaturesCommand.java",
      "features/command/src/test/java/org/apache/karaf/features/command/ListFeaturesCommandTest.java",
      "itests/test/src/test/java/org/apache/karaf/itests/FeatureTest.java"
    ],
    "duration_s": 0.022,
    "budget_s": 217.311,
    "remaining_budget_at_turn_s": 0.01,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 217.323
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.022 s, which is very short but still uses up a significant portion of the remaining budget of 0.01 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.022",
    "remaining_budget_at_turn_s: 0.01"
  ],
  "ok": true,
  "error": null
}
```
