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
                <el-button size="small" :loading="uploadingAvatar">更换头像</el-button>
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
                <el-form-item label="手机号">
                  <el-input 
                    :value="userStore.userInfo.phone || '未绑定'"
                    placeholder="未绑定"
                    :prefix-icon="Iphone"
                    disabled
                    class="readonly-input"
                  />
                  <span class="form-tip">请在安全设置中绑定手机号</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱">
                  <el-input 
                    :value="userStore.userInfo.email || '未绑定'"
                    placeholder="未绑定"
                    :prefix-icon="Message"
                    disabled
                    class="readonly-input"
                  />
                  <span class="form-tip">请在安全设置中绑定邮箱</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
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
              <div class="address-form">
                <el-row :gutter="12">
                  <el-col :span="8">
                    <el-select 
                      v-model="profileForm.province" 
                      placeholder="请选择省份"
                      @change="handleProvinceChange"
                      style="width: 100%"
                    >
                      <el-option 
                        v-for="province in provinces" 
                        :key="province.code"
                        :label="province.name" 
                        :value="province.code"
                      />
                    </el-select>
                  </el-col>
                  <el-col :span="8">
                    <el-select 
                      v-model="profileForm.city" 
                      placeholder="请选择城市"
                      @change="handleCityChange"
                      :disabled="!profileForm.province"
                      style="width: 100%"
                    >
                      <el-option 
                        v-for="city in cities" 
                        :key="city.code"
                        :label="city.name" 
                        :value="city.code"
                      />
                    </el-select>
                  </el-col>
                  <el-col :span="8">
                    <el-select 
                      v-model="profileForm.district" 
                      placeholder="请选择区县"
                      :disabled="!profileForm.city"
                      style="width: 100%"
                    >
                      <el-option 
                        v-for="district in districts" 
                        :key="district.code"
                        :label="district.name" 
                        :value="district.code"
                      />
                    </el-select>
                  </el-col>
                </el-row>
              <el-input 
                  v-model="profileForm.detailAddress" 
                  placeholder="请输入详细地址（街道、门牌号等）"
                maxlength="200"
                show-word-limit
                  style="margin-top: 12px"
              />
              </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveProfile" :loading="savingProfile">保存修改</el-button>
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
              <el-button link type="primary" @click="openPasswordDialog">修改</el-button>
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
          
          <!-- 已认证状态展示 -->
          <div class="verification-status" v-if="userStore.verification.status === 'approved' && !showReverifyForm">
            <div class="status-success">
              <el-icon><CircleCheckFilled /></el-icon>
              <div class="status-text">
                <h4>认证成功</h4>
                <p>您已完成实名认证，已解锁所有高级功能权限</p>
              </div>
            </div>
            
            <div class="verified-info-card">
              <div class="info-row">
                <span class="label">真实姓名</span>
                <span class="value">{{ maskName(userStore.verification.real_name) }}</span>
              </div>
              <div class="info-row">
                <span class="label">身份证号</span>
                <span class="value">{{ maskIdCard(userStore.verification.id_card_number) }}</span>
              </div>
              <div class="info-actions">
                <el-button type="primary" plain @click="showReverifyForm = true">更换认证信息</el-button>
              </div>
            </div>
          </div>
          
          <!-- 审核中状态 -->
          <div class="verification-status" v-else-if="userStore.verification.status === 'pending' && !showReverifyForm">
            <div class="status-pending">
              <el-icon><Clock /></el-icon>
              <div class="status-text">
                <h4>审核中</h4>
                <p>您的认证资料正在审核中，请耐心等待</p>
              </div>
              <div class="status-actions" style="margin-left: auto">
                <el-button type="danger" plain @click="handleWithdrawVerification">撤回申请</el-button>
              </div>
            </div>
          </div>
          
          <!-- 认证表单（未认证、审核失败或点击更换时显示） -->
          <div class="verification-form" v-else>
            <div v-if="userStore.verification.status === 'rejected'" class="reject-alert">
              <el-alert
                type="error"
                :title="`认证失败: ${userStore.verification.reject_reason || '资料不符合要求'}`"
                :closable="false"
                show-icon
                style="margin-bottom: 24px"
              />
            </div>
            
            <el-form 
              :model="verifyForm" 
              :rules="verifyRules" 
              ref="verifyFormRef" 
              label-position="top"
            >
              <el-row :gutter="24">
                <el-col :span="12">
                  <el-form-item label="真实姓名" prop="realName">
                    <el-input v-model="verifyForm.realName" placeholder="依照身份证上的姓名填写" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="身份证号码" prop="idCardNumber">
                    <el-input v-model="verifyForm.idCardNumber" placeholder="18位二代身份证号码" maxlength="18" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="24">
                <el-col :span="8">
                  <el-form-item label="身份证正面" prop="idCardFront">
                    <el-upload
                      action="#"
                      :show-file-list="false"
                      :before-upload="(file) => handleIdCardUpload(file, 'front')"
                      class="id-card-uploader"
                    >
                      <div class="id-card-upload" :class="{ loading: uploadingIdFront }">
                        <img v-if="verifyPreview.idCardFront" :src="verifyPreview.idCardFront" alt="身份证正面" />
                        <div v-else class="upload-placeholder">
                          <el-icon><Plus /></el-icon>
                          <span>点击上传正面</span>
                        </div>
                        <div v-if="uploadingIdFront" class="upload-loading">
                          <el-icon class="is-loading"><Loading /></el-icon>
                        </div>
                      </div>
                    </el-upload>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="身份证反面" prop="idCardBack">
                    <el-upload
                      action="#"
                      :show-file-list="false"
                      :before-upload="(file) => handleIdCardUpload(file, 'back')"
                    >
                      <div class="id-card-upload" :class="{ loading: uploadingIdBack }">
                        <img v-if="verifyPreview.idCardBack" :src="verifyPreview.idCardBack" alt="身份证反面" />
                        <div v-else class="upload-placeholder">
                          <el-icon><Plus /></el-icon>
                          <span>点击上传反面</span>
                        </div>
                        <div v-if="uploadingIdBack" class="upload-loading">
                          <el-icon class="is-loading"><Loading /></el-icon>
                        </div>
                      </div>
                    </el-upload>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="手持身份证/人脸照片 (可选)" prop="facePhoto">
                    <el-upload
                      action="#"
                      :show-file-list="false"
                      :before-upload="(file) => handleIdCardUpload(file, 'face')"
                    >
                      <div class="id-card-upload" :class="{ loading: uploadingFace }">
                        <img v-if="verifyPreview.facePhoto" :src="verifyPreview.facePhoto" alt="手持照片" />
                        <div v-else class="upload-placeholder">
                          <el-icon><Plus /></el-icon>
                          <span>点击上传照片</span>
                        </div>
                        <div v-if="uploadingFace" class="upload-loading">
                          <el-icon class="is-loading"><Loading /></el-icon>
                        </div>
                      </div>
                    </el-upload>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item style="margin-top: 32px">
                <el-button 
                  type="primary" 
                  size="large"
                  @click="handleSubmitVerification"
                  :loading="submittingVerify"
                >
                  提交认证
                </el-button>
                <el-button 
                  v-if="userStore.verification.status === 'approved' || userStore.verification.status === 'pending'"
                  size="large"
                  @click="showReverifyForm = false"
                >
                  取消
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
    <!-- Password Dialog (Handles both Change and Reset) -->
    <el-dialog 
      v-model="showPasswordDialog" 
      class="custom-password-dialog split-layout"
      width="850px"
      align-center
      destroy-on-close
      :show-close="true"
      @closed="resetPasswordDialog"
    >
      <div class="dialog-split-container">
        <!-- Left Sidebar -->
        <div class="dialog-sidebar">
          <div class="sidebar-content">
            <div class="brand-area">
              <div class="logo-icon">
                <el-icon><Lock /></el-icon>
              </div>
              <h3>{{ passwordMode === 'change' ? '安全中心' : '找回密码' }}</h3>
              <p class="desc">{{ passwordMode === 'change' ? '定期更新密码可以有效保护您的账户安全' : '我们将帮助您通过安全的方式重置密码' }}</p>
            </div>
            
            <div class="security-features">
              <div class="feature-item">
                <el-icon><CircleCheckFilled /></el-icon>
                <span>银行级数据加密</span>
              </div>
              <div class="feature-item">
                <el-icon><CircleCheckFilled /></el-icon>
                <span>实时安全监控</span>
              </div>
              <div class="feature-item">
                <el-icon><CircleCheckFilled /></el-icon>
                <span>异常登录提醒</span>
              </div>
            </div>
            
            <div class="sidebar-footer">
              <p>DarkVision LPR</p>
              <span>Security Center</span>
            </div>
          </div>
          <div class="sidebar-bg-decor"></div>
        </div>

        <!-- Right Form Area -->
        <div class="dialog-main">
          <div class="main-header">
            <h3>{{ passwordMode === 'change' ? '修改密码' : '重置密码' }}</h3>
          </div>

          <el-form 
            v-if="passwordMode === 'change'"
            :model="passwordForm" 
            :rules="passwordRules" 
            ref="passwordFormRef" 
            label-position="top"
            class="modern-form"
            hide-required-asterisk
          >
            <el-form-item label="当前密码" prop="oldPassword">
              <el-input 
                v-model="passwordForm.oldPassword" 
                type="password" 
                show-password 
                placeholder="请输入当前密码"
                class="custom-input"
              />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input 
                v-model="passwordForm.newPassword" 
                type="password" 
                show-password 
                placeholder="请输入新密码（6-20位）"
                class="custom-input"
              />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirmPassword">
              <el-input 
                v-model="passwordForm.confirmPassword" 
                type="password" 
                show-password 
                placeholder="请再次输入新密码"
                class="custom-input"
              />
            </el-form-item>
            
            <div class="form-actions">
              <div class="action-link" @click="switchPasswordMode('reset')">
                <span>忘记密码？</span>
              </div>
              <el-button 
                type="primary" 
                class="submit-btn" 
                @click="handlePasswordSubmit" 
                :loading="passwordLoading"
              >
                确认修改
              </el-button>
            </div>
          </el-form>

          <el-form 
            v-else
            :model="forgotPasswordForm" 
            :rules="forgotPasswordRules" 
            ref="forgotPasswordFormRef" 
            label-position="top"
            class="modern-form"
            hide-required-asterisk
          >
            <!-- 简化布局，移除多余Icon，保持干净 -->
            <el-form-item label="验证方式" v-if="availableMethods.length > 1" class="method-select">
              <el-radio-group v-model="forgotPasswordMethod" @change="handleMethodChange" class="custom-radio-group">
                <el-radio-button label="phone" v-if="userStore.userInfo.phone">手机号</el-radio-button>
                <el-radio-button label="email" v-if="userStore.userInfo.email">邮箱</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item :label="forgotPasswordMethod === 'phone' ? '手机号' : '邮箱'" prop="account">
              <el-input 
                v-model="forgotPasswordForm.account" 
                disabled
                class="custom-input readonly"
              />
            </el-form-item>
            
            <el-form-item label="验证码" prop="code">
              <div class="code-input-group">
                <el-input 
                  v-model="forgotPasswordForm.code" 
                  placeholder="6位验证码" 
                  maxlength="6"
                  class="custom-input code-field"
                />
                <el-button 
                  type="primary" 
                  plain
                  @click="sendForgotPasswordCode" 
                  :disabled="forgotPasswordCodeDisabled"
                  :loading="sendingForgotPasswordCode"
                  class="send-code-btn"
                >
                  {{ forgotPasswordCodeButtonText }}
                </el-button>
              </div>
            </el-form-item>
            
            <el-form-item label="设置新密码" prop="newPassword">
              <el-input
                v-model="forgotPasswordForm.newPassword"
                type="password"
                placeholder="请输入新密码（6-20位）"
                show-password
                class="custom-input"
              />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="confirmPassword">
              <el-input
                v-model="forgotPasswordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                show-password
                class="custom-input"
              />
            </el-form-item>
            
            <div class="form-actions">
              <div class="action-link" @click="switchPasswordMode('change')">
                <el-icon><User /></el-icon>
                <span>返回修改</span>
              </div>
              <el-button 
                type="primary" 
                class="submit-btn" 
                @click="handlePasswordSubmit" 
                :loading="passwordLoading"
              >
                重置密码
              </el-button>
            </div>
          </el-form>
        </div>
      </div>
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
    
    <!-- 忘记密码对话框 (移除，已合并到修改密码) -->

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useUserStore } from '@/store/user'
import { 
  User, Lock, Postcard, Link, Trophy, Iphone, Message, 
  CircleCheckFilled, Clock, Plus, Loading, 
  Check, ChatDotRound
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { uploadImage } from '@/api/recognition'
import { updateProfile, resetPassword, changePassword, sendSmsCode as sendSmsCodeAPI, sendEmailCode as sendEmailCodeAPI, submitVerification, withdrawVerification } from '@/api/auth'

const userStore = useUserStore()
const activeTab = ref('profile')

const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()
const forgotPasswordFormRef = ref<FormInstance>()
const phoneFormRef = ref<FormInstance>()
const emailFormRef = ref<FormInstance>()
const verifyFormRef = ref<FormInstance>()

const showPasswordDialog = ref(false)
const passwordMode = ref<'change' | 'reset'>('change')
const showPhoneDialog = ref(false)
const showEmailDialog = ref(false)
const uploadingAvatar = ref(false)
const uploadingIdFront = ref(false)
const uploadingIdBack = ref(false)
const uploadingFace = ref(false)
const savingProfile = ref(false)
const submittingVerify = ref(false)
const showReverifyForm = ref(false)
const passwordLoading = ref(false)
const sendingForgotPasswordCode = ref(false)
const forgotPasswordCodeDisabled = ref(false)
const forgotPasswordCountdown = ref(0)
const forgotPasswordMethod = ref<'phone' | 'email'>('phone')

// 存储原始OSS URL（用于保存到数据库）
const originalAvatarUrl = ref<string>('')

const availableMethods = computed(() => {
  const methods: { label: string; value: 'phone' | 'email' }[] = []
  if (userStore.userInfo.phone) methods.push({ label: '手机号', value: 'phone' })
  if (userStore.userInfo.email) methods.push({ label: '邮箱', value: 'email' })
  return methods
})

const handleMethodChange = (val: any) => {
  const method = val as 'phone' | 'email'
  forgotPasswordMethod.value = method
  if (method === 'phone') {
    forgotPasswordForm.account = userStore.userInfo.phone || ''
  } else {
    forgotPasswordForm.account = userStore.userInfo.email || ''
  }
}

// 格式化地址字符串
const formatAddress = (province: string, city: string, district: string, detail: string) => {
  const parts = [province, city, district, detail].filter(Boolean)
  return parts.join('/')
}

// 省市区数据（硬编码，主要省份和城市）
// 注意：必须在 initAddressParts 之前定义
const provinceCityData: Record<string, { name: string; cities: Record<string, { name: string; districts: string[] }> }> = {
  '110000': {
    name: '北京市',
    cities: {
      '110100': {
        name: '北京市',
        districts: ['东城区', '西城区', '朝阳区', '丰台区', '石景山区', '海淀区', '门头沟区', '房山区', '通州区', '顺义区', '昌平区', '大兴区', '怀柔区', '平谷区', '密云区', '延庆区']
      }
    }
  },
  '120000': {
    name: '天津市',
    cities: {
      '120100': {
        name: '天津市',
        districts: ['和平区', '河东区', '河西区', '南开区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区', '武清区', '宝坻区', '滨海新区', '宁河区', '静海区', '蓟州区']
      }
    }
  },
  '310000': {
    name: '上海市',
    cities: {
      '310100': {
        name: '上海市',
        districts: ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区', '虹口区', '杨浦区', '闵行区', '宝山区', '嘉定区', '浦东新区', '金山区', '松江区', '青浦区', '奉贤区', '崇明区']
      }
    }
  },
  '330000': {
    name: '浙江省',
    cities: {
      '330100': {
        name: '杭州市',
        districts: ['上城区', '下城区', '江干区', '拱墅区', '西湖区', '滨江区', '萧山区', '余杭区', '富阳区', '临安区', '桐庐县', '淳安县', '建德市']
      },
      '330200': {
        name: '宁波市',
        districts: ['海曙区', '江北区', '北仑区', '镇海区', '鄞州区', '奉化区', '象山县', '宁海县', '余姚市', '慈溪市']
      },
      '330300': {
        name: '温州市',
        districts: ['鹿城区', '龙湾区', '瓯海区', '洞头区', '永嘉县', '平阳县', '苍南县', '文成县', '泰顺县', '瑞安市', '乐清市', '龙港市']
      }
    }
  },
  '440000': {
    name: '广东省',
    cities: {
      '440100': {
        name: '广州市',
        districts: ['荔湾区', '越秀区', '海珠区', '天河区', '白云区', '黄埔区', '番禺区', '花都区', '南沙区', '从化区', '增城区']
      },
      '440300': {
        name: '深圳市',
        districts: ['罗湖区', '福田区', '南山区', '宝安区', '龙岗区', '盐田区', '龙华区', '坪山区', '光明区', '大鹏新区']
      },
      '440400': {
        name: '珠海市',
        districts: ['香洲区', '斗门区', '金湾区']
      }
    }
  },
  '510000': {
    name: '四川省',
    cities: {
      '510100': {
        name: '成都市',
        districts: ['锦江区', '青羊区', '金牛区', '武侯区', '成华区', '龙泉驿区', '青白江区', '新都区', '温江区', '双流区', '郫都区', '新津区', '都江堰市', '彭州市', '邛崃市', '崇州市', '简阳市', '金堂县', '大邑县', '蒲江县']
      }
    }
  },
  '320000': {
    name: '江苏省',
    cities: {
      '320100': {
        name: '南京市',
        districts: ['玄武区', '秦淮区', '建邺区', '鼓楼区', '浦口区', '栖霞区', '雨花台区', '江宁区', '六合区', '溧水区', '高淳区']
      },
      '320500': {
        name: '苏州市',
        districts: ['虎丘区', '吴中区', '相城区', '姑苏区', '吴江区', '常熟市', '张家港市', '昆山市', '太仓市']
      }
    }
  }
}

// Profile Form - 初始化时需要先解析地址
const initAddressParts = () => {
  const address = userStore.userProfile.address
  if (!address) return { province: '', city: '', district: '', detailAddress: '' }
  
  const parts = address.split('/')
  const provinceName = parts[0] || ''
  const cityName = parts[1] || ''
  const districtName = parts[2] || ''
  const detailAddress = parts.slice(3).join('/') || ''
  
  // 查找省份代码
  const provinceCode = Object.keys(provinceCityData).find(
    code => provinceCityData[code].name === provinceName
  ) || ''
  
  // 如果找到省份，查找城市代码
  let cityCode = ''
  if (provinceCode) {
    const provinceData = provinceCityData[provinceCode]
    cityCode = Object.keys(provinceData.cities).find(
      code => provinceData.cities[code].name === cityName
    ) || ''
  }
  
  // 如果找到城市，查找区县代码
  let districtCode = ''
  if (provinceCode && cityCode) {
    const provinceData = provinceCityData[provinceCode]
    const cityData = provinceData.cities[cityCode]
    if (cityData) {
      const index = cityData.districts.findIndex(d => d === districtName)
      if (index !== -1) {
        districtCode = `${cityCode}${String(index + 1).padStart(2, '0')}`
      }
    }
  }
  
  return {
    province: provinceCode,
    city: cityCode,
    district: districtCode,
    detailAddress
  }
}

const addressParts = initAddressParts()
const profileForm = reactive({
  nickname: userStore.userInfo.nickname,
  gender: userStore.userProfile.gender || 'unknown',
  birthday: userStore.userProfile.birthday || '',
  province: addressParts.province,
  city: addressParts.city,
  district: addressParts.district,
  detailAddress: addressParts.detailAddress
})

// 省份列表
const provinces = computed(() => {
  return Object.keys(provinceCityData).map(code => ({
    code,
    name: provinceCityData[code].name
  }))
})

// 城市列表（根据选中的省份）
const cities = computed(() => {
  if (!profileForm.province) return []
  const provinceData = provinceCityData[profileForm.province]
  if (!provinceData) return []
  return Object.keys(provinceData.cities).map(code => ({
    code,
    name: provinceData.cities[code].name
  }))
})

// 区县列表（根据选中的城市）
const districts = computed(() => {
  if (!profileForm.province || !profileForm.city) return []
  const provinceData = provinceCityData[profileForm.province]
  if (!provinceData) return []
  const cityData = provinceData.cities[profileForm.city]
  if (!cityData) return []
  return cityData.districts.map((name, index) => ({
    code: `${profileForm.city}${String(index + 1).padStart(2, '0')}`,
    name
  }))
})

// 省市区变更处理
const handleProvinceChange = () => {
  profileForm.city = ''
  profileForm.district = ''
}

const handleCityChange = () => {
  profileForm.district = ''
}

const profileRules: FormRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 50, message: '昵称长度为2-50个字符', trigger: 'blur' }
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

