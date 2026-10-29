# Tensor and GPU references

Reviewed 2026-10-21. These are concise source-derived lessons plus their intended application. Consult current primary documentation for implementation details and architecture-specific behavior.

## Sasha Rush's Tensor Puzzles

[srush/Tensor-Puzzles](https://github.com/srush/tensor-puzzles) uses small exercises to teach broadcasting and indexing from first principles. The notebook pairs operations with straightforward specifications and executable checks.

Application: understand the index mapping and shape algebra, and keep a trustworthy reference when changing a tensor operation. The one-line requirement and restricted operators are deliberate teaching constraints; they are not Praneel's general coding style. Use named intermediates, library reductions, or standard primitives whenever they make real code better. Mathematical elegance includes reasonable memory use.

## Hazy Research

[Hazy Research's blog](https://hazyresearch.stanford.edu/blog) is an ongoing source for hardware-aware ML systems work. A concrete reviewed example is [ThunderKittens 2.0](https://hazyresearch.stanford.edu/blog/2026-02-19-tk-2), which discusses removing internal complexity, inspecting generated instructions, memory consistency, pipelining, occupancy surprises, and careful kernel benchmarking.

Application: question overhead at abstraction boundaries and measure the generated program on the target device. Read the post relevant to the present bottleneck rather than loading the whole blog. A cleaner abstraction can improve both maintenance and execution; more elaborate code is not evidence of a better kernel. Revalidate architectural tricks and benchmarking conditions before transferring results to another GPU.

## Programming Massively Parallel Processors notes

[Steven Gong's PMPP notes](https://stevengong.co/notes/Programming-Massively-Parallel-Processors) collect learning notes on GPU execution, thread organization, global-memory access, tiling, coalescing, and the relationship between computation and memory movement.

Application: derive how threads map to contiguous data and how reused data moves through the memory hierarchy. Check synchronization and edge conditions when introducing tiles. These are a reader's notes, including learning questions and illustrative code, not an authoritative API reference or a source of production-ready snippets. Verify CUDA details in NVIDIA's documentation and against the actual device/toolchain.
