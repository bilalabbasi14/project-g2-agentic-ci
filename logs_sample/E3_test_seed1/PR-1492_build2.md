# Trace of PR-1492_build2

Run: `E3_test_seed1` · events: 48

## 1. pipeline · state

- time: 2026-11-07T14:58:49.305Z
- latency: —

```json
{
  "stage": "loaded",
  "n_candidates": 114,
  "n_history_builds": 100
}
```

## 2. pipeline · state

- time: 2026-11-07T14:58:49.383Z
- latency: —

```json
{
  "stage": "dante_scored",
  "n_candidates": 114
}
```

## 3. pipeline · state

- time: 2026-11-07T14:58:49.387Z
- latency: —

```json
{
  "stage": "shortlisted",
  "shortlist": [
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest"
  ]
}
```

## 4. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:52.729Z
- latency: 3.323 s

```json
{
  "test": "org.apache.karaf.kar.internal.KarTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1676,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "relevance": 0.1,
  "reason": "The test class does not directly interact with the Karaf Maven plugin or its functionality.",
  "confidence": 0.8
}
```

## 5. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:55.822Z
- latency: 3.086 s

```json
{
  "test": "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1698,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "relevance": 0.2,
  "reason": "The test class does not directly interact with the KarMojo class or the KarArtifactInstallerTest class, which are the primary targets of the code change.",
  "confidence": 0.8
}
```

## 6. semantic_analyzer · llm_call

- time: 2026-11-07T14:58:57.953Z
- latency: 2.123 s

```json
{
  "test": "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1330,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven plugin or its functionality.",
  "confidence": 1
}
```

## 7. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:00.458Z
- latency: 2.497 s

```json
{
  "test": "org.apache.karaf.obr.command.util.FileUtilTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1586,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "relevance": 0.1,
  "reason": "The test class does not directly interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 0.8
}
```

## 8. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:02.901Z
- latency: 2.435 s

