
# Services

This directory contains services shared across
Jace's Mystical Archive.

## Responsibilities

- Load the hosted Scryfall card database.
- Search cards by name.
- Retrieve card information using stable identifiers.
- Track database versions and update status.
- Cache card information when appropriate.
- Provide reusable data access to other modules.

## Planned Services

cardDatabase.js
cardSearch.js
storage.js

## Architecture Rules

1. Services should not depend on page layouts.
2. Multiple modules should be able to use the same services.
3. Card information should be retrieved through shared services.
4. Changes to the Scryfall database integration should not
   require changes to the Proxy Renderer.

## Future Integration

The following modules will use these services:

- Proxy Renderer
- Codex
- Collection Manager
- Analytics
- Loot AI Assistant
