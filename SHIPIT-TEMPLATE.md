# 🚢 ShipIt — Non-Coder App Builder System

> Build your app. Ship it. No coding required.

---

## HOW TO USE THIS TEMPLATE

Work through each section in order. Complete one stage before moving to the next. Do not skip ahead — the structure exists for a reason.

**The 5 Stages:**
1. 🎯 Define (What are you building and why)
2. 🏗️ Scaffold (Set up your tools and project)
3. 🔨 Build (Step-by-step feature creation)
4. 🐛 Fix (Debug guide for common errors)
5. 🚀 Launch (Deploy and get your first users)

---

## STAGE 1: 🎯 DEFINE

### 1.1 Your App Idea (Fill in below)

**App Name:** _______________

**Core Problem It Solves:** _______________

**Who It's For:** _______________

**What It Does (One Sentence):** _______________

---

### 1.2 The "Kill Your App" Mindset

**Instructors at a Singapore vibe coding workshop taught this: Don't fall in love with your app.**

When vibe coding is fast, it's smarter to start over than patch a broken product. Killing an app isn't failure — it's feedback.

**Use this check before every build session:**

> "If this feature/fix takes more than 2 hours and the app still doesn't work — would I rather start over?"

If yes → Start a fresh project. Copy your working code into it. Don't keep patching.

---

### 1.3 Define Your MVP Scope

**The ONE thing your app must do to be considered a success:**

1. _______________
2. _______________
3. _______________

**Features that are NICE TO HAVE but NOT REQUIRED for launch:**

- _______________
- _______________
- _______________

**When to stop adding features:**
You stop when the CORE functionality works AND you've reached your launch readiness score of 7/10.

---

### 1.3 Prompt Quality Checklist

Before you send ANY prompt to your AI, check:

- [ ] Does it explain WHO the user is?
- [ ] Does it explain WHAT the expected output looks like?
- [ ] Does it explain WHAT should NOT happen?
- [ ] Does it provide CONTEXT about the existing codebase?
- [ ] Does it specify CONSTRAINTS (tech stack, style, etc.)?

If any of these are missing → rewrite before sending.

---

## STAGE 2: 🏗️ SCAFFOLD

### 2.1 Tool Setup

**Recommended Stack for Non-Coders:**

| Tool | Purpose | Free? |
|------|---------|-------|
| Cursor AI | Code generation + editing | Free tier |
| Replit | Cloud deployment | Free tier |
| Supabase | Database + auth | Free tier |
| Railway | Backend hosting | Free tier |
| Vercel | Frontend hosting | Free tier |

**Set up in this order:**
1. [ ] Create Replit account
2. [ ] Create Supabase account
3. [ ] Create Railway account
4. [ ] Create Vercel account
5. [ ] Install Cursor on your computer

---

### 2.2 First Project Setup

**In Cursor:**
1. Open Cursor → New Project
2. Name it: [Your App Name]
3. Tell Cursor: "I'm building [one sentence description]. Set up a [React/Next.js] project with Supabase integration."

**After setup, SAVE this system prompt to a notepad:**

```
You are helping me build [app name]. I am not a coder.
- Explain what you're doing in plain English
- When you make changes, tell me what changed
- If something breaks, explain the error simply
- Never assume I know programming terms
```

**Save this prompt for every new session.**

---

## STAGE 3: 🔨 BUILD

### Build Sequence (Do In Order)

Work through these in order. Each builds on the last. Do not skip to auth/database until the basic UI works.

**Step 1: Basic Layout**
Prompt: "Create a navigation bar with links to [pages]. Create a footer. Use Tailwind CSS. Keep it simple."

**Step 2: Landing Page**
Prompt: "Create a landing page with a hero section, a features section, and a CTA button. The CTA goes to /signup."

**Step 3: Signup Flow**
Prompt: "Create a signup page with email and password. Connect it to Supabase auth. Show a success message after signup."

**Step 4: Database Structure**
Prompt: "Create a Supabase table called [your_table_name] with these fields: [list fields]. Show me the SQL to create it."

**Step 5: Connect Data to UI**
Prompt: "Connect the landing page to Supabase. Show the user's [data] on the dashboard."

**Step 6: Core Feature**
Prompt: "[Specific description of your #1 feature]. Use the existing Supabase setup."

---

### Build Progress Tracker

- [ ] Step 1: Basic Layout
- [ ] Step 2: Landing Page
- [ ] Step 3: Signup Flow
- [ ] Step 4: Database Structure
- [ ] Step 5: Data Connected to UI
- [ ] Step 6: Core Feature

---

## STAGE 4: 🐛 FIX

