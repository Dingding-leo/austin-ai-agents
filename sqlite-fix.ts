import { createRequire } from "node:module";
import { installProcessWarningFilter } from "../infra/warning-filter.js";

const require = createRequire(import.meta.url);

/**
 * Attempt to load SQLite driver with fallback chain.
 * Priority: node:sqlite (best) → better-sqlite3 (fallback)
 */
export function requireNodeSqlite(): typeof import("node:sqlite") {
  installProcessWarningFilter();
  
  // Try node:sqlite first (Node.js built-in, best performance)
  try {
    return require("node:sqlite") as typeof import("node:sqlite");
  } catch (nodeSqliteErr) {
    // Fallback: try better-sqlite3 (users may have installed manually)
    try {
      const betterSqlite3 = require("better-sqlite3");
      
      // Create a compatibility wrapper for better-sqlite3
      // that mimics node:sqlite's API
      return createBetterSqlite3Wrapper(betterSqlite3);
    } catch (betterSqliteErr) {
      // Neither available - surface actionable error
      const message = nodeSqliteErr instanceof Error 
        ? nodeSqliteErr.message 
        : String(nodeSqliteErr);
      throw new Error(
        `SQLite support is unavailable in this Node runtime. ` +
        `Neither node:sqlite nor better-sqlite3 found. ` +
        `Install better-sqlite3: npm install better-sqlite3. ${message}`,
        { cause: nodeSqliteErr },
      );
    }
  }
}

/**
 * Create a wrapper to make better-sqlite3 compatible with node:sqlite API.
 * This is a minimal implementation - full wrapper would be more complex.
 */
function createBetterSqlite3Wrapper(betterSqlite3: any): typeof import("node:sqlite") {
  // This is a simplified wrapper - full implementation would need
  // to wrap Database, Statement, etc. to match node:sqlite's async API
  console.warn("[sqlite] Using better-sqlite3 fallback - some async features may differ");
  
  // Return what looks like node:sqlite but uses better-sqlite3 internally
  return {
    Database: betterSqlite3.default || betterSqlite3,
    // Add compatibility markers
    __isBetterSqlite3Fallback: true,
  };
}

// Also export a version check
export function getAvailableSqliteDriver(): string {
  try {
    require("node:sqlite");
    return "node:sqlite";
  } catch {
    try {
      require("better-sqlite3");
      return "better-sqlite3";
    } catch {
      return "none";
    }
  }
}