// Forgot Password Form
const forgotPasswordForm = reactive({
  account: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPasswordForgot = (_rule: any, value: string, callback: any) => {
  if (value !== forgotPasswordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const forgotPasswordRules: FormRules = {
  account: [
    { required: true, message: '请选择验证方式', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPasswordForgot, trigger: 'blur' }
  ]
}

const forgotPasswordCodeButtonText = computed(() => {
  return forgotPasswordCountdown.value > 0 ? `${forgotPasswordCountdown.value}s` : '获取验证码'
})

const startForgotPasswordCountdown = () => {
  forgotPasswordCodeDisabled.value = true
  forgotPasswordCountdown.value = 60
  const timer = setInterval(() => {
    forgotPasswordCountdown.value--
    if (forgotPasswordCountdown.value <= 0) {
      clearInterval(timer)
      forgotPasswordCodeDisabled.value = false
    }
  }, 1000)
}

// Verification Form
const verifyForm = reactive({
  realName: '',
  idCardNumber: '',
  idCardFront: '',
  idCardBack: '',
  facePhoto: ''
})

const verifyPreview = reactive({
  idCardFront: '',
  idCardBack: '',
  facePhoto: ''
})

const verifyRules: FormRules = {
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度为2-20个字符', trigger: 'blur' }
  ],
  idCardNumber: [
    { required: true, message: '请输入身份证号码', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号码', trigger: 'blur' }
  ],
  idCardFront: [{ required: true, message: '请上传身份证正面照片', trigger: 'change' }],
  idCardBack: [{ required: true, message: '请上传身份证反面照片', trigger: 'change' }]
}

// Methods
const maskPhone = (phone: string | null | undefined) => {
  if (!phone) return '未绑定'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const maskOpenId = (openId: string) => {
  if (!openId) return ''
  return openId.length > 8 ? openId.slice(0, 4) + '****' + openId.slice(-4) : '****'
}

const maskName = (name: string | null | undefined) => {
  if (!name) return ''
  if (name.length <= 1) return name
  return name.charAt(0) + '*'.repeat(name.length - 1)
}

const maskIdCard = (idCard: string | null) => {
  if (!idCard) return ''
  if (idCard.length < 10) return idCard
  return idCard.slice(0, 3) + '***********' + idCard.slice(-4)
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

const handleAvatarUpload = async (file: File) => {
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请上传图片文件')
    return false
  }
  
  // 验证文件大小（2MB）
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  
  try {
    uploadingAvatar.value = true
    const res: any = await uploadImage(file)
    if (res.code === 20000 && res.data) {
      // 保存原始OSS URL（用于后端保存）
      originalAvatarUrl.value = res.data.url
      // 使用原始URL用于立即显示
      userStore.userInfo.avatar_url = res.data.url
      ElMessage.success('头像上传成功')
    } else {
      ElMessage.error(res.message || '头像上传失败')
    }
  } catch (error: any) {
    console.error('Avatar upload error:', error)
    ElMessage.error(error?.response?.data?.message || '头像上传失败')
  } finally {
    uploadingAvatar.value = false
  }
  
  return false
}

const handleIdCardUpload = async (file: File, type: 'front' | 'back' | 'face') => {
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请上传图片文件')
    return false
  }
  
  // 验证文件大小（5MB）
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过5MB')
    return false
  }

  try {
    if (type === 'front') uploadingIdFront.value = true
    else if (type === 'back') uploadingIdBack.value = true
    else uploadingFace.value = true

    const res: any = await uploadImage(file)
    if (res.code === 20000 && res.data) {
      const url = res.data.url
      
      if (type === 'front') {
        verifyForm.idCardFront = url
        verifyPreview.idCardFront = url
      } else if (type === 'back') {
        verifyForm.idCardBack = url
        verifyPreview.idCardBack = url
      } else {
        verifyForm.facePhoto = url
        verifyPreview.facePhoto = url
      }
      ElMessage.success('上传成功')
    } else {
      ElMessage.error(res.message || '上传失败')
    }
  } catch (error: any) {
    console.error('Upload error:', error)
    ElMessage.error(error?.response?.data?.message || '上传失败')
  } finally {
    if (type === 'front') uploadingIdFront.value = false
    else if (type === 'back') uploadingIdBack.value = false
    else uploadingFace.value = false
  }
  return false
}

const handleSaveProfile = async () => {
  if (!profileFormRef.value) return
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        savingProfile.value = true
        
        // 格式化地址
        const provinceName = provinces.value.find(p => p.code === profileForm.province)?.name || ''
        const cityName = cities.value.find(c => c.code === profileForm.city)?.name || ''
        const districtName = districts.value.find(d => d.code === profileForm.district)?.name || ''
        const fullAddress = formatAddress(provinceName, cityName, districtName, profileForm.detailAddress)
        
        // 调用API更新用户信息
        // 使用原始OSS URL（如果有新上传），否则使用当前的avatar_url
        const avatarToSave = originalAvatarUrl.value || userStore.userInfo.avatar_url
        
        const res = await updateProfile({
          nickname: profileForm.nickname,
          avatar_url: avatarToSave || undefined,
          gender: profileForm.gender as 'male' | 'female' | 'unknown',
          birthday: profileForm.birthday || undefined,
          address: fullAddress || undefined
        })
        
        if (res.code === 20000 && res.data) {
          // 更新store中的用户信息
          userStore.userInfo.nickname = profileForm.nickname
          // 后端返回的是公网URL，直接使用
          userStore.userInfo.avatar_url = res.data.avatar_url || userStore.userInfo.avatar_url
          userStore.userProfile.gender = profileForm.gender as any
          userStore.userProfile.birthday = profileForm.birthday || null
          userStore.userProfile.address = fullAddress || null
          
          // 清空临时存储的原始URL
          originalAvatarUrl.value = ''
          
          ElMessage.success('保存成功')
        } else {
          ElMessage.error(res.message || '保存失败')
        }
      } catch (error: any) {
        console.error('Save profile error:', error)
        ElMessage.error(error?.response?.data?.message || '保存失败')
      } finally {
        savingProfile.value = false
      }
    }
  })
}

