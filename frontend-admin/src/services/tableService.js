import apiClient from './apiClient'

export const tableService = {
  async getTables(storeId) {
    const { data } = await apiClient.get(`/stores/${storeId}/tables`)
    return data
  },
  async setupTable(storeId, tableNo, password) {
    const { data } = await apiClient.post(`/stores/${storeId}/tables`, { table_no: tableNo, password })
    return data
  },
  async endSession(storeId, tableId) {
    const { data } = await apiClient.post(`/stores/${storeId}/tables/${tableId}/session/end`)
    return data
  },
  async getHistory(storeId, tableId, dateFrom = null, dateTo = null) {
    const params = {}
    if (dateFrom) params.date_from = dateFrom
    if (dateTo) params.date_to = dateTo
    const { data } = await apiClient.get(`/stores/${storeId}/tables/${tableId}/history`, { params })
    return data
  }
}