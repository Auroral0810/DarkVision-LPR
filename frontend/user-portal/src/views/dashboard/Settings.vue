<template>
  <div class="settings-view">
    <div class="settings-container">
      <div class="settings-menu">
        <div 
          class="menu-item" 
          :class="{ active: activeTab === 'profile' }"
          @click="activeTab = 'profile'"
        >
          <el-icon><User /></el-icon>
          <span>基本信息</span>
        </div>
        <div 
          class="menu-item" 
          :class="{ active: activeTab === 'security' }"
          @click="activeTab = 'security'"
        >
          <el-icon><Lock /></el-icon>
          <span>安全设置</span>
        </div>
        <div 
          class="menu-item" 
          :class="{ active: activeTab === 'verification' }"
          @click="activeTab = 'verification'"
        >
          <el-icon><Postcard /></el-icon>
          <span>实名认证</span>
          <el-badge v-if="userStore.verification.status === 'pending'" :value="1" class="badge" />
        </div>
        <div 
          class="menu-item" 
          :class="{ active: activeTab === 'third-party' }"
          @click="activeTab = 'third-party'"
        >
          <el-icon><Link /></el-icon>
          <span>第三方登录</span>
        </div>
        <div 
          class="menu-item" 
          :class="{ active: activeTab === 'membership' }"
          @click="activeTab = 'membership'"
        >
          <el-icon><Trophy /></el-icon>
          <span>会员权益</span>
        </div>
      </div>
      
      <div class="settings-content">
        <!-- Profile Section -->
        <div v-show="activeTab === 'profile'" class="content-section">
          <h3>基本信息</h3>
          <div class="avatar-uploader">
            <el-avatar :size="80" :src="userStore.userInfo.avatar_url || ''">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="upload-actions">
              <el-upload
                action="#"
                :show-file-list="false"
                :before-upload="handleAvatarUpload"
              >
                <el-button size="small">更换头像</el-button>
              </el-upload>
              <span class="tip">支持 JPG/PNG，最大 2MB</span>
            </div>
          </div>
          
          <el-form 
            :model="profileForm" 
            label-position="top" 
            class="settings-form"
            :rules="profileRules"
            ref="profileFormRef"
          >
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="手机号" prop="phone">
                  <el-input 
                    v-model="profileForm.phone" 
                    placeholder="请输入手机号"
                    :prefix-icon="Iphone"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="昵称" prop="nickname">
                  <el-input 
                    v-model="profileForm.nickname" 
                    placeholder="请输入昵称"
                    maxlength="50"
                    show-word-limit
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="邮箱" prop="email">
                  <el-input 
                    v-model="profileForm.email" 
                    placeholder="请输入邮箱（可选）"
                    :prefix-icon="Message"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="性别" prop="gender">
                  <el-select v-model="profileForm.gender" placeholder="请选择" style="width: 100%">
                    <el-option label="男" value="male" />
                    <el-option label="女" value="female" />
                    <el-option label="未知" value="unknown" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="生日" prop="birthday">
                  <el-date-picker
                    v-model="profileForm.birthday"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="地址" prop="address">
              <el-input 
                v-model="profileForm.address" 
                type="textarea" 
                :rows="3"
                placeholder="请输入详细地址"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveProfile">保存修改</el-button>
              <el-button @click="resetProfileForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <!-- Security Section -->
        <div v-show="activeTab === 'security'" class="content-section">
          <h3>安全设置</h3>
          <div class="security-list">
            <div class="security-item">
              <div class="info">
                <h4>登录密码</h4>
                <p>建议定期修改密码以保护账户安全</p>
              </div>
              <el-button link type="primary" @click="showPasswordDialog = true">修改</el-button>
            </div>
            
            <div class="security-item">
              <div class="info">
                <h4>手机号</h4>
                <p>当前绑定: {{ maskPhone(userStore.userInfo.phone) }}</p>
              </div>
              <el-button link type="primary" @click="showPhoneDialog = true">更换</el-button>
            </div>
            
            <div class="security-item">
              <div class="info">
                <h4>邮箱</h4>
                <p>{{ userStore.userInfo.email || '未绑定' }}</p>
              </div>
              <el-button link type="primary" @click="showEmailDialog = true">
                {{ userStore.userInfo.email ? '更换' : '绑定' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- Verification Section -->
        <div v-show="activeTab === 'verification'" class="content-section">
          <h3>实名认证</h3>
          <div class="verification-status" v-if="userStore.verification.status === 'approved'">
            <div class="status-success">
              <el-icon><CircleCheckFilled /></el-icon>
              <div class="status-text">
                <h4>认证成功</h4>
                <p>您已完成实名认证，已解锁所有高级功能权限</p>
              </div>
            </div>
          </div>
          
          <div class="verification-status" v-else-if="userStore.verification.status === 'pending'">
            <div class="status-pending">
              <el-icon><Clock /></el-icon>
              <div class="status-text">
                <h4>审核中</h4>
                <p>您的认证资料正在审核中，请耐心等待</p>
              </div>
            </div>
          </div>
          
          <div class="verification-status" v-else-if="userStore.verification.status === 'rejected'">
            <el-alert
              type="error"
              :title="`认证失败: ${userStore.verification.reject_reason || '资料不符合要求'}`"
              :closable="false"
              show-icon
            />
          </div>
          
          <div class="verification-form" v-if="userStore.verification.status !== 'approved'">
            <el-form label-position="top">
              <el-form-item label="身份证正面">
                <el-upload
                  action="#"
                  :show-file-list="false"
                  :before-upload="(file) => handleIdCardUpload(file, 'front')"
                >
                  <div class="id-card-upload">
                    <el-icon v-if="!userStore.verification.id_card_front"><Plus /></el-icon>
                    <img v-else :src="userStore.verification.id_card_front" alt="身份证正面" />
                    <span>{{ userStore.verification.id_card_front ? '重新上传' : '点击上传' }}</span>
                  </div>
                </el-upload>
              </el-form-item>
              
              <el-form-item label="身份证反面">
                <el-upload
                  action="#"
                  :show-file-list="false"
                  :before-upload="(file) => handleIdCardUpload(file, 'back')"
                >
                  <div class="id-card-upload">
                    <el-icon v-if="!userStore.verification.id_card_back"><Plus /></el-icon>
                    <img v-else :src="userStore.verification.id_card_back" alt="身份证反面" />
                    <span>{{ userStore.verification.id_card_back ? '重新上传' : '点击上传' }}</span>
                  </div>
                </el-upload>
              </el-form-item>
              
              <el-form-item label="人脸活体照片（可选）">
                <el-upload
                  action="#"
                  :show-file-list="false"
                  :before-upload="(file) => handleIdCardUpload(file, 'face')"
                >
                  <div class="id-card-upload">
                    <el-icon v-if="!userStore.verification.face_photo"><Plus /></el-icon>
                    <img v-else :src="userStore.verification.face_photo" alt="人脸照片" />
                    <span>{{ userStore.verification.face_photo ? '重新上传' : '点击上传' }}</span>
                  </div>
                </el-upload>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  :disabled="!userStore.verification.id_card_front || !userStore.verification.id_card_back"
                  @click="handleSubmitVerification"
                >
                  提交认证
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        
        <!-- Third Party Login Section -->
        <div v-show="activeTab === 'third-party'" class="content-section">
          <h3>第三方登录绑定</h3>
          <p class="section-desc">绑定第三方账号后，您可以使用这些账号快速登录</p>
          
          <div class="third-party-list">
            <div 
              class="third-party-item"
              v-for="item in userStore.thirdPartyLogins" 
              :key="item.provider"
            >
              <div class="provider-info">
                <div class="provider-icon" :class="item.provider">
                  <el-icon v-if="item.provider === 'wechat'"><ChatDotRound /></el-icon>
                  <el-icon v-else-if="item.provider === 'qq'"><User /></el-icon>
                  <el-icon v-else><Link /></el-icon>
                </div>
                <div class="provider-details">
                  <h4>{{ getProviderName(item.provider) }}</h4>
                  <p>{{ item.bound ? `已绑定: ${maskOpenId(item.open_id)}` : '未绑定' }}</p>
                </div>
              </div>
              <el-button 
                :type="item.bound ? 'danger' : 'primary'"
                @click="handleThirdPartyBind(item.provider)"
              >
                {{ item.bound ? '解绑' : '绑定' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- Membership Section -->
        <div v-show="activeTab === 'membership'" class="content-section">
          <h3>会员权益</h3>
          <div class="membership-card" :class="userStore.userInfo.role.toLowerCase()">
            <div class="membership-header">
              <div class="membership-badge">
                <el-icon><Trophy /></el-icon>
                <span>{{ userStore.membershipInfo.name }}</span>
              </div>
              <div class="membership-status" v-if="userStore.isVIP">
                <span v-if="userStore.membership.expire_date">
                  到期时间: {{ new Date(userStore.membership.expire_date).toLocaleDateString('zh-CN') }}
                </span>
                <span v-else>永久有效</span>
              </div>
            </div>
            
            <div class="quota-grid">
              <div class="quota-item">
                <span class="label">每日识别额度</span>
                <span class="value">{{ formatQuota(userStore.quota.daily) }}</span>
              </div>
              <div class="quota-item">
                <span class="label">批量识别</span>
                <span class="value">{{ formatQuota(userStore.quota.maxBatch) }}张/次</span>
              </div>
              <div class="quota-item">
                <span class="label">视频识别</span>
                <span class="value">{{ formatQuota(userStore.quota.video) }}个/月</span>
              </div>
              <div class="quota-item">
                <span class="label">API调用</span>
                <span class="value">{{ formatQuota(userStore.quota.api) }}次/日</span>
              </div>
              <div class="quota-item">
                <span class="label">云端存储</span>
                <span class="value">{{ formatQuota(userStore.quota.storage) }}GB</span>
              </div>
            </div>
            
            <div class="features-section">
              <h4>功能权益</h4>
              <div class="features-list">
                <div 
                  class="feature-item" 
                  v-for="(feature, index) in userStore.membershipInfo.features" 
                  :key="index"
                >
                  <el-icon><Check /></el-icon>
                  <span>{{ feature }}</span>
                </div>
              </div>
            </div>
            
            <div class="membership-actions" v-if="!userStore.isVIP">
              <el-button type="primary" size="large" round @click="handleUpgrade">
                升级到 VIP
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Dialogs -->
    <el-dialog v-model="showPasswordDialog" title="修改密码" width="500px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-position="top">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>
    
    <el-dialog v-model="showPhoneDialog" title="更换手机号" width="500px">
      <el-form :model="phoneForm" :rules="phoneRules" ref="phoneFormRef" label-position="top">
        <el-form-item label="新手机号" prop="phone">
          <el-input v-model="phoneForm.phone" placeholder="请输入新手机号" />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="code-input">
            <el-input v-model="phoneForm.code" placeholder="请输入验证码" />
            <el-button @click="sendPhoneCode">发送验证码</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPhoneDialog = false">取消</el-button>
        <el-button type="primary" @click="handleChangePhone">确定</el-button>
      </template>
    </el-dialog>
    
    <el-dialog v-model="showEmailDialog" title="绑定/更换邮箱" width="500px">
      <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef" label-position="top">
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="emailForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="code-input">
            <el-input v-model="emailForm.code" placeholder="请输入验证码" />
            <el-button @click="sendEmailCode">发送验证码</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEmailDialog = false">取消</el-button>
        <el-button type="primary" @click="handleChangeEmail">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { 
  User, Lock, Postcard, Link, Trophy, Iphone, Message, 
  CircleCheckFilled, WarningFilled, Clock, Plus, Check,
  ChatDotRound
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('profile')

const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()
const phoneFormRef = ref<FormInstance>()
const emailFormRef = ref<FormInstance>()

const showPasswordDialog = ref(false)
const showPhoneDialog = ref(false)
const showEmailDialog = ref(false)

// Profile Form
const profileForm = reactive({
  phone: userStore.userInfo.phone,
  nickname: userStore.userInfo.nickname,
  email: userStore.userInfo.email || '',
  gender: userStore.userProfile.gender || 'unknown',
  birthday: userStore.userProfile.birthday || '',
  address: userStore.userProfile.address || ''
})

const profileRules: FormRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 50, message: '昵称长度为2-50个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ]
}

// Password Form
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// Phone Form
const phoneForm = reactive({
  phone: '',
  code: ''
})

const phoneRules: FormRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

// Email Form
const emailForm = reactive({
  email: '',
  code: ''
})

const emailRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

// Methods
const maskPhone = (phone: string) => {
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const maskOpenId = (openId: string) => {
  if (!openId) return ''
  return openId.length > 8 ? openId.slice(0, 4) + '****' + openId.slice(-4) : '****'
}

const getProviderName = (provider: string) => {
  const map: Record<string, string> = {
    wechat: '微信',
    qq: 'QQ',
    github: 'GitHub'
  }
  return map[provider] || provider
}


const formatQuota = (value: number | typeof Infinity) => {
  return value === Infinity ? '无限' : value.toString()
}

const handleAvatarUpload = (file: File) => {
  // TODO: Upload to OSS
  const reader = new FileReader()
  reader.onload = (e) => {
    userStore.userInfo.avatar_url = e.target?.result as string
    ElMessage.success('头像上传成功')
  }
  reader.readAsDataURL(file)
  return false
}

const handleIdCardUpload = (file: File, type: 'front' | 'back' | 'face') => {
  // TODO: Upload to OSS
  const reader = new FileReader()
  reader.onload = (e) => {
    const url = e.target?.result as string
    if (type === 'front') {
      userStore.verification.id_card_front = url
    } else if (type === 'back') {
      userStore.verification.id_card_back = url
    } else {
      userStore.verification.face_photo = url
    }
    ElMessage.success('上传成功')
  }
  reader.readAsDataURL(file)
  return false
}

const handleSaveProfile = async () => {
  if (!profileFormRef.value) return
  await profileFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: Call API
      userStore.userInfo.phone = profileForm.phone
      userStore.userInfo.nickname = profileForm.nickname
      userStore.userInfo.email = profileForm.email || null
      userStore.userProfile.gender = profileForm.gender as any
      userStore.userProfile.birthday = profileForm.birthday || null
      userStore.userProfile.address = profileForm.address || null
      ElMessage.success('保存成功')
    }
  })
}

const resetProfileForm = () => {
  profileForm.phone = userStore.userInfo.phone
  profileForm.nickname = userStore.userInfo.nickname
  profileForm.email = userStore.userInfo.email || ''
  profileForm.gender = userStore.userProfile.gender || 'unknown'
  profileForm.birthday = userStore.userProfile.birthday || ''
  profileForm.address = userStore.userProfile.address || ''
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: Call API
      ElMessage.success('密码修改成功')
      showPasswordDialog.value = false
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    }
  })
}