const resetProfileForm = () => {
  const addressParts = initAddressParts()
  profileForm.nickname = userStore.userInfo.nickname
  profileForm.gender = userStore.userProfile.gender || 'unknown'
  profileForm.birthday = userStore.userProfile.birthday || ''
  profileForm.province = addressParts.province
  profileForm.city = addressParts.city
  profileForm.district = addressParts.district
  profileForm.detailAddress = addressParts.detailAddress
}

const openPasswordDialog = () => {
  passwordMode.value = 'change'
  showPasswordDialog.value = true
}

const switchPasswordMode = (mode: 'change' | 'reset') => {
  passwordMode.value = mode
  if (mode === 'reset') {
    if (availableMethods.value.length > 0) {
      handleMethodChange(availableMethods.value[0].value)
    } else {
      ElMessage.warning('请先绑定手机号或邮箱')
    }
  }
}

const resetPasswordDialog = () => {
  // 重置所有表单数据
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  
  forgotPasswordForm.account = ''
  forgotPasswordForm.code = ''
  forgotPasswordForm.newPassword = ''
  forgotPasswordForm.confirmPassword = ''
}

const handlePasswordSubmit = async () => {
  if (passwordMode.value === 'change') {
    await handleChangePassword()
  } else {
    await handleForgotPassword()
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        passwordLoading.value = true
        await changePassword({
          old_password: passwordForm.oldPassword,
          new_password: passwordForm.newPassword,
          confirm_password: passwordForm.confirmPassword
        })
        ElMessage.success('密码修改成功，请重新登录')
      showPasswordDialog.value = false
        // 退出登录
        userStore.logout()
        // 跳转到登录页
        window.location.href = '/login'
      } catch (error: any) {
        console.error('Change password error:', error)
        ElMessage.error(error?.response?.data?.message || '密码修改失败')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

const handleForgotPassword = async () => {
  if (!forgotPasswordFormRef.value) return
  await forgotPasswordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        passwordLoading.value = true
        await resetPassword({
          account: forgotPasswordForm.account,
          code: forgotPasswordForm.code,
          new_password: forgotPasswordForm.newPassword,
          confirm_password: forgotPasswordForm.confirmPassword
        })
        ElMessage.success('密码重置成功，请重新登录')
        showPasswordDialog.value = false
        // 退出登录
        userStore.logout()
        // 跳转到登录页
        window.location.href = '/login'
      } catch (error: any) {
        console.error('Reset password error:', error)
        ElMessage.error(error?.response?.data?.message || '密码重置失败')
      } finally {
        passwordLoading.value = false
      }
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

const sendPhoneCode = async () => {
  if (!phoneForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  try {
    await sendSmsCodeAPI(phoneForm.phone, 'bind')
    ElMessage.success('验证码已发送')
  } catch (error: any) {
    console.error('Send code error:', error)
    ElMessage.error(error?.response?.data?.message || '验证码发送失败')
  }
}

const sendEmailCode = async () => {
  if (!emailForm.email) {
    ElMessage.warning('请先输入邮箱')
    return
  }
  try {
    await sendEmailCodeAPI(emailForm.email, 'bind')
    ElMessage.success('验证码已发送')
  } catch (error: any) {
    console.error('Send code error:', error)
    ElMessage.error(error?.response?.data?.message || '验证码发送失败')
  }
}

const handleSubmitVerification = async () => {
  if (!verifyFormRef.value) return
  await verifyFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submittingVerify.value = true
        
        await submitVerification({
          real_name: verifyForm.realName,
          id_card_number: verifyForm.idCardNumber,
          id_card_front: verifyForm.idCardFront,
          id_card_back: verifyForm.idCardBack,
          face_photo: verifyForm.facePhoto || undefined
        })
        
        ElMessage.success('实名认证资料提交成功，请等待审核')
        showReverifyForm.value = false
        
        // 刷新用户信息以获取最新状态
        await userStore.updateUserInfo()
      } catch (error: any) {
        console.error('Verify submit error:', error)
        ElMessage.error(error?.response?.data?.message || '资料提交失败，请重试')
      } finally {
        submittingVerify.value = false
      }
    }
  })
}

