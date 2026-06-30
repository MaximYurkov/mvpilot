module.exports = {
  'frontend/**/*.{ts,tsx,js,jsx}': [() => 'npm --prefix frontend run lint', 'prettier --write'],
  '*.{md,json}': 'prettier --write',
};
