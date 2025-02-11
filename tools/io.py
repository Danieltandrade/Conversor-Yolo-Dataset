"""
Módulo de entrada e saída de dados

Modulos:

- class_mapping: Função para mapear as classes do Open Images Dataset para YOLO
- output_paths: Função para criar a estrutura de pastas do dataset YOLO
"""

import os
import pandas as pd

# Mapeamento das classes Open Images → YOLO
def class_mapping(dataset_dir):
    """
    Função para mapear as classes do Open Images Dataset para YOLO
    
    Args:
        dataset_dir (str): Caminho do dataset

    Returns:
        dict: Mapeamento das classes
    """
    path_class = os.path.join(dataset_dir, "class_names.csv")
    num_class = int(input("Digite o numero de classes: "))

    classes = []
    class_map = {}

    for i in range(num_class):
        class_name = input(f"Digite o nome da classe {i}: ")
        classes.append(class_name)

    df = pd.read_csv(path_class)
    for class_name in classes:
        row = df[df.iloc[:, 1] == class_name].iloc[0]
        class_code = row.iloc[0]
        class_map[class_code] = class_name

    return {v: k for k, v in class_map.items()}

def output_paths(class_map, dataset_dir):
    """
    Função para criar a estrutura de pastas do dataset YOLO

    Args:
        class_map (dict): Mapeamento das classes
        dataset_dir (str): Caminho do dataset

    Returns:
        dict: Arquivos CSV
        str: Diretórios de pastas de imagens e pastas de labels
    """

    output_dir = input("Digite o caminho da pasta de saída: ")
    # Diretórios do dataset
    images_dir = os.path.join(dataset_dir, "dataset", "images")
    yolo_dir = os.path.join(output_dir, "yolo_dataset")

    # Arquivos CSV
    annotations = {
        "train": os.path.join(dataset_dir,"oidv6-train.csv"),
        "val": os.path.join(dataset_dir,"oidv7-validation.csv"),
        "test": os.path.join(dataset_dir,"oidv7-test.csv"),
    }

    # Criar estrutura de diretórios YOLO
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(yolo_dir, "images", split), exist_ok=True)
        os.makedirs(os.path.join(yolo_dir, "labels", split), exist_ok=True)
    
    # Cria o arquivo de configuração data.yaml
    with open(os.path.join(yolo_dir, "data.yaml"), "w") as f:
        f.write(f"train: {os.path.join(yolo_dir, 'images', 'train')}\n")
        f.write(f"val: {os.path.join(yolo_dir, 'images', 'val')}\n")
        f.write(f"test: {os.path.join(yolo_dir, 'images', 'test')}\n")
        f.write(f"nc: {len(class_map)}\n")
        f.write(f"names: {[code for code in sorted(class_map.keys())]}\n")

    return annotations, images_dir, yolo_dir
