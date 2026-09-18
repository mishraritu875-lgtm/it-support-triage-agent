import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT_NAMES = (
    "ritu-it-support-intake",
    "ritu-it-support-knowledge",
    "ritu-it-support-triage",
)


class FoundryConfigTests(unittest.TestCase):
    def test_workflow_invokes_agents_in_order(self):
        workflow = yaml.safe_load((ROOT / "workflow.yaml").read_text(encoding="utf-8"))
        actions = workflow["trigger"]["actions"]
        self.assertEqual(workflow["kind"], "workflow")
        self.assertEqual([a["agent"]["name"] for a in actions], list(AGENT_NAMES))
        self.assertTrue(all(a["kind"] == "InvokeAzureAgent" for a in actions))

    def test_agent_definitions_exist_and_have_instructions(self):
        for name in AGENT_NAMES:
            with self.subTest(name=name):
                agent = yaml.safe_load((ROOT / "agents" / f"{name}.yaml").read_text(encoding="utf-8"))
                self.assertEqual(agent["name"], name)
                self.assertEqual(agent["definition"]["kind"], "prompt")
                self.assertTrue(agent["definition"]["instructions"].strip())

    def test_knowledge_agent_has_file_search(self):
        agent = yaml.safe_load((ROOT / "agents" / "ritu-it-support-knowledge.yaml").read_text(encoding="utf-8"))
        self.assertIn("file_search", [tool["type"] for tool in agent["definition"]["tools"]])


if __name__ == "__main__":
    unittest.main()
