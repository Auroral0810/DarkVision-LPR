/**
 * API响应码枚举
 */
export const enum ApiCodeEnum {
  /**
   * 成功
   */
  SUCCESS = 20000,
  /**
   * 错误
   */
  ERROR = "B0001",

  /**
   * 访问令牌无效或过期
   */
  ACCESS_TOKEN_INVALID = "A0230",

  /**
   * 刷新令牌无效或过期
   */
  REFRESH_TOKEN_INVALID = "A0231",

  /**
   * 未登录/token失效 (40100)
   */
  UNAUTHORIZED = 40100,

  /**
   * Token过期 (40101)
   */
  TOKEN_EXPIRED = 40101,

  /**
   * Token无效 (40102) - 也用于强制下线
   */
  TOKEN_INVALID = 40102,

  /**
   * 用户已被封禁 (40206)
   */
  USER_BANNED = 40206,
}
