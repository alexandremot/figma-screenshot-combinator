import logging
import os
import shutil
import zipfile

# BASE_DIR = raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class UnzipService:
    def __init__(self, uploads_dir=None, temp_dir=None):
        self.uploads_dir = uploads_dir or os.path.join(BASE_DIR, "upload")
        self.temp_dir = temp_dir or os.path.join(BASE_DIR, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.logger = logging.getLogger("unzip_service")

    def unzip_file(self, zip_path):
        base_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(self.temp_dir, base_name)

        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)

        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                parts = member.split('/')
                if parts[0] == base_name:
                    parts = parts[1:]

                if not parts:
                    continue

                target_path = os.path.join(extract_path, *parts)

                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)

        return extract_path
