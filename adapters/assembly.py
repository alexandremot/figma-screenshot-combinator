from dependency_injector import containers, providers
from domain.services import FileService, ItemServiceImpl
from adapters.db_repo import InMemoryItemRepository
from adapters.file_storage import LocalFileStorage
from adapters.unzip_service import UnzipService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["blueprints.main"])
    item_repository = providers.Singleton(InMemoryItemRepository)
    item_service = providers.Factory(ItemServiceImpl, item_repository=item_repository)
    file_storage = providers.Singleton(LocalFileStorage, base_dir="uploads")
    file_service = providers.Factory(FileService, storage=file_storage)
    unzip_service = providers.Factory(UnzipService)
