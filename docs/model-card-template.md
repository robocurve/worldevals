# Model card template

Copy everything below the line into the checkpoint repo's `README.md` and replace every
`<placeholder>`. Remove the ```yaml fence lines so the metadata block starts with `---`
on line 1 (the Hub only parses unfenced frontmatter). Keep the section order. Follow the
writing-style rules in model-cards.md: no em dashes in prose, no rhetorical bold, no
decorative emoji. Rules and the gating checklist: [model-cards.md](model-cards.md).

---

```yaml
---
library_name: <lerobot | transformers | ...>
pipeline_tag: robotics
license: <inherited license, or `other` + license_name + license_link>
base_model: <org/base-model>
datasets:
  - <org/dataset>
tags:
  - robotics
  - vla
  - <robot>
  - <method>
inference: false
# RECOMMENDED:
# co2_eq_emissions: {emissions: <g>, source: "<estimator>", training_type: "fine-tuning",
#                    geographical_location: "<region|unknown (...)>", hardware_used: "<n x GPU>"}
# model-index: [{name: <repo>, results: [{task: {type: robotics},
#   dataset: {type: <id>, name: <name>},
#   metrics: [{type: <metric>, name: <display>, value: <n>}]}]}]
---
```

# <Model name: robot + method in plain words>

[![Evaluate with Inspect Robots](https://img.shields.io/badge/evaluate%20with-Inspect%20Robots-indigo)](https://github.com/robocurve/inspect-robots)
[![Adapters: <embodiment>](https://img.shields.io/badge/adapters-inspect--robots--<embodiment>-blue)](https://github.com/robocurve/inspect-robots-<embodiment>)
[![Benchmarks: WorldEvals](https://img.shields.io/badge/benchmarks-WorldEvals-2ea44f)](https://worldevals.org)
[![Catalog: WorldPolicies](https://img.shields.io/badge/catalog-WorldPolicies-yellow)](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37)

<≤3 sentences: [base model](link) + method (LoRA/full FT; what's frozen) + robot +
[dataset](link). Adapter/merge status and where raw adapters live.>

## Intended use & safety

- **Intended use:** research/evaluation on <exact embodiment> for <task families>.
- **Out of scope:** other embodiments/rigs without fine-tuning (no zero-shot embodiment
  transfer); unattended operation; operation near people without hardware e-stop and
  enforced workspace/torque limits.
- **Validation status:** <offline action-loss only | open-loop MSE | sim rollouts |
  real-robot rollouts> (<link evidence>). Users are responsible for safe integration
  (guardrails, e-stop, workspace limits) before any deployment.

## Training

| | |
|---|---|
| Data | <N repos / N episodes / N frames-or-hours; filter rule; split rule (level, %, seed)> |
| Embodiment | <tag/config; state keys idx layout; action keys idx layout> |
| Image preprocessing | <resolution; aspect handling; augmentations> |
| Schedule | <steps; global batch × accum; lr + schedule; n× GPU type> |
| Checkpoint selection | <rule, e.g. argmin held-out eval loss over keeps every N steps → step S> |
| Headline curve | <metric>: <start> → <best> |

## Losses & evaluation

- **Training loss:** <objective, precisely>; trainable: <...>; frozen: <...>.
- **Eval regime:** <offline action loss | open-loop MSE | sim closed-loop | real closed-loop>.
  <Methodology: split/samples/normalization-parity/seeding, or tasks/trials/criterion/judge.>
- **Comparisons:** <linked protocol/artifact, or delete this line>.
- **Scope:** <what the metric does not show>.

## Provenance

| | |
|---|---|
| Trained by | <person/org, dates> |
| Training code | <URL, or "<repo> (private): <one-clause contents>"> |
| Framework | <framework @ commit; torch X, transformers Y, <adapter lib> Z> |
| Compute provider | <provider, n× GPU type; CPU/RAM if dataloading-bound> |
| Wall-clock | <hours; preemptions: <n>, max steps lost <m> | none> |
| Total compute | <FLOPs or GPU-hours + method + uncertainty | unknown (<why>)> |
| Cost | <USD run / USD project-total | unknown (<why>)> |
| Experiment tracking | <platform, project, run ids | unknown (<why>)> |
| Card authorship | <author; "reconstructed from <artifacts>" vs first-hand> |

## Usage

```python
<zero-edit loading snippet>
```

- **Observations:** cameras <key: what it views, WxH>; state <key → [i:j]> (<units/convention>).
- **Actions:** <key → [i:j]>, <absolute|delta> <units/normalization convention>,
  horizon <H> steps<, control ~<f> Hz if known>. Normalization statistics: <path in repo>.
- **Serving:** <server script / client adapter links>.

## Data provenance & caveats

- <Origin; license of each source or of the manifest + per-source statement.>
- <Known data issues: duplicates/imbalance/scene bias.>
- <Eval-vs-deployment limits; "no real-robot rollouts yet" if true.>
- <Instabilities/failed attempts, or link to the repo's incident log.>

## Versioning & contact

- <`main` stability statement; pin by revision for reproduction<; new_version chain note>.>
- Issues: <HF Discussions link or GitHub issues link>.
