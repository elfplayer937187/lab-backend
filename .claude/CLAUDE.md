# lab-backend 项目规范

## 1. 项目简介

AI 实验室后端服务。对外提供 HTTP API,涵盖三类能力:

- **用户与认证**:注册、登录、JWT 鉴权
- **实验室业务**:实验室相关的核心业务数据管理
- **AI 能力**:基于 LangGraph 的对话与 Agent 编排,ChromaDB 做向量检索

技术栈已由 `requirements.txt` 锁定,但**项目代码尚未开始编写**(`app/` 目录还不存在)。本文件是后续所有开发必须遵守的约定。

---

## 2. 技术栈

| 领域 | 选型 | 版本 |
|---|---|---|
| Web 框架 | FastAPI | 0.115.13 |
| ASGI 服务器 | uvicorn | 0.34.0 |
| ORM | SQLAlchemy | 2.0.41 |
| 数据库驱动 | PyMySQL(MySQL) | 1.1.1 |
| 配置管理 | pydantic-settings | 2.7.1 |
| 密码哈希 | bcrypt | 5.0.0 |
| 令牌 | PyJWT | 2.13.0 |
| 表单/文件上传 | python-multipart | 0.0.32 |
| Agent 编排 | LangGraph | 1.2.11 |
| LLM 客户端 | langchain-openai | 1.6.2 |
| LLM 核心抽象 | langchain-core | 1.6.3 |
| 向量库 | ChromaDB | 1.5.9 |
| 状态持久化 | langgraph-checkpoint-redis | 0.5.2 |

### 两个易踩的点

1. **数据库是同步的**。用 `pymysql`,不是 `asyncpg` / `aiomysql`。见第 6 节的异步约定。
2. **JWT 用 PyJWT,密码用 bcrypt 原生库**。项目**没有**安装 `passlib`,也**没有** `python-jose`。不要写 `from jose import jwt`,也不要写 `from passlib.context import CryptContext`。

### 依赖管理规则

- 所有直接依赖**必须**登记在 `requirements.txt`,并写死版本号(`==`)。
- 不要依赖传递依赖。当前 venv 里的 `redis` 只是 `langgraph-checkpoint-redis` 拉进来的间接依赖,但它会被业务代码直接 `import`,这是**反面例子**——后续用到 Redis 时必须把 `redis` 显式加进 `requirements.txt`。
- venv 中**不存在** `alembic`、`pytest`、`loguru`、`celery`,不要 import。

---



## 4. 常用命令

以下命令在当前环境可直接执行:

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 生成依赖清单(仅在显式添加依赖后使用)
pip freeze > requirements.txt

# 启动开发服务(热重载)
# 注意:需先创建 app/main.py,当前尚未创建,此命令暂时会失败
uvicorn app.main:app --reload --port 8000

# 格式化代码
.\.venv\Scripts\ruff.exe format app\ tests\

# 静态检查
.\.venv\Scripts\ruff.exe check app\

# 静态检查并自动修复(import 排序等)
.\.venv\Scripts\ruff.exe check --fix app\
```

接口文档(服务启动后):

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

### 代码质量工具(已配置)

| 工具 | 管什么 | 配置文件 |
|---|---|---|
| **Ruff** | Python 的格式化 + 静态检查(替代 black / isort / flake8) | `ruff.toml` |
| **Prettier** | JSON / Markdown / YAML 等非 Python 文件 | `.prettierrc.json` + `.prettierignore` |
| **VSCode** | 保存时自动格式化、4 空格缩进、100 字符标尺 | `.vscode/settings.json` |

要点:

- **Ruff 同时承担格式化与 lint**,`ruff.toml` 里已设 `quote-style = 'single'`(单引号)和 `line-length = 100`,与本文档第 6 节的风格规范一致。
- **Prettier 不能格式化 Python**,Python 一律交给 Ruff。
- 在 VSCode 里保存文件会自动格式化。`.vscode/settings.json` 已入库,但**扩展需要各自安装**,见 `.vscode/extensions.json` 的推荐列表(`charliermarsh.ruff`、`esbenp.prettier-vscode`)。
- 提交前建议手动跑一次 `ruff check app\`,不要只依赖编辑器的自动修复。

### 待引入的工具(引入时按下表落地,避免重复决策)

| 工具 | 用途 | 约定 |
|---|---|---|
| `alembic` | 数据库迁移 | 引入后配置文件放项目根目录 `alembic.ini`,迁移脚本放 `alembic/`。表结构变更一律走迁移脚本 |
| `pytest` + `httpx` | 测试 | 测试放 `tests/`,文件名 `test_*.py`。FastAPI 用 `TestClient`(`httpx` 已在 venv 中) |
| `loguru` | 日志 | 若要引入,统一在 `app/` 下封装 logger,不要在业务代码里裸用 `print` |

---

## 5. 环境变量规范

### 读取方式

**所有配置集中在 `app/config.py`**,用一个 `Settings(BaseSettings)` 类读取 `.env`:

```python
from pathlib import Path

from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / '.env'


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str

    model_config = {
        'env_file': ENV_FILE,
        'env_file_encoding': 'utf-8',
        'extra': 'ignore',
    }


settings = Settings()  # type: ignore[call-arg]
```

- **禁止**在业务代码里散落 `os.getenv(...)` / `os.environ[...]`。
- 其他模块统一 `from app.config import settings`。
- 新增配置项时,**必须同步更新 `Settings` 类**,并同步更新 `.env` 与 `.env.example`。
- **密钥类字段一律不写默认值**(如 `DATABASE_URL: str` 而非 `= 'mysql+pymysql://root:密码@...'`),缺失时应当启动即报错。写死默认值等于把密码提交进 git。
  - 副作用:静态分析器(Pylance)看不到 pydantic-settings 从 `.env` 注入的过程,会误报 `Settings()` 缺参数,故加 `# type: ignore[call-arg]` 抑制。这是有意为之,不要为了消警告而加回默认值。

### 当前配置项

`.env` 现有两条(端口 3308,库名 `my_lab`):

```
DATABASE_URL=mysql+pymysql://<user>:<password>@127.0.0.1:3308/my_lab
DB_ECHO=true
```

### 预期配置项(按需补充)

| 键名 | 用途 |
|---|---|
| `DATABASE_URL` | MySQL 连接串,已存在 |
| `DB_ECHO` | 是否打印 SQL,已存在(开发开、生产关) |
| `JWT_SECRET` | JWT 签名密钥 |
| `JWT_ALGORITHM` | 签名算法,通常 `HS256` |
| `JWT_EXPIRE_MINUTES` | token 有效期 |
| `REDIS_URL` | LangGraph checkpointer 的 Redis 连接串 |
| `LLM_BASE_URL` | LLM 服务的 OpenAI 兼容地址 |
| `LLM_API_KEY` | LLM 服务密钥 |
| `LLM_MODEL` | 模型名 |
| `CHROMA_PERSIST_DIR` | ChromaDB 持久化目录 |

### LLM 接入约定

调用的是**国内 OpenAI 兼容接口**(DeepSeek / 通义 / 智谱等),通过 openai SDK 的 `base_url` 指向服务地址:

```python
from langchain_openai import ChatOpenAI

from app.core.config import settings


def build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
    )
```

- `api_key` 和 `base_url` **严禁硬编码**,一律从 `settings` 取。
- **模型名不写死在业务代码里**,统一走 `settings.LLM_MODEL`,便于换供应商。
- 密钥不得出现在日志、异常信息、提交记录中。

### `.env` 纪律

- `.env` 已在 `.gitignore` 中,**永不入库**。
- 需要提交的是 `.env.example`,只写键名和占位值,不含真实密钥。
- 新增环境变量后,记得同步更新 `.env.example`。

---

## 6. 代码风格

### 基础

- Python 3.13,遵循 PEP 8,4 空格缩进。
- **字符串一律用单引号** `'...'`。含中文标点的字符串**必须**用单引号,避免中文弯引号被转成直引号后与字符串边界冲突。
- 行宽 100 字符。
- 以上三条**由 Ruff 强制执行**:`ruff.toml` 中 `quote-style = 'single'`、`indent-width = 4`、`line-length = 100`。不要手工调整这些格式,交给 `ruff format`。`ruff check` 还负责 import 排序(`I001`)。

### 类型注解

- **所有函数签名标注参数与返回值类型**,包括 `def`、`async def`、类的 `__init__` 之外的方法。
- ORM 模型使用 SQLAlchemy 2.0 的声明式风格,**不用 1.x 的 `Column(...)`**:

```python
from sqlalchemy.orm import Mapped, mapped_column


class Lab(Base):
    __tablename__ = 'lab'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
```

- Pydantic 模型同样写全注解,用 `Field(...)` 补充校验约束。

### 命名

| 对象 | 风格 | 示例 |
|---|---|---|
| 函数、变量、模块 | `snake_case` | `get_user_by_id` |
| 类、Pydantic 模型、ORM 模型 | `PascalCase` | `UserCreate` |
| 常量 | `UPPER_CASE` | `MAX_RETRY` |
| 私有成员 | 单下划线前缀 | `_hash_password` |

ORM 模型的 `__tablename__` 用小写单数或复数需在项目内保持一致,建议统一用**小写下划线复数**,如 `labs`、`users`。

### 导入顺序

三组,组间空一行:

```python
# 1. 标准库
from datetime import datetime, timedelta

# 2. 第三方
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 3. 本项目
from app.database import get_db
from app.modules.auth.service import authenticate
```

### 异步约定(重要)

因为底层是**同步** SQLAlchemy + PyMySQL:

- **涉及数据库访问的函数写成同步 `def`**。FastAPI 会自动把同步路由函数丢进线程池执行,不会阻塞事件循环。
- **不要**在同步函数里 `await`,也**不要**为了"显得异步"而把所有函数改成 `async def` —— 那样反而会在事件循环里执行阻塞的 DB I/O。
- 只有真正的异步 I/O(如流式调用 LLM、`httpx.AsyncClient` 请求外部服务)才用 `async def`。

⛔ **禁止使用 `create_async_engine` / `AsyncSession` / `async_sessionmaker`**。

PyMySQL 是同步驱动,SQLAlchemy 的 asyncio 扩展只接受异步驱动。一旦写成:

```python
engine = create_async_engine(settings.DATABASE_URL)  # DATABASE_URL 是 mysql+pymysql://
```

会在**这一行**直接抛异常,应用连启动都做不到:

```
sqlalchemy.exc.InvalidRequestError: The asyncio extension requires an
async driver to be used. The loaded 'pymysql' is not async.
```

如果将来确实要改成异步,需要**三件事一起改**,缺一不可:安装 `aiomysql`、把 `DATABASE_URL` 改成 `mysql+aiomysql://`、重写 `app/database.py` 与所有 service 层函数。不要只改其中一处。

### 提交规范

仓库尚无提交,按 Conventional Commits 写 commit message(与兄弟项目 `lab-fronted` 的 commitlint 风格对齐):

```
feat: 新增用户登录接口
fix: 修正 token 过期时间计算错误
docs: 补充环境变量说明
refactor: 拆分 auth service
chore: 升级 fastapi 版本
```

### 安全红线

- 密码**只存 bcrypt 哈希**,绝不存明文,绝不写进日志或异常信息。
- 任何密钥、连接串、token 不得硬编码在代码里。
- 提交前确认 `.env` 未被 `git add`。

---

## 7. 当前进度与待办

项目处于起步阶段,**尚无任何业务代码**。已完成:依赖清单、代码质量工具链(第 4 节)、`app/config.py`、`app/database.py`(同步)、`.env.example`。

接下来需要落地的骨架(按顺序):

1. `app/security.py` —— bcrypt 哈希 + JWT 签发/校验
2. `app/deps.py` —— `get_current_user` 等公共依赖(会话依赖 `get_db` 已在 `app/database.py`)
3. `app/main.py` —— FastAPI 实例、路由挂载、CORS
4. `app/modules/auth/` —— 第一个功能模块,作为后续模块的参考样板
5. 按第 5 节补齐 `Settings` 字段(`JWT_SECRET`、`LLM_*` 等)与对应 `.env` 键
6. 引入 `alembic`,建立首次迁移
7. 引入 `pytest`,建立 `tests/`

---

## 8. 问题记录规范

排查出的问题、踩过的坑、由此固化的决策,落盘到 `.claude/logs/`,不要只留在对话里。

### 目录格式

**每次记录新建一个时间戳文件夹,md 放里面:**

```
.claude/logs/2026-10-06_173523/issues.md
```

- 文件夹名 `yyyy-MM-dd_HHmmss`(如 `2026-10-06_173523`)。**不能含冒号**,Windows 路径不允许,所以用 `_` 分隔
- 生成命令:`Get-Date -Format 'yyyy-MM-dd_HHmmss'`
- 一次会话一个目录,主文件固定叫 `issues.md`。**新建目录,不要往旧的时间戳目录里追加**

### 内容要求

四部分:记录时间与背景、问题清单(标**状态**和**严重程度**)、问题详情(现象 → 报错原文 → 原因 → 修复)、待办。

- **报错原样粘贴**,不要转述 —— 原文能搜到答案,转述不能
- **区分「已验证」和「推断」**,并说明为何没能实测(如服务未启动)
- **记录决策的「为什么」**,不只是「改成了什么」。否则后人会觉得麻烦而改回去

### 与 CLAUDE.md 的分工

一条信息**三个月后仍要照着做** → 写进 CLAUDE.md;只是**这次为什么这么改** → 写进 logs。

> `.claude/logs/` 目前被 `.gitignore` 的 `logs/` 规则忽略,不会入库。要共享需加例外 `!.claude/logs/`。
