# Stimulus Mapping

Task: `Oddball Task (MMN/P3)`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `standard` | `standard_cue`, `standard_target` | `W2003906510` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for STANDARD; target token for condition-specific response context. |
| `deviant` | `deviant_cue`, `deviant_target` | `W2003906510` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for DEVIANT; target token for condition-specific response context. |
| `target` | `target_cue`, `target_target` | `W2003906510` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for TARGET; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
