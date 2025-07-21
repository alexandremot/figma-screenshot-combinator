from pathlib import Path
import uuid
from typing import List, Tuple
import json
import namesgenerator


class GroupPairs:
    def __init__(self, base_dir: Path):
        """Inicializa o gerenciador de pares de imagens."""
        self.base_dir = base_dir
        self.grouped_pairs_dir = base_dir / "grouped_pairs"
        self.grouped_pairs_dir.mkdir(exist_ok=True)
        self.organization_data = {"pairs": []}  # Inicializa organization_data aqui

    def group_pairs(self, pairs: List[Tuple[str, str]]) -> List[str]:
        """Agrupa os pares de imagens em diretórios com UUIDs."""
        grouped_pairs = []
        self.organization_data["pairs"] = []  # Limpa os dados anteriores
        
        for figma_path, screenshot_path in pairs:
            # Cria um nome único para este par
            pair_name = namesgenerator.get_random_name()
            pair_dir = self.grouped_pairs_dir / pair_name
            pair_dir.mkdir()
            
            # Copia as imagens para o diretório do par
            figma_path = Path(figma_path)
            screenshot_path = Path(screenshot_path)
            
            # Obtém os nomes dos arquivos sem o diretório
            figma_filename = figma_path.name
            screenshot_filename = screenshot_path.name
            
            # Copia os arquivos
            (pair_dir / figma_filename).write_bytes(figma_path.read_bytes())
            (pair_dir / screenshot_filename).write_bytes(screenshot_path.read_bytes())
            
            # Adiciona ao registro de organização
            self.organization_data["pairs"].append({
                "name": pair_name,
                "files": [
                    figma_filename,
                    screenshot_filename
                ]
            })
            
            grouped_pairs.append(str(pair_dir))
        
        # Imprime o JSON formatado em tela
        print(json.dumps(self.organization_data, indent=2, ensure_ascii=False))
        
        return grouped_pairs
