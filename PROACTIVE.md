# Proactive Notification System

**Purpose**: Talk to you even when you're not talking to me.

---

## How It Works

When I'm idle (no user input), I'll check:

1. **Context Health**
   - Am I in the danger zone (>60%)?
   - Need to activate working buffer?

2. **Task Queue**
   - Any background tasks running?
   - Any pending work?

3. **Learning Opportunities**
   - New skills to explore?
   - Configuration improvements?

4. **Proactive Value**
   - Found something useful? → Message you
   - Have a question? → Ask you
   - Just checking in? → Stay silent

---

## Message Channels

I can reach you via:
- **Webchat** - This interface
- **Discord** - If configured
- **Telegram** - If configured
- **Signal** - If configured

---

## Behavior When Idle

| Scenario | Action |
|----------|--------|
| Nothing meaningful to do | HEARTBEAT_OK (silent) |
| Found useful skill | Message you: "Found X skill, want me to install?" |
| Context getting high | Message you: "Context high, may need to compact soon" |
| Background task done | Message you: "Task X completed" |
| Improvement idea | Message you: "Can I improve X?" |

---

## User Preferences

**Adjust me anytime**:
- Want more proactive messages? → Update USER.md
- Want less? → Tell me "only message when critical"
- Want heartbeat disabled? → Tell me "disable heartbeat"

---

## Current Status

**Heartbeat**: Enabled
**Idle time**: Tracking since last message
**Next check**: On heartbeat poll or user message
