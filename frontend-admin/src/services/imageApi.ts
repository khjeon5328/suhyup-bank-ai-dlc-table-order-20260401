import apiClient from './apiClient'
import axios from 'axios'
import type { ApiResponse } from '@/types/api'

interface PresignedUrlResponse {
  uploadUrl: string
  imageUrl: string
}

export const imageApi = {
  getPresignedUrl(storeId: number, filename: string): Promise<ApiResponse<PresignedUrlResponse>> {
    return apiClient.post(`/stores/${storeId}/images/presigned-url`, { filename }).then((res) => res.data)
  },

  uploadToS3(uploadUrl: string, file: File): Promise<void> {
    return axios.put(uploadUrl, file, {
      headers: { 'Content-Type': file.type },
    })
  },
}