const handleWithdrawVerification = async () => {
  try {
    await ElMessageBox.confirm('确定要撤回实名认证申请吗？', '提示', {
      type: 'warning',
      confirmButtonText: '确定撤回',
      cancelButtonText: '取消'
    })
    
    await withdrawVerification()
    ElMessage.success('已撤回申请')
    await userStore.updateUserInfo()
    resetVerifyForm() 
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('Withdraw error:', error)
      ElMessage.error(error?.response?.data?.message || '撤回失败，请重试')
    }
  }
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

const sendForgotPasswordCode = async () => {
  if (!forgotPasswordForm.account) {
    return
  }
  try {
    sendingForgotPasswordCode.value = true
    if (forgotPasswordMethod.value === 'email') {
      await sendEmailCodeAPI(forgotPasswordForm.account, 'reset_password')
    } else {
      await sendSmsCodeAPI(forgotPasswordForm.account, 'reset_password')
    }
    ElMessage.success('验证码已发送')
    startForgotPasswordCountdown()
  } catch (error: any) {
    console.error('Send code error:', error)
    ElMessage.error(error?.response?.data?.message || '验证码发送失败')
  } finally {
    sendingForgotPasswordCode.value = false
  }
}

// 移除原来的 handleForgotPassword, 因为已经重写了


