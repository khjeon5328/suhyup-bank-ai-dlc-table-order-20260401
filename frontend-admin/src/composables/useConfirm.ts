import { ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'

interface ConfirmOptions {
  title?: string
  confirmButtonText?: string
  cancelButtonText?: string
  type?: 'warning' | 'info' | 'success' | 'error'
}

export function useConfirm() {
  const { t } = useI18n()

  async function confirm(message: string, options?: ConfirmOptions): Promise<boolean> {
    try {
      await ElMessageBox.confirm(message, options?.title ?? t('common.confirm'), {
        confirmButtonText: options?.confirmButtonText ?? t('common.confirm'),
        cancelButtonText: options?.cancelButtonText ?? t('common.cancel'),
        type: options?.type ?? 'warning',
      })
      return true
    } catch {
      return false
    }
  }

  return { confirm }
}
