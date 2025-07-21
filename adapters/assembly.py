from dependency_injector import containers, providers
from domain.services import FileService, ItemServiceImpl, ImageComparisonService
from adapters.db_repo import InMemoryItemRepository
from adapters.file_storage import LocalFileStorage
from adapters.unzip_service import UnzipService
from adapters.image_sorter import ImageComparisonAdapter

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["blueprints.main"])
    
    # Repositórios
    item_repository = providers.Singleton(InMemoryItemRepository)
    
    # Serviços
    item_service = providers.Factory(
        ItemServiceImpl,
        item_repository=item_repository
    )
    
    # Armazenamento de arquivos
    file_storage = providers.Singleton(
        LocalFileStorage,
        base_dir="uploads"
    )
    file_service = providers.Factory(
        FileService,
        storage=file_storage
    )
    
    # Serviços de processamento
    unzip_service = providers.Factory(UnzipService)
    image_comparison_adapter = providers.Singleton(ImageComparisonAdapter)
    image_comparison_service = providers.Factory(
        ImageComparisonService,
        comparison_port=image_comparison_adapter
    )
