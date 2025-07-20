# blueprints/main.py
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from domain.services import ItemService
from adapters.assembly import Container

main = APIRouter()

@main.get('/items')
@inject
def read_items(
    service: ItemService = Depends(Provide[Container.item_service])
):
    return service.get_all_items()
