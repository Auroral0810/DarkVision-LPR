import { defineMock as originalDefineMock } from "vite-plugin-mock-dev-server";

/**
 * 自定义 defineMock，自动添加 /api/v1 前缀
 * 根据文档：https://www.youlai.tech/vue-docs/guide/mock.html
 */
export const defineMock = (mocks: any[]) => {
  return originalDefineMock(
    mocks.map((mock) => {
      // 如果 mock 有 body，转换为 response 函数
      if (mock.body && !mock.response) {
        mock.response = () => mock.body;
        delete mock.body;
      }
      // 拼接完整 URL: /api/v1/ + menus/routes
      mock.url = `/api/v1/${mock.url}`.replace(/\/+/g, "/");
      return mock;
    })
  );
};
