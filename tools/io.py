"""
Módulo de entrada e saída de dados

Modulos:

- class_mapping: Função para mapear as classes do Open Images Dataset para YOLO
- output_paths: Função para criar a estrutura de pastas do dataset YOLO
"""

import os
import pandas as pd

def class_mapping(dataset_dir, num_class):
    """
    Função para mapear as classes do Open Images Dataset para YOLO
    
    Args:
        dataset_dir (str): Caminho do dataset

    Returns:
        class_map (dict): Mapeamento das classes
    """
    path_class = os.path.join(dataset_dir, "class_names.csv")

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

def output_paths(add_test, class_map, dataset_dir):
    """
    Função para criar a estrutura de pastas do dataset YOLO

    Args:
        add_test (bool): Adicionar pasta de teste
        class_map (dict): Mapeamento das classes
        dataset_dir (str): Caminho do dataset

    Returns:
        annotations (dict): Arquivos CSV
        images_dir (str): Diretório das imagens
        yolo_dir (str): Diretório do dataset YOLO
    """

    output_dir = input("Digite o caminho da pasta de saída: ")

    # Diretórios do dataset
    images_dir = os.path.join(dataset_dir, "dataset", "images")
    yolo_dir = os.path.join(output_dir, "yolo_dataset")

    # Arquivos CSV
    if add_test:
        annotations = {
            "train": os.path.join(dataset_dir,"oidv6-train.csv"),
            "val": os.path.join(dataset_dir,"oidv7-validation.csv"),
            "test": os.path.join(dataset_dir,"oidv7-test.csv")
        }
    else:
        annotations = {
            "train": os.path.join(dataset_dir,"oidv6-train.csv"),
            "val": os.path.join(dataset_dir,"oidv7-validation.csv")
        }

    # Criar estrutura de diretórios YOLO
    for split in ["train", "val", "test"] if add_test else ["train", "val"]:
        os.makedirs(os.path.join(yolo_dir, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(yolo_dir, split, "labels"), exist_ok=True)
    
    # Cria o arquivo de configuração data.yaml
    with open(os.path.join(yolo_dir, "data.yaml"), "w") as f:
        f.write(f"train: {os.path.join(yolo_dir, 'images', 'train')}\n")
        f.write(f"val: {os.path.join(yolo_dir, 'images', 'val')}\n")
        f.write(f"test: {os.path.join(yolo_dir, 'images', 'test')}\n") if add_test else None
        f.write(f"nc: {len(class_map)}\n")
        f.write(f"names: {[code for code in sorted(class_map.keys())]}\n")

    return annotations, images_dir, yolo_dir
