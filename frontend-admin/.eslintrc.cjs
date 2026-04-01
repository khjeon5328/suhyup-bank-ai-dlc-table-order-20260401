module.exports = {
  root: true, env: { node: true, browser: true, es2020: true },
  extends: ['eslint:recommended', 'plugin:vue/vue3-recommended', 'plugin:@typescript-eslint/recommended'],
  parser: 'vue-eslint-parser',
  parserOptions: { parser: '@typescript-eslint/parser', ecmaVersion: 2020, sourceType: 'module' },
  rules: { 'vue/multi-word-component-names': 'off', '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }] },
}
