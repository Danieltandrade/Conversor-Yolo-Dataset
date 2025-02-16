"""
Arquivo main.py contendo o script principal.

Modulos:

- io: Módulo de entrada e saída de dados.
- data_processing: Módulo de processamento de dados.

Executa o script principal para obter o dataset reorganizado.
"""

from tools import output_paths
from tools import class_mapping
from tools import images_and_labels_processing

import os
import sys

def main():
    """
    Função principal do script.

    Executa o script principal para obter o dataset reorganizado.
    """
    try:
        # Obter o caminho do dataset OIDV7
        dataset_dir = input("Digite o caminho do dataset OIDV7: ")

        # Modificar "add_test = True" ou adicionar a linha comentada abaixo para adicionar a pasta de teste
        # add_test = input("Deseja adicionar a pasta de teste? (S/N): ").lower() == "s"
        add_test = False

        # Verificar se o caminho do dataset é válido
        if not os.path.exists(dataset_dir):
            print("Erro: O caminho do dataset não é válido.")
            sys.exit(1)

        # Obter o número de classes
        num_class = int(input("Digite o número de classes: "))

        # Verificar se o número de classes é válido
        if num_class <= 1:
            print("Erro: O número de classes deve ser maior que zero.")
            sys.exit(1)

        # Obter o mapeamento de classes
        class_map = class_mapping(dataset_dir, num_class)

        # Obter as saídas do dataset YOLO
        annotations, images_dir, yolo_dir = output_paths(add_test=False, class_map=class_map, dataset_dir=dataset_dir)

        # Processar as imagens e labels
        images_and_labels_processing(add_test, annotations=annotations, class_map=class_map, images_dir=images_dir, yolo_dir=yolo_dir)

        print("Dataset reorganizado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()