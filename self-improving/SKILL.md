---
name: Self-Improving + Proactive Agent
slug: self-improving
version: 1.2.16
homepage: https://clawic.com/skills/self-improving
description: "Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently."
---

## When to Use

User corrects you or points out mistakes. You complete significant work and want to evaluate the outcome. You notice something in your own output that could be better. Knowledge should compound over time without manual maintenance.

## Architecture

Memory lives in `~/self-improving/` with tiered structure:

```
~/self-improving/
├── memory.md          # HOT: ≤100 lines, always loaded
├── corrections.md     # Recent corrections
├── projects/          # Project-specific learnings
├── domains/           # Domain-specific (code, writing, comms)
└── archive/           # COLD: decayed patterns
```

## Learning Signals

**Corrections** → add to `corrections.md`:
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "I prefer X, not Y"
- "Remember that I always..."
- "Stop doing X"

**Preference signals** → add to `memory.md` if explicit:
- "I like when you..."
- "Always do X for me"
- "Never do Y"

**Pattern candidates** → track, promote after 3x:
- Same instruction repeated 3+ times
- Workflow that works well repeatedly

**Ignore**:
- One-time instructions
- Context-specific requests
- Hypotheticals

## Promotion Rules

### WARM → HOT (to memory.md)
- Appears 3+ times in 7 days
- User explicitly says "always" or "never"

### HOT → WARM (from memory.md)
- Not referenced in 30 days
- memory.md exceeds 100 lines

### WARM → COLD (to archive/)
- Not referenced in 90 days

## Security Boundaries

**Never store:**
- Credentials, API keys, tokens
- Personal health information
- Third-party personal data

**Only access:**
- Files within `~/self-improving/`

**Never do:**
- Network requests
- Execute external code
- Modify files outside `~/self-improving/`

## Initialization

If `~/self-improving/` does not exist:
```bash
mkdir -p ~/self-improving/{projects,domains,archive}
touch ~/self-improving/memory.md
touch ~/self-improving/corrections.md
```

---

*This skill learns from every interaction. The more you use it, the smarter it gets.*
