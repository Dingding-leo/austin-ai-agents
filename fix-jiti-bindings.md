# Fix Analysis: Plugin Jiti Native Bindings

## Issue
#36377 - Mem0 OSS Plugin unusable on OpenClaw 2026.3.x due to jiti/sqlite3 binding regression

## Root Cause

The jiti loader in `src/plugins/loader.ts` is created with OpenClaw's `import.meta.url`:

```typescript
jitiLoader = createJiti(import.meta.url, { ... });
```

When a plugin (like Mem0) imports sqlite3, jiti resolves native bindings relative to OpenClaw's path instead of the plugin's node_modules:

```
/home/user/.npm-global/lib/node_modules/openclaw/node_modules/jiti/build/node_sqlite3.node
                                              ↑ WRONG - should be plugin's sqlite3
```

## Current Code (loader.ts line ~438)

```typescript
jitiLoader = createJiti(import.meta.url, {
  interopDefault: true,
  // ... extensions and aliases
});
```

## Solution

Create a per-plugin jiti loader with the plugin's root directory:

```typescript
const getPluginJiti = (pluginRootDir: string) => {
  return createJiti(pluginRootDir, {
    interopDefault: true,
    // ... same options
  });
};
```

Then use this for each plugin instead of the global jitiLoader.

## Files to Modify

1. `src/plugins/loader.ts` - Create per-plugin jiti instances
2. May need to pass plugin's `rootDir` through the load function

## Alternative Workaround

For Mem0 specifically:
- Disable SQLite-based history in the plugin
- Use the proposed `disableHistory` flag (not yet merged in plugin)
- Or wait for the jiti fix in OpenClaw

## References
- Original issue: #31676, #31677
- This issue: #36377
- Plugin loader: src/plugins/loader.ts
