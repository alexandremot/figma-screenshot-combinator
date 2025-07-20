# blueprints/main.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from dependency_injector.wiring import inject, Provide
from domain.services import ItemService, FileService
from adapters.assembly import Container
from adapters.file_storage import LocalFileStorage
from adapters.unzip_service import UnzipService

main = APIRouter()


@main.get('/items')
@inject
def read_items(
    service: ItemService = Depends(Provide[Container.item_service])
):
    return service.get_all_items()


@main.get('/')
def read_root():
    return {'message': 'Hello World'}


@main.post("/upload-zip")
@inject
async def upload_zip(
    file: UploadFile = File(...),
    file_service: FileService = Depends(Provide[Container.file_service]),
    unzip_service: UnzipService = Depends(Provide[Container.unzip_service])
):
    contents = await file.read()
    try:
        saved_path = file_service.save_zip(file.filename, contents)
        extract_path = unzip_service.unzip_file(saved_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"saved_path": saved_path, "extract_path": extract_path}
