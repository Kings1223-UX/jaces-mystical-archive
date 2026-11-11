
/**
 * Jace's Mystical Archive
 * Shared Scryfall Card Database Service
 * Version 1.3
 */

const DATABASE_URL = "./cards.json";
const VERSION_URL = "./database-version.json";

let cards = [];
let databaseVersion = null;
let loaded = false;

/**
 * Load the hosted card database.
 */
export async function loadCardDatabase() {
  if (loaded) return cards;

  const response = await fetch(DATABASE_URL);

  if (!response.ok) {
    throw new Error(
      `Database request failed: ${response.status}`
    );
  }

  const data = await response.json();

  if (!Array.isArray(data)) {
    throw new Error("Invalid card database format.");
  }

  cards = data;
  loaded = true;

  return cards;
}

/**
 * Search cards by name.
 */
export function searchCards(query, limit = 10) {
  if (!query || !loaded) return [];

  const normalized = query.trim().toLowerCase();

  const startsWith = [];
  const contains = [];

  for (const card of cards) {
    const name = card.name.toLowerCase();

    if (name.startsWith(normalized)) {
      startsWith.push(card);
    } else if (name.includes(normalized)) {
      contains.push(card);
    }
  }

  return [...startsWith, ...contains].slice(0, limit);
}

/**
 * Find a card by its exact name.
 */
export function getCardByName(name) {
  if (!loaded) return null;

  const normalized = name.trim().toLowerCase();

  return cards.find(
    card => card.name.toLowerCase() === normalized
  ) || null;
}

/**
 * Retrieve database version information.
 */
export async function getDatabaseVersion() {
  if (databaseVersion) return databaseVersion;

  const response = await fetch(VERSION_URL);

  if (!response.ok) {
    throw new Error("Unable to retrieve database version.");
  }

  databaseVersion = await response.json();

  return databaseVersion;
}

/**
 * Check whether the database is loaded.
 */
export function isDatabaseReady() {
  return loaded;
}
