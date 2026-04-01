const isProd = import.meta.env.PROD

export const logger = {
  info(component, action, message) {
    if (!isProd) console.log(`[${new Date().toISOString()}] [${component}] ${action}: ${message}`)
  },
  error(component, action, message) {
    console.error(`[${new Date().toISOString()}] [${component}] ${action}: ${message}`)
  }
}