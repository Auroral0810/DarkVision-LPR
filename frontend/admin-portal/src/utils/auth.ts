import { Storage } from "./storage";
import { AUTH_KEYS, ROLE_ROOT } from "@/constants";
import { useUserStoreHook } from "@/store/modules/user-store";
import router from "@/router";

// 负责本地凭证与偏好的读写
export const AuthStorage = {
  getAccessToken(): string {
    const isRememberMe = Storage.get<boolean>(AUTH_KEYS.REMEMBER_ME, false);
    return isRememberMe
      ? Storage.get(AUTH_KEYS.ACCESS_TOKEN, "")
      : Storage.sessionGet(AUTH_KEYS.ACCESS_TOKEN, "");
  },

  setAccessToken(accessToken: string, rememberMe: boolean = false): void {
    Storage.set(AUTH_KEYS.REMEMBER_ME, rememberMe);
    if (rememberMe) {
      Storage.set(AUTH_KEYS.ACCESS_TOKEN, accessToken);
      Storage.sessionRemove(AUTH_KEYS.ACCESS_TOKEN);
    } else {
      Storage.sessionSet(AUTH_KEYS.ACCESS_TOKEN, accessToken);
      Storage.remove(AUTH_KEYS.ACCESS_TOKEN);
    }
  },

  clearAuth(): void {
    Storage.remove(AUTH_KEYS.ACCESS_TOKEN);
    Storage.sessionRemove(AUTH_KEYS.ACCESS_TOKEN);
    Storage.remove(AUTH_KEYS.REMEMBER_ME);
  },

  getRememberMe(): boolean {
    return Storage.get<boolean>(AUTH_KEYS.REMEMBER_ME, false);
  },

  getUserInfo<T>(): T | undefined {
    const isRememberMe = this.getRememberMe();
    if (isRememberMe) {
      return Storage.get<T>(AUTH_KEYS.USER_INFO);
    }
    return Storage.sessionGet<T>(AUTH_KEYS.USER_INFO);
  },

  setUserInfo<T>(userInfo: T): void {
    const isRememberMe = this.getRememberMe();
    if (isRememberMe) {
      Storage.set(AUTH_KEYS.USER_INFO, userInfo);
      Storage.sessionRemove(AUTH_KEYS.USER_INFO);
    } else {
      Storage.sessionSet(AUTH_KEYS.USER_INFO, userInfo);
      Storage.remove(AUTH_KEYS.USER_INFO);
    }
  },

  clearUserInfo(): void {
    Storage.remove(AUTH_KEYS.USER_INFO);
    Storage.sessionRemove(AUTH_KEYS.USER_INFO);
  },
};

/**
 * 权限判断
 */
export function hasPerm(value: string | string[], type: "button" | "role" = "button"): boolean {
  const { roles, perms } = useUserStoreHook().userInfo;

  if (!roles) {
    return false;
  }

  // 超级管理员拥有所有权限
  if (type === "button" && roles.includes(ROLE_ROOT)) {
    return true;
  }

  const auths = (type === "button" ? perms : roles) || [];
  return typeof value === "string"
    ? auths.includes(value)
    : value.some((perm) => auths.includes(perm));
}

/**
 * 重定向到登录页面
 */
export async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  ElNotification({
    title: "提示",
    message,
    type: "warning",
    duration: 3000,
  });

  await useUserStoreHook().resetAllState();

  try {
    // 跳转到登录页，保留当前路由用于登录后跳转
    const currentPath = router.currentRoute.value.fullPath;
    await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
  } catch (error) {
    console.error("Redirect to login error:", error);
    // 强制跳转，即使路由重定向失败
    window.location.href = "/login";
  }
}
