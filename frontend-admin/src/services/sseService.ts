import type { SSEEvent, SSEEventType } from '@/types/sse'

type SSEHandler = (event: SSEEvent) => void
type SSEStatus = 'connected' | 'reconnecting' | 'disconnected'

const MAX_RETRIES = 3

class SSEService {
  private eventSource: EventSource | null = null
  private handlers: Map<string, Set<SSEHandler>> = new Map()
  private retryCount = 0
  private _status: SSEStatus = 'disconnected'
  private storeId: number | null = null

  get status(): SSEStatus {
    return this._status
  }

  connect(storeId: number): void {
    this.disconnect()
    this.storeId = storeId
    this.retryCount = 0
    this.createConnection()
  }

  private createConnection(): void {
    if (!this.storeId) return

    const baseUrl = import.meta.env.VITE_SSE_BASE_URL
    this.eventSource = new EventSource(`${baseUrl}/${this.storeId}/events`, {
      withCredentials: true,
    })

    this.eventSource.onopen = () => {
      this._status = 'connected'
      this.retryCount = 0
    }

    this.eventSource.onmessage = (event: MessageEvent) => {
      try {
        const sseEvent: SSEEvent = JSON.parse(event.data)
        this.dispatchEvent(sseEvent)
      } catch {
        // ignore malformed events
      }
    }

    this.eventSource.onerror = () => {
      this.eventSource?.close()
      this.eventSource = null

      if (this.retryCount < MAX_RETRIES) {
        this._status = 'reconnecting'
        this.retryCount++
        this.createConnection()
      } else {
        this._status = 'disconnected'
      }
    }
  }

  private dispatchEvent(event: SSEEvent): void {
    const typeHandlers = this.handlers.get(event.type)
    if (typeHandlers) {
      typeHandlers.forEach((handler) => handler(event))
    }
    // Also dispatch to wildcard listeners
    const allHandlers = this.handlers.get('*')
    if (allHandlers) {
      allHandlers.forEach((handler) => handler(event))
    }
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
    this._status = 'disconnected'
    this.storeId = null
    this.retryCount = 0
  }

  onEvent(type: SSEEventType | '*', handler: SSEHandler): void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set())
    }
    this.handlers.get(type)!.add(handler)
  }

  offEvent(type: SSEEventType | '*', handler: SSEHandler): void {
    const typeHandlers = this.handlers.get(type)
    if (typeHandlers) {
      typeHandlers.delete(handler)
    }
  }
}

export const sseService = new SSEService()
