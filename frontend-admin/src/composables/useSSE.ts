import { ref, onUnmounted } from 'vue'
import { sseService } from '@/services/sseService'
import { useOrderStore } from '@/stores/orderStore'

export function useSSE() {
  const connected = ref(false)

  function connect(storeCode: string): void {
    const orderStore = useOrderStore()
    sseService.on('order_created', (d: any) => orderStore.addOrder(d.data || d))
    sseService.on('order_status_changed', (d: any) => orderStore.updateOrderInList(d.order_id, d.new_status))
    sseService.on('order_deleted', (d: any) => orderStore.removeOrderFromList(d.order_id))
    sseService.connect(storeCode)
    connected.value = true
  }

  function disconnect(): void {
    sseService.disconnect()
    connected.value = false
  }

  onUnmounted(() => disconnect())

  return { connected, connect, disconnect }
}
