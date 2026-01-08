<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <!-- FAQ Tab -->
      <el-tab-pane label="常见问题 (FAQ)" name="faq">
        <div class="filter-container">
          <el-button type="primary" icon="Plus" @click="handleAddFaq">新增问题</el-button>
        </div>

        <el-table v-loading="loading" :data="faqs" border style="width: 100%; margin-top: 20px;">
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="category.name" label="分类" width="120" align="center">
             <template #default="{ row }">
                <el-tag v-if="row.category">{{ row.category.name }}</el-tag>
                <span v-else>-</span>
             </template>
          </el-table-column>
          <el-table-column prop="question" label="问题" min-width="200" />
          <el-table-column prop="view_count" label="浏览" width="80" align="center" />
          <el-table-column prop="sort_order" label="排序" width="80" align="center" />
          <el-table-column prop="is_hot" label="热门" width="80" align="center">
            <template #default="{ row }">
               <el-tag :type="row.is_hot ? 'danger' : 'info'" size="small">{{ row.is_hot ? 'HOT' : '普通' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center">
            <template #default="{ row }">
              <el-button type="primary" link @click="handleEditFaq(row)">编辑</el-button>
              <el-button type="danger" link @click="handleDeleteFaq(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- Category Tab -->
      <el-tab-pane label="分类管理" name="category">
        <div class="filter-container">
          <el-button type="primary" icon="Plus" @click="handleAddCat">新增分类</el-button>
        </div>
        <el-table :data="faqCategories" border style="width: 100%; margin-top: 20px;">
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="name" label="分类名称" />
          <el-table-column prop="sort_order" label="排序" width="100" align="center" />
          <el-table-column label="操作" width="180" align="center">
            <template #default="{ row }">
              <el-button type="primary" link @click="handleEditCat(row)">编辑</el-button>
              <el-button type="danger" link @click="handleDeleteCat(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- FAQ Dialog -->
    <el-dialog
      :title="isEditFaq ? '编辑问题' : '新增问题'"
      v-model="faqDialogVisible"
      width="600px"
    >
      <el-form ref="faqFormRef" :model="faqForm" :rules="faqRules" label-width="80px">
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="faqForm.category_id" placeholder="请选择分类">
            <el-option
              v-for="cat in faqCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="问题" prop="question">
          <el-input v-model="faqForm.question" placeholder="请输入问题" />
        </el-form-item>
        <el-form-item label="回答" prop="answer">
          <el-input v-model="faqForm.answer" type="textarea" :rows="5" placeholder="请输入回答" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="faqForm.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="热门" prop="is_hot">
          <el-switch v-model="faqForm.is_hot" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="faqDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitFaq" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Category Dialog -->
    <el-dialog
      :title="isEditCat ? '编辑分类' : '新增分类'"
      v-model="catDialogVisible"
      width="400px"
    >
      <el-form ref="catFormRef" :model="catForm" :rules="catRules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="catForm.name" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="catForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="catDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitCat" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useContentStore } from '@/store/modules/content-store'
import { storeToRefs } from 'pinia'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useContentStore()
const { faqs, faqCategories, loading } = storeToRefs(store)

const activeTab = ref('faq')
const submitLoading = ref(false)

// FAQ Logic
const faqDialogVisible = ref(false)
const isEditFaq = ref(false)
const faqFormRef = ref()
const faqForm = ref({
  id: undefined,
  category_id: undefined,
  question: '',
  answer: '',
  sort_order: 0,
  is_hot: false
})
const faqRules = {
  question: [{ required: true, message: '必填', trigger: 'blur' }],
  answer: [{ required: true, message: '必填', trigger: 'blur' }]
}

function handleAddFaq() {
  isEditFaq.value = false
  faqForm.value = { id: undefined, category_id: undefined, question: '', answer: '', sort_order: 0, is_hot: false }
  faqDialogVisible.value = true
}
function handleEditFaq(row: any) {
  isEditFaq.value = true
  faqForm.value = { ...row }
  faqDialogVisible.value = true
}
function handleDeleteFaq(row: any) {
  ElMessageBox.confirm('确认删除?', '提示').then(async () => {
    await store.deleteFaq(row.id)
    ElMessage.success('删除成功')
  })
}
async function handleSubmitFaq() {
  if(!faqFormRef.value) return
  await faqFormRef.value.validate(async (valid: boolean) => {
    if(valid){
        submitLoading.value = true
        try {
            if(isEditFaq.value) await store.updateFaq(faqForm.value.id, faqForm.value)
            else await store.createFaq(faqForm.value)
            ElMessage.success('操作成功')
            faqDialogVisible.value = false
        } finally{ submitLoading.value = false }
    }
  })
}

// Category Logic
const catDialogVisible = ref(false)
const isEditCat = ref(false)
const catFormRef = ref()
const catForm = ref({ id: undefined, name: '', sort_order: 0 })
const catRules = { name: [{ required: true, message: '必填', trigger: 'blur' }] }

function handleAddCat() {
    isEditCat.value = false
    catForm.value = { id: undefined, name: '', sort_order: 0 }
    catDialogVisible.value = true
}
function handleEditCat(row: any) {
    isEditCat.value = true
    catForm.value = { ...row }
    catDialogVisible.value = true
}
function handleDeleteCat(row: any) {
   ElMessageBox.confirm('确认删除?', '提示').then(async () => {
    await store.deleteFaqCategory(row.id)
    ElMessage.success('删除成功')
  })
}
async function handleSubmitCat() {
  if(!catFormRef.value) return
  await catFormRef.value.validate(async (valid: boolean) => {
    if(valid){
        submitLoading.value = true
        try {
            if(isEditCat.value) await store.updateFaqCategory(catForm.value.id, catForm.value)
            else await store.createFaqCategory(catForm.value)
            ElMessage.success('操作成功')
            catDialogVisible.value = false
        } finally{ submitLoading.value = false }
    }
  })
}

onMounted(() => {
  store.fetchFaqs()
  store.fetchFaqCategories()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.filter-container {
    margin-bottom: 20px;
}
</style>
