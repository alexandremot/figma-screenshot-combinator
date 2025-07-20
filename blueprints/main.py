# blueprints/main.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from dependency_injector.wiring import inject, Provide
from domain.services import ItemService
from adapters.assembly import Container
from adapters.file_storage import LocalFileStorage
from domain.services import FileService

main = APIRouter()
storage = LocalFileStorage()
file_service = FileService(storage)


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
async def upload_zip(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        saved_path = file_service.save_zip(file.filename, contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"saved_path": saved_path}
