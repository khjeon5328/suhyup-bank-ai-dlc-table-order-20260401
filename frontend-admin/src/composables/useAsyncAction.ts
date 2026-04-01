import { ref } from 'vue'

export function useAsyncAction() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function execute<T>(action: () => Promise<T>): Promise<T | undefined> {
    loading.value = true
    error.value = null
    try {
      const result = await action()
      return result
    } catch (e: unknown) {
      error.value = (e as Error).message
      return undefined
    } finally {
      loading.value = false
    }
  }

  return { loading, error, execute }
}
