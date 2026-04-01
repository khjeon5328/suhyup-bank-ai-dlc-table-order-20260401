export interface Menu { id: number; storeId: number; name: string; price: number; description: string | null; category: string; imageUrl: string | null; displayOrder: number; createdAt: string; updatedAt: string }
export interface MenuCreateRequest { name: string; price: number; description?: string; category: string; imageUrl?: string }
export interface MenuUpdateRequest { name?: string; price?: number; description?: string; category?: string; imageUrl?: string }
export interface MenuOrderUpdate { menuId: number; displayOrder: number }
export interface Category { id: number; name: string; menuCount: number; displayOrder: number }
export interface CategoryCreateRequest { name: string }
export interface CategoryUpdateRequest { name?: string }
export interface CategoryOrderUpdate { categoryId: number; displayOrder: number }
