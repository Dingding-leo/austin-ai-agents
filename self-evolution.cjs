#!/usr/bin/env node

/**
 * Self-Evolution Engine
 * Analyzes capabilities, identifies gaps, generates improvement plans
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/Users/tsliu/Downloads/Openclaw/.state/.openclaw/workspace-dev';
const CAPABILITIES_FILE = path.join(WORKSPACE, 'capabilities.json');
const IMPROVEMENTS_FILE = path.join(WORKSPACE, 'improvements.json');

// Core capability categories - more comprehensive
const CAPABILITY_CATEGORIES = {
  'Language & Code': ['node', 'npm', 'npx', 'python', 'python3', 'go', 'rustc', 'cargo', 'java', 'gcc', 'clang', 'ruby', 'php', 'perl', 'bash', 'zsh', 'shell'],
  'AI & ML': ['openai', 'anthropic', 'gemini', 'llm', 'image', 'whisper', 'tts', 'ml', 'ai'],
  'Web & Network': ['curl', 'wget', 'nginx', 'apache', 'browser', 'chrome', 'firefox', 'http', 'https', 'ssh', 'scp'],
  'Data': ['json', 'yaml', 'xml', 'sql', 'mysql', 'postgres', 'sqlite', 'csv', 'pdf', 'pandoc'],
  'System': ['file', 'disk', 'process', 'exec', 'docker', 'git', 'ssh', 'scp', 'rsync'],
  'Communication': ['discord', 'slack', 'whatsapp', 'telegram', 'signal', 'imessage', 'email', 'sag', 'wacli', 'himalaya', 'apple-notes', 'things-mac', 'notion', 'trello'],
  'Media': ['image', 'video', 'audio', 'ffmpeg', 'gif', 'photo', 'camera', 'spotify', 'vlc', 'convert', 'sips'],
  'Cloud': ['aws', 'gcp', 'azure', 'docker', 'kubectl', 'helm', 'terraform'],
  'Security': ['encrypt', 'key', 'vault', 'openssl', 'ssl', 'tls', 'ssh', 'gpg'],
  'DevOps': ['ci', 'cd', 'jenkins', 'circleci', 'travis', 'test', 'monitor']
};

// Check what tools/CLIs are available
function detectCapabilities() {
  const detected = {
    timestamp: new Date().toISOString(),
    categories: {},
    raw: []
  };
  
  // Check common binaries
  const binaries = ['node', 'python3', 'go', 'rustc', 'docker', 'gh', 'git', 'npm', 'npx'];
  
  for (const bin of binaries) {
    try {
      const result = require('child_process').execFileSync(`which ${bin}`, { encoding: 'utf8' });
      if (result.trim()) {
        detected.raw.push(bin);
      }
    } catch (e) {
      // Not found
    }
  }
  
  // Check homebrew packages - FIXED
  try {
    const brew = require('child_process').execSync('ls /opt/homebrew/bin/', { encoding: 'utf8' });
    const packages = brew.trim().split('\n').filter(p => p.trim() && !p.startsWith('@'));
    detected.raw.push(...packages);
  } catch (e) {}
  
  // Also check OpenClaw skills directory
  const skillsDir = '/Users/tsliu/Downloads/Openclaw/skills';
  try {
    const skills = fs.readdirSync(skillsDir);
    for (const skill of skills) {
      if (!detected.raw.includes(skill)) {
        detected.raw.push(skill);
      }
    }
  } catch (e) {}
  
  // Categorize
  for (const [category, keywords] of Object.entries(CAPABILITY_CATEGORIES)) {
    detected.categories[category] = [];
    for (const keyword of keywords) {
      for (const tool of detected.raw) {
        if (tool.toLowerCase().includes(keyword.toLowerCase())) {
          if (!detected.categories[category].includes(tool)) {
            detected.categories[category].push(tool);
          }
        }
      }
    }
  }
  
  return detected;
}

// Identify gaps
function identifyGaps(detected) {
  const gaps = [];
  const threshold = 2; // Minimum tools per category
  
  for (const [category, tools] of Object.entries(detected.categories)) {
    if (tools.length < threshold) {
      gaps.push({
        category,
        current: tools.length,
        needed: threshold,
        suggestion: `Add more ${category.toLowerCase()} tools`
      });
    }
  }
  
  return gaps;
}

// Generate improvement plan
function generatePlan(detected, gaps) {
  const plan = {
    generated: new Date().toISOString(),
    strengths: [],
    improvements: [],
    nextActions: []
  };
  
  // Find strengths
  for (const [category, tools] of Object.entries(detected.categories)) {
    if (tools.length >= 3) {
      plan.strengths.push({ category, tools });
    }
  }
  
  // Plan improvements
  for (const gap of gaps) {
    plan.improvements.push({
      category: gap.category,
      priority: gap.current === 0 ? 'high' : 'medium',
      action: `Install/配置 ${gap.category} tools`
    });
  }
  
  // Next actions
  plan.nextActions = [
    'Install missing CLI tools',
    'Configure more skill integrations',
    'Add cloud provider support',
    'Enable more communication channels'
  ];
  
  return plan;
}

// Main
const detected = detectCapabilities();
const gaps = identifyGaps(detected);
const plan = generatePlan(detected, gaps);

console.log('\n=== SELF-EVOLUTION ANALYSIS ===\n');
console.log('Detected Capabilities:', detected.raw.length, 'tools');
console.log('\nBy Category:');
for (const [cat, tools] of Object.entries(detected.categories)) {
  if (tools.length > 0) {
    console.log(`  ${cat}: ${tools.length} (${tools.join(', ').slice(0, 50)}...)`);
  }
}

console.log('\n=== GAPS ===');
for (const gap of gaps) {
  console.log(`  [${gap.category}] Has ${gap.current}, needs ${gap.needed}`);
}

console.log('\n=== IMPROVEMENT PLAN ===');
for (const imp of plan.improvements) {
  console.log(`  [${imp.priority}] ${imp.category}: ${imp.action}`);
}

console.log('\n=== STRENGTHS ===');
for (const str of plan.strengths) {
  console.log(`  ✓ ${str.category}: ${str.tools.join(', ')}`);
}

// Save results
fs.writeFileSync(CAPABILITIES_FILE, JSON.stringify(detected, null, 2));
fs.writeFileSync(IMPROVEMENTS_FILE, JSON.stringify(plan, null, 2));

console.log('\n✓ Saved to capabilities.json and improvements.json');
