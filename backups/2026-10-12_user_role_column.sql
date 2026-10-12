-- user.role 列删除前的数据备份
-- 备份时间: 2026-10-12
-- 背景: role 列已从 User 模型移除(app/User/database.py),角色改由独立的 role 表管理。
--       该列是模型删列之前 Base.metadata.create_all() 建的,代码里已无任何引用。
--       删除前把列定义和 4 行数据留在这里,需要时可完整恢复。

-- ---- 恢复:先加回列,再写回数据 ----

ALTER TABLE `user`
    ADD COLUMN `role` VARCHAR(7) NOT NULL DEFAULT 'student'
        COMMENT '角色: student-学生,admin-管理员' AFTER `name`;

-- 删除时的用户表:4 行,role 取值只有 admin / student 两种
UPDATE `user` SET `role` = 'admin' WHERE `id` = 1; -- root
UPDATE `user` SET `role` = 'student' WHERE `id` = 2; -- zhangsan
UPDATE `user` SET `role` = 'student' WHERE `id` = 3; -- lisi
UPDATE `user` SET `role` = 'student' WHERE `id` = 6; -- rootwe