const handleChangePhone = async () => {
  if (!phoneFormRef.value) return
  await phoneFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: Call API
      userStore.userInfo.phone = phoneForm.phone
      ElMessage.success('手机号更换成功')
      showPhoneDialog.value = false
      phoneForm.phone = ''
      phoneForm.code = ''
    }
  })
}

const handleChangeEmail = async () => {
  if (!emailFormRef.value) return
  await emailFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: Call API
      userStore.userInfo.email = emailForm.email
      ElMessage.success('邮箱绑定成功')
      showEmailDialog.value = false
      emailForm.email = ''
      emailForm.code = ''
    }
  })
}

const sendPhoneCode = () => {
  if (!phoneForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  // TODO: Call API
  ElMessage.success('验证码已发送')
}

const sendEmailCode = () => {
  if (!emailForm.email) {
    ElMessage.warning('请先输入邮箱')
    return
  }
  // TODO: Call API
  ElMessage.success('验证码已发送')
}

const handleSubmitVerification = () => {
  // TODO: Call API
  userStore.verification.status = 'pending'
  ElMessage.success('认证资料已提交，请等待审核')
}

const handleThirdPartyBind = async (provider: string) => {
  const item = userStore.thirdPartyLogins.find(p => p.provider === provider)
  if (!item) return
  
  if (item.bound) {
    try {
      await ElMessageBox.confirm('确定要解绑该账号吗？', '提示', {
        type: 'warning'
      })
      // TODO: Call API
      item.bound = false
      item.open_id = ''
      ElMessage.success('解绑成功')
    } catch {
      // User cancelled
    }
  } else {
    // TODO: Redirect to OAuth
    ElMessage.info(`正在跳转到${getProviderName(provider)}授权页面...`)
    // Simulate binding
    setTimeout(() => {
      item.bound = true
      item.open_id = 'mock_' + Math.random().toString(36).substr(2, 9)
      ElMessage.success('绑定成功')
    }, 1000)
  }
}

const handleUpgrade = () => {
  ElMessage.info('正在跳转到订阅页面...')
  // router.push('/upgrade')
}

onMounted(() => {
  resetProfileForm()
})
</script>

<style scoped lang="scss">
.settings-view {
  width: 100%;
}

.settings-container {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.settings-menu {
  width: 240px;
  background: white;
  border-radius: 16px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  position: sticky;
  top: 100px;
  
  .menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 8px;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
    position: relative;
    
    &:hover {
      background: #f8fafc;
      color: #334155;
    }
    
    &.active {
      background: #eff6ff;
      color: #2563eb;
    }
    
    .badge {
      margin-left: auto;
    }
  }
}

.settings-content {
  flex: 1;
}

.content-section {
  background: white;
  padding: 32px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  margin-bottom: 24px;
  
  h3 {
    margin: 0 0 24px;
    font-size: 18px;
    color: #0f172a;
    padding-bottom: 16px;
    border-bottom: 1px solid #f1f5f9;
  }
  
  .section-desc {
    color: #64748b;
    margin-bottom: 24px;
  }
}

.avatar-uploader {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
  
  .upload-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    
    .tip {
      font-size: 12px;
      color: #94a3b8;
    }
  }
}

.settings-form {
  max-width: 800px;
}

.security-list {
  .security-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #f8fafc;
    
    &:last-child { border-bottom: none; }
    
    .info {
      h4 { margin: 0 0 4px; font-size: 14px; color: #334155; }
      p { margin: 0; font-size: 13px; color: #94a3b8; }
    }
  }
}

.code-input {
  display: flex;
  gap: 12px;
  
  .el-input {
    flex: 1;
  }
}

.verification-status {
  margin-bottom: 24px;
  
  .status-success,
  .status-pending {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    border-radius: 12px;
    
    .el-icon {
      font-size: 32px;
    }
    
    .status-text {
      h4 { margin: 0 0 4px; font-size: 16px; }
      p { margin: 0; font-size: 14px; color: #64748b; }
    }
  }
  
  .status-success {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #10b981;
  }
  
  .status-pending {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #f59e0b;
  }
}

.id-card-upload {
  width: 200px;
  height: 120px;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
  
  &:hover {
    border-color: #3b82f6;
    background: #eff6ff;
  }
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
  }
  
  span {
    font-size: 12px;
    color: #64748b;
  }
}

.third-party-list {
  .third-party-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-bottom: 16px;
    
    &:last-child { margin-bottom: 0; }
    
    .provider-info {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .provider-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        
        &.wechat { background: #07c160; }
        &.qq { background: #12b7f5; }
        &.github { background: #24292e; }
      }
      
      .provider-details {
        h4 { margin: 0 0 4px; font-size: 16px; color: #0f172a; }
        p { margin: 0; font-size: 13px; color: #94a3b8; }
      }
    }
  }
}

.membership-card {
  border-radius: 16px;
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border: 2px solid #e2e8f0;
  
  &.vip {
    background: linear-gradient(135deg, #fff7ed 0%, #ffffff 100%);
    border-color: #fbbf24;
  }
  
  &.company {
    background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
    border-color: #3b82f6;
  }
  
  .membership-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid #e2e8f0;
    
    .membership-badge {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 24px;
      font-weight: 700;
      color: #0f172a;
    }
    
    .membership-status {
      color: #64748b;
      font-size: 14px;
    }
  }
  
  .quota-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
    
    .quota-item {
      background: white;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      
      .label {
        display: block;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 8px;
      }
      
      .value {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
      }
    }
  }
  
  .features-section {
    margin-bottom: 24px;
    
    h4 {
      margin: 0 0 16px;
      font-size: 16px;
      color: #0f172a;
    }
    
    .features-list {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
      
      .feature-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #334155;
        font-size: 14px;
        
        .el-icon {
          color: #10b981;
        }
      }
    }
  }
  
  .membership-actions {
    text-align: center;
    padding-top: 24px;
    border-top: 1px solid #e2e8f0;
  }
}
</style>