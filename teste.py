
from tools import data_processing
from tools import io

if __name__ == "__main__":

    print("Bem-vindo ao reorganizador de dataset para YOLO!")
    print("Por favor, siga os passos abaixo para obter o dataset reorganizado!")

    dataset_dir = input("Digite o caminho do dataset OIDV7: ")

    class_map = io.class_mapping(dataset_dir)

    dataset_dir, images_dir, yolo_dir, annotations = io.output_paths(class_map, dataset_dir)

    data_processing.data_processing(class_map, yolo_dir)

    data_processing.images_and_labels_processing(annotations, class_map, dataset_dir, images_dir, yolo_dir)

    print("Dataset reorganizado com sucesso!")