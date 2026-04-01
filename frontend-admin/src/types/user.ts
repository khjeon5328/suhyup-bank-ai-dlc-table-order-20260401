import type { UserRole } from './auth'
export interface User { id: number; storeId: number; username: string; role: UserRole; createdAt: string }
export interface UserCreateRequest { username: string; password: string; role: UserRole }
export interface UserUpdateRequest { username?: string; password?: string; role?: UserRole }
