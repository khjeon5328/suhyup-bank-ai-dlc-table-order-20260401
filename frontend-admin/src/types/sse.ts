import type { Order } from './order'
export enum SSEEventType { ORDER_CREATED = 'order_created', ORDER_STATUS_CHANGED = 'order_status_changed', ORDER_DELETED = 'order_deleted' }
export interface SSEOrderCreatedData { order: Order }
export interface SSEOrderStatusChangedData { orderId: number; status: string; tableId: number }
export interface SSEOrderDeletedData { orderId: number; tableId: number }
export type SSEEventData = SSEOrderCreatedData | SSEOrderStatusChangedData | SSEOrderDeletedData
export interface SSEEvent { type: SSEEventType; data: SSEEventData; timestamp: string }
