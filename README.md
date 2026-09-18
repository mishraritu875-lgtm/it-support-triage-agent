# IT Support Triage Workflow

A Microsoft Foundry workflow for fictional workplace IT requests. Three prompt agents run in sequence: intake gathers facts, knowledge retrieves guidance from an attached IT Support Guide, and triage recommends a next action and whether human review is needed. The helpdesk makes any final priority decision.

## Repository contents

- `workflow.yaml`: exported Foundry orchestration definition.
- `agents/*.yaml`: exported agent versions and instructions.
- `tests/test_config.py`: offline checks of the exported configuration.
- `.github/workflows/validate.yml`: runs those checks on GitHub.

These YAML files describe Foundry assets; running a local YAML check does **not** run the hosted agents. The knowledge agent's `vector_store_ids` points to a separate Foundry resource and does not contain the IT Support Guide. Obtain the guide from its owner and recreate/upload it in your own Foundry project when deploying a copy. Do not publish the guide without permission.

## Run in Foundry

1. Open project `agentathon-level3-ai` in Microsoft Foundry.
2. Open `ritu-it-support-workflow`, choose version 2, and use **Preview** with a fictional support request.
3. Inspect the agent responses and cited guide section. The Foundry project and model deployment must be accessible to your account.

## Local validation

Install Python 3.10+ and run:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

This validates YAML structure without Azure credentials or paid model calls.

## Configuration and secrets

`.env.example` documents configuration for a future local client or deployment script. Copy it to `.env` and fill it in locally. `.env` is ignored by Git. Use GitHub Actions secrets for credentials if you add an authenticated deployment workflow. Prefer Azure identity federation over long-lived API keys when available. Never put tokens or passwords in YAML, commits, screenshots, or CI logs.

The exported agent files contain Foundry-generated identity and resource identifiers. Review them before using a public repository. Those identifiers are not credentials, but a new deployment will need new agent identities and a new vector store.

## Deploy a copy

1. Create a Foundry project and deploy a model compatible with the agents' `gpt-4.1-mini` configuration.
2. Create the intake, knowledge, and triage prompt agents using the instructions in `agents/`. Configure the knowledge agent's file search against a newly uploaded approved IT Support Guide. Replace project-specific vector store and identity references rather than copying the exported IDs blindly.
3. Create the sequential workflow from `workflow.yaml` and select the three new agents.
4. Save/publish the workflow version in Foundry, run Preview, and verify the output and guide citation.

These are manual Foundry deployment steps. GitHub Actions currently runs offline validation only; there is no automated Foundry deployment and no public demo URL in this repository.

## Evaluation and evidence

A previous Foundry run, `ritu-it-support-workflow-custom-eval`, reported 15/15 passing synthetic cases with rubric `it_support_triage_quality`. This is a model-based evaluation of that run, not proof that this repository can recreate its environment or that every real request succeeds. Add an authorized screenshot or run URL under `evidence/` if you want reviewers to verify it.

After GitHub Actions succeeds, link its actual run here. Add a deployment URL only if you have published a working endpoint or demo accessible to reviewers.

## Validation checklist

- [x] Workflow and three agent YAML exports included
- [x] Local offline configuration checks included
- [x] GitHub Actions validation workflow configured
- [ ] GitHub Actions run passed (verify after pushing)
- [ ] Approved IT Support Guide attached to deployment
- [ ] New deployment responds to a fictional request
- [ ] Basic escalation and missing-information cases reviewed
- [ ] Accessible demo/deployment URL provided, if required
- [GitHub Actions validation: passed](https://github.com/mishraritu875-lgtm/it-support-triage-agent/actions/runs/35374190072)

## Configuration review

All three exports enable `web_search`, while the knowledge agent says to use only the approved guide and the triage agent says not to search the web. Before the next evaluation or deployment, disable web search where it is not needed, save new agent versions, and rerun representative tests. The YAML here documents the versions originally evaluated; it has not silently modified the deployed agents.
