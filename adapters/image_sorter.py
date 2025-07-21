# adapters/image_comparison_sort.py
from PIL import Image, ImageFilter, ImageOps
from pathlib import Path
from typing import List, Tuple
from scipy.optimize import linear_sum_assignment
import numpy as np
from domain.ports import ImageComparisonPort
from domain.entities import ImagePair, ComparisonResult

class ImageComparisonAdapter(ImageComparisonPort):
    def __init__(self):
        # Configurações para preprocessamento
        self.tamanho_alvo = (64, 64)  # Aumentado para capturar mais detalhes
        self.limiar_binarizacao = 128
        self.kernel_blur = (2, 2)  # Ajustado para melhor redução de ruído
        self.debug = False
        self.temp_dir = Path("temp")

    def carregar_imagens(self, diretorio: Path) -> List[Tuple[str, Image.Image]]:
        """Carrega todas as imagens de um diretório e retorna uma lista de tuplas
        contendo o caminho e a imagem."""
        arquivos = list(diretorio.glob("*.png")) + list(diretorio.glob("*.jpg"))
        return [(str(arquivo), Image.open(arquivo)) for arquivo in arquivos]

    def preprocessar(self, imagem: Image.Image) -> Image.Image:
        """Aplica várias técnicas de preprocessamento para melhorar a comparação."""
        if self.debug:
            imagem.save('debug_original.png')
        # Converte para escala de cinza
        img = imagem.convert('L')
        if self.debug:
            img.save('debug_cinza.png')
        # Aplica equalização de histograma para melhorar contraste
        img = Image.fromarray(np.array(img))
        img = ImageOps.equalize(img)
        if self.debug:
            img.save('debug_equalizado.png')
        # Aplica blur gaussiano suave
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        if self.debug:
            img.save('debug_blur.png')
        # Redimensiona mantendo proporção
        img = img.resize(self.tamanho_alvo, Image.Resampling.LANCZOS)
        if self.debug:
            img.save('debug_redimensionado.png')
        return img

    def calcular_ssim(self, img1_array: np.ndarray, img2_array: np.ndarray) -> float:
        """Calcula o Structural Similarity Index (SSIM) entre duas imagens."""
        # Garante que os arrays sejam do tipo float
        img1_array = img1_array.astype(np.float64)
        img2_array = img2_array.astype(np.float64)
        
        mu1 = np.mean(img1_array)
        mu2 = np.mean(img2_array)
        sigma1 = np.std(img1_array)
        sigma2 = np.std(img2_array)
        sigma12 = np.mean((img1_array - mu1) * (img2_array - mu2))
        k1, k2 = 0.01, 0.03
        L = 255.0  # Usando float em vez de int
        c1 = (k1 * L)**2
        c2 = (k2 * L)**2
        return ((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)) / \
               ((mu1**2 + mu2**2 + c1) * (sigma1**2 + sigma2**2 + c2))

    def calcular_diferenca(self, img1: Image.Image, img2: Image.Image) -> float:
        """Calcula a diferença média entre duas imagens usando múltiplas métricas."""
        # Converte imagens para arrays numpy
        img1_array = np.array(img1)
        img2_array = np.array(img2)
        
        # Calcula diferença de histograma
        hist1 = np.array(img1.histogram())
        hist2 = np.array(img2.histogram())
        diff_hist = np.sum(np.abs(hist1 - hist2)) / (hist1.size * 255.0)
        
        # Calcula diferença estrutural (SSIM)
        ssim = self.calcular_ssim(img1_array, img2_array)
        
        # Combina as métricas com pesos ajustados
        return 0.2 * diff_hist + 0.8 * (1 - ssim)  # Maior peso para SSIM

    def compare_images(self, figma_dir: Path = None, screenshots_dir: Path = None) -> ComparisonResult:
        """Encontra os pares correspondentes entre imagens do Figma e screenshots.
        
        Se os diretórios não forem especificados, usa os diretórios padrão em temp/figma e temp/screenshots.
        """
        # Usa diretórios padrão se não forem especificados
        if figma_dir is None:
            figma_dir = self.temp_dir / "figma"
        if screenshots_dir is None:
            screenshots_dir = self.temp_dir / "screenshots"
        
        # Verifica se os diretórios existem
        if not figma_dir.exists():
            raise FileNotFoundError(f"Diretório de figma não encontrado: {figma_dir}")
        if not screenshots_dir.exists():
            raise FileNotFoundError(f"Diretório de screenshots não encontrado: {screenshots_dir}")
        
        # Carrega e preprocessa as imagens
        figma_list = [(nome, self.preprocessar(img)) for nome, img in self.carregar_imagens(figma_dir)]
        screenshots_list = [(nome, self.preprocessar(img)) for nome, img in self.carregar_imagens(screenshots_dir)]
        
        # Cria matriz de similaridade
        n_figmas = len(figma_list)
        n_screenshots = len(screenshots_list)
        matriz_similaridade = np.zeros((n_figmas, n_screenshots))
        
        # Calcula similaridades e mostra valores de debug
        for i, (_, img1) in enumerate(figma_list):
            for j, (_, img2) in enumerate(screenshots_list):
                diff = self.calcular_diferenca(img1, img2)
                matriz_similaridade[i][j] = diff
                if self.debug:
                    print(f"Comparação: {figma_list[i][0]} vs {screenshots_list[j][0]} - Diferença: {diff:.4f}")
        
        # Aplica algoritmo húngaro
        row_ind, col_ind = linear_sum_assignment(matriz_similaridade)
        
        # Monta os pares finais
        pairs = [
            ImagePair(
                figma_list[i][0],
                screenshots_list[j][0],
                matriz_similaridade[i][j]
            )
            for i, j in zip(row_ind, col_ind)
        ]
        
        return ComparisonResult(pairs, len(pairs))
    