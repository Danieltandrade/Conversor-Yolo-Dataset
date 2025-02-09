
from tqdm import tqdm

import os
import pandas as pd
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

def images_and_labels_processing(annotations, class_map, images_dir, yolo_dir):

    def convert_to_yolo_format(classe, image_name, labels_used_df):
        row = labels_used_df[labels_used_df["ImageID"] == image_name[0]].iloc[0]
        class_id = classe
        x_center = (row["XMin"] + row["XMax"]) / 2
        y_center = (row["YMin"] + row["YMax"]) / 2
        width = row["XMax"] - row["XMin"]
        height = row["YMax"] - row["YMin"]

        return f"{class_id} {x_center} {y_center} {width} {height}"
    
    total_images = int(input("Digite a quantidade total de imagens de cada classe: "))

    images_by_folder = {
        "train": int(total_images * 0.85),
        "val": int(total_images * 0.10),
        "test": int(total_images * 0.05)
    }

    for classe in class_map:
        print(f"Processando imagens e labels de {classe}...")
        # Percorre os arquivos CSV para cada pasta
        for i in annotations.keys():
            df = pd.read_csv(annotations[i])
            labels_used_df = df[df["LabelName"] == class_map[classe]]

            for image in tqdm(labels_used_df["ImageID"].sample(images_by_folder[i]), desc=f"Gravando imagens para {i}"):
                image_path = os.path.join(images_dir, image + ".jpg")
                destination_path = os.path.join(yolo_dir, "images", i, image + ".jpg")
                shutil.copy(image_path, destination_path)

                # Cria o arquivo de label
                image_name= os.path.splitext(image)
                label_path = os.path.join(yolo_dir, "labels", i, image_name[0] + ".txt")
                with open(label_path, "w") as f:
                    labels = convert_to_yolo_format(classe, image_name, labels_used_df)
                    f.write(labels + "\n")
