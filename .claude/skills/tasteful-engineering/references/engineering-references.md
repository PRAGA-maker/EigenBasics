# Engineering reference intent

Reviewed 2026-10-21. The guidance below is a synthesis for Praneel's harness, not a reproduction of the sources or an endorsement by their authors. Recheck live sources before relying on changing benchmark details.

## Senior SWE-Bench

[Snorkel's Senior SWE-Bench](https://snorkel.ai/leaderboard/senior-swe-bench/) distinguishes passing functional checks from producing a tasteful patch. It evaluates fit with existing repository practices and code quality as well as required behavior. Its requests deliberately leave implementation decisions to the engineer.

Application: inspect the actual system, infer appropriate boundaries, and make a focused change that belongs in the repository. Passing a narrow test does not excuse unnecessary architecture or a brittle workaround. Benchmark patch-size gates are evaluation machinery; do not impose a universal line-count limit on production work.

## sudo L7

[Surge's sudo L7](https://surgehq.ai/blog/sudo-l7) emphasizes professional judgment around working code: understand what exists, recognize concrete production consequences, verify relevant failure cases, and report truthfully.

Application: evaluate whether the proposed implementation serves the user's real objective. For example, acknowledging a failed webhook before durable capture can lose events; logging complete payloads can expose sensitive data. A schema migration may need a credible partial-failure and recovery story. Apply these considerations when the task involves them, and proceed autonomously within the user's authorization for routine work.

## Companion technical references

The tensor and GPU skill preserves the other requested resources, with conditional guidance for broadcasting, kernels, and quantized distributed ML. Read those references when the workload calls for them; ordinary software edits do not require GPU tuning or a literature review.
