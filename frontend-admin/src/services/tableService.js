import apiClient from './apiClient'

export const tableService = {
  async getTables(storeCode) {
    const { data } = await apiClient.get(`/stores/${storeCode}/tables`)
    return data
  },
  async setupTable(storeCode, tableNo, password) {
    const { data } = await apiClient.post(`/stores/${storeCode}/tables`, { table_no: tableNo, password })
    return data
  },
  async endSession(storeCode, tableNo) {
    const { data } = await apiClient.post(`/stores/${storeCode}/tables/${tableNo}/session/end`)
    return data
  },
  async getHistory(storeCode, tableNo, dateFrom = null, dateTo = null) {
    const params = {}
    if (dateFrom) params.date_from = dateFrom
    if (dateTo) params.date_to = dateTo
    const { data } = await apiClient.get(`/stores/${storeCode}/tables/${tableNo}/history`, { params })
    return data
  }
}