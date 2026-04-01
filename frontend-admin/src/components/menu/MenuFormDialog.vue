<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useMenuStore } from '@/stores/menu'
import { useImageUpload } from '@/composables/useImageUpload'
import type { Menu, Category } from '@/types/menu'
import type { FormInstance } from 'element-plus'

const props = defineProps<{
  visible: boolean
  menu: Menu | null
  categories: Category[]
}>()

const emit = defineEmits<{ (e: 'update:visible', val: boolean): void }>()
const { t } = useI18n()
const authStore = useAuthStore()
const menuStore = useMenuStore()
const { uploading, upload } = useImageUpload()

const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({
  name: '',
  price: 0,
  description: '',
  category: '',
  imageUrl: '',
})

const rules = {
  name: [
    { required: true, message: () => t('menu.validation.nameRequired'), trigger: 'blur' },
    { max: 50, message: () => t('menu.validation.nameMaxLength'), trigger: 'blur' },
  ],
  price: [
    { required: true, message: () => t('menu.validation.priceRequired'), trigger: 'blur' },
    { type: 'number' as const, min: 0, message: () => t('menu.validation.priceMin'), trigger: 'blur' },
  ],
  category: [{ required: true, message: () => t('menu.validation.categoryRequired'), trigger: 'change' }],
  description: [{ max: 200, message: () => t('menu.validation.descriptionMaxLength'), trigger: 'blur' }],
}

watch(() => props.visible, (val) => {
  if (val && props.menu) {
    form.name = props.menu.name
    form.price = props.menu.price
    form.description = props.menu.description ?? ''
    form.category = props.menu.category
    form.imageUrl = props.menu.imageUrl ?? ''
  } else if (val) {
    form.name = ''
    form.price = 0
    form.description = ''
    form.category = ''
    form.imageUrl = ''
  }
})

async function handleImageUpload(file: File): Promise<void> {
  const url = await upload(file)
  if (url) form.imageUrl = url
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !authStore.storeId) return

  loading.value = true
  try {
    const data = {
      name: form.name,
      price: form.price,
      description: form.description || undefined,
      category: form.category,
      imageUrl: form.imageUrl || undefined,
    }
    if (props.menu) {
      await menuStore.updateMenu(authStore.storeId, props.menu.id, data)
      ElMessage.success(t('menu.updateSuccess'))
    } else {
      await menuStore.createMenu(authStore.storeId, data)
      ElMessage.success(t('menu.createSuccess'))
    }
    emit('update:visible', false)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="menu ? t('menu.editMenu') : t('menu.addMenu')"
    width="500px"
    data-testid="menu-form-dialog"
    @update:model-value="emit('update:visible', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item :label="t('menu.name')" prop="name">
        <el-input v-model="form.name" data-testid="input-menu-name" />
      </el-form-item>
      <el-form-item :label="t('menu.price')" prop="price">
        <el-input-number v-model="form.price" :min="0" data-testid="input-menu-price" />
      </el-form-item>
      <el-form-item :label="t('menu.description')" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="3" data-testid="input-menu-description" />
      </el-form-item>
      <el-form-item :label="t('menu.category')" prop="category">
        <el-select v-model="form.category" data-testid="select-menu-category">
          <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.name" />
        </el-select>
      </el-form-item>
      <el-form-item :label="t('menu.image')">
        <el-upload
          :show-file-list="false"
          :auto-upload="false"
          accept="image/*"
          @change="(uploadFile: any) => handleImageUpload(uploadFile.raw)"
        >
          <el-button :loading="uploading" data-testid="upload-menu-image">{{ t('menu.image') }}</el-button>
        </el-upload>
        <el-image v-if="form.imageUrl" :src="form.imageUrl" style="width: 100px; height: 100px; margin-top: 8px" fit="cover" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" :loading="loading" data-testid="menu-form-submit" @click="handleSubmit">
        {{ t('common.save') }}
      </el-button>
    </template>
  </el-dialog>
</template>
