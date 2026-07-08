# Model cards for Robocurve HuggingFace uploads

Every checkpoint published to the [robocurve](https://huggingface.co/robocurve) org **must**
ship a model card following this guide. The primary audience is a publishing agent (Claude
session) following it mechanically at publish time. Fill in
[`model-card-template.md`](model-card-template.md) top-to-bottom, then verify with the
checklist at the bottom of this page. Sections must appear in the template's order.

Reference implementations (updated to comply with this standard):
[gr00t-n1.7-so101-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-so101-molmoact2) and
[gr00t-n1.7-yam-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-yam-molmoact2).

## Ground rules

- **REQUIRED vs RECOMMENDED.** Every REQUIRED field must be present. If a REQUIRED value is
  genuinely unrecoverable (e.g. publishing a teammate's checkpoint from artifacts), write
  `unknown (<why>)` — never silently omit the row. RECOMMENDED fields may be omitted.
- Write the card **at publish time, from the run's artifacts** (`trainer_state.json`, wandb,
  eval results files, decision records) — not from memory.
- Numbers over adjectives ("eval loss 1.129 → 0.0273", never "converged well"). Every number
  must be traceable to a named artifact.
- USD for costs; SI units elsewhere; state units explicitly for actions/state.

## Sections

### 1. YAML frontmatter (REQUIRED)

The Hub parses these fields — they power search filters, the model tree, dataset links, and
code snippets. Prose without metadata is unfindable.

```yaml
---
library_name: <e.g. lerobot, transformers; omit only if no library integration exists>
pipeline_tag: robotics
license: <see procedure below>
base_model: <hub id of the base checkpoint>       # powers the finetune/model tree
datasets:
  - <hub id of each training dataset that exists on the Hub>
tags:
  - robotics
  - vla
  - <robot/embodiment, e.g. so101, yam, bimanual>
  - <method/family, e.g. gr00t, pi0, lora>
  - lerobot          # only if the training data is LeRobot-format
inference: false     # robot policies cannot run in the hosted widget
---
```

**License procedure (REQUIRED):** a fine-tune inherits the most restrictive license among
(a) the base model and (b) any training-data source. Do NOT default to `apache-2.0`.
For a custom license (e.g. NVIDIA License on GR00T models):

```yaml
license: other
license_name: nvidia-license
license_link: https://huggingface.co/nvidia/GR00T-N1.7-3B/blob/main/LICENSE
```

List data-source licenses in §8 (Caveats). If sources conflict, use the most restrictive and
enumerate the conflicts there.

**co2_eq_emissions (RECOMMENDED)** — Hub-parsed schema, grams CO2eq:

```yaml
co2_eq_emissions:
  emissions: <grams>
  source: "estimated via mlco2.github.io/impact"   # or CodeCarbon
  training_type: "fine-tuning"
  geographical_location: <region or "unknown (provider does not disclose)">
  hardware_used: "1x H100 80GB"
```

**model-index (RECOMMENDED)** — makes eval numbers machine-readable (renders the
"Evaluation results" widget; use `task.type: robotics`):

```yaml
model-index:
  - name: <repo name>
    results:
      - task: {type: robotics}
        dataset: {type: <hub id or protocol name>, name: <display name>}
        metrics:
          - {type: <e.g. open_loop_mse, eval_loss, success_rate>, name: <display>, value: <n>}
```

### 2. Header (REQUIRED)

At most three sentences: base model + method (LoRA/full FT; what's frozen) + robot/embodiment
+ dataset. State whether adapters are merged and where raw adapters live if published.
Link every **named artifact**: base model, each dataset, training-code repo, method libraries,
papers. (Ordinary nouns like "camera" need no link.)

### 3. Intended use & safety (REQUIRED)

These checkpoints command physical actuators. Three bullets, none skippable:

- **Intended use:** research/evaluation on `<exact embodiment>` for `<task families>`.
- **Out of scope:** any other embodiment or rig without fine-tuning (VLA policies do not
  zero-shot transfer across embodiments — say so); unattended operation; operation near
  people without a hardware e-stop and enforced workspace/torque limits.
- **Validation status:** exactly one of `offline action-loss only` / `open-loop MSE` /
  `sim rollouts` / `real-robot rollouts`, with a link to the evidence. Users are responsible
  for safe integration (guardrails, e-stop, workspace limits) before any deployment.

### 4. Training (REQUIRED)

A table with one row each:

| Row | Must include |
|---|---|
| Data | counts (source repos / episodes / frames or hours), filter rule, train/test split rule (level + % + seed if applicable) |
| Embodiment | embodiment tag/config name; state & action keys with index layout |
| Image preprocessing | resolution, aspect-ratio handling (e.g. letterbox), augmentations |
| Schedule | steps, batch (global × accum), LR + schedule, hardware (GPU type × count) |
| Checkpoint selection | the RULE (e.g. "argmin held-out eval loss over keeps every N steps"), not just the chosen step |
| Headline curve | start → best of the named metric |

### 5. Losses & evaluation (REQUIRED)

- **Training loss:** name the actual objective (e.g. "flow-matching velocity MSE over a
  16-step action chunk"); state what is frozen/trainable.
- **Eval regime:** declare exactly one primary regime — `offline action loss` /
  `open-loop MSE` / `sim closed-loop` / `real closed-loop` — then its methodology:
  - offline/open-loop: split (level, %, seed), sample count, normalization parity with
    training, seeding/caching that makes values comparable across steps and runs;
  - rollouts (sim or real): task list, trials per task, success criterion, who/what judged,
    initial-state randomization.
- **Comparisons:** any cross-model claim ("matches π0.5") must link the other model's eval
  artifact or a written protocol; otherwise omit the comparison.
- **Scope note:** say what the metric does NOT show (action-prediction loss ≠ task success).

### 6. Provenance (REQUIRED table; every row present, `unknown (<why>)` allowed)

| Row | Content |
|---|---|
| Trained by | person/org + dates |
| Training code | URL. Private repos: mark `(private)` and summarize contents in one clause, or mirror the plan into the card |
| Framework | training framework + **pinned commit**; versions of at minimum torch, transformers, and any adapter/PEFT library |
| Compute provider | provider + GPU type × count; CPU/RAM when dataloading was the bottleneck or config differs from provider default |
| Wall-clock | hours; preemption count and max steps lost (write "none" if none) |
| Total compute (RECOMMENDED) | FLOPs or GPU-hours + measurement method + stated uncertainty |
| Cost (RECOMMENDED) | USD, run and project-total (sweeps + failed attempts included) |
| Experiment tracking | wandb/other project + run ids, or `unknown (...)` |
| Authorship of this card | who wrote it; if publishing another's checkpoint: credit the trainer and mark which facts are reconstructed from artifacts vs. known first-hand |

### 7. Usage & I/O contract (REQUIRED)

The section that makes a robot checkpoint usable at all:

- Copy-paste loading snippet requiring zero edits.
- **Observation contract:** camera key names (and what each views), image resolution,
  state vector layout (key → index range).
- **Action contract:** dimension layout (key → index range), absolute vs delta, units or
  normalization convention, action-chunk horizon, control frequency if known, and **where
  normalization statistics live** in the repo (e.g. `experiment_cfg/`, `statistics.json`).
- Serving/deployment pointer (server script, client adapter).

### 8. Data provenance & caveats (REQUIRED)

- Data origin; license of each source (or of the mixture manifest + a statement that
  per-source licenses apply and where to find them).
- Known data issues: duplicates, imbalance, single-scene bias, teleoperator style.
- Honest limits of the eval relative to deployment. "No real-robot rollouts yet" if true.
- Training instabilities/failed attempts, or a link to the repo's incident log — a reader
  choosing hyperparameters learns more from "lr 6e-4 NaN'd at step 2.5k" than from the winner.

### 9. Versioning & contact (REQUIRED)

- If this card supersedes a checkpoint, set `new_version:` frontmatter on the old repo.
- State whether `main` is stable; recommend pinning by revision hash for reproduction.
- Where to report issues (HF Discussions on the repo, or a GitHub issues link).

## Failure modes to avoid (observed in the wild)

1. **Rich prose, empty metadata** — great documentation nobody can filter/find (no
   `pipeline_tag`, `datasets`, `base_model`). The model tree breaks for your downstream users.
2. **Rich metadata, no eval/safety prose** — users cannot judge fitness for their rig.
3. **Undocumented normalization/embodiment assumptions** — produces silently wrong actions
   on real hardware. The I/O contract (§7) exists because of this.
4. **License mismatch with the backbone** — stamping `apache-2.0` on a fine-tune of a
   custom-licensed base (NVIDIA License, Gemma, …). Use the license procedure in §1.
5. **Unfalsifiable eval claims** — success rates without trial counts/criteria, or numbers
   buried in images where no tooling can read them.

## Checklist (REQUIRED gate — copy into the publish commit/PR; any unchecked box blocks publish)

Frontmatter
- [ ] `license` set via the inheritance procedure (not defaulted)
- [ ] `base_model`, `pipeline_tag: robotics`, `tags` (robot + method), `inference: false`
- [ ] `datasets:` listing Hub-resident training data
- [ ] `library_name` set (or confirmed no library integration exists)

Body
- [ ] Header ≤3 sentences; every named artifact linked; adapter/merge status stated
- [ ] Intended use + out-of-scope + validation status (with e-stop/supervision language)
- [ ] Training table: data counts + filter/split rule (level, %, seed)
- [ ] Training table: embodiment config + state/action key layout
- [ ] Training table: image preprocessing (resolution + aspect handling)
- [ ] Training table: schedule (steps, batch, LR, hardware)
- [ ] Training table: checkpoint-selection RULE + headline curve (start → best, metric named)
- [ ] Training loss objective named; frozen/trainable stated
- [ ] Eval regime declared + methodology (split/samples/parity/seeding, or tasks/trials/criterion/judge)
- [ ] Cross-model comparisons linked to a protocol/artifact, or removed
- [ ] Metric scope note ("what this does not show")
- [ ] Provenance: all 9 rows present (`unknown (<why>)` where unrecoverable)
- [ ] Provenance: framework commit pinned; torch/transformers/adapter-lib versions
- [ ] Provenance: card authorship + reconstructed-vs-first-hand marking if third-party
- [ ] Usage: zero-edit loading snippet
- [ ] Usage: camera key names + resolutions
- [ ] Usage: action layout, absolute/delta, units/normalization, horizon, stats location
- [ ] Caveats: per-source data licensing statement
- [ ] Caveats: known data issues + eval-vs-deployment limits
- [ ] Caveats: instabilities/failed attempts included or linked
- [ ] Versioning + contact stated
- [ ] Card written from named run artifacts at publish time
