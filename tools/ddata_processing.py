"""
"""

from tqdm import tqdm

import os
import pandas as pd
import random
import shutil

def create_yolo_dir(class_map, yolo_dir):

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
        f.write(f"names: {[class_map[code] for code in sorted(class_map.keys())]}\n")

    print("Diretórios YOLO criados com sucesso!")

# def images_and_labels_processing(annotations, class_map, dataset_dir, images_dir, yolo_dir):
#     # Obter a lista de imagens na pasta
#     unique_images = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]

#     total_images = int(input("Digite a quantidade total de imagens de cada classe: "))

#     selected_images = {}
#     for class_name in class_map.values():
#         imagens_por_classe = total_images

#         train_images = int(imagens_por_classe * 0.85)
#         val_images = int(imagens_por_classe * 0.10)
#         test_images = int(imagens_por_classe * 0.05)

#         selected_images[class_name] = {
#             'train': random.sample(list(unique_images), train_images),
#             'val': random.sample(list(unique_images), val_images),
#             'test': random.sample(list(unique_images), test_images)
#         }

#     # Processar cada conjunto de dados (train, val, test)
#     for split_name, _ in annotations.items():
#         for class_name, images in selected_images.items():
#             for image in tqdm(images[split_name], desc=f"Gravando imagens para {split_name}"):
                
#                 image_path = os.path.join(images_dir, image)
#                 destination_path = os.path.join(yolo_dir, "images", split_name, image)
#                 shutil.copy(image_path, destination_path)

#             for image in tqdm(images[split_name], desc=f"Convertendo e gravando labels para {split_name}"):
#                 image_name, _ = os.path.splitext(image)
#                 label_path = os.path.join(yolo_dir, "labels", split_name, image_name + ".txt")
#                 if not os.path.exists(label_path):
#                     with open(label_path, "w") as f:
#                         f.write("conteudo do arquivo de label\n")
#                 with open(label_path, "r") as f:
#                     lines = f.readlines()

#                 output_label_path = os.path.join(yolo_dir, "labels", split_name, image_name + ".txt")
#                 with open(output_label_path, "w") as f:
#                     for line in lines:
#                         class_id, x, y, w, h = line.strip().split()
#                         class_id = list(class_map.keys())[list(class_map.values()).index(class_name)]
#                         f.write(f"{class_id} {x} {y} {w} {h}\n")

def images_and_labels_processing(annotations, class_map, images_dir, yolo_dir):
    """
    Processa as imagens e labels do Open Images Dataset para o formato YOLO.

    Parâmetros:
    - annotations: Dicionário contendo caminhos para os arquivos CSV de anotações (train, val, test).
    - class_map: Dicionário que mapeia IDs das classes para nomes das classes.
    - images_dir: Caminho para o diretório de imagens original.
    - yolo_dir: Caminho para o diretório de saída do dataset formatado para YOLO.
    """

    # Lê os arquivos CSV e armazena os DataFrames
    dataframes = {}
    for split, csv_path in annotations.items():
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Erro: Arquivo CSV não encontrado: {csv_path}")
        dataframes[split] = pd.read_csv(csv_path)

    # Verifica se todas as colunas essenciais existem em cada DataFrame
    required_columns = {"ImageID", "LabelName", "XMin", "XMax", "YMin", "YMax"}
    for split, df in dataframes.items():
        if not required_columns.issubset(set(df.columns)):
            raise KeyError(f"O DataFrame '{split}' não contém todas as colunas esperadas: {required_columns}")

        # Remove espaços extras nos nomes das colunas (caso existam)
        df.columns = df.columns.str.strip()

    # Solicita ao usuário o número total de imagens por classe
    total_images_per_class = int(input("Digite a quantidade total de imagens de cada classe: "))

    # Divide a quantidade total de imagens em treino (85%), validação (10%) e teste (5%)
    train_size = int(total_images_per_class * 0.85)
    val_size = int(total_images_per_class * 0.10)
    test_size = total_images_per_class - train_size - val_size

    # Armazena imagens selecionadas para cada conjunto (train, val, test)
    selected_images = {"train": set(), "val": set(), "test": set()}

    for class_id, class_name in class_map.items():
        # Filtra imagens únicas para a classe nos 3 datasets
        unique_images = set()
        for split in ["train", "val", "test"]:
            unique_images.update(dataframes[split][dataframes[split]["LabelName"] == class_id]["ImageID"].unique())

        unique_images = list(unique_images)
        random.shuffle(unique_images)

        # Verifica se há imagens suficientes
        if len(unique_images) < total_images_per_class:
            print(f"Atenção: Apenas {len(unique_images)} imagens disponíveis para a classe '{class_name}'!")

        # Distribui as imagens entre train, val e test
        selected_images["train"].update(unique_images[:train_size])
        selected_images["val"].update(unique_images[train_size:train_size + val_size])
        selected_images["test"].update(unique_images[train_size + val_size:total_images_per_class])

    # Função para copiar imagens e converter labels
    def process_split(split_name):
        print(f"Processando {split_name}...")

        # Diretórios para salvar imagens e labels
        images_output_dir = os.path.join(yolo_dir, "images", split_name)
        labels_output_dir = os.path.join(yolo_dir, "labels", split_name)
        os.makedirs(images_output_dir, exist_ok=True)
        os.makedirs(labels_output_dir, exist_ok=True)

        # Filtra anotações apenas para as imagens selecionadas neste split
        split_annotations = dataframes[split_name][dataframes[split_name]["ImageID"].isin(selected_images[split_name])]

        # Processa cada imagem e suas labels
        for image_id in tqdm(selected_images[split_name]):
            # Caminhos da imagem original e de destino
            image_filename = f"{image_id}.jpg"
            image_source_path = os.path.join(images_dir, image_filename)
            image_dest_path = os.path.join(images_output_dir, image_filename)

            # Copia a imagem apenas se existir
            if os.path.exists(image_source_path):
                shutil.copy(image_source_path, image_dest_path)

                # Cria o arquivo de label correspondente
                label_output_path = os.path.join(labels_output_dir, f"{image_id}.txt")
                with open(label_output_path, "w") as label_file:
                    # Obtém as anotações da imagem atual
                    image_annotations = split_annotations[split_annotations["ImageID"] == image_id]

                    for _, row in image_annotations.iterrows():
                        class_id = list(class_map.keys()).index(row["LabelName"])  # Obtém índice da classe
                        x_center = (row["XMin"] + row["XMax"]) / 2
                        y_center = (row["YMin"] + row["YMax"]) / 2
                        width = row["XMax"] - row["XMin"]
                        height = row["YMax"] - row["YMin"]

                        # Formato YOLO: class_id x_center y_center width height
                        label_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

    # Processa cada divisão de dados (train, val, test)
    for split in ["train", "val", "test"]:
        process_split(split)

    print("\n✅ Dataset convertido para o formato YOLO com sucesso!")
