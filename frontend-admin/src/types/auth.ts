export enum UserRole { OWNER = 'owner', MANAGER = 'manager' }
export interface LoginCredentials { storeId: string; username: string; password: string }
export interface AuthTokens { accessToken: string; tokenType: string; expiresIn: number }
export interface AuthUser { id: number; storeId: number; username: string; role: UserRole; storeName: string }
