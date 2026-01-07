import request from "@/utils/request";

/** 公告响应接口 */
export interface AnnouncementItem {
  id: number;
  title: str;
  content: str;
  display_position: str;
  start_time?: string;
  end_time?: string;
  is_enabled: boolean;
  created_at: string;
}

const WebsiteAPI = {
  /** 获取最新动态 (最近5条) */
  getLatestNews() {
    return request<any, AnnouncementItem[]>({
      url: "/api/v1/website/latest-news",
      method: "get",
    });
  },
};

export default WebsiteAPI;
