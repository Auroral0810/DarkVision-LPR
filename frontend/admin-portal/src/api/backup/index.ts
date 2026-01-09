import request from '@/utils/request';

export interface BackupRecord {
  id: number;
  filename: string;
  file_path: string;
  file_size: number;
  created_at: string;
  created_by: number;
  creator_name: string;
  status: string;
  description?: string;
}

export interface BackupQuery {
  page: number;
  size: number;
  start_time?: string;
  end_time?: string;
}

class BackupApi {
  /**
   * 获取备份列表
   */
  static getBackupList(params: BackupQuery) {
    return request({
      url: '/api/admin/backup/list',
      method: 'get',
      params,
    });
  }

  /**
   * 创建备份
   */
  static createBackup(data: { description?: string }) {
    return request({
      url: '/api/admin/backup/create',
      method: 'post',
      data,
    });
  }

  /**
   * 删除备份
   */
  static deleteBackup(id: number) {
    return request({
      url: `/api/admin/backup/${id}`,
      method: 'delete',
    });
  }

  /**
   * 恢复备份
   */
  static restoreBackup(id: number) {
    return request({
      url: `/api/admin/backup/${id}/restore`,
      method: 'post',
      timeout: 120000 // Increase timeout for restore
    });
  }

  /**
   * 下载备份文件 (以Blob形式)
   */
  static downloadBackup(id: number) {
    return request({
      url: `/api/admin/backup/${id}/download`,
      method: 'get',
      responseType: 'blob'
    });
  }
}

export default BackupApi;
