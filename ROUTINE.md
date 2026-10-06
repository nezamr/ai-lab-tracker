# Monthly update routine

This is the prompt the scheduled agent runs on the 1st of each month. It also works as a manual run: "follow ROUTINE.md".

## Steps

1. **Set the window.** The issue month is the month that just ended (YYYY-MM). Research runs from 7 days before the latest `valid_from` in `data/features.csv` through today. The overlap catches late-reported items; already-recorded ones get skipped. The issue covers **every** row with `valid_from` in the issue month, including rows an earlier run added.
2. **Research.** For each lab in `data/labs.csv`, check its listed sources, then run a web search for "<lab> launch OR release OR announces" in the window. Record only items that have a primary or reputable source. Never invent dates or features.
3. **Compare against current state.** Load the rows where `is_current=true`. For each finding:
   - **New feature:** append a row with `change_type=new`.
   - **Change to an existing `id`** (new version, GA from beta, pricing, a major capability): set the old row's `valid_to` to the new date and `is_current=false`, then append the new row with `change_type=changed`.
   - **Retirement or deprecation:** close the old row the same way, then append a row with `change_type=retired` and `status=retired` or `status=deprecated`.
   - **Already recorded:** skip it.
4. **Discover new labs.** Search for AI labs that broke out in the window: new frontier or open-weight labs, notable startups shipping their first product, and existing companies entering the space. Example queries: "new AI lab launches first model", "AI startup releases model", "open-weight model release" plus the month. Add a lab only when it has **shipped a product or model people can use**, has a primary source, and has gotten notable coverage. Funding news alone doesn't count.
   - Append it to `data/labs.csv` with `added_on=<today>`, `active=true`, and a group: `frontier`, `media`, or `fast-follower`, or `emerging` if none of those fit.
   - Append its first products to `features.csv` as `change_type=new`.
   - If a tracked lab shuts down, is acquired, or goes quiet for 6+ months, set `active=false`. Don't delete it.
   - Promote a lab out of `emerging` once it clearly fits a group.
5. **Validate.** Run `python3 scripts/validate.py`. It must pass.
6. **Write the issue** to `newsletters/YYYY-MM.md` using the format below, then add or update its entry in `newsletters/index.json` (`{"month","title","summary"}`).
7. **Commit and push:** `git commit -am "Issue YYYY-MM" && git push`. Vercel deploys the push.

## Issue format

```markdown
# AI Lab Tracker: <Month YYYY>

<2-3 sentence summary of the month's biggest themes>

## Headlines

- 3-5 most important items, each one line, with a link

## Frontier labs

### <Lab>

- 🆕 **Feature**: what it is. [source](url)
- 🔄 **Feature**: what changed (was X, now Y). [source](url)
- 🪦 **Feature**: retired or deprecated. [source](url)

## Image & video labs

...

## Fast followers

...

## New on the radar

- **<Lab>** (group): who they are and what they shipped. [source](url)
- Labs marked inactive this month, if any

## By the numbers

| Group | New | Changed | Retired |
```

Leave out labs that had no events in the month. Keep it tight: one line per item.
