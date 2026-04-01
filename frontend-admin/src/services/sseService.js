const MAX_RETRIES = 10
const RETRY_DELAY = 3000

export class SSEService {
  constructor() { this.eventSource = null; this.retryCount = 0; this.handlers = {}; this.onMaxRetriesExceeded = null; this._storeCode = null }

  connect(storeCode) {
    this._storeCode = storeCode
    const token = localStorage.getItem('admin_token')
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api/v1'
    this.disconnect()
    this.eventSource = new EventSource(`${baseUrl}/stores/${storeCode}/events/admin?token=${token}`)
    this.eventSource.onopen = () => { this.retryCount = 0 }
    // Listen for named events (backend sends "event: order_created" etc.)
    for (const type of Object.keys(this.handlers)) {
      this.eventSource.addEventListener(type, (e) => {
        try { const d = JSON.parse(e.data); this.handlers[type](d) } catch {}
      })
    }
    this.eventSource.onerror = () => {
      this.eventSource.close()
      if (this.retryCount < MAX_RETRIES) { this.retryCount++; setTimeout(() => this.connect(storeCode), RETRY_DELAY) }
      else if (this.onMaxRetriesExceeded) this.onMaxRetriesExceeded()
    }
  }
  on(type, handler) { this.handlers[type] = handler }
  disconnect() { if (this.eventSource) { this.eventSource.close(); this.eventSource = null } }
}

export const sseService = new SSEService()
