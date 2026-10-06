# AI Lab Tracker

Monthly newsletter and dashboard tracking product and feature changes at frontier, image/video, and fast-follower AI labs.

## Layout

- `data/labs.csv`: the labs tracked, with their group (frontier, media, fast-follower, emerging), source URLs, `added_on`, and `active`. The monthly routine adds new labs and marks dead ones inactive; it never deletes them.
- `data/features.csv`: an SCD Type 2 history table. Each event is one row. When a feature changes, the old row is closed (`valid_to` set, `is_current=false`). Never rewrite history; append to it.
- `newsletters/YYYY-MM.md` + `newsletters/index.json`: the monthly issues.
- `index.html`: a static dashboard (d3, Observable Plot, and marked, all from CDN). No build step. Vercel serves the repo root.
- `scripts/validate.py`: checks CSV integrity (schema, enums, one current row per id, closed rows chained).
- `ROUTINE.md`: the monthly update procedure. The scheduled cloud routine follows it.

## Conventions

- `id` is a stable slug per feature (`openai-codex`) and stays the same across versions of that feature. A major new model family gets a new id; a point release counts as `changed`.
- Enums: category ∈ model, consumer-app, agent, developer, enterprise, media, voice, hardware, other. change_type ∈ new, changed, retired. status ∈ preview, beta, ga, deprecated, retired.
- Every row needs a `source_url`. Never fabricate.

## Local preview

`python3 -m http.server 8000`, then open http://localhost:8000
