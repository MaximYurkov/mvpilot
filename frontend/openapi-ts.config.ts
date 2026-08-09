import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: 'fetch',
  input: 'https://raw.githubusercontent.com/MaximYurkov/mvpilot/dev-backend/backend/openapi.json',
  output: './src/api',
});
