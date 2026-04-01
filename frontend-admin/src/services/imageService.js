import apiClient from './apiClient'

export const imageService = {
  async getPresignedUrl(storeId, filename) {
    const { data } = await apiClient.post(`/stores/${storeId}/images/presigned-url`, { filename })
    return data
  },
  async uploadToS3(presignedUrl, file) {
    await fetch(presignedUrl, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
  }
}