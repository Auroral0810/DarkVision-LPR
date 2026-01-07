import request from "@/utils/request";

const AUTH_BASE_URL = "/api/v1/auth";

const AuthAPI = {
  /** 管理员登录接口（支持邮箱或手机号）*/
  login(data: AdminLoginData) {
    // 构建通用请求体
    const requestBody: any = {
      account: data.account,
      password: data.password,
      captcha_code: data.captchaCode,
      captcha_key: data.captchaKey
    };
    
    return request<any, AdminLoginResult>({
      url: "/api/admin/login",
      method: "post",
      data: requestBody,
      headers: {
        "Content-Type": "application/json",
      },
    });
  },

  /** 退出登录接口 */
  logout() {
    return request({
      url: "/api/admin/logout",
      method: "post",
    });
  },

  /** 获取验证码接口*/
  getCaptcha(captchaId?: string) {
    return request<any, CaptchaResult>({
      url: "/api/v1/captcha/generate",
      method: "get",
      params: {
        captcha_id: captchaId,
      },
    });
  },
};

export default AuthAPI;

/** 管理员登录表单数据 */
export interface AdminLoginData {
  /** 账号（邮箱或手机号） */
  account: string;
  /** 密码 */
  password: string;
  /** 验证码缓存key */
  captchaKey?: string;
  /** 验证码 */
  captchaCode?: string;
  /** 记住我 */
  rememberMe?: boolean;
}

/** 管理员登录响应 */
export interface AdminLoginResult {
  /** 访问令牌 */
  access_token: string;
  /** 令牌类型 */
  token_type: string;
  /** 用户信息 */
  user_info: UserInfo;
}

/** 用户信息 */
export interface UserInfo {
  id: number;
  phone?: string;
  nickname: string;
  email?: string;
  avatar_url?: string;
  // 其他用户字段根据需要添加
}

/** 验证码信息 */
export interface CaptchaResult {
  /** 验证码ID */
  captcha_id: string;
  /** 验证码图片Base64字符串 */
  image_base64: string;
  /** 过期时间(秒) */
  expire_seconds: number;
}
