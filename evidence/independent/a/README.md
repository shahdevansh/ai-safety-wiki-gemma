# Independent evaluator A

Prospective requirements and expected source excerpts are in [test_plan.md](test_plan.md) and [cases.json](cases.json). Read the [final regression report](final-independent-report.md) for the latest candidate and the [initial report](independent-report.md) for the distinct earlier run. Original cases and checks were unchanged. Raw automatic output is preserved separately and is not treated as a grading verdict.

Run after the parent provides the sanitized freeze and isolation wrapper:

```sh
python3 evaluate.py --config approved-run.json --run
```

Configuration fields:

```json
{
  "project": "/absolute/frozen/project",
  "command_prefix": ["/absolute/approved-isolation-wrapper"],
  "cli": ["python3", "wiki.py"],
  "expected_model": "gemma4:e2b-it-qat",
  "expected_model_digest": null,
  "endpoint": "http://127.0.0.1:11434",
  "offline_proof_path": "/absolute/isolation-proof.json",
  "approval_note": "Parent approved frozen project and this execution wrapper.",
  "command_timeout_seconds": 1800,
  "search_without_model_prefix": null
}
```

The prefix is prepended to every CLI command. `search_without_model_prefix`, if supplied, is an alternative approved prefix that prevents access to the model endpoint. The evaluator never starts or stops the user's model daemon. Each run gets a fresh local project copy under `runs/`. Existing submission outputs and evals are excluded. Machine findings in `summary.json` and `review.md` require a semantic review of the actual answers before a final verdict. Neither keyword matches nor authentic quotations alone prove entailment.
