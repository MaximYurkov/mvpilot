import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: './openapi.json',
  output: './generated',
  plugins: ['@hey-api/typescript'],
});
