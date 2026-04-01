export interface ApiResponse<T> { success: boolean; data: T; message: string | null }
export interface ApiError { status: number; message: string; detail: string | null }
export interface PaginatedResponse<T> { items: T[]; total: number; page: number; pageSize: number }
export interface DateRange { dateFrom: string; dateTo: string }