### Common Errors and How to Fix Them

**Error: "Auth not working"**
→ Did you enable Email auth in Supabase Dashboard → Authentication → Providers?
→ Did you add the Supabase URL and anon key to your .env file?
→ Fix: "My Supabase auth isn't working. Here's what I tried: [describe]. What did I miss?"

**Error: "AI keeps rewriting code that was working"**
→ Context window collapse. Stop immediately.
→ Do: Copy your current working code to a backup file
→ Do: Start a fresh Cursor session with your backup code
→ Do: Give AI only ONE specific task at a time
→ Prevention: Use checkpoint prompts (see 4.2)

**Error: "App works locally but breaks on deployment"**
→ This is deployment anxiety. Common. Systematic fix:
1. Run `npm run build` locally — does it succeed?
2. Check Railway/Vercel logs for the specific error
3. Common fix: "The deployment failed with [error]. My tech stack is [Replit/Next.js]. What caused this?"

**Error: "AI gave me code and it's completely wrong"**
→ Your prompt was too vague. Start over with:
→ "I need you to [specific task]. The existing code is [file location]. Constraints: [list]. Do NOT [things to avoid]."

---

### 4.2 Checkpoint Prompt System

When your project gets large, use this before each major session:

```
SESSION CHECKPOINT
Project: [name]
Last completed: [what you finished]
Current goal: [what you're working on]
What broke last session: [if anything]
Key files: [list the 3-5 main files]
Tech stack: [list]
```

Paste this at the start of every session. It prevents context collapse.

---

### 4.3 Scope Creep Prevention

**Before adding ANY new feature, ask:**

1. Is this needed for the MVP? (Yes/No)
2. Will users leave if this is missing? (Yes/No)
3. Can I add this AFTER launch? (Yes/No)

If Yes to #3 → write it down in "Post-Launch Ideas" and move on.

---

## STAGE 5: 🚀 LAUNCH

### Pre-Launch Checklist

**Technical:**
- [ ] App loads without errors locally
- [ ] Signup/login works
- [ ] Core feature works for at least one user
- [ ] No console errors (Cursor → Console tab)
- [ ] Deployment succeeds on Vercel/Railway
- [ ] Live URL is accessible

**Content:**
- [ ] Landing page explains what the app does
- [ ] Clear call-to-action (signup / try now)
- [ ] Privacy policy (required for auth apps)
- [ ] Contact info or support link

---

### 5.1 Deployment Debug Cheatsheet

**Vercel Deployment Fails:**
Error: "Module not found" → Run `npm install` in terminal first
Error: "Build timeout" → Reduce initial load; remove large imports
Error: "Environment variable not set" → Add to Vercel → Settings → Environment Variables

**Railway Deployment Fails:**
Error: "Port not found" → Set PORT=3000 in Railway settings
Error: "Database connection failed" → Check Supabase connection string in .env

**General Rule:** Always check the deployment logs first. The error message tells you exactly what's wrong 80% of the time.

---

### 5.2 Get Your First Users

**Option 1: Post in communities**
- Share in r/SideProject, r/Entrepreneur, relevant niche subreddits
- Frame: "I built [app] in [timeframe] using vibe coding. Here's what I learned."

**Option 2: Direct outreach**
- Find 5 people who have the problem your app solves
- Message them directly with the link

**Option 3: Product Hunt**
- Launch on Product Hunt (free)
- Prepare: screenshots, 1-sentence description, your story

---

## PROMPT LIBRARY

### Startup Prompts to Copy and Use

**"Set up my project":**
"I want to build [description]. I have no coding experience. Set up a [Next.js/React] project with Supabase for auth and database. Give me step-by-step instructions."

**"Add a new page":**
"Create a new page at /[pagename]. It should have [elements]. Link it in the navigation. Keep the style consistent with the rest of the app."

**"Debug this error":**
"I'm getting this error: [paste error]. My tech stack is [list]. I'm not a coder — can you explain what went wrong and give me the exact fix?"

**"Add auth protection":**
"Protect the /dashboard page so only logged-in users can see it. If someone isn't logged in, send them to /login. Show me what to add and where."

---

## POST-LAUNCH IDEAS

Track features and improvements here for after your MVP is live:

1. _______________
2. _______________
3. _______________

---

## RESOURCE LINKS

- Supabase Docs: https://supabase.com/docs
- Cursor AI: https://cursor.sh
- Railway Deployment: https://railway.app
- Vercel Deployment: https://vercel.com
- Tailwind CSS: https://tailwindcss.com

---

*ShipIt — Built for non-coders who want to actually ship.*
*Version 1.0 | 2026*
