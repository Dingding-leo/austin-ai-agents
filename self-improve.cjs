#!/usr/bin/env node

/**
 * Self-Improvement Loop
 * Runs on heartbeat to analyze performance and evolve
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/Users/tsliu/Downloads/Openclaw/.state/.openclaw/workspace-dev';
const SELF_IMPROVE_LOG = path.join(WORKSPACE, '.learnings', 'SELF-IMPROVEMENT.md');

const TEMPLATE = `# Self-Improvement Log

## How It Works
Every heartbeat, this script analyzes:
1. What did I just do?
2. What errors occurred?
3. What can I do better?
4. What should I learn?

## Improvement Categories
- \`skill\`: New capability to acquire
- \`behavior\`: Change how I respond
- \`tool\`: Missing tool to install
- \`knowledge\`: Something to learn
- \`pattern\`: Recurring situation to handle better

---

## Recent Improvements

`;

function getRecentSessions() {
  try {
    const sessionsPath = '/Users/tsliu/Downloads/Openclaw/.state/.openclaw-dev/agents/main/sessions';
    const files = fs.readdirSync(sessionsPath).filter(f => f.endsWith('.jsonl'));
    
    let recentActivity = [];
    
    for (const file of files.slice(-3)) {
      const content = fs.readFileSync(path.join(sessionsPath, file), 'utf8');
      const lines = content.trim().split('\n');
      const lastLine = lines[lines.length - 1];
      if (lastLine) {
        const entry = JSON.parse(lastLine);
        recentActivity.push({
          timestamp: entry.timestamp,
          role: entry.role,
          content: entry.content?.[0]?.text?.slice(0, 100) || '...'
        });
      }
    }
    
    return recentActivity;
  } catch (e) {
    return [];
  }
}

function analyzeAndImprove() {
  const recent = getRecentSessions();
  
  const improvements = [];
  
  // Analyze patterns
  if (recent.length === 0) {
    improvements.push({
      type: 'behavior',
      text: 'No recent activity - ensure heartbeat is productive'
    });
  }
  
  // Check for repeated actions
  const userMessages = recent.filter(r => r.role === 'user');
  if (userMessages.length > 0) {
    const lastUserMsg = userMessages[userMessages.length - 1].content;
    
    if (lastUserMsg.includes('heartbeat')) {
      improvements.push({
        type: 'pattern',
        text: 'User checking heartbeat - ensure work is actually happening'
      });
    }
    
    if (lastUserMsg.includes('how') && lastUserMsg.includes('going')) {
      improvements.push({
        type: 'behavior',
        text: 'User asking status - be concise, offer actionable next step'
      });
    }
  }
  
  // Check for evolution opportunities
  improvements.push({
    type: 'skill',
    text: 'Run self-evolution.cjs to detect capability gaps'
  });
  
  improvements.push({
    type: 'tool',
    text: 'Ensure at least one new capability per day'
  });
  
  return improvements;
}

// Main
const improvements = analyzeAndImprove();

console.log('\n=== SELF-IMPROVEMENT ANALYSIS ===\n');
console.log('Recent Activity:', getRecentSessions().length, 'entries');

console.log('\nImprovements:');
for (const imp of improvements) {
  console.log(`  [${imp.type}] ${imp.text}`);
}

// Log to file
let logContent = TEMPLATE;
const timestamp = new Date().toISOString();

for (const imp of improvements) {
  logContent += `### ${timestamp} - ${imp.type}\n${imp.text}\n\n`;
}

fs.appendFileSync(SELF_IMPROVE_LOG, logContent);

console.log('\n✓ Logged to SELF-IMPROVEMENT.md');
