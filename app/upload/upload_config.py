import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import HTTPBearer

from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.oss.oss_client import get_temporary_url
from app.common.oss.oss_client import upload_file as oss_upload_file

api_bearer = HTTPBearer()

file_router = APIRouter(tags=["文件管理"], dependencies=[Depends(api_bearer)])

max_file_size = 1024 * 1024 * 10  # 10MB

allowed_files = [".jpg", ".png", ".jpeg", ".gif", ".pdf", ".txt", ".word"]


@file_router.post("/upload", summary="上传文件", description="上传文件")
def upload_file(file: UploadFile = File(...)):
    """上传文件到阿里云 OSS。"""
    if not file.filename:
        raise BusinessError(code=400, message="文件名不能为空")

    origin_name = os.path.basename(file.filename)
    ext = Path(origin_name).suffix.lower()

    if ext not in allowed_files:
        raise BusinessError(code=400, message="文件格式不支持")

    if file.size and file.size > max_file_size:
        raise BusinessError(
            code=400, message=f"文件大小超出{file.size // 1024 // 1024}MB"
        )

    result = oss_upload_file(
        prefix="upload", file_name=origin_name, file_content=file
    )
    key = result["key"]
    return success_response(
        data={
            "origin_name": origin_name,
            # 业务表里存 key;bucket 是私有的,签名 URL 会过期,不能入库
            "key": key,
            "size": file.size,
            # 临时访问地址,仅用于前端立即展示
            "url": get_temporary_url(key),
        }
    )
