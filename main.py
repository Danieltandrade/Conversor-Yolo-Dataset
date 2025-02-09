"""
"""

from tools import io
from tools import data_processing

if __name__ == "__main__":

    print("Por favor, siga os passos abaixo para obter o dataset reorganizado!")

    dataset_dir = input("Digite o caminho do dataset OIDV7: ")

    class_map = io.class_mapping(dataset_dir)

    images_dir, yolo_dir, annotations = io.output_paths(class_map, dataset_dir)

    data_processing.images_and_labels_processing(annotations, class_map, images_dir, yolo_dir)

    print("Dataset reorganizado com sucesso!")
