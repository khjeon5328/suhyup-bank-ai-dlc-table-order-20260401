import apiClient from './apiClient'

export const authService = {
  async loginTable(storeCode, tableNo, password) {
    const { data } = await apiClient.post('/auth/login/table', {
      store_code: storeCode,
      table_no: tableNo,
      password
    })
    return data
  }
}