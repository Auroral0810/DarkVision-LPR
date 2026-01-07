<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <!-- FAQ Items Tab -->
      <el-tab-pane label="常见问题管理" name="faqs">
        <div class="search-container">
           <el-select v-model="currCategoryId" placeholder="选择分类" @change="handleCategoryChange" clearable style="width: 200px; margin-right: 10px;">
              <el-option 
                v-for="cat in categories" 
                :key="cat.id" 
                :label="cat.name" 
                :value="cat.id" 
              />
           </el-select>
           <el-button type="primary" icon="Plus" @click="handleAddFaq">新增问题</el-button>
        </div>

        <el-card shadow="never" class="mt-20">
          <el-table v-loading="loadingFaq" :data="faqList" border highlight-current-row>
            <el-table-column label="ID" prop="id" width="80" align="center" />
            <el-table-column label="问题" prop="question" />
            <el-table-column label="分类" width="150">
               <template #default="{ row }">
                  <el-tag v-if="row.category">
                    {{ row.category.name }}
                  </el-tag>
                  <span v-else>未分类</span>
               </template>
            </el-table-column>
            <el-table-column label="排序" prop="sort_order" width="80" align="center" />
            <el-table-column label="热门" width="80" align="center">
              <template #default="{ row }">
                <el-tag :type="row.is_hot ? 'danger' : 'info'">
                   {{ row.is_hot ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="浏览" prop="view_count" width="80" align="center" />
            <el-table-column label="创建时间" prop="created_at" width="180">
               <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
               </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center">
              <template #default="scope">
                <el-button type="primary" size="small" link icon="Edit" @click="handleEditFaq(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" link icon="Delete" @click="handleDeleteFaq(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <!-- Categories Tab -->
      <el-tab-pane label="分类管理" name="categories">
         <div class="search-container">
           <el-button type="primary" icon="Plus" @click="handleAddCat">新增分类</el-button>
        </div>
        <el-card shadow="never" class="mt-20">
          <el-table v-loading="loadingCat" :data="categories" border highlight-current-row>
             <el-table-column label="ID" prop="id" width="80" align="center" />
             <el-table-column label="分类名称" prop="name" />
             <el-table-column label="排序" prop="sort_order" align="center" />
             <el-table-column label="操作" width="200" align="center">
              <template #default="scope">
                <el-button type="primary" size="small" link icon="Edit" @click="handleEditCat(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" link icon="Delete" @click="handleDeleteCat(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- FAQ Dialog -->
    <el-dialog 
      v-model="dialogFaq.visible" 
      :title="dialogFaq.title" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formFaqRef" :model="formFaq" :rules="rulesFaq" label-width="80px">
        <el-form-item label="问题" prop="question">
          <el-input v-model="formFaq.question" placeholder="请输入问题" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
           <el-select v-model="formFaq.category_id" placeholder="请选择分类">
              <el-option 
                v-for="cat in categories" 
                :key="cat.id" 
                :label="cat.name" 
                :value="cat.id" 
              />
           </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="formFaq.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="热门" prop="is_hot">
          <el-switch v-model="formFaq.is_hot" active-text="是" inactive-text="否" />
        </el-form-item>
        <el-form-item label="回答" prop="answer">
          <el-input 
            v-model="formFaq.answer" 
            type="textarea" 
            :rows="6" 
            placeholder="请输入回答" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogFaq.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitFaq">确定</el-button>
      </template>
    </el-dialog>

    <!-- Category Dialog -->
    <el-dialog 
      v-model="dialogCat.visible" 
      :title="dialogCat.title" 
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form ref="formCatRef" :model="formCat" :rules="rulesCat" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="formCat.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="formCat.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogCat.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitCat">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ContentAPI, { type Faq, type FaqCategory } from '@/api/content-api'
import dayjs from 'dayjs'

const activeTab = ref('faqs')
const loadingFaq = ref(false)
const loadingCat = ref(false)
const categories = ref<FaqCategory[]>([])
const faqList = ref<Faq[]>([])
const currCategoryId = ref<number | undefined>(undefined)

// --- FAQ State ---
const dialogFaq = reactive({ visible: false, title: '', isEdit: false })
const formFaqRef = ref()
const formFaq = reactive({
  id: undefined as number | undefined,
  question: '',
  answer: '',
  category_id: undefined as number | undefined,
  sort_order: 0,
  is_hot: false
})
const rulesFaq = {
  question: [{ required: true, message: '请输入问题', trigger: 'blur' }],
  answer: [{ required: true, message: '请输入回答', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

// --- Category State ---
const dialogCat = reactive({ visible: false, title: '', isEdit: false })
const formCatRef = ref()
const formCat = reactive({
  id: undefined as number | undefined,
  name: '',
  sort_order: 0
})
const rulesCat = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

// --- Common ---
function formatDate(date: string) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function fetchCategories() {
  loadingCat.value = true
  try {
    const res = await ContentAPI.getFaqCategories()
    categories.value = res as any
  } finally {
    loadingCat.value = false
  }
}

async function fetchFaqs() {
  loadingFaq.value = true
  try {
    const params = currCategoryId.value ? { category_id: currCategoryId.value } : {}
    const res = await ContentAPI.getFaqs(params)
    faqList.value = res as any
  } finally {
    loadingFaq.value = false
  }
}

// --- FAQ Actions ---
function handleCategoryChange() {
  fetchFaqs()
}

function resetFormFaq() {
  formFaq.id = undefined
  formFaq.question = ''
  formFaq.answer = ''
  formFaq.category_id = undefined
  formFaq.sort_order = 0
  formFaq.is_hot = false
}

function handleAddFaq() {
  resetFormFaq()
  dialogFaq.title = '新增问题'
  dialogFaq.isEdit = false
  dialogFaq.visible = true
}

function handleEditFaq(row: Faq) {
  resetFormFaq()
  Object.assign(formFaq, row)
  dialogFaq.title = '编辑问题'
  dialogFaq.isEdit = true
  dialogFaq.visible = true
}

async function handleDeleteFaq(row: Faq) {
  await ElMessageBox.confirm(`确认删除问题 "${row.question}" 吗?`, '警告', { type: 'warning' })
  try {
    await ContentAPI.deleteFaq(row.id)
    ElMessage.success('删除成功')
    fetchFaqs()
  } catch (error) {}
}

async function handleSubmitFaq() {
  if (!formFaqRef.value) return
  await formFaqRef.value.validate()
  try {
    if (dialogFaq.isEdit && formFaq.id) {
      await ContentAPI.updateFaq(formFaq.id, formFaq)
      ElMessage.success('更新成功')
    } else {
      await ContentAPI.createFaq(formFaq)
      ElMessage.success('创建成功')
    }
    dialogFaq.visible = false
    fetchFaqs()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// --- Category Actions ---
function resetFormCat() {
  formCat.id = undefined
  formCat.name = ''
  formCat.sort_order = 0
}

function handleAddCat() {
  resetFormCat()
  dialogCat.title = '新增分类'
  dialogCat.isEdit = false
  dialogCat.visible = true
}

function handleEditCat(row: FaqCategory) {
  resetFormCat()
  Object.assign(formCat, row)
  dialogCat.title = '编辑分类'
  dialogCat.isEdit = true
  dialogCat.visible = true
}

async function handleDeleteCat(row: FaqCategory) {
  await ElMessageBox.confirm(`确认删除分类 "${row.name}" 吗?`, '警告', { type: 'warning' })
  try {
    await ContentAPI.deleteFaqCategory(row.id)
    ElMessage.success('删除成功')
    fetchCategories()
    fetchFaqs() // Refresh FAQs as category links are removed
  } catch (error) {}
}

async function handleSubmitCat() {
  if (!formCatRef.value) return
  await formCatRef.value.validate()
  try {
    if (dialogCat.isEdit && formCat.id) {
      await ContentAPI.updateFaqCategory(formCat.id, formCat)
      ElMessage.success('更新成功')
    } else {
      await ContentAPI.createFaqCategory(formCat)
      ElMessage.success('创建成功')
    }
    dialogCat.visible = false
    fetchCategories()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchCategories()
  fetchFaqs()
})
</script>

<style scoped>
.mt-20 {
  margin-top: 20px;
}
</style>
