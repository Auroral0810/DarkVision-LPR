<template>
  <div class="register-content">
    <!-- 头部图标和标题 -->
    <div class="header-section">
      <div class="icon-wrapper">
        <el-icon :size="28" color="#F56C6C"><Lock /></el-icon>
      </div>
      <h3 class="title">{{ t("login.adminAccessOnly") }}</h3>
      <p class="subtitle">{{ t("login.adminAccessInfo") }}</p>
    </div>

    <!-- 管理员联系卡片列表 -->
    <div class="contact-list">
      <div class="list-label">{{ t("login.contactAdmins") }}</div>

      <!-- 超级管理员卡片 -->
      <div class="admin-card super-admin">
        <div class="card-left">
          <el-avatar :size="44" class="admin-avatar super">
            <el-icon :size="22"><UserFilled /></el-icon>
          </el-avatar>
        </div>
        <div class="card-right">
          <div class="admin-header">
            <span class="name">{{ t("login.superAdmin") }}</span>
            <el-tag size="small" effect="dark" type="danger" round>ROOT</el-tag>
          </div>
          <p class="desc">{{ t("login.superAdminDesc") }}</p>
          
          <!-- 电话联系方式 -->
          <div class="contact-row" @click="copyPhone('15968588744')">
            <el-icon class="phone-icon"><Iphone /></el-icon>
            <span class="phone-number">159 6858 8744</span>
            <el-icon class="copy-icon"><DocumentCopy /></el-icon>
          </div>
        </div>
      </div>

      <!-- 用户管理员卡片 -->
      <div class="admin-card normal-admin">
        <div class="card-left">
          <el-avatar :size="44" class="admin-avatar normal">
            <el-icon :size="22"><User /></el-icon>
          </el-avatar>
        </div>
        <div class="card-right">
          <div class="admin-header">
            <span class="name">{{ t("login.userAdmin") }}</span>
            <el-tag size="small" effect="plain" type="info" round>ADMIN</el-tag>
          </div>
          <p class="desc">{{ t("login.userAdminDesc") }}</p>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="action-footer">
      <el-button type="primary" class="login-btn" size="large" round @click="toLogin">
        {{ t("login.backToLogin") }}
      </el-button>

      <div class="help-tip">
        <el-icon><InfoFilled /></el-icon>
        <span>{{ t("login.adminHelpText") }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { UserFilled, User, InfoFilled, Lock, Iphone, DocumentCopy } from "@element-plus/icons-vue";

const { t } = useI18n();
const emit = defineEmits(["update:modelValue"]);

const toLogin = () => emit("update:modelValue", "login");

// 复制电话号码
const copyPhone = (phone: string) => {
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(phone)
      .then(() => {
        ElMessage.success(t("login.copied"));
      })
      .catch(() => {
        ElMessage.warning("复制失败，请手动复制");
      });
  } else {
    // 兼容性处理
    const input = document.createElement("input");
    input.value = phone;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
    ElMessage.success(t("login.copied"));
  }
};
</script>

<style lang="scss" scoped>
.register-content {
  padding: 10px 10px 0;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-section {
  text-align: center;
  margin-bottom: 24px;

  .icon-wrapper {
    width: 56px;
    height: 56px;
    background: var(--el-color-danger-light-9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    transition: transform 0.3s;
    
    &:hover {
      transform: scale(1.05);
    }
  }

  .title {
    font-size: 20px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin: 0 0 8px;
  }

  .subtitle {
    font-size: 14px;
    color: var(--el-text-color-secondary);
    line-height: 1.5;
    margin: 0;
    padding: 0 20px;
  }
}

.contact-list {
  margin-bottom: 28px;

  .list-label {
    font-size: 13px;
    color: var(--el-text-color-secondary);
    margin-bottom: 12px;
    font-weight: 500;
  }
}

.admin-card {
  display: flex;
  padding: 16px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  margin-bottom: 12px;
  transition: all 0.3s;
  cursor: default;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--el-box-shadow-light);
    border-color: var(--el-color-primary-light-7);
  }

  &.super-admin {
    background: linear-gradient(
      to right bottom,
      var(--el-bg-color),
      var(--el-color-primary-light-9)
    );
    border-color: var(--el-color-primary-light-8);
  }

  .card-left {
    margin-right: 16px;
    
    .admin-avatar {
      transition: transform 0.3s;
      
      &.super {
        background: var(--el-color-primary-light-8);
        color: var(--el-color-primary);
      }
      &.normal {
        background: var(--el-fill-color);
        color: var(--el-text-color-regular);
      }
    }
  }

  &:hover .admin-avatar {
    transform: scale(1.1) rotate(5deg);
  }

  .card-right {
    flex: 1;
    min-width: 0;

    .admin-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;

      .name {
        font-weight: 600;
        font-size: 15px;
        color: var(--el-text-color-primary);
      }
    }

    .desc {
      font-size: 12px;
      color: var(--el-text-color-secondary);
      margin: 0 0 10px;
      line-height: 1.4;
    }

    .contact-row {
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.6);
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
      border: 1px solid transparent;

      &:hover {
        background: #fff;
        border-color: var(--el-color-primary-light-5);
        
        .phone-number, .phone-icon {
          color: var(--el-color-primary);
        }
        
        .copy-icon {
          opacity: 1;
          transform: translateX(0);
        }
      }

      .phone-icon {
        margin-right: 6px;
        font-size: 14px;
        color: var(--el-text-color-regular);
      }

      .phone-number {
        font-family: monospace;
        font-weight: 600;
        font-size: 14px;
        color: var(--el-text-color-regular);
        letter-spacing: 0.5px;
      }

      .copy-icon {
        margin-left: 8px;
        font-size: 12px;
        color: var(--el-color-primary);
        opacity: 0;
        transform: translateX(-4px);
        transition: all 0.2s;
      }
    }
  }
}

.action-footer {
  display: flex;
  flex-direction: column;
  align-items: center;

  .login-btn {
    width: 100%;
    height: 44px;
    font-size: 16px;
    margin-bottom: 16px;
    box-shadow: var(--el-box-shadow-lighter);
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: var(--el-box-shadow);
    }
  }

  .help-tip {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    
    .el-icon {
      font-size: 14px;
    }
  }
}
</style>