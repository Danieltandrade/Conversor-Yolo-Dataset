"""
Arquivo main.py contendo o script principal.

Modulos:

- io: Módulo de entrada e saída de dados.
- data_processing: Módulo de processamento de dados.

Executa o script principal para obter o dataset reorganizado.
"""

from tools import io
from tools import data_processing

if __name__ == "__main__":

    print("Siga os passos abaixo para obter o dataset reorganizado!")

    dataset_dir = input("Digite o caminho do dataset OIDV7: ")

    class_map = io.class_mapping(dataset_dir)

    annotations, images_dir, yolo_dir = io.output_paths(class_map, dataset_dir)

    data_processing.images_and_labels_processing(annotations, class_map, images_dir, yolo_dir)

    print("Dataset reorganizado com sucesso!")
