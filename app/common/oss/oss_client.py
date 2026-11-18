import logging
import uuid
from datetime import timedelta
from pathlib import Path

import alibabacloud_oss_v2 as oss
from fastapi import UploadFile

from app.config import settings

logger = logging.getLogger(__name__)


def create_oss_client() -> oss.Client:
    config = oss.config.load_default()
    # .env 里的 AK 由 pydantic-settings 读进 settings,不会写进 os.environ,
    # 所以不能用 EnvironmentVariableCredentialsProvider,直接传静态凭据。
    config.credentials_provider = oss.credentials.StaticCredentialsProvider(
        settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET
    )
    # region 填 cn-hangzhou 这种格式,不带 oss- 前缀
    config.region = settings.OSS_REGION
    return oss.Client(config)


# 全局唯一实例
client = create_oss_client()


def public_url(key: str) -> str:
    """把对象 key 拼成可直接访问的 URL(公共读 bucket 才有意义)。"""
    return (
        f"https://{settings.OSS_BUCKET}."
        f"oss-{settings.OSS_REGION}.aliyuncs.com/{key}"
    )


def upload_file(prefix: str, file_name: str, file_content: UploadFile):
    """把上传文件写入 OSS,返回对象 key;展示用 public_url(key) 拼 URL。"""
    name = file_name or file_content.filename or ""
    ext = Path(name).suffix.lower()
    # UUID 文件名不会覆盖,也可以避免中文名、重名和路径注入
    key = f"{prefix.strip('/')}/{uuid.uuid4().hex}{ext}"
    client.put_object(
        oss.PutObjectRequest(
            bucket=settings.OSS_BUCKET,
            key=key,
            body=file_content.file,
            content_type=file_content.content_type or "application/octet-stream",
            # 文件名不可变,可以给长缓存
            cache_control="public, max-age=31536000, immutable",
        )
    )
    return {
        "key": key,
        "file_name": file_name,
    }


def delete_file(key: str):
    """删除 OSS 上的文件。"""
    try:
        client.delete_object(
            oss.DeleteObjectRequest(bucket=settings.OSS_BUCKET, key=key)
        )
        return "already deleted"
    except Exception as e:
        logger.error(e)
        return "something wrong"


def get_temporary_url(key: str, expires = timedelta(hours=10)):
    """获取临时访问 URL。"""
    return client.presign(
        oss.GetObjectRequest(bucket=settings.OSS_BUCKET, key=key),
        expires=expires,
    ).url


def to_access_url(
    value: str | None, expires: timedelta = timedelta(hours=10)
) -> str | None:
    """把库里的值转成可访问的 URL。

    空值、旧的 /uploads/... 本地路径、已存的完整 URL 原样返回(兼容历史数据),
    其余视为 OSS key,现签临时 URL。
    """
    if not value or value.startswith(("http://", "https://", "/")):
        return value
    return get_temporary_url(value, expires)
