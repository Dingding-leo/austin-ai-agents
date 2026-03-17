#!/usr/bin/env node

/**
 * Patch config.ts to fix RangeError in buildMergedSchemaCacheKey
 * Fix: Add caching with smaller cache keys
 */

import { readFileSync, writeFileSync } from 'fs';

const filePath = process.argv[2] || './src/gateway/server-methods/config.ts';
let content = readFileSync(filePath, 'utf8');

// Check if already patched
if (content.includes('schemaCache')) {
  console.log('Already patched');
  process.exit(0);
}

// Add cache variables after imports
const importSection = `import { buildConfigSchema, type ConfigSchemaResponse } from "../../config/schema.js";
import { createHash } from "crypto";`;

const cacheVars = `import { buildConfigSchema, type ConfigSchemaResponse } from "../../config/schema.js";
import { createHash } from "crypto";

// Cache for schema to prevent RangeError with large configs
let schemaCache: { key: string; value: ConfigSchemaResponse; timestamp: number } | null = null;
const SCHEMA_CACHE_TTL_MS = 60000;

function buildSchemaCacheKey(plugins: any[], channels: any[]): string {
  // Use only IDs and counts - much smaller than full schema
  const pluginIds = plugins.map(p => p.id).sort().join(',');
  const channelIds = channels.map(c => c.id).sort().join(',');
  return createHash('sha256').update(\`p:\${plugins.length}:\${pluginIds}|c:\${channels.length}:\${channelIds}\`).digest('hex').slice(0, 32);
}`;

content = content.replace(
  'import { buildConfigSchema, type ConfigSchemaResponse } from "../../config/schema.js";',
  cacheVars
);

// Now add caching to loadSchemaWithPlugins function
const oldFunction = `function loadSchemaWithPlugins(): ConfigSchemaResponse {
  const cfg = loadConfig();
  const workspaceDir = resolveAgentWorkspaceDir(cfg, resolveDefaultAgentId(cfg));
  const pluginRegistry = loadOpenClawPlugins({
    config: cfg,
    cache: true,
    workspaceDir,
    logger: {
      info: () => {},
      warn: () => {},
      error: () => {},
      debug: () => {},
    },
  });
  // Note: We can't easily cache this, as there are no callback that can invalidate
  // our cache. However, both loadConfig() and loadOpenClawPlugins() already cache
  // their results, and buildConfigSchema() is just a cheap transformation.
  return buildConfigSchema({`;

const newFunction = `function loadSchemaWithPlugins(): ConfigSchemaResponse {
  const cfg = loadConfig();
  const workspaceDir = resolveAgentWorkspaceDir(cfg, resolveDefaultAgentId(cfg));
  const pluginRegistry = loadOpenClawPlugins({
    config: cfg,
    cache: true,
    workspaceDir,
    logger: {
      info: () => {},
      warn: () => {},
      error: () => {},
      debug: () => {},
    },
  });
  
  // Build plugin/channel metadata for cache key (not full schema)
  const pluginsMeta = pluginRegistry.plugins.map((plugin) => ({
    id: plugin.id,
    name: plugin.name,
    description: plugin.description,
    configUiHints: plugin.configUiHints,
    configSchema: plugin.configJsonSchema,
  }));
  const channelsMeta = listChannelPlugins().map((entry) => ({
    id: entry.id,
    label: entry.meta.label,
    description: entry.meta.blurb,
    configSchema: entry.configSchema?.schema,
    configUiHints: entry.configSchema?.uiHints,
  }));
  
  // Check cache with small key
  const cacheKey = buildSchemaCacheKey(pluginsMeta, channelsMeta);
  if (schemaCache && schemaCache.key === cacheKey && Date.now() - schemaCache.timestamp < SCHEMA_CACHE_TTL_MS) {
    return schemaCache.value;
  }
  
  const result = buildConfigSchema({`;

content = content.replace(oldFunction, newFunction);

// Also need to fix the return statement
const oldReturn = `}));
}

export const configHandlers: GatewayRequestHandlers = {`;

const newReturn = `}));
  
  // Cache the result
  schemaCache = { key: cacheKey, value: result, timestamp: Date.now() };
  return result;
}

export const configHandlers: GatewayRequestHandlers = {`;

content = content.replace(oldReturn, newReturn);

writeFileSync(filePath, content);
console.log('Patched successfully');
