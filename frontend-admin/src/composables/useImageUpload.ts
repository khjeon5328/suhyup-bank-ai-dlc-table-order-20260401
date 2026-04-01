import { ref } from 'vue'
import { imageApi } from '@/services/imageApi'
import { useAuthStore } from '@/stores/auth'

export function useImageUpload() {
  const uploading = ref(false)
  const imageUrl = ref<string | null>(null)

  async function upload(file: File): Promise<string | null> {
    const authStore = useAuthStore()
    if (!authStore.storeId) return null

    uploading.value = true
    try {
      const response = await imageApi.getPresignedUrl(authStore.storeId, file.name)
      await imageApi.uploadToS3(response.data.uploadUrl, file)
      imageUrl.value = response.data.imageUrl
      return response.data.imageUrl
    } catch {
      return null
    } finally {
      uploading.value = false
    }
  }

  return { uploading, imageUrl, upload }
}