const resetVerifyForm = () => {
  verifyForm.realName = userStore.verification.real_name || ''
  verifyForm.idCardNumber = userStore.verification.id_card_number || ''
  verifyForm.idCardFront = userStore.verification.id_card_front || ''
  verifyForm.idCardBack = userStore.verification.id_card_back || ''
  verifyForm.facePhoto = userStore.verification.face_photo || ''
  verifyPreview.idCardFront = userStore.verification.id_card_front || ''
  verifyPreview.idCardBack = userStore.verification.id_card_back || ''
  verifyPreview.facePhoto = userStore.verification.face_photo || ''
  if (verifyFormRef.value) {
    verifyFormRef.value.clearValidate()
  }
}

onMounted(() => {
  resetProfileForm()
  resetVerifyForm()
})

// 监听 store 数据变化，确保异步加载的数据能同步到表单
watch(() => userStore.userProfile, () => {
  resetProfileForm()
}, { deep: true })

watch(() => userStore.userInfo, () => {
  resetProfileForm()
}, { deep: true })

watch(() => userStore.verification, () => {
  resetVerifyForm()
}, { deep: true })
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
  
  .readonly-input {
    :deep(.el-input__inner) {
      background-color: #f5f7fa;
      color: #909399;
      cursor: not-allowed;
    }
  }
  
  .form-tip {
    display: block;
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
  }
  
  .address-form {
    width: 100%;
  }
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

