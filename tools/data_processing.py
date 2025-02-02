"""
"""

from tqdm import tqdm

import os
import pandas as pd
import random
import shutil

# Mapeamento das classes Open Images → YOLO
def class_mapping2(dataset_dir):
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

    return class_map

def data_processing(class_map, yolo_dir):

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

def images_and_labels_processing(annotations, class_map, dataset_dir, images_dir, yolo_dir):
    # Obter a lista de imagens na pasta
    unique_images = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]

    selected_images = {}
    for class_name in class_map.values():
        total_images = int(input("Digite a quantidade total de imagens para a(s) classe(s): "))

        train_images = int(total_images * 0.85)
        val_images = int(total_images * 0.10)
        test_images = int(total_images * 0.05)

        selected_images[class_name] = {
            'train': random.sample(list(unique_images), train_images),
            'val': random.sample(list(unique_images), val_images),
            'test': random.sample(list(unique_images), test_images)
        }

    # Processar cada conjunto de dados (train, val, test)
    for split_name, _ in annotations.items():
        for class_name, images in selected_images.items():
            for image in tqdm(images[split_name], desc=f"Gravando imagens para {split_name}"):
                
                image_path = os.path.join(images_dir, image)
                destination_path = os.path.join(yolo_dir, "images", split_name, image)
                shutil.copy(image_path, destination_path)

            for image in tqdm(images[split_name], desc=f"Convertendo e gravando labels para {split_name}"):
                image_name, _ = os.path.splitext(image)
                label_path = os.path.join(yolo_dir, "labels", split_name, image_name + ".txt")
                if not os.path.exists(label_path):
                    with open(label_path, "w") as f:
                        f.write("conteudo do arquivo de label\n")
                with open(label_path, "r") as f:
                    lines = f.readlines()

                output_label_path = os.path.join(yolo_dir, "labels", split_name, image_name + ".txt")
                with open(output_label_path, "w") as f:
                    for line in lines:
                        class_id, x, y, w, h = line.strip().split()
                        class_id = list(class_map.keys())[list(class_map.values()).index(class_name)]
                        f.write(f"{class_id} {x} {y} {w} {h}\n")
