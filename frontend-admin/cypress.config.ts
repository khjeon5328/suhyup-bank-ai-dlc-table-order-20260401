import { defineConfig } from 'cypress'
export default defineConfig({ e2e: { baseUrl: 'http://localhost:3001', specPattern: 'tests/e2e/specs/**/*.cy.ts', supportFile: 'tests/e2e/support/e2e.ts' } })
