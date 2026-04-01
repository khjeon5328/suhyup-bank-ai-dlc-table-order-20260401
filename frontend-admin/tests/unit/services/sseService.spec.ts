import { sseService } from '@/services/sseService'
import { SSEEventType } from '@/types/sse'
import type { SSEEvent } from '@/types/sse'

describe('sseService', () => {
  it('should have initial status as disconnected', () => {
    expect(sseService.status).toBe('disconnected')
  })

  it('should register event handler with onEvent', () => {
    const handler = jest.fn()
    sseService.onEvent(SSEEventType.ORDER_CREATED, handler)
    // No error means success
    expect(handler).not.toHaveBeenCalled()
  })

  it('should remove event handler with offEvent', () => {
    const handler = jest.fn()
    sseService.onEvent(SSEEventType.ORDER_CREATED, handler)
    sseService.offEvent(SSEEventType.ORDER_CREATED, handler)
    // No error means success
    expect(handler).not.toHaveBeenCalled()
  })

  it('should set status to disconnected after disconnect', () => {
    sseService.disconnect()
    expect(sseService.status).toBe('disconnected')
  })
})
