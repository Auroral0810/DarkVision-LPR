import request from "@/utils/request";

const TrackingAPI = {
  /** 页面访问埋点 */
  trackPageView(data: { page_path: string; page_type?: "admin" | "user" | "website" }) {
    return request({
      url: "/api/v1/tracking/page-view",
      method: "post",
      data: {
        page_path: data.page_path,
        page_type: data.page_type || "user",
      },
    });
  },
};

export default TrackingAPI;

