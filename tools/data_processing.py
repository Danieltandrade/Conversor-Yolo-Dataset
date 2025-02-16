"""
Módulo de processamento de dados

Modulos:

- images_and_labels_processing: Função para processar os arquivos de imagens e labels e copiar 
para as pastas de treinamento e validação.
"""

from tqdm import tqdm

import os
import pandas as pd
import shutil

def images_and_labels_processing(add_test, annotations, class_map, images_dir, yolo_dir):
 
    total_images = int(input("Digite a quantidade total de imagens de cada classe: "))

    # Divide as imagens para treinamento, validação e teste caso "add_test" seja True
    if add_test:
        images_by_folder = {
        "train": int(total_images * 0.85),
        "val": int(total_images * 0.10),
        "test": int(total_images * 0.05)
        }
    else:
        images_by_folder = {
        "train": int(total_images * 0.90),
        "val": int(total_images * 0.10)
        }

    # Percorre as classes obtidas do parâmetro class_map
    for file_path in annotations.keys():
        df = pd.read_csv(annotations[file_path])

        # Seleciona as imagens e labels para cada pasta
        for index in range(len(class_map)):
            processing_df = df[df["LabelName"] == list(class_map.values())[index]].sample(images_by_folder[file_path])
            if index == 0:
                labels_used_df = processing_df.reset_index(drop=True)
            else:
                labels_used_df = pd.concat([labels_used_df, processing_df], ignore_index=True)
                labels_used_df= labels_used_df.reset_index(drop=True)

        # Copia as imagens para as pastas de treinamento, validação e teste
        for image in tqdm(labels_used_df["ImageID"], desc=f"Gravando imagens para {file_path}"):
            image_path = os.path.join(images_dir, image + ".jpg")
            destination_path = os.path.join(yolo_dir, file_path, "images", image + ".jpg")
            shutil.copy(image_path, destination_path)

        # Copia os labels para as pastas de treinamento, validação e teste
        images_path = os.path.join(yolo_dir, file_path, "images")
        images_names = [os.path.splitext(arq)[0] for arq in os.listdir(images_path)]
        for image_name in tqdm(images_names, desc=f"Gravando labels para {file_path}"):
            for index, rows in labels_used_df[labels_used_df["ImageID"] == image_name].iterrows():
                class_id = list(class_map.values()).index(rows["LabelName"])
                x_center = (rows["XMin"] + rows["XMax"]) / 2
                y_center = (rows["YMin"] + rows["YMax"]) / 2
                width = rows["XMax"] - rows["XMin"]
                height = rows["YMax"] - rows["YMin"]

                yoloLabel = f"{class_id} {x_center} {y_center} {width} {height}\n"
                with open(os.path.join(yolo_dir, file_path, "labels", image_name + ".txt"), "a") as f:
                    f.write(yoloLabel)
