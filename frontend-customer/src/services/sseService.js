import { logger } from '../utils/logger'

const MAX_RETRIES = 10
const RETRY_DELAY = 3000

export class SSEService {
  constructor() {
    this.eventSource = null
    this.retryCount = 0
    this.handlers = {}
    this.onMaxRetriesExceeded = null
  }

  connect(storeCode, tableNo) {
    const token = localStorage.getItem('token')
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api/v1'
    const url = `${baseUrl}/stores/${storeCode}/events/table/${tableNo}?token=${token}`

    this.disconnect()
    this.eventSource = new EventSource(url)

    this.eventSource.onopen = () => {
      this.retryCount = 0
      logger.info('SSEService', 'connect', 'Connected')
    }

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        const handler = this.handlers[data.type]
        if (handler) handler(data)
      } catch (err) {
        logger.error('SSEService', 'onmessage', err.message)
      }
    }

    this.eventSource.onerror = () => {
      this.eventSource.close()
      if (this.retryCount < MAX_RETRIES) {
        this.retryCount++
        logger.info('SSEService', 'reconnect', `Retry ${this.retryCount}/${MAX_RETRIES}`)
        setTimeout(() => this.connect(storeCode, tableNo), RETRY_DELAY)
      } else {
        logger.error('SSEService', 'connect', 'Max retries exceeded')
        if (this.onMaxRetriesExceeded) this.onMaxRetriesExceeded()
      }
    }
  }

  on(eventType, handler) {
    this.handlers[eventType] = handler
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
  }
}

export const sseService = new SSEService()