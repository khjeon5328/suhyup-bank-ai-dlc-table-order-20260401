import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.config.errorHandler = (err, instance) => {
  const name = instance?.$options?.name || 'Unknown'
  console.error(`[${new Date().toISOString()}] [${name}] ${err.message}`)
}

app.mount('#app')