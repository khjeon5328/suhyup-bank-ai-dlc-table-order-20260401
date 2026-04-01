import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import OrderStatusButton from '@/components/common/OrderStatusButton.vue'
import { OrderStatus } from '@/types/order'
import ko from '@/locales/ko.json'
import en from '@/locales/en.json'

const i18n = createI18n({
  legacy: false,
  locale: 'ko',
  messages: { ko, en },
})

function mountButton(currentStatus: OrderStatus) {
  return mount(OrderStatusButton, {
    props: { currentStatus },
    global: { plugins: [i18n] },
  })
}

describe('OrderStatusButton', () => {
  it('should show "준비 시작" for pending status', () => {
    const wrapper = mountButton(OrderStatus.PENDING)
    expect(wrapper.text()).toContain('준비 시작')
  })

  it('should show "완료 처리" for preparing status', () => {
    const wrapper = mountButton(OrderStatus.PREPARING)
    expect(wrapper.text()).toContain('완료 처리')
  })

  it('should not render button for completed status', () => {
    const wrapper = mountButton(OrderStatus.COMPLETED)
    expect(wrapper.find('[data-testid="order-status-button"]').exists()).toBe(false)
  })

  it('should emit change event on click', async () => {
    const wrapper = mountButton(OrderStatus.PENDING)
    await wrapper.find('[data-testid="order-status-button"]').trigger('click')
    expect(wrapper.emitted('change')).toBeTruthy()
    expect(wrapper.emitted('change')![0]).toEqual([OrderStatus.PREPARING])
  })
})
