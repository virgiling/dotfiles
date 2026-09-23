---
name: diagnosing-bugs
description: Diagnose a reproducible failure, unexplained bug, or performance regression. Use when root-cause investigation is needed; skip for an already-understood trivial fix.
---

# Diagnose a bug

1. Read the reported symptom, relevant code, recent changes, and any existing failing check. Separate observations from hypotheses.
2. Find the smallest useful feedback signal: an existing test, CLI/HTTP reproduction, fixture, trace, or benchmark. Measure the baseline before optimizing.
3. Test plausible causes with targeted probes, changing one variable at a time. Keep failed hypotheses only when they help avoid repeated work.
4. Apply a scoped fix. Add a regression test when it can detect the real failure through an appropriate public boundary; do not add a test that merely repeats the implementation.
5. Run the original reproduction and relevant required checks. Remove temporary instrumentation and report the cause, fix, verification, and residual uncertainty.

If the environment cannot reproduce the failure, continue useful code/trace analysis and label conclusions as unverified. Ask for the specific missing artifact or access only when it blocks progress. Do not invent a fixed number of hypotheses or retry indefinitely without new evidence.

For a genuinely human-only reproduction, adapt [the optional HITL script](scripts/hitl-loop.template.sh). Inspect it before execution.
