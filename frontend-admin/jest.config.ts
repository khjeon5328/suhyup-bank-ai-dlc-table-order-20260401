import type { Config } from 'jest'
const config: Config = {
  testEnvironment: 'jsdom',
  transform: { '^.+\\.vue$': '@vue/vue3-jest', '^.+\\.tsx?$': 'ts-jest' },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'vue', 'json'],
  moduleNameMapper: { '^@/(.*)$': '<rootDir>/src/$1' },
  testMatch: ['<rootDir>/tests/unit/**/*.spec.ts'],
}
export default config
