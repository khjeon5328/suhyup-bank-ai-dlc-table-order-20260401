export enum OrderStatus { PENDING = 'pending', PREPARING = 'preparing', COMPLETED = 'completed' }
export interface OrderItem { id: number; menuId: number; menuName: string; quantity: number; unitPrice: number; subtotal: number }
export interface Order { id: number; orderNumber: string; storeId: number; tableId: number; sessionId: number; items: OrderItem[]; totalAmount: number; status: OrderStatus; createdAt: string; updatedAt: string }
export interface OrderHistory { id: number; orderNumber: string; tableId: number; tableNumber: number; items: OrderItem[]; totalAmount: number; status: OrderStatus; createdAt: string; archivedAt: string }
export interface OrderStatusCount { pending: number; preparing: number; completed: number }
