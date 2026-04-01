import { ref } from 'vue'
import { defineStore } from 'pinia'
import { tableApi } from '@/services/tableApi'
import type { TableSummary } from '@/types/table'

export const useTableStore = defineStore('table', () => {
  const tables = ref<TableSummary[]>([])
  const newOrderTableIds = ref<Set<number>>(new Set())
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTables(storeId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await tableApi.getTables(storeId)
      tables.value = response.data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function setupTable(storeId: number, tableNumber: number, password: string): Promise<void> {
    const response = await tableApi.setupTable(storeId, tableNumber, password)
    tables.value.push(response.data)
  }

  async function endSession(storeId: number, tableId: number): Promise<void> {
    await tableApi.endSession(storeId, tableId)
    const table = tables.value.find((t) => t.tableId === tableId)
    if (table) {
      table.hasActiveSession = false
      table.totalOrderAmount = 0
      table.orderCount = 0
      table.latestOrders = []
      table.statusSummary = { pending: 0, preparing: 0, completed: 0 }
    }
  }

  function markAsRead(tableId: number): void {
    newOrderTableIds.value.delete(tableId)
  }

  function addNewOrderAlert(tableId: number): void {
    newOrderTableIds.value.add(tableId)
  }

  function $reset(): void {
    tables.value = []
    newOrderTableIds.value = new Set()
    loading.value = false
    error.value = null
  }

  return {
    tables,
    newOrderTableIds,
    loading,
    error,
    fetchTables,
    setupTable,
    endSession,
    markAsRead,
    addNewOrderAlert,
    $reset,
  }
})
