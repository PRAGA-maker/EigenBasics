---
name: tasteful-engineering
description: "Apply Praneel's code-quality preferences when implementing, debugging, refactoring, reviewing, or designing technical systems: clear code, repository fit, sound judgment, and proportionate verification. Includes scripts, notebooks, infrastructure, and ML code."
---

# Tasteful Engineering

Praneel values code that an experienced maintainer would choose to keep: clear, economical, correct, and appropriate to the system. Treat engineering taste as part of the deliverable, even when the request only names a feature or bug.

## Make the right change

- Inspect nearby implementations, callers, existing utilities, and relevant tests before choosing a design. Infer routine implementation details from the codebase. Reuse functionality that already meets the need.
- Identify the behavior and invariants that must hold. For debugging, seek the causal failure path; fix the cause at the right boundary instead of accumulating symptom-specific branches.
- Choose the smallest coherent solution that fully handles the requested behavior. Preserve useful abstractions and conventions. Introduce a new layer, dependency, generalized framework, or configuration option when it solves a concrete problem.
- Consider consequences where they actually apply: data integrity, trust boundaries, compatibility, concurrency, cancellation, partial failure, and recovery. Raise a concrete conflict with the user's objective and propose a practical alternative. Do not turn ordinary edits into a universal risk or approval checklist.

## Make it pleasant to maintain

- Prefer explicit data flow, meaningful names, narrow responsibilities, and interfaces that make invalid states difficult to express. Keep non-obvious invariants close to the code that relies on them.
- Use simple expressions and standard library or project primitives when they clarify the operation. Split dense expressions when intermediate names expose meaning. Brevity is useful when it removes concepts, not merely lines.
- Keep error handling at meaningful boundaries. Preserve diagnostic context; avoid broad catch-and-continue paths, silent fallback values, and success-shaped output after failure.
- Comment on rationale, constraints, and surprising tradeoffs. Remove obsolete code and unnecessary scaffolding introduced by the change. Keep unrelated cleanup out of the patch.
- For technical explanations and design work, apply the same judgment to the proposed solution; do not create code or process artifacts merely to demonstrate that this skill was used.

## Earn confidence proportionately

Use the repository's relevant checks. For substantive behavior changes, choose examples or regression checks that distinguish a correct implementation from a plausible wrong one; exercise consequential failure paths when relevant. Routine reversible edits need lightweight verification. Review the final diff for accidental scope, duplication, and unnecessary complexity.

Treat performance as an empirical question when it motivates the work: establish the workload and baseline, identify the bottleneck, then compare equivalent behavior. Report what was actually checked and any material limits; distinguish a hypothesis from a measured result.

For tensor transformations, GPU kernels, or performance-sensitive ML systems, also use `/tensor-kernel-engineering`: read the [companion skill](../tensor-kernel-engineering/SKILL.md) and only its relevant references.

## Reference intent

Read [engineering references](references/engineering-references.md) when applying benchmark-derived judgment or explaining the origin of these preferences. These are inspirations for engineering decisions, not benchmark-specific score targets or a mandate to run benchmark suites.
