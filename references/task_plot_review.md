# Task Plot Review

## Evidence Match

- Pass: title and construct match the three-stimulus visual oddball task.
- Pass: Standard, Deviant, and Target rows match configured conditions and weights.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Stimulus response window -> Outcome classification -> ITI.
- Pass: timing labels match human config: 300 ms fixation, 500 ms stimulus, 500 ms ITI.
- Pass: standard and deviant rows show withheld responses; target row shows SPACE response.
- Pass: outcome classification is marked as internal, with no per-trial feedback screen.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
