import { useAsyncAction } from '@/composables/useAsyncAction'

describe('useAsyncAction', () => {
  it('should have loading false initially', () => {
    const { loading } = useAsyncAction()
    expect(loading.value).toBe(false)
  })

  it('should set loading true during execution', async () => {
    const { loading, execute } = useAsyncAction()
    let loadingDuringExec = false

    await execute(async () => {
      loadingDuringExec = loading.value
      return 'result'
    })

    expect(loadingDuringExec).toBe(true)
    expect(loading.value).toBe(false)
  })

  it('should return result on success', async () => {
    const { execute } = useAsyncAction()
    const result = await execute(async () => 'hello')
    expect(result).toBe('hello')
  })

  it('should set error on failure', async () => {
    const { error, execute } = useAsyncAction()
    await execute(async () => {
      throw new Error('test error')
    })
    expect(error.value).toBe('test error')
  })
})
