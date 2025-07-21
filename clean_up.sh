#!/bin/bash

# Caminhos das pastas
UPLOADS_DIR="uploads"
TEMP_DIR="temp"

# Remove todos os arquivos e subpastas (mas mantém as pastas principais)
find "$UPLOADS_DIR" -mindepth 1 -exec rm -rf {} +
find "$TEMP_DIR" -mindepth 1 -exec rm -rf {} +

echo "Arquivos e subpastas removidos de $UPLOADS_DIR e $TEMP_DIR"
