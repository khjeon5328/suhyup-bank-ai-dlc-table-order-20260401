import { ref, onUnmounted } from 'vue'
import { sseService } from '@/services/sseService'
import { useOrderStore } from '@/stores/order'
import { useTableStore } from '@/stores/table'
import { SSEEventType } from '@/types/sse'
import type { SSEEvent, SSEOrderCreatedData } from '@/types/sse'

export function useSSE() {
  const connected = ref(false)
  const retryCount = ref(0)
  let statusInterval: ReturnType<typeof setInterval> | null = null

  function handleEvent(event: SSEEvent): void {
    const orderStore = useOrderStore()
    const tableStore = useTableStore()

    orderStore.handleSSEEvent(event)

    if (event.type === SSEEventType.ORDER_CREATED) {
      const data = event.data as SSEOrderCreatedData
      tableStore.addNewOrderAlert(data.order.tableId)
    }
  }

  function connect(storeId: number): void {
    sseService.connect(storeId)
    sseService.onEvent('*', handleEvent)

    statusInterval = setInterval(() => {
      connected.value = sseService.status === 'connected'
      retryCount.value = sseService.status === 'reconnecting' ? retryCount.value + 1 : 0
    }, 2000)
  }

  function disconnect(): void {
    sseService.offEvent('*', handleEvent)
    sseService.disconnect()
    if (statusInterval) {
      clearInterval(statusInterval)
      statusInterval = null
    }
    connected.value = false
    retryCount.value = 0
  }

  onUnmounted(() => {
    disconnect()
  })

  return { connected, retryCount, connect, disconnect }
}
