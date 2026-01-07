import { store } from "@/store";

import AuthAPI, { type AdminLoginData, type UserInfo } from "@/api/auth-api";

import { AuthStorage } from "@/utils/auth";
import { usePermissionStoreHook } from "@/store/modules/permission-store";
import { useDictStoreHook } from "@/store/modules/dict-store";
import { useTagsViewStore } from "@/store";
import { cleanupWebSocket } from "@/plugins/websocket";

export const useUserStore = defineStore("user", () => {
  // 用户信息 - 从本地存储恢复（如果存在）
  const userInfo = ref<UserInfo>(AuthStorage.getUserInfo<UserInfo>() || {} as UserInfo);

  function login(loginData: AdminLoginData) {
    return new Promise<void>((resolve, reject) => {
      AuthAPI.login(loginData)
        .then((data) => {
          const { access_token, user_info } = data;
          // 保存token，支持记住我
          AuthStorage.setAccessToken(access_token, loginData.rememberMe || false);
          // 保存用户信息到内存和本地存储
          Object.assign(userInfo.value, user_info);
          AuthStorage.setUserInfo(user_info);
          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  }

  /**
   * 获取管理员信息
   */
  function getUserInfo() {
    return new Promise<UserInfo>((resolve, reject) => {
      AuthAPI.getUserInfo()
        .then((data) => {
          Object.assign(userInfo.value, data);
          AuthStorage.setUserInfo(data);
          resolve(data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  }

  /**
   * 登出
   */
  function logout() {
    return new Promise<void>((resolve, reject) => {
      AuthAPI.logout()
        .then(() => {
          // 重置所有系统状态
          resetAllState();
          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  }

  /**
   * 重置所有系统状态
   * 统一处理所有清理工作，包括用户凭证、路由、缓存等
   */
  function resetAllState() {
    // 1. 重置用户状态
    resetUserState();

    // 2. 重置其他模块状态
    // 重置路由
    usePermissionStoreHook().resetRouter();
    // 清除字典缓存
    useDictStoreHook().clearDictCache();
    // 清除标签视图
    useTagsViewStore().delAllViews();

    // 3. 清理 WebSocket 连接
    cleanupWebSocket();
    console.log("[UserStore] WebSocket connections cleaned up");

    return Promise.resolve();
  }

  /**
   * 重置用户状态
   * 仅处理用户模块内的状态
   */
  function resetUserState() {
    // 清除用户凭证
    AuthStorage.clearAuth();
    // 清除持久化的用户信息
    AuthStorage.clearUserInfo();
    // 重置用户信息
    userInfo.value = {} as UserInfo;
  }

  return {
    userInfo,
    isLoggedIn: () => !!AuthStorage.getAccessToken(),
    login,
    logout,
    getUserInfo,
    resetAllState,
    resetUserState,
  };
});

/**
 * 在组件外部使用UserStore的钩子函数
 * @see https://pinia.vuejs.org/core-concepts/outside-component-usage.html
 */
export function useUserStoreHook() {
  return useUserStore(store);
}
