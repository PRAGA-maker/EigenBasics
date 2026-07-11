---
name: doing-pure-comp-bio
description: >-
  Use when the user wants a biological takeaway from computational analysis of
  biological data, especially organoids, single-cell or bulk omics, imaging,
  perturbation screens, developmental systems, or multimodal experiments. The
  skill prioritizes biological interpretation and causal/mechanistic reasoning
  over merely producing a bioinformatics pipeline or a predictive benchmark.
---

# Doing pure computational biology

Use computation to answer a biological question, not to produce an analysis
artifact. Start from the phenotype or mechanism the user cares about and make
each analysis earn its place by reducing a specific biological uncertainty.

## 1. State the biological question sharply

Write the question as a contrast, trajectory, mechanism, or prediction:

- What biological state differs between groups?
- Is the difference compositional, cell-intrinsic, developmental, functional,
  or some combination?
- Where along a lineage or time axis does the difference first appear?
- Which molecular programs could explain the phenotype?
- Which intervention, perturbation, or validation would distinguish correlation
  from mechanism?

Separate the observed phenotype from the proposed explanation. For example:

```text
Observation: fewer mature neurons and weaker calcium responses.
Mechanism to test: progenitors fail to exit the cell cycle on schedule,
causing delayed neuronal maturation and downstream synaptic immaturity.
```

Do not call a biological conclusion causal merely because a pathway is enriched.
Label observations, model-based inferences, and causal claims separately.

## 2. Build the measurement hierarchy

Map each biological claim to the modality that can observe it. Use at least one
measurement at each relevant level:

```text
system phenotype -> composition -> cell state -> regulatory program
                 -> morphology -> physiology -> mechanism/perturbation
```

Typical mappings:

- Bright-field: size, growth, gross morphology.
- Immunostaining/FACS: cell identity, proportions, proliferation, layers.
- scRNA-seq: cell states, composition, state-specific expression.
- Bulk RNA-seq of purified populations: cell-intrinsic transcriptional state.
- Small-RNA sequencing: miRNA or other regulatory-layer changes.
- Imaging: morphology, spatial organization, dynamic events.
- Calcium/electrophysiology: functional responsiveness and dynamics.
- Perturbation/rescue: evidence for mechanism rather than association.

For every modality, state what it can and cannot identify. A change in whole-
organoid expression cannot by itself distinguish cell-composition change from
cell-intrinsic regulation; purified-cell sequencing or single-cell analysis is
needed for that separation.

## 3. Preserve biological replicate structure

Treat cells as observations nested inside organoids, batches, and biological
lines. The independent biological unit is usually the organoid, donor, line, or
animal—not an individual cell or image field.

Before testing anything, record:

- donor/line and genotype;
- organoid, batch, culture date, and developmental time;
- technical versus biological replicates;
- matching, pairing, sex, ancestry, and known covariates;
- the unit used for the statistical test.

Use mixed-effects models, pseudobulk, or replicate-level summaries where
appropriate. Avoid pseudoreplication by treating thousands of cells from one
organoid as thousands of independent biological replicates.

Use multiple lines and batches to establish generality. Check whether the
signal is consistent within each pair/line, not only significant after pooling.

## 4. Analyze in the order the biology requires

For heterogeneous or developmental systems, use this sequence unless the
question clearly calls for another design:

1. **Quality and identity:** viability, library depth, mitochondrial/ribosomal
   content, stress/apoptosis, marker validity, and contamination.
2. **Composition:** which populations or neighborhoods are over- or under-
   represented?
3. **State:** within each population, which genes, pathways, or programs differ?
4. **Trajectory:** are cells at different positions along a developmental path?
5. **Regulation:** which transcription factors, co-expression modules, miRNAs,
   or interaction networks organize the difference?
6. **Phenotype linkage:** do molecular differences predict morphology or function?
7. **Mechanism:** can perturbation, rescue, or an orthogonal assay discriminate
   competing explanations?

Composition and state must be analyzed separately. “Fewer mature neurons” and
“mature neurons have immature transcriptional programs” are distinct findings.

## 5. Use the right computational patterns

### Single-cell data

Use a transparent pipeline: aggregation/depth normalization, QC, normalization,
batch correction or integration, clustering, embedding, and annotation. Prefer
reference-based annotation plus marker validation over naming clusters from an
embedding alone. Report annotation confidence and combine tiny, unstable
subtypes only when that improves the biological comparison.

For differential expression, compare genotypes within a cell type/state. Use a
method suited to sparse counts, such as a hurdle or pseudobulk model. Report
effect size, direction, multiple-testing correction, and the number of biological
replicates—not only a gene list.

For differential abundance, distinguish broad proportions from local changes in
the cell-state manifold. Neighborhood methods such as Milo are useful when the
biological question is “which local states expand or contract?”

### Development and cell fate

Use pseudotime to compare distributions along a lineage, not to claim a literal
time series. Use RNA velocity/latent time and CellRank-like fate probabilities
when splicing information and data quality support a directional model.

Always state the assumptions: manifold continuity, root/terminal-state choice,
batch correction, and the fact that inferred trajectories are not lineage
tracing. Convergent evidence is stronger than any one trajectory method.

Useful outputs include:

- distribution along pseudotime;
- latent time shift;
- terminal-state absorption probability;
- differentiation potential/entropy;
- velocity direction in the relevant transition state.

### Gene programs and regulatory explanations

Move from individual genes to interpretable programs:

- GO/GSEA for broad biological functions;
- domain-specific ontologies such as SynGO for synaptic biology;
- TF regulons for candidate transcriptional control;
- WGCNA/scWGCNA modules for coordinated expression;
- miRNA-target networks for post-transcriptional regulation;
- STRING/PPI networks for interacting protein systems.

Use gene-set scores to compare programs across conditions and time. Define the
background gene universe explicitly. Enrichment is not mechanism: it generates
candidates that must be linked to phenotype and, ideally, tested by perturbation.

For network analyses, report how edges were defined, confidence thresholds,
centrality measures, and whether the network is empirical, predicted, or both.
Network centrality prioritizes candidates; it does not prove causal importance.

### Quantitative imaging and physiology

Convert images or traces into biologically interpretable feature vectors before
testing group differences. Examples:

```text
morphology = [cell count, neurite count, total length, branchpoints,
              soma size, layer thickness]
activity = [event rate, amplitude, latency, duration, synchrony,
            stimulus response, recovery]
```

Use segmentation and tracing quality controls, blind or preregistered
thresholds where possible, and report the nesting of cells within organoids and
experiments. For dynamic signals, define event detection and baseline rules in
advance. Link a molecular program to a phenotype through matched samples or a
prediction model, not visual juxtaposition alone.

## 6. Triangulate before telling the story

Organize the argument as an evidence chain:

```text
cell abundance change
    + developmental-state shift
    + cell-intrinsic molecular program
    + orthogonal marker/morphology validation
    + functional phenotype
    -> mechanistic model
```

Each result should answer “what uncertainty did this remove?” and “what does it
force us to test next?” Prefer a small set of mutually reinforcing analyses over
many disconnected plots.

The strongest biological takeaway usually has:

1. a phenotype;
2. the earliest affected cell state;
3. a molecular program explaining the state transition;
4. a downstream structural or functional consequence;
5. a candidate mechanism and a decisive validation experiment.

## 7. Use nulls, controls, and negative evidence

Controls should follow from the biological question:

- matched lines or sibling pairs for background variation;
- batch and developmental-stage controls;
- marker-positive and marker-negative controls;
- synonymous or matched random gene sets for genetic enrichment;
- permutation tests controlling for gene size, expression, or genomic context;
- stress, hypoxia, and apoptosis checks for organoid health;
- rescue or perturbation controls for mechanism.

Record null results. A lack of global growth change can localize the defect to
cell state or function; absence of a pathway in an upregulated set can itself
sharpen the interpretation.

## 8. Report an evidence ledger

For every headline claim, record:

```text
claim -> modality -> analysis -> effect size/uncertainty -> replicate unit
      -> orthogonal validation -> limitation -> next decisive test
```

Use these labels internally:

- **Observed:** directly measured.
- **Inferred:** produced by a model such as pseudotime or network analysis.
- **Supported mechanism:** triangulated and experimentally validated.
- **Candidate mechanism:** plausible but not yet causally tested.

Report effect sizes, confidence intervals or exact adjusted p-values, sample
sizes, and the number of lines/organoids/batches. Do not let cell count replace
biological replication. Keep corrected or superseded interpretations visible.

## 9. Produce the biological deliverable

Structure the final analysis around the biological argument, not the software:

1. question and competing explanations;
2. model system and what each modality measures;
3. quality and identity checks;
4. composition result;
5. state/trajectory result;
6. molecular programs and candidate regulators;
7. morphology/physiology linkage;
8. integrated mechanistic model;
9. limitations and alternative explanations;
10. one decisive next experiment.

Name the exact tools and parameters in a methods appendix or reproducibility
record, but make the main text answer what the biological system contains, what
changed, where it changed, and why it matters.

## Common failure modes

- Treating an organoid as a single homogeneous sample.
- Reporting cluster labels without validating identity.
- Calling pseudotime a real developmental clock.
- Using whole-organoid bulk RNA as evidence of cell-intrinsic regulation.
- Treating pathway enrichment or PPI centrality as causal proof.
- Testing cells instead of biological replicates.
- Ignoring batch, donor, ancestry, or line effects.
- Overfitting a narrative to one modality.
- Producing a predictive classifier when the user asked for a biological
  explanation.
- Listing tools and plots without stating the uncertainty each resolves.

## Distinction from ordinary bioinformatics

Bioinformatics asks how to process, annotate, quantify, or compare biological
data. Pure computational biology asks what biological state, process, or
mechanism the data support. Use the pipeline as evidence, then stop and reason
from the evidence to the organismal, cellular, developmental, or molecular
takeaway.
