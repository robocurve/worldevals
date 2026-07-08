# Model cards for Robocurve HuggingFace uploads

Every checkpoint published to the [robocurve](https://huggingface.co/robocurve) org **must**
ship a model card following this guide. Agents (Claude sessions) publishing future checkpoints:
read this before writing the card. The reference implementations are
[gr00t-n1.7-so101-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-so101-molmoact2) and
[gr00t-n1.7-yam-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-yam-molmoact2).

## Why this exists

WorldEvals compares policies across labs, robots, and training stacks. A benchmark number is
only interpretable if the checkpoint behind it documents what it was trained on, how, at what
cost, and what its eval numbers actually measure. Cards written from memory a week later are
wrong; write the card at publish time, from the run's own artifacts (trainer state, wandb,
decision records).

## Required sections

### 1. YAML frontmatter (machine-readable)

```yaml
---
license: apache-2.0            # or the tightest license the data permits
base_model: nvidia/GR00T-N1.7-3B
tags: [robotics, vla, <robot>, <method>, lerobot]
---
```

`base_model` matters: it powers HF's finetune graph and lets people trace lineage.

### 2. Header — what this is, in two sentences

Base model + method (LoRA/full FT) + robot/embodiment + dataset. Link every noun.
State whether adapters are merged, and where the raw adapters live if published.

### 3. Training table

One row each: data (counts: repos/episodes/frames + how filtered/split), embodiment/modality
mapping, image preprocessing, schedule (steps, batch, LR + schedule, hardware), checkpoint
selection rule, and the headline curve (start → best, with the metric named).

### 4. Losses — train AND eval, explicitly

The single most-skipped section, and the one reviewers need most:

- **Training loss**: name the actual objective (e.g. "flow-matching velocity MSE on 16-step
  action chunks"), not just "the model's loss". Say what is frozen.
- **Eval/test loss or metric**: same objective on held-out data, or a different metric
  (open-loop MSE, success rate)? Spell out the split (episode-level? repo-level? %),
  the sample count, normalization parity with training, and any seeding/caching that makes
  numbers comparable across steps or runs.
- Say what the metric does NOT show (action-prediction loss ≠ task success).

### 5. Provenance table

| Field | What to include |
|---|---|
| Trained by | person/org + dates |
| Training code | repo link — must include the plan/decision records, not just scripts |
| Framework | training framework + **pinned commit**, key library versions |
| Compute provider | provider + GPU type/count + CPU/RAM if it mattered |
| Wall-clock | hours, noting preemptions/resumes if relevant |
| Total compute | FLOPs estimate + how it was measured, with caveats stated |
| Cost | run cost and project-total (sweeps + failed attempts count — report them honestly) |
| Experiment tracking | wandb/other project + run ids |

### 6. Usage

Copy-pasteable loading snippet, serving instructions, and the I/O contract: camera key
names, state/action dimension layout and units, action horizon. This is where robot
checkpoints differ from LLMs — an undocumented modality mapping makes the checkpoint useless.

### 7. Data provenance & caveats

- Where the data came from, licenses (including per-source licenses for community mixtures).
- Known data issues (duplicates, imbalance, single-scene bias).
- Honest limits: what the eval measures vs. what deployment needs; "no real-robot rollouts
  yet" if true.

## Style rules

- Numbers over adjectives ("eval loss 1.129 → 0.0273", never "converged well").
- Every claim traceable to an artifact (trainer_state.json, wandb, eval_results.json).
- Failed attempts and instabilities belong in the card or the linked repo — a reader
  choosing hyperparameters learns more from "6e-4 NaN'd at step 2.5k" than from the winner.
- If publishing someone else's checkpoint, credit the trainer in Provenance and mark what
  was reconstructed from artifacts vs. known first-hand.
- Uncertain measurements get their uncertainty stated (e.g. FLOPs "order-of-magnitude,
  method X undercounts Y").

## Checklist (copy into the publish PR/commit)

- [ ] Frontmatter: license, base_model, tags
- [ ] Two-sentence header, all nouns linked
- [ ] Training table with counts, schedule, selection rule
- [ ] Losses: training objective AND eval metric, with split methodology
- [ ] Provenance: trainer, code link, framework pin, provider, compute, cost, tracking
- [ ] Usage: loading snippet + modality/action contract
- [ ] Caveats: data licenses, known issues, eval limits
