import uuid
from fastapi import APIRouter, Depends, File, UploadFile
import os

from fastapi.security import HTTPBearer
from app.common.base_response import success_response
from app.common.business_error import BusinessError
from pathlib import Path
from datetime import datetime
from app.config import UPLOAD_DIR

api_bearer=HTTPBearer()

file_router = APIRouter(tags=["文件管理"],dependencies=[Depends(api_bearer)])

max_file_size = 1024 * 1024 * 10  # 10MB

allowed_files = [".jpg", ".png", ".jpeg", ".gif", ".pdf", ".txt", ".word"]


@file_router.post("/upload",summary="上传文件",description="上传文件")
def upload_file(file: UploadFile = File(...)):
    """上传文件"""
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

    disk_name = (
        f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{uuid.uuid4().hex[:8]}{ext}"
    )

    disk_path = UPLOAD_DIR

    if not disk_path.exists():
        os.mkdir(disk_path)

    with open(disk_path / disk_name, "wb") as f:
        f.write(file.file.read())

    return success_response(
        data={
            "origin_name": origin_name,
            "disk_name": disk_name,
            "size": file.size,
            "url": f"/uploads/{disk_name}",
        }
    )
