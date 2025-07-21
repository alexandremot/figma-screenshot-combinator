# blueprints/main.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from dependency_injector.wiring import inject, Provide
from domain.services import ItemService, FileService
from adapters.assembly import Container
from adapters.file_storage import LocalFileStorage
from adapters.unzip_service import UnzipService
from adapters.image_sorter import ImageComparisonAdapter
from pathlib import Path 

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
    unzip_service: UnzipService = Depends(Provide[Container.unzip_service]),
    image_comparison_service: ImageComparisonAdapter = Depends(Provide[Container.image_comparison_service])
):
    contents = await file.read()
    try:
        saved_path = file_service.save_zip(file.filename, contents)
        extract_path = unzip_service.unzip_file(saved_path)
        
        # Processa as imagens usando os diretórios padrão
        comparison_result = image_comparison_service.compare_images(
            figma_dir=Path(extract_path) / "figma",
            screenshots_dir=Path(extract_path) / "screenshots"
        )
        
        return {
            "saved_path": str(saved_path),
            "extract_path": str(extract_path),
            "comparison_result": {
                "pairs": [
                    {
                        "figma_path": str(pair.figma_path),
                        "screenshot_path": str(pair.screenshot_path),
                        "similarity_score": pair.similarity_score
                    }
                    for pair in comparison_result.pairs
                ],
                "total_comparisons": comparison_result.total_comparisons
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagens: {str(e)}")
