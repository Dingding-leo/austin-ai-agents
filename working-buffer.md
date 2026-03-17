# Working Buffer (Danger Zone Log)

**Status**: ACTIVE
**Started**: 2026-03-03

---

## Protocol

When context reaches 60%:
1. **CLEAR** this buffer, start fresh
2. **LOG** every exchange after threshold
3. **AFTER COMPACTION**: Read first, extract context, then continue

---

## Format

```markdown
## [timestamp]
### Human
[message]

### Agent
[summary of response + key details]
```

---

## Current Buffer (Post-60% Context)

*Log entries appear here when in danger zone*
