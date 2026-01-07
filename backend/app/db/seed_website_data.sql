
-- 插入系统用户（如果尚未存在，用于关联 created_by 字段）
-- 假设 id=1 是系统管理员
INSERT IGNORE INTO users (id, phone, nickname, password_hash, user_type, status) VALUES 
(1, '13800000000', 'Admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin', 'active');

-- =============================================
-- 1. 首页轮播图 (Carousels)
-- =============================================
INSERT INTO carousels (title, image_url, link_url, sort_order, is_enabled) VALUES
('智能感知，精准识别', 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80', NULL, 1, 1),
('夜间识别，清晰如昼', 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80', NULL, 2, 1);

-- =============================================
-- 2. 系统公告 (Announcements)
-- =============================================
INSERT INTO announcements (title, content, display_position, start_time, end_time, is_enabled, created_by) VALUES
('系统维护通知', 'DarkVision LPR 将于本周六凌晨 2:00 进行系统升级，预计耗时 2 小时。', 'banner', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 1);

-- =============================================
-- 3. 常见问题 (FAQs)
-- =============================================
-- 分类
INSERT INTO faq_categories (id, name, sort_order) VALUES
(1, '新手入门', 1),
(2, '会员服务', 2),
(3, '技术支持', 3);

-- 问题
INSERT INTO faqs (category_id, question, answer, sort_order, view_count, is_hot) VALUES
(1, '如何开始使用系统？', '注册账号后即可开始使用，普通用户每日有20次免费识别机会。您可以在控制台查看详细的使用指南。', 1, 100, 1),
(1, '支持哪些图片格式？', '支持 JPG、PNG、BMP 等常见图片格式。单张图片建议在 5MB 以内，VIP 用户支持最大 10MB 的高清图片。', 2, 90, 0),
(2, '如何升级到 VIP？', '在价格页面选择 VIP 方案，点击购买并完成支付后，您的账号将立即升级，享受更多权益。', 3, 80, 1),
(2, '是否提供 API 接口？', '是的，VIP 用户和企业用户可以使用 RESTful API 接口。我们提供完善的 API 文档和多语言 SDK。', 4, 70, 0);

-- =============================================
-- 4. 客户端下载 (Client Downloads)
-- =============================================
INSERT INTO client_downloads (os, version, download_url, changelog, release_date, is_latest) VALUES
('windows', 'v1.0.0', 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_x64_zh%2DCN.msi', 'Initial Release', '2026-01-01', 1),
('macos', 'v1.0.0', 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_aarch64.dmg', 'Initial Release', '2026-01-01', 1),
('linux', 'v1.0.0', 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/easy%2Drename_1.0.0_amd64.deb', 'Initial Release', '2026-01-01', 1);

-- =============================================
-- 5. 文档 (Documents)
-- =============================================
INSERT INTO documents (title, doc_type, content, version, is_current, created_by) VALUES
('技术文档', 'tech', '## 架构概览\n\nDarkVision LPR 采用微服务架构...\n\n## 部署指南\n\n1. Docker Compose...\n', '1.0.0', 1, 1),
('服务协议', 'service_agreement', '## 1. 服务内容\n\n本协议是您与 DarkVision 之间关于使用本服务的法律协议...', '1.0.0', 1, 1),
('隐私政策', 'privacy_policy', '## 1. 信息收集\n\n我们收集您的以下信息以提供更好的服务...', '1.0.0', 1, 1);

-- =============================================
-- 6. 套餐 (Packages - 对应 Pricing.vue)
-- =============================================
-- 注意：packages 表在 Section 4，这里一并插入
INSERT INTO packages (id, name, code, price, duration_months, description, is_active) VALUES
(1, '免费版', 'free', 0.00, NULL, '个人学习与体验', 1),
(2, 'VIP 会员', 'vip_monthly', 99.00, 1, '专业开发者与小型团队', 1),
(3, '企业版', 'enterprise_custom', 0.00, NULL, '大型企业与定制化需求', 1);

-- 套餐功能点 (Package Features)
INSERT INTO package_features (package_id, feature_key, feature_value) VALUES
(1, 'daily_limit', '20'),
(1, 'max_image_size', '5MB'),
(1, 'history_retention', '7 days'),
(2, 'daily_limit', '500'),
(2, 'api_limit', '5000'),
(2, 'batch_size', '50'),
(2, 'video_limit', '10'),
(3, 'daily_limit', 'Unlimited'),
(3, 'custom_model', 'Yes'),
(3, 'private_deployment', 'Optional');

-- =============================================
-- 7. 系统配置 (System Configs)
-- =============================================
INSERT INTO system_configs (config_key, config_value, description, is_public) VALUES
('total_recognition_count', '125680', '累计识别车牌数量', 1),
('service_availability', '99.9%', '服务可用性', 1),
('enterprise_clients', '500+', '企业客户数量', 1);

