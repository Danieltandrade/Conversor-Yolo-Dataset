"""
Arquivo utils.py contendo funções auxiliares para verificação da existencia de pastas e arquivos.

Modulos:
- validate_input_params
"""

import os

def validate_input_params(images_dir, labels_dir, yolo_dataset_dir):
    """
    Função para verificação da existência de pastas e arquivos.

    Args:
        images_dir (str): Caminho para a pasta de imagens.
        labels_dir (str): Caminho para a pasta de labels.
        output_dir (str): Caminho para a pasta de saída.

    Returns:
        bool: True se as pastas e arquivos existirem, False caso contrário.
    """

    if not os.path.exists(images_dir):
        raise ValueError(f'A pasta de imagens "{images_dir}" não encontrada!')
    if not os.path.exists(labels_dir):
        raise ValueError(f'A pasta de labels "{labels_dir}" não encontrada!')
    if not os.path.exists(yolo_dataset_dir):
        os.makedirs(yolo_dataset_dir)

    return True