.form-link {
  text-align: right;
  margin-bottom: 10px;
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
  position: relative;
  
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

  &.loading {
    cursor: not-allowed;
    opacity: 0.7;
  }

  .upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .upload-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 6px;
    font-size: 24px;
    color: #3b82f6;
  }
}

.verified-info-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  margin-top: 24px;
  border: 1px solid #e2e8f0;
  
  .info-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
    
    &:last-child {
      border-bottom: none;
    }
    
    .label {
      color: #64748b;
      font-size: 14px;
    }
    
    .value {
      color: #0f172a;
      font-weight: 600;
      font-family: monospace;
    }
  }
  
  .info-actions {
    margin-top: 20px;
    text-align: right;
  }
}

.verification-form {
  margin-top: 8px;
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

/* Split Layout Password Dialog Styles */
.custom-password-dialog {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  
  .el-dialog__header {
    margin: 0;
    padding: 0;
    display: none; /* Hide default header */
  }
  
  .el-dialog__body {
    padding: 0;
  }
}

.dialog-split-container {
  display: flex;
  height: 520px; /* Reduced height to fit better */
  
  /* Left Sidebar Styling */
  .dialog-sidebar {
    width: 300px;
    flex-shrink: 0;
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    position: relative;
    overflow: hidden;
    color: white;
    display: flex;
    flex-direction: column;
    
    .sidebar-bg-decor {
      position: absolute;
      top: -100px;
      right: -100px;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
    }
    
    .sidebar-content {
      position: relative;
      z-index: 1;
      padding: 32px 24px;
      height: 100%;
      display: flex;
      flex-direction: column;
      
      .brand-area {
        margin-bottom: 32px;
        
        .logo-icon {
          width: 42px;
          height: 42px;
          background: rgba(255, 255, 255, 0.2);
          backdrop-filter: blur(10px);
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
          margin-bottom: 16px;
          border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        h3 {
          margin: 0 0 8px;
          font-size: 20px;
          font-weight: 700;
          letter-spacing: -0.025em;
        }
        
        .desc {
          margin: 0;
          font-size: 13px;
          opacity: 0.8;
          line-height: 1.5;
        }
      }
      
      .security-features {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 16px;
        
        .feature-item {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 13px;
          
          .el-icon {
            font-size: 16px;
            color: #60a5fa; /* Lighter blue for icons */
            background: rgba(255, 255, 255, 0.1);
            padding: 4px;
            border-radius: 50%;
          }
        }
      }
      
      .sidebar-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 16px;
        
        p {
          margin: 0 0 2px;
          font-weight: 600;
          font-size: 13px;
        }
        
        span {
          font-size: 11px;
          opacity: 0.6;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
      }
    }
  }
  
  /* Right Main Content Styling */
  .dialog-main {
    flex: 1;
    padding: 32px 40px;
    background: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    
    .main-header {
      margin-bottom: 24px;
      text-align: center;
      
      h3 {
        margin: 0;
        font-size: 22px;
        color: #0f172a;
        font-weight: 700;
      }
    }
  }
}

.modern-form {
  .el-form-item {
    margin-bottom: 20px; /* Reduced margin */
    
    :deep(.el-form-item__label) {
      padding-bottom: 6px;
      font-weight: 500;
      font-size: 13px;
      color: #334155;
      line-height: 1.2;
    }
  }
  
  .custom-input {
    :deep(.el-input__wrapper) {
      padding: 6px 12px; /* Reduced padding */
      border-radius: 8px; 
      background-color: #f8fafc;
      box-shadow: 0 0 0 1px #e2e8f0 inset;
      transition: all 0.2s;
      
      &:hover {
        background-color: #fff;
        box-shadow: 0 0 0 1px #cbd5e1 inset;
      }
      
      &.is-focus {
        background-color: #fff;
        box-shadow: 0 0 0 2px #3b82f6 inset;
      }
    }
    
    :deep(.el-input__inner) {
      height: 32px; /* Reduced height */
      font-size: 14px;
    }

    &.readonly {
      :deep(.el-input__wrapper) {
        background-color: #f1f5f9;
        box-shadow: none;
      }
    }
    
    &.code-field {
      :deep(.el-input__wrapper) {
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
      }
    }
  }

  .method-select {
    margin-bottom: 20px;
    
    .custom-radio-group {
      width: 100%;
      display: flex;
      gap: 12px;
      
      :deep(.el-radio-button) {
        flex: 1;
      }
      
      :deep(.el-radio-button__inner) {
        width: 100%;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0;
        box-shadow: none !important;
        padding: 6px;
        height: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        background: white;
        color: #64748b;
        transition: all 0.2s;
      }
      
      :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
        background: #eff6ff;
        border-color: #3b82f6;
        color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6 !important;
        font-weight: 600;
      }
    }
  }

  .code-input-group {
    display: flex;
    gap: 0;
    width: 100%; /* Ensure full width alignment */
    
    .code-field {
      flex: 1;
    }
    
    .send-code-btn {
      height: 46px; /* Matched to new input total height (32+12+2) */
      border-radius: 0 8px 8px 0;
      padding: 0 16px;
      font-weight: 500;
      margin-left: -1px;
      z-index: 1;
      font-size: 13px;
    }
  }
  
  .form-actions {
    margin-top: 24px;
    
    .submit-btn {
      width: 100%;
      height: 44px; /* Slightly reduced */
      border-radius: 22px;
      font-size: 15px;
      font-weight: 600;
      background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
      border: none;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
      transition: all 0.2s;
      
      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
    
    .action-link {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-bottom: 16px;
      color: #64748b;
      cursor: pointer;
      font-size: 13px;
      transition: color 0.2s;
      
      &:hover {
        color: #3b82f6;
      }
    }
  }
}
</style>