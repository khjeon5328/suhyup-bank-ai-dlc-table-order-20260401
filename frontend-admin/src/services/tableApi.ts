import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type { TableSummary } from '@/types/table'

export const tableApi = {
  getTables(storeId: number): Promise<ApiResponse<TableSummary[]>> {
    return apiClient.get(`/stores/${storeId}/tables`).then((res) => res.data)
  },

  setupTable(storeId: number, tableNumber: number, password: string): Promise<ApiResponse<TableSummary>> {
    return apiClient.post(`/stores/${storeId}/tables`, { tableNumber, password }).then((res) => res.data)
  },

  endSession(storeId: number, tableId: number): Promise<ApiResponse<null>> {
    return apiClient.post(`/stores/${storeId}/tables/${tableId}/session/end`).then((res) => res.data)
  },
}
