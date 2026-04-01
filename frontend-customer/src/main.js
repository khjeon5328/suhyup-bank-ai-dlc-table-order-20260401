import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import { logger } from './utils/logger'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.config.errorHandler = (err, instance, info) => {
  const component = instance?.$options?.name || 'Unknown'
  logger.error(component, 'unhandled', err.message)
}

window.addEventListener('unhandledrejection', (event) => {
  logger.error('Global', 'unhandledRejection', event.reason?.message || 'Unknown error')
})

app.mount('#app')