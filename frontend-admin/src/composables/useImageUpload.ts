import { ref } from 'vue'
import { imageService } from '@/services/imageService'
import { useAuthStore } from '@/stores/authStore'

export function useImageUpload() {
  const authStore = useAuthStore()
  const uploading = ref(false)
  const imageUrl = ref('')

  async function uploadImage(file: File): Promise<string> {
    uploading.value = true
    try {
      const { presigned_url, file_url } = await imageService.getPresignedUrl(authStore.storeCode, file.name)
      await imageService.uploadToS3(presigned_url, file)
      imageUrl.value = file_url
      return file_url
    } finally {
      uploading.value = false
    }
  }

  return { uploading, imageUrl, uploadImage }
}