```json
{
  "test": "org.apache.karaf.features.internal.service.LocationPatternTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1738,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 9. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:05.361Z
- latency: 2.452 s

```json
{
  "test": "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1612,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 10. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:07.722Z
- latency: 2.352 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1637,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 11. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:10.099Z
- latency: 2.369 s

```json
{
  "test": "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1578,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 12. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:12.592Z
- latency: 2.486 s

```json
{
  "test": "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1692,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 13. semantic_analyzer · llm_call

- time: 2026-11-07T14:59:14.986Z
- latency: 2.384 s

```json
{
  "test": "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
  "attempt": 0,
  "cached": false,
  "prompt_tokens": 1635,
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
diff --git a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
--- a/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
+++ b/tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
@@ -19,11 +19,31 @@
 
 import java.io.*;
 import java.lang.*;
+import java.util.*;
+import java.util.zip.*;
 
 // check if the kar archive has been pushed to the repository
 File generated = new File(basedir, "target/test-kar-packaging-1.0-SNAPSHOT.kar");
-if (generated.exists()) {
-    return true;
+if (!generated.exists()) {
+    return false;
 }
 
-return false;
\ No newline at end of file
+// check Reproducible Builds outputTimestamp
+ZipFile zipFile = new ZipFile(generated);
+Enumeration entries = zipFile.entries();
+long timestamp = -1;
+
+while(entries.hasMoreElements()) {
+    ZipEntry entry = entries.nextElement();
+    long t = entry.getTime();
+    if (timestamp == -1) {
+        timestamp = t;
+    }
+    if (t != timestamp) {
+        System.out.println(entry.getName() + " entry last modified = " + t + ", expected " + timestamp);
+        return false;
+    }
+}
+zipFile.close();
+
+return true;
\ No newline at end of file
diff --git a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
--- a/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
+++ b/tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java
@@ -124,6 +124,16 @@ public class KarMojo extends MojoSupport {
     @Parameter(defaultValue = "${repositoryPath}")
     private String repositoryPath = "repository/";
 
+    /**
+     * Timestamp for reproducible output archive entries, either formatted as ISO 8601
+     * <code>yyyy-MM-dd'T'HH:mm:ssXXX</code> or as an int representing seconds since the epoch (like
+     * <a href="https://reproducible-builds.org/docs/source-date-epoch/">SOURCE_DATE_EPOCH</a>).
+     *
+     * @since 4.4.0
+     */
+    @Parameter(defaultValue = "${project.build.outputTimestamp}")
+    private String outputTimestamp;
+    
     private static final Pattern mvnPattern = Pattern.compile("mvn:([^/ ]+)/([^/ ]+)/([^/ ]*)(/([^/ ]+)(/([^/ ]+))?)?");
 
 
@@ -246,10 +256,13 @@ private File createArchive(List<Artifact> bundles, File featuresFile, String gro
         File archiveFile = getArchiveFile(outputDirectory, finalName, classifier);
 
         MavenArchiver archiver = new MavenArchiver();
+        archiver.setCreatedBy("Kar Maven Plugin", "org.apache.karaf.tooling", "karaf-maven-plugin");
         MavenArchiveConfiguration configuration = new MavenArchiveConfiguration();
         configuration.addManifestEntries(archive.getManifestEntries());
         archiver.setArchiver(jarArchiver);
         archiver.setOutputFile(archiveFile);
+        // configure for Reproducible Builds based on outputTimestamp value
+        arch
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
  "reason": "The test class does not interact with the Karaf Maven Plugin or its functionality.",
  "confidence": 1
}
```

## 14. orchestrator · llm_call

- time: 2026-11-07T14:59:17.655Z
- latency: 2.535 s

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
- n_dirs = 2: number of distinct folders those files are in
- lines_added = 38: added lines in the diff
- lines_removed = 5: removed lines in the diff
- recent_failure_density = 0: share of the last 10 history builds with at least one failing test
- n_candidates = 114: number of candidate test classes
- shortlist_size = 10: number of shortlisted test classes (shown below)
- rel_mean_shortlist = 0.04: mean relevance used over the shortlisted tests
- rel_max = 0.2: highest relevance used over all candidates
- n_rel_ge_05 = 0: shortlisted tests with relevance >= 0.5
- hist_max = 0: highest history score over all candidates
- hist_mean_shortlist = 0: mean history score over the shortlisted tests

Changed files (2):
- tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh
- tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java

Shortlisted tests (test | history | tfidf relevance | llm relevance | duration s):
- org.apache.karaf.kar.internal.KarTest | 0.000 | 1.000 | 0.100 | 1.717
- org.apache.karaf.deployer.kar.KarArtifactInstallerTest | 0.000 | 0.882 | 0.200 | 0.064
- org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest | 0.000 | 0.726 | 0.000 | 0.27
- org.apache.karaf.obr.command.util.FileUtilTest | 0.000 | 0.723 | 0.100 | 0.029
- org.apache.karaf.features.internal.service.LocationPatternTest | 0.000 | 0.656 | 0.000 | 0.008
- org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest | 0.000 | 0.640 | 0.000 | 0.655
- org.apache.karaf.features.internal.service.FeaturesProcessorTest | 0.000 | 0.638 | 0.000 | 0.613
- org.apache.karaf.features.internal.service.FeatureConfigInstallerTest | 0.000 | 0.633 | 0.000 | 0.003
- org.apache.karaf.features.internal.service.BootFeaturesInstallerTest | 0.000 | 0.625 | 0.000 | 0.173
- org.apache.karaf.config.core.impl.JsonConfigInstallerTest | 0.000 | 0.572 | 0.000 | 0.153

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
{"action": "final", "w": 0.2, "confidence": 0.8, "reason": "Low relevance and no recent failures indicate a need to trust history more."}
```

## 15. orchestrator · decision

- time: 2026-11-07T14:59:17.672Z
- latency: —

```json
{
  "w": 0.2,
  "confidence": 0.8,
  "source": "agent",
  "reason": "Low relevance and no recent failures indicate a need to trust history more.",
  "tool_calls": 0
}
```

## 16. pipeline · state

- time: 2026-11-07T14:59:17.952Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest"
  ]
}
```

## 17. pipeline · state

- time: 2026-11-07T14:59:17.970Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest"
  ]
}
```

## 18. pipeline · state

- time: 2026-11-07T14:59:17.988Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.config.core.impl.KarafConfigurationPluginTest",
    "org.apache.karaf.config.command.UpdateCommandTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.config.core.impl.ConfigMBeanImplTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.config.core.impl.JsonConfigInstallerTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.client.ClientConfigTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.audit.util.FastDateFormatTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.deployer.blueprint.BlueprintDeploymentListenerTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.deployer.spring.SpringDeploymentListenerTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest"
  ]
}
```

