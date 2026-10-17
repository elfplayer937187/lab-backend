# 1. 改完模型后，生成迁移脚本（这一步不碰数据库）
.\.venv\Scripts\alembic.exe revision --autogenerate -m "加了什么字段"

# 2. 应用，真正改库
.\.venv\Scripts\alembic.exe upgrade head    
