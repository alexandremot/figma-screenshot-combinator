# adapters/assembly.py
from dependency_injector import containers, providers
from domain.services import ItemServiceImpl
from adapters.db_repo import InMemoryItemRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["blueprints.main"])
    item_repository = providers.Singleton(InMemoryItemRepository)
    item_service = providers.Factory(ItemServiceImpl, item_repository=item_repository)
