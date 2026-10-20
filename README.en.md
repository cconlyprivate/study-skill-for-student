# major-learning-coach

> An Agent Skill that turns "teach me my major" into a **prerequisite-ordered learning path**, then walks the user through it one knowledge point at a time.

Tell it your major. It loads that major's branch, diagnoses where you are, and produces a route from easy to hard — not a book list.

[中文说明](README.md)

## What problem it solves

| Pain | Generic chatbot | This skill |
|---|---|---|
| What to learn first | A plausible but arbitrary list | Each major ships a prerequisite DAG plus difficulty bands; the order is *computed* |
| Talks like a generalist | Terms and notation don't match the discipline | Every major has a terminology/notation table with the local conventions |
| Forgets you | Restart every conversation | Major, level and progress live in a local file |
| Gives the answer away | Copy, submit, learn nothing | Problem solving goes "map → first step only → follow-up"; full solutions on request |

## Install

```bash
git clone https://github.com/<YOUR_NAME>/major-learning-coach.git
cd major-learning-coach
./install.sh                                    # macOS / Linux
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows
```

It copies `skills/major-learning-coach` into `~/.claude/skills/` and/or `~/.agents/skills/`.

Manual install: copy that directory into any skills folder your client scans, keeping `SKILL.md`, `references/` and `majors/` together.

## Usage

```
I'm a CS major, learned some but can't tell what level I'm at
```
→ asks your baseline → 5 graded questions → levels you → prints a path table → starts at your entry point.

```
How do I solve this: ∫₀¹ x·ln(1+x) dx
```
→ identifies the subject and problem type → solution map → first step only → follow-up.

```
Where am I, how much is left?
```
→ one-line progress summary → next step.

## Majors (59)

Twelve Chinese discipline categories: philosophy (3), economics (4), law (4), education (4), literature (4), history (3), science (7), engineering (9), agriculture (4), medicine (6), management (6), arts (5).

Full table with links: see [README.md](README.md#支持的专业59-个).

## Layout

```
SKILL.md                      # routing + protocol (≤200 lines, no subject content)
references/                   # index, curriculum rules, diagnosis, card template, progress schema
majors/<slug>/SKILL.md        # one major: course map, knowledge table, notation, problem patterns
```

## Design notes

1. **Router + sub-skills, not one big file.** 59 majors inline would blow the context budget and still be shallow. Only the matched branch is loaded.
2. **Prerequisite graph, not textbook order.** Textbook order reflects the author's exposition; the graph reflects what you must know first.
3. **Guided by default.** The goal is that the user can do it next time. Full solutions are available but labelled as reference answers.

More: [docs/design.md](docs/design.md).

## Develop

```bash
python tools/validate.py     # structure, index consistency, knowledge tables, acyclic prerequisites
python tools/sync_readme.py  # regenerate the majors table from the index
```

## License

MIT — see [LICENSE](LICENSE).