## 19. pipeline · state

- time: 2026-11-07T14:59:18.076Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.instance.command.CreateCommandTest"
  ]
}
```

## 20. pipeline · state

- time: 2026-11-07T14:59:18.090Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest"
  ]
}
```

## 21. pipeline · state

- time: 2026-11-07T14:59:18.104Z
- latency: —

```json
{
  "stage": "selected",
  "method": "DANTE-CCH-shipped",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.webconsole.instance.InstancePluginTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.support.ShellUtilTest",
    "org.apache.karaf.event.command.EventDisplayCommandTest",
    "org.apache.karaf.event.command.EventPrinterTest",
    "org.apache.karaf.event.command.EventSendCommandTest",
    "org.apache.karaf.event.command.EventTailCommandTest",
    "org.apache.karaf.event.service.EventCollectorTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.features.AppendTest",
    "org.apache.karaf.features.ConditionalTest",
    "org.apache.karaf.features.FeaturesServiceTest",
    "org.apache.karaf.features.RepositoryTest",
    "org.apache.karaf.features.command.ListFeaturesCommandTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.model.JsonTest",
    "org.apache.karaf.features.internal.osgi.ActivatorTest",
    "org.apache.karaf.features.internal.region.FeaturesDependenciesTest",
    "org.apache.karaf.features.internal.region.SubsystemTest",
    "org.apache.karaf.features.internal.repository.RepositoryTest",
    "org.apache.karaf.features.internal.service.BlacklistTest",
    "org.apache.karaf.features.internal.service.BootFeaturesInstallerTest",
    "org.apache.karaf.features.internal.service.DeployerTest",
    "org.apache.karaf.features.internal.service.FeatureConfigInstallerTest",
    "org.apache.karaf.features.internal.service.FeaturePatternTest",
    "org.apache.karaf.features.internal.service.FeaturesProcessorTest",
    "org.apache.karaf.features.internal.service.FeaturesServiceImplTest",
    "org.apache.karaf.features.internal.service.FeaturesValidationTest",
    "org.apache.karaf.features.internal.service.LocationPatternTest",
    "org.apache.karaf.features.internal.service.OverridesTest",
    "org.apache.karaf.features.internal.service.StateStorageTest",
    "org.apache.karaf.features.management.codec.JmxFeatureTest",
    "org.apache.karaf.features.management.codec.JmxRepositoryTest",
    "org.apache.karaf.http.core.internal.HttpMBeanImplTest",
    "org.apache.karaf.http.core.internal.proxy.BalancingPoliciesTest",
    "org.apache.karaf.instance.command.CreateCommandTest",
    "org.apache.karaf.instance.core.InstanceSettingsTest",
    "org.apache.karaf.instance.core.internal.InstanceServiceImplTest",
    "org.apache.karaf.instance.core.management.internal.InstanceServiceMBeanImplTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.main.ExecuteTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.jaas.modules.jdbc.JdbcLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.BadReferenceTest",
    "org.apache.karaf.jaas.modules.ldap.LDAPPubkeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCacheTest",
    "org.apache.karaf.jaas.modules.ldap.LdapCaseInsensitiveDNTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest"
  ]
}
```

