# ML systems boundaries

Reviewed 2026-10-21. Read this reference for quantized training/inference integration, LoRA, or distributed rollout systems.

## SkyRL example

[SkyRL's Kimi K2 INT4/LoRA example](https://docs.skyrl.ai/docs/examples/kimi_k2_int4_lora) describes a distributed recipe with a fixed INT4 serving base, trainer-side master weights and adapters, quantization-aware forward behavior, and synchronization of adapters to inference workers. The recipe checks quantization consistency and documents requirements across nodes.

Application: make representation boundaries explicit. Verify which weights are frozen, trainable, quantized, exported, and actually served. Check quantizer conventions and trainer/rollout agreement rather than assuming identical checkpoint names imply identical numerical behavior. Track adapter versions and rollout freshness. Account for storage, memory, communication, checkpoint recovery, and per-node environment consistency.

The URL's model example, package versions, hardware, paths, and numerical conventions can change. Fetch the live documentation and inspect the matching repository revision before reusing commands or settings. This example does not imply a default model, GPU topology, quantizer, or training backend for other projects.

## Applying the lesson

Treat a pipeline as a set of contracts between components. A locally correct training step can still produce an incorrect system if the inference workers load stale adapters or use incompatible weight representations. Verify the relevant boundary on a small workload before scaling an already-authorized experiment. Distinguish numerical agreement, learning behavior, and throughput evidence in reporting.
