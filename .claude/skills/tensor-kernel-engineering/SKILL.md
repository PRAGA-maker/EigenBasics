---
name: tensor-kernel-engineering
description: "Design and review tensor operations, CUDA/Triton GPU kernels, and performance-sensitive ML systems using explicit shape reasoning, numerical correctness, hardware-aware design, and fair benchmarks. Use for tensor vectorization, kernel optimization, and quantized or distributed training/inference."
---

# Tensor and Kernel Engineering

Bring the clarity of tensor puzzles and the discipline of good kernel engineering to the actual workload. Complexity earns its place through correctness, clarity, or measured benefit.

## Tensor reasoning

- Establish input/output shapes, axis meanings, dtypes, devices, layout assumptions, broadcasting, and reduction semantics before transforming an operation. State these in code or explanation when they are non-obvious.
- Use broadcasting, indexing, reductions, and matrix operations to express the mathematics clearly. Prefer mature optimized operators when they fit. Puzzle-specific restrictions on line length or allowed operators do not apply to production code.
- Account for allocations and memory traffic: a compact broadcast may materialize a quadratic intermediate; a reshape may copy; an expanded view may alias. Avoid eliminating a readable loop by creating an impractical tensor.
- For substantive transformations, compare with a simple trusted reference. Choose relevant adversarial cases: asymmetric dimensions, singleton axes, irregular sizes, strides, masking, and numerical extremes. Check gradients when training behavior changes, and choose tolerances appropriate to dtype and accumulation.

## GPU performance

Start with a representative workload and an optimized library baseline. Determine whether the limiting cost is computation, memory movement, launches, synchronization, or communication before choosing an optimization. A custom kernel is useful when the workload justifies its maintenance cost.

When implementing a kernel, reason explicitly about work ownership and memory access. Consider coalescing, reuse and tiling, register/shared-memory pressure, occupancy, and overlap only as relevant to the bottleneck. Guard boundary tiles and establish race-free synchronization, including asynchronous lifetimes. Verify architecture and compiler assumptions instead of copying hardware-specific tricks blindly.

Benchmark equivalent inputs, precision, semantics, and device conditions. Warm up compilation and execution; use GPU events or correct synchronization for timing. Describe whether allocation, transfers, communication, and cache effects are included. Report variability and end-to-end impact where consequential. An isolated microbenchmark is evidence for that workload, not a universal speed claim. If suitable hardware is unavailable, report that limitation and leave performance claims unverified.

## Load relevant depth

- For tensor/vectorization and GPU kernels, read [tensor and GPU references](references/tensor-and-gpu.md).
- For quantized rollouts, LoRA, or distributed training/inference, read [ML systems boundaries](references/ml-systems.md) and verify the current project's implementation and dependencies before using recipe-specific settings.

These references guide design. They do not authorize launching a training run, buying compute, or adding a particular framework to unrelated work.
