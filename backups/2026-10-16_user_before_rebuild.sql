-- 重建 my_lab 之前导出的 user 表备份
-- 行数: 15
-- 列: id, username, password, name, role, email, phone, avatar, status, created_at, updated_at

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `role` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色: student-学生,admin-管理员',
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `status` int NOT NULL COMMENT '状态: 0-禁用,1-启用',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (1, 'admin', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '超级管理员', 'admin', 'admin@lab.local', '13800000001', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (2, 'zhangsan', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '张三', 'student', 'zhangsan@lab.local', '13800000002', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (3, 'lisi', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '李四', 'student', 'lisi@lab.local', '13800000003', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (4, 'wangwu', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '王五', 'student', 'wangwu@lab.local', '13800000004', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (5, 'zhaoliu', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '赵六', 'student', 'zhaoliu@lab.local', '13800000005', NULL, 0, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (6, 'sunqi', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '孙七', 'student', 'sunqi@lab.local', '13800000006', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (7, 'zhouba', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '周八', 'student', 'zhouba@lab.local', '13800000007', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (8, 'wujiu', '$2b$12$TqWwH7g5E5raPO/xbNvsXOKcVr9EBNxcqdt4SPQTqdeM5QONgYvqm', '吴九', 'admin', 'wujiu@lab.local', '13800000008', NULL, 1, '2026-10-07 21:59:00', '2026-10-07 21:59:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (9, 'elf', '$2b$12$jF3j.y4YZzufojga2byEsOUgKwa2FzMhFoD5ogUYUG8iuAVWvpr8i', 'string', 'student', 'string', '13061139701', NULL, 1, '2026-10-07 22:08:59', '2026-10-07 22:08:59');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (10, 'admin1', '$2b$12$gXggdCmNeWTkQ/UOGsBq/eqGScG8SU0ub.L8183rEjJYWtQSF7YlK', '112', 'student', '', '17712327930', NULL, 1, '2026-10-09 23:02:00', '2026-10-09 23:02:00');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (11, 'elf1', '111111', 'string', 'student', 'string', '13061139701', NULL, 1, '2026-10-11 15:17:16', '2026-10-11 15:17:16');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (12, 'elf12', '111111', 'string', 'student', 'string', '13061139701', NULL, 1, '2026-10-11 15:20:25', '2026-10-11 15:20:25');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (13, 'elf122', '$2b$12$k6iMGmm4FdEa5myppTsTCe.9KoOthIz5BiTZNL71EtUiKDUWmCmca', 'string', 'student', 'string', '13061139701', NULL, 1, '2026-10-11 15:20:35', '2026-10-11 15:20:35');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (14, 'eee', '$2b$12$6krE4XLdtBkLthh300B2gertGY9Km/LBHe9ib5gb4vc2/bPTo3OAO', 'nb', 'student', '', '13395250030', NULL, 1, '2026-10-11 21:15:08', '2026-10-11 21:15:08');
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`, `email`, `phone`, `avatar`, `status`, `created_at`, `updated_at`) VALUES (15, 'admin112', '$2b$12$qxfip4kOS7hv4rbv1G8WcutxLg72.ZFz4iWkBrwaf50ljnDTRFI/a', 'adwaw', 'student', '', '17712327930', NULL, 1, '2026-10-11 22:20:10', '2026-10-11 22:20:10');
