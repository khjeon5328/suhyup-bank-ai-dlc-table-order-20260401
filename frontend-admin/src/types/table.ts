import type { Order, OrderStatusCount } from './order'
export interface TableSession { id: number; tableId: number; startedAt: string; endedAt: string | null }
export interface Table { id: number; storeId: number; tableNumber: number; hasActiveSession: boolean; currentSession: TableSession | null }
export interface TableSummary { tableId: number; tableNumber: number; hasActiveSession: boolean; totalOrderAmount: number; orderCount: number; latestOrders: Order[]; statusSummary: OrderStatusCount }
