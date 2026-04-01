import { ref } from 'vue'
import { defineStore } from 'pinia'
import { userApi } from '@/services/userApi'
import type { User, UserCreateRequest, UserUpdateRequest } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchUsers(storeId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await userApi.getUsers(storeId)
      users.value = response.data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function createUser(storeId: number, data: UserCreateRequest): Promise<void> {
    const response = await userApi.createUser(storeId, data)
    users.value.push(response.data)
  }

  async function updateUser(storeId: number, userId: number, data: UserUpdateRequest): Promise<void> {
    const response = await userApi.updateUser(storeId, userId, data)
    const index = users.value.findIndex((u) => u.id === userId)
    if (index !== -1) {
      users.value[index] = response.data
    }
  }

  async function deleteUser(storeId: number, userId: number): Promise<void> {
    await userApi.deleteUser(storeId, userId)
    users.value = users.value.filter((u) => u.id !== userId)
  }

  function $reset(): void {
    users.value = []
    loading.value = false
    error.value = null
  }

  return {
    users,
    loading,
    error,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    $reset,
  }
})
