import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createI18n } from 'vue-i18n'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import ko from './locales/ko.json'
import en from './locales/en.json'

const savedLocale = localStorage.getItem('locale') || 'ko'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'ko',
  messages: { ko, en },
})

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(ElementPlus)

app.config.errorHandler = (err, _instance, info) => {
  console.error('[Global Error]', err, info)
}

app.mount('#app')
