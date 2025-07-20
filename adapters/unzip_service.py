import os
import zipfile
import logging

# BASE_DIR = raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class UnzipService:
    def __init__(self, uploads_dir=None, temp_dir=None):
        self.uploads_dir = uploads_dir or os.path.join(BASE_DIR, "upload")
        self.temp_dir = temp_dir or os.path.join(BASE_DIR, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.logger = logging.getLogger("unzip_service")


    def unzip_file(self, zip_path):
        extract_path = os.path.join(
            self.temp_dir, os.path.splitext(os.path.basename(zip_path))[0]
        )
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                # Ignora diretórios
                if not member.endswith('/'):
                    # Extrai apenas o nome do arquivo, ignorando subpastas
                    filename = os.path.basename(member)
                    if filename:  # Evita strings vazias
                        dest = os.path.join(extract_path, filename)
                        with zip_ref.open(member) as source, open(dest, "wb") as target:
                            target.write(source.read())
        return extract_path


    # método para descompactar todos os arquivos zip na pasta de uploads
    # (manter aqui para o caso de vir a precisar no futuro)
    def unzip_all(self):
        for filename in os.listdir(self.uploads_dir):
            if filename.endswith(".zip"):
                zip_path = os.path.join(self.uploads_dir, filename)
                self.unzip_file(zip_path)
