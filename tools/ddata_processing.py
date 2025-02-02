"""
"""

import os
import pandas as pd
import random
import shutil

# Mapeamento das classes Open Images → YOLO
def class_mapping(dataset_dir):

    path_class = os.path.join(dataset_dir, "class_names.csv")
    num_class = int(input("Digite o numero de classes: "))

    classes = []
    class_map = {}

    for i in range(num_class):
        class_name = input(f"Digite o nome da classe {i}: ")
        classes.append(class_name)
        i += i

    df = pd.read_csv(path_class)
    for class_name in classes:
        row = df[df.iloc[:, 1] == class_name].iloc[0]
        class_code = row.iloc[0]
        class_map[class_code] = class_name

    return class_map

def data_processing(annotations, class_map, images_dir, yolo_dir):

    def convert_annotations(csv_file, split, image_ids, class_map=class_map, images_dir=images_dir, yolo_dir=yolo_dir):
        """Converte anotações do Open Images V7 para o formato YOLO"""
        df = pd.read_csv(csv_file)
        df = df[df["LabelName"].isin(class_map.keys())]  # Filtra apenas Bus e Truck
        df = df[df["ImageID"].isin(image_ids)]  # Seleciona apenas as imagens escolhidas
    
        for _, row in df.iterrows():
            image_id = row["ImageID"]
            label = class_map[row["LabelName"]]
            for i in range(len(class_map)):
                if label == list(class_map.values())[i]:
                    num_label = i
                    break
            
            # Coordenadas normalizadas
            x_center = (row["XMin"] + row["XMax"]) / 2
            y_center = (row["YMin"] + row["YMax"]) / 2
            width = row["XMax"] - row["XMin"]
            height = row["YMax"] - row["YMin"]

            # Criar arquivo de rótulo YOLO
            label_path = os.path.join(yolo_dir, "labels", split, f"{image_id}.txt")
            with open(label_path, "a") as f:
                f.write(f"{num_label} {x_center} {y_center} {width} {height}\n")

            # Copiar imagem para o diretório YOLO
            src_image_path = os.path.join(images_dir, f"{image_id}.jpg")
            dst_image_path = os.path.join(yolo_dir, "images", split, f"{image_id}.jpg")
            if os.path.exists(src_image_path):  
                shutil.copy(src_image_path, dst_image_path)

    # Solicita ao usuário a quantidade total de imagens
    total_images = int(input("Digite a quantidade total de imagens para o dataset(train + val + test): "))

    # Definição das quantidades para cada conjunto
    num_train = int(total_images * 0.80)
    num_val = int(total_images * 0.10)
    num_test = int(total_images * 0.10)

    print("Processando informações...\nPode demorar alguns minutos, por favor, aguarde...")

    # Seleciona imagens aleatoriamente de cada CSV
    selected_images = {}
    for split, csv_file in annotations.items():
        df = pd.read_csv(csv_file)
        df = df[df["LabelName"].isin(class_map.keys())]  # Filtra apenas Bus e Truck
        unique_images = df["ImageID"].unique()

        num_samples = {"train": num_train, "val": num_val, "test": num_test}[split]
        selected_images[split] = random.sample(list(unique_images), min(num_samples, len(unique_images)))

    # Processar cada conjunto de dados (train, val, test)
    for split, csv_file in annotations.items():
        convert_annotations(csv_file, split, selected_images[split])

    print("Conversão concluída!")