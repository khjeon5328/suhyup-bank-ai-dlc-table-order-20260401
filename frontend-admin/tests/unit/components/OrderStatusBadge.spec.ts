import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import OrderStatusBadge from '@/components/common/OrderStatusBadge.vue'
import { OrderStatus } from '@/types/order'
import ko from '@/locales/ko.json'
import en from '@/locales/en.json'

const i18n = createI18n({
  legacy: false,
  locale: 'ko',
  messages: { ko, en },
})

function mountBadge(status: OrderStatus) {
  return mount(OrderStatusBadge, {
    props: { status },
    global: { plugins: [i18n] },
  })
}

describe('OrderStatusBadge', () => {
  it('should display pending text', () => {
    const wrapper = mountBadge(OrderStatus.PENDING)
    expect(wrapper.text()).toContain('대기')
  })

  it('should display preparing text', () => {
    const wrapper = mountBadge(OrderStatus.PREPARING)
    expect(wrapper.text()).toContain('준비 중')
  })

  it('should display completed text', () => {
    const wrapper = mountBadge(OrderStatus.COMPLETED)
    expect(wrapper.text()).toContain('완료')
  })
})
