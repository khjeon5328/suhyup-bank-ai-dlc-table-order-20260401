import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type { TableSummary } from '@/types/table'

export const tableApi = {
  getTables(storeId: number): Promise<ApiResponse<TableSummary[]>> {
    return apiClient.get(`/stores/${storeId}/tables`).then((res) => res.data)
  },

  setupTable(storeId: number, tableNo: number, password: string): Promise<ApiResponse<TableSummary>> {
    return apiClient.post(`/stores/${storeId}/tables`, { table_no: tableNo, password }).then((res) => res.data)
  },

  endSession(storeId: number, tableNo: number): Promise<ApiResponse<null>> {
    return apiClient.post(`/stores/${storeId}/tables/${tableNo}/session/end`).then((res) => res.data)
  },
}
