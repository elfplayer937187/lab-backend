from fastapi import APIRouter, File, UploadFile

from app.common.oss.oss_client import delete_file, get_temporary_url, upload_file

test_router = APIRouter(prefix="/test", tags=["测试"])


@test_router.post("/")
def test(file: UploadFile = File(...)):
    return upload_file(prefix="test", file_name=f"{file.filename}", file_content=file)


@test_router.delete("/delete")
def delete(key: str):
    return delete_file(key)


@test_router.get("/eee")
def presign(key: str):
    return get_temporary_url(key)