## 22. pipeline · state

- time: 2026-11-07T14:59:18.183Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest"
  ]
}
```

## 23. pipeline · state

- time: 2026-11-07T14:59:18.196Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest"
  ]
}
```

## 24. pipeline · state

- time: 2026-11-07T14:59:18.208Z
- latency: —

```json
{
  "stage": "selected",
  "method": "LLM-relevance",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.command.CreateCommandTest"
  ]
}
```

## 25. pipeline · state

- time: 2026-11-07T14:59:18.291Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest"
  ]
}
```

## 26. pipeline · state

- time: 2026-11-07T14:59:18.305Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest"
  ]
}
```

## 27. pipeline · state

- time: 2026-11-07T14:59:18.318Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Tuned-weight (LLM)",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.command.CreateCommandTest"
  ]
}
```

## 28. pipeline · state

- time: 2026-11-07T14:59:18.403Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest"
  ]
}
```

## 29. pipeline · state

- time: 2026-11-07T14:59:18.420Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest"
  ]
}
```

## 30. pipeline · state

- time: 2026-11-07T14:59:18.435Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Agent-weighted",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.command.CreateCommandTest"
  ]
}
```

## 31. pipeline · state

- time: 2026-11-07T14:59:18.472Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.05,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest"
  ]
}
```

## 32. explainer · explanation

- time: 2026-11-07T14:59:21.752Z
- latency: 3.264 s

```json
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.audit.logger.EventLoggerTest",
    "rank_by_value": 37,
    "n_candidates": 114,
    "n_selected": 31,
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 1.315,
    "budget_s": 4.368,
    "remaining_budget_at_turn_s": 0.038,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 5.645
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration of 1.315 s exceeds the remaining budget of 0.038 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 1.315",
    "remaining_budget_at_turn_s: 0.038"
  ],
  "ok": true,
  "error": null
}
```

## 33. explainer · explanation

- time: 2026-11-07T14:59:25.101Z
- latency: 3.329 s

```json
{
  "test": "org.apache.karaf.features.RepositoryTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.features.RepositoryTest",
    "rank_by_value": 66,
    "n_candidates": 114,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.features.RepositoryTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.008,
    "budget_s": 4.368,
    "remaining_budget_at_turn_s": 0.002,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.374
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.008 s, which is less than the remaining budget of 0.002 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.008",
    "remaining_budget_at_turn_s: 0.002"
  ],
  "ok": true,
  "error": null
}
```

## 34. explainer · explanation

- time: 2026-11-07T14:59:28.478Z
- latency: 3.363 s

```json
{
  "test": "org.apache.karaf.features.FeaturesServiceTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.features.FeaturesServiceTest",
    "rank_by_value": 67,
    "n_candidates": 114,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.features.FeaturesServiceTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.068,
    "budget_s": 4.368,
    "remaining_budget_at_turn_s": 0.002,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.434
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.068 s, which is less than the remaining budget of 0.002 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.068",
    "remaining_budget_at_turn_s: 0.002"
  ],
  "ok": true,
  "error": null
}
```

## 35. explainer · explanation

- time: 2026-11-07T14:59:31.649Z
- latency: 3.153 s

```json
{
  "test": "org.apache.karaf.features.ConditionalTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.features.ConditionalTest",
    "rank_by_value": 68,
    "n_candidates": 114,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.features.ConditionalTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.905,
    "budget_s": 4.368,
    "remaining_budget_at_turn_s": 0.002,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 5.271
  },
  "justification": "Skipping it is reasonable: it has no relevance and its duration of 0.905 s is less than the remaining budget of 0.002 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.905",
    "remaining_budget_at_turn_s: 0.002"
  ],
  "ok": true,
  "error": null
}
```

## 36. explainer · explanation

- time: 2026-11-07T14:59:35.025Z
- latency: 3.361 s

```json
{
  "test": "org.apache.karaf.features.AppendTest",
  "budget": 0.05,
  "evidence": {
    "test": "org.apache.karaf.features.AppendTest",
    "rank_by_value": 69,
    "n_candidates": 114,
    "n_selected": 31,
    "history": {
      "test": "org.apache.karaf.features.AppendTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.024,
    "budget_s": 4.368,
    "remaining_budget_at_turn_s": 0.002,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 4.39
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.024 s, which is less than the remaining budget of 0.002 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.024",
    "remaining_budget_at_turn_s: 0.002"
  ],
  "ok": true,
  "error": null
}
```

## 37. pipeline · state

- time: 2026-11-07T14:59:35.097Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.1,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest"
  ]
}
```

## 38. explainer · explanation

- time: 2026-11-07T14:59:38.281Z
- latency: 3.169 s

```json
{
  "test": "org.apache.karaf.audit.logger.EventLoggerTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.audit.logger.EventLoggerTest",
    "rank_by_value": 37,
    "n_candidates": 114,
    "n_selected": 47,
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 1.315,
    "budget_s": 8.735,
    "remaining_budget_at_turn_s": 0.69,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 9.36
  },
  "justification": "Skipping it is reasonable: it has no relevance and its duration of 1.315 s is well within the remaining budget of 0.69 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 1.315",
    "remaining_budget_at_turn_s: 0.69"
  ],
  "ok": true,
  "error": null
}
```

## 39. explainer · explanation

- time: 2026-11-07T14:59:41.044Z
- latency: 2.750 s

```json
{
  "test": "org.apache.karaf.features.RepositoryTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.features.RepositoryTest",
    "rank_by_value": 66,
    "n_candidates": 114,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.features.RepositoryTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.008,
    "budget_s": 8.735,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 8.743
  },
  "justification": "Skipping it is reasonable: it has a duration of 0.008 s, which fits within the remaining budget of 0.0 s when it was reached.",
  "cited_facts": [
    "duration_s: 0.008",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 40. explainer · explanation

- time: 2026-11-07T14:59:44.118Z
- latency: 3.061 s

```json
{
  "test": "org.apache.karaf.features.FeaturesServiceTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.features.FeaturesServiceTest",
    "rank_by_value": 67,
    "n_candidates": 114,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.features.FeaturesServiceTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.068,
    "budget_s": 8.735,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 8.803
  },
  "justification": "Skipping it is reasonable: it has no relevance and its duration is 0.068 s, which fits within the remaining budget of 0.0 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.068",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 41. explainer · explanation

- time: 2026-11-07T14:59:47.277Z
- latency: 3.146 s

```json
{
  "test": "org.apache.karaf.features.ConditionalTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.features.ConditionalTest",
    "rank_by_value": 68,
    "n_candidates": 114,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.features.ConditionalTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.905,
    "budget_s": 8.735,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 9.64
  },
  "justification": "Skipping it is reasonable: it has no relevance and its duration of 0.905 s is less than the remaining budget of 0.0 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.905",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 42. explainer · explanation

- time: 2026-11-07T14:59:50.562Z
- latency: 3.268 s

```json
{
  "test": "org.apache.karaf.features.AppendTest",
  "budget": 0.1,
  "evidence": {
    "test": "org.apache.karaf.features.AppendTest",
    "rank_by_value": 69,
    "n_candidates": 114,
    "n_selected": 47,
    "history": {
      "test": "org.apache.karaf.features.AppendTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.024,
    "budget_s": 8.735,
    "remaining_budget_at_turn_s": 0.0,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 8.759
  },
  "justification": "Skipping it is reasonable: it has a relevance score of 0.0 and a very short duration of 0.024 s, which fits within the remaining budget of 0.0 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.024",
    "remaining_budget_at_turn_s: 0.0"
  ],
  "ok": true,
  "error": null
}
```

## 43. pipeline · state

- time: 2026-11-07T14:59:50.637Z
- latency: —

```json
{
  "stage": "selected",
  "method": "Full system",
  "budget": 0.2,
  "selected": [
    "org.apache.karaf.deployer.kar.KarArtifactInstallerTest",
    "org.apache.karaf.obr.command.util.FileUtilTest",
    "org.apache.karaf.kar.internal.KarTest",
    "org.apache.karaf.maven.SettingsTest",
    "org.apache.karaf.management.internal.JMXSecurityMBeanImplTestCase",
    "org.apache.karaf.management.KarafMBeanServerGuardTest",
    "org.apache.karaf.main.lock.StatementsTest",
    "org.apache.karaf.main.lock.PostgreSQLJDBCLockTest",
    "org.apache.karaf.main.lock.OracleJDBCLockTest",
    "org.apache.karaf.main.lock.MySQLJDBCLockTest",
    "org.apache.karaf.main.lock.DerbyJDBCLockTest",
    "org.apache.karaf.main.lock.DefaultJDBCLockTest",
    "org.apache.karaf.main.MainTest",
    "org.apache.karaf.main.MainStartTest",
    "org.apache.karaf.maven.command.MavenConfigurationSupportTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2XmlImplTest",
    "org.apache.karaf.log.core.internal.LogServiceLog4j2ImplTest",
    "org.apache.karaf.jaas.modules.syncope.SyncopeLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyLoginModuleTest",
    "org.apache.karaf.jaas.modules.publickey.PublicKeyEncodingTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesLoginModuleTest",
    "org.apache.karaf.jaas.modules.properties.PropertiesBackingEngineTest",
    "org.apache.karaf.jaas.modules.ldap.LdapSpecialCharsInPasswordTest",
    "org.apache.karaf.jaas.modules.ldap.LdapPoolingTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleWithEscapesTest",
    "org.apache.karaf.jaas.modules.ldap.LdapLoginModuleTest",
    "org.apache.karaf.log.core.internal.SetLogLevelTest",
    "org.apache.karaf.util.config.ConfigurationPIDTest",
    "org.apache.karaf.util.BundleUtilsTest",
    "org.apache.karaf.tools.utils.KarafPropertiesEditorTest",
    "org.apache.karaf.system.internal.SystemServiceImplTest",
    "org.apache.karaf.specs.locator.OsgiLocatorTest",
    "org.apache.karaf.shell.support.table.ShellTableTest",
    "org.apache.karaf.shell.support.ansi.AnsiSplitterTest",
    "org.apache.karaf.audit.logger.EventLoggerTest",
    "org.apache.karaf.shell.impl.console.session.SessionFactoryImplTest",
    "org.apache.karaf.shell.impl.console.parsing.ParsingTest",
    "org.apache.karaf.shell.impl.console.commands.help.wikidoc.WikiParserTest",
    "org.apache.karaf.shell.impl.action.command.ActionMaskingCallbackTest",
    "org.apache.karaf.shell.commands.impl.ThreadsTest",
    "org.apache.karaf.maven.core.MavenRepositoryURLTest",
    "org.apache.karaf.service.guard.tools.ACLConfigurationParserTest",
    "org.apache.karaf.service.guard.impl.GuardingFindHookTest",
    "org.apache.karaf.service.guard.impl.GuardingEventHookTest",
    "org.apache.karaf.service.guard.impl.ActivatorTest",
    "org.apache.karaf.service.command.ObjectClassMatcherTest",
    "org.apache.karaf.service.command.ListServicesTest",
    "org.apache.karaf.service.command.ListServiceNamesTest",
    "org.apache.karaf.profile.impl.ProfilesTest",
    "org.apache.karaf.packages.core.internal.filter.FilterParserTest",
    "org.apache.karaf.packages.core.internal.ImportDetailsTest",
    "org.apache.karaf.shell.commands.impl.InfoTest",
    "org.apache.karaf.features.internal.model.ConfigTest",
    "org.apache.karaf.features.internal.download.impl.DownloadManagerHelperTest",
    "org.apache.karaf.features.extension.StoredWiringResolverTest",
    "org.apache.karaf.features.extension.BundleWiresTest",
    "org.apache.karaf.event.service.TopicPredicateTest",
    "org.apache.karaf.jaas.modules.audit.AbstractAuditLoginModuleTest",
    "org.apache.karaf.instance.core.management.internal.InstanceToTableMapperTest",
    "org.apache.karaf.instance.command.CreateCommandTest"
  ]
}
```

## 44. explainer · explanation

- time: 2026-11-07T14:59:53.828Z
- latency: 3.176 s

```json
{
  "test": "org.apache.karaf.features.RepositoryTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.features.RepositoryTest",
    "rank_by_value": 66,
    "n_candidates": 114,
    "n_selected": 60,
    "history": {
      "test": "org.apache.karaf.features.RepositoryTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.008,
    "budget_s": 17.471,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 17.471
  },
  "justification": "Skipping it is reasonable: it has no relevance and its duration is 0.008 s, which fits exactly into the remaining budget of 0.008 s.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.008",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```

## 45. explainer · explanation

- time: 2026-11-07T14:59:57.201Z
- latency: 3.358 s

```json
{
  "test": "org.apache.karaf.features.FeaturesServiceTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.features.FeaturesServiceTest",
    "rank_by_value": 67,
    "n_candidates": 114,
    "n_selected": 60,
    "history": {
      "test": "org.apache.karaf.features.FeaturesServiceTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.068,
    "budget_s": 17.471,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 17.531
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.068 s, which is less than the remaining budget of 0.008 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.068",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```

## 46. explainer · explanation

- time: 2026-11-07T15:00:00.538Z
- latency: 3.323 s

```json
{
  "test": "org.apache.karaf.features.ConditionalTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.features.ConditionalTest",
    "rank_by_value": 68,
    "n_candidates": 114,
    "n_selected": 60,
    "history": {
      "test": "org.apache.karaf.features.ConditionalTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.905,
    "budget_s": 17.471,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 18.368
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.905 s, but only 0.008 s of the budget was left when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.905",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```

## 47. explainer · explanation

- time: 2026-11-07T15:00:03.888Z
- latency: 3.337 s

```json
{
  "test": "org.apache.karaf.features.AppendTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.features.AppendTest",
    "rank_by_value": 69,
    "n_candidates": 114,
    "n_selected": 60,
    "history": {
      "test": "org.apache.karaf.features.AppendTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.024,
    "budget_s": 17.471,
    "remaining_budget_at_turn_s": 0.008,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 17.487
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.024 s, which is less than the remaining budget of 0.008 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.024",
    "remaining_budget_at_turn_s: 0.008"
  ],
  "ok": true,
  "error": null
}
```

## 48. explainer · explanation

- time: 2026-11-07T15:00:07.317Z
- latency: 3.415 s

```json
{
  "test": "org.apache.karaf.event.command.EventTailCommandTest",
  "budget": 0.2,
  "evidence": {
    "test": "org.apache.karaf.event.command.EventTailCommandTest",
    "rank_by_value": 72,
    "n_candidates": 114,
    "n_selected": 60,
    "history": {
      "test": "org.apache.karaf.event.command.EventTailCommandTest",
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
      "tooling/karaf-maven-plugin/src/it/test-kar-packaging/verify.bsh",
      "tooling/karaf-maven-plugin/src/main/java/org/apache/karaf/tooling/KarMojo.java"
    ],
    "duration_s": 0.237,
    "budget_s": 17.471,
    "remaining_budget_at_turn_s": 0.006,
    "skip_cause": "did_not_fit",
    "fits_if_budget_s": 17.702
  },
  "justification": "Skipping it is risky: it has no relevance score and its duration is 0.237 s, which is less than the remaining budget of 0.006 s when it was reached.",
  "cited_facts": [
    "relevance_used: 0.0",
    "duration_s: 0.237",
    "remaining_budget_at_turn_s: 0.006"
  ],
  "ok": true,
  "error": null
}
```
