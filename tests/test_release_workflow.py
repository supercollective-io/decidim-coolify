"""Execute release gating shell steps against disposable Git histories.

Actionlint checks the workflow schema separately. These tests exercise failure
propagation and stale-source behaviour without GitHub or registry credentials.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def shell_step(name):
    lines = (ROOT / ".github/workflows/images.yml").read_text().splitlines()
    start = lines.index("      - name: " + name)
    run = lines.index("        run: |", start) + 1
    script = []
    for line in lines[run:]:
        if line and not line.startswith("          "):
            break
        script.append(line[10:])
    return "\n".join(script)


def execute(script, cwd, values):
    env = dict(os.environ, **values)
    return subprocess.run(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
                          cwd=cwd, env=env, text=True, capture_output=True)


class RequiredResultsTests(unittest.TestCase):
    def test_required_failures_cannot_be_reported_as_success(self):
        script = shell_step("Check required results")
        for image_checks, candidates in ((False, False), (True, False), (True, True)):
            success = dict(CHANGES_RESULT="success", IMAGES_REQUIRED=str(image_checks).lower(),
                           DOCS_RESULT="skipped" if image_checks else "success",
                           QUICK_RESULT="success" if image_checks else "skipped",
                           TEST_RESULT="success" if image_checks and not candidates else "skipped",
                           CANDIDATES_REQUIRED=str(candidates).lower(),
                           CANDIDATES_RESULT="success" if candidates else "skipped")
            self.assertEqual(execute(script, ROOT, success).returncode, 0)
            for field in (key for key, value in success.items() if value == "success"):
                for failure in ("failure", "cancelled", "skipped"):
                    with self.subTest(image_checks=image_checks, candidates=candidates, field=field, result=failure):
                        self.assertNotEqual(execute(script, ROOT, dict(success, **{field: failure})).returncode, 0)


@unittest.skipUnless(shutil.which("jq"), "publication metadata checks require jq (available in CI)")
class PublicationMetadataTests(unittest.TestCase):
    def digest(self, metadata):
        script = shell_step("Assemble tested images without rebuilding")
        query = re.search(r'''digest=\$\(jq -er '([^']+)' "\$RUNNER_TEMP/published.json"\)''', script)
        self.assertIsNotNone(query, "cannot find publication digest extraction")
        return subprocess.run(["jq", "-er", query.group(1)], input=json.dumps(metadata),
                              text=True, capture_output=True)

    def test_reads_imagetools_create_descriptor(self):
        # Docker's documented imagetools create --metadata-file output differs
        # from build metadata: https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/
        digest = "sha256:19ffeab6f8bc9293ac2c3fdf94ebe28396254c993aea0b5a542cfb02e0883fa3"
        result = self.digest({
            "containerimage.descriptor": {
                "mediaType": "application/vnd.oci.image.index.v1+json",
                "digest": digest,
                "size": 4654,
            },
            "image.name": "docker.io/user/app",
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), digest)

    def test_missing_publication_descriptor_fails(self):
        for metadata in ({}, {"containerimage.descriptor": {}},
                         {"containerimage.digest": "sha256:" + "a" * 64}):
            with self.subTest(metadata=metadata):
                self.assertNotEqual(self.digest(metadata).returncode, 0)


class CurrentSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Release test")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", "/dev/null")
        self.git("commit", "--allow-empty", "-qm", "source")
        self.source = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              text=True, capture_output=True).stdout

    def check(self, source=None):
        output = self.root / "output"
        output.write_text("")
        result = execute(shell_step("Reject a superseded application build"), self.root, {
            "SOURCE_REVISION": source or self.source,
            "GITHUB_OUTPUT": str(output),
            "GITHUB_STEP_SUMMARY": str(self.root / "summary"),
        })
        return result, output.read_text()

    def test_unchanged_source_is_eligible(self):
        result, output = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("current=true", output)

    def test_only_prose_and_compose_may_advance_without_a_new_build(self):
        for path, eligible in (
            ("README.md", True), ("docs/OPERATIONS.md", True),
            ("docs/nested/guide.md", True), ("compose.yaml", True),
            ("app/README.md", False), ("app/app/example.rb", False),
            ("Dockerfile", False), ("docker/entrypoint", False),
            (".github/workflows/images.yml", False), ("new-unknown-file", False),
        ):
            with self.subTest(path=path):
                self.git("reset", "--hard", self.source)
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("changed\n")
                self.git("add", path)
                self.git("commit", "-qm", "advance")
                result, output = self.check()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual("current=true" in output, eligible)

    def test_invalid_revision_is_a_failure_not_a_successful_skip(self):
        result, output = self.check("missing-revision")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("current=true", output)


if __name__ == "__main__":
    unittest.main()
