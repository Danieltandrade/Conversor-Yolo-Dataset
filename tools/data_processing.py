
from tqdm import tqdm

import os
import pandas as pd
import shutil

def images_and_labels_processing(annotations, class_map, images_dir, yolo_dir):
    """
    Função para processar os arquivos de imagens e labels e copiar para as pastas de treinamento e validação.

    Args:
        annotations (dict): Arquivos CSV
        class_map (dict): Mapeamento das classes
        images_dir (str): Diretório das imagens
        yolo_dir (str): Diretório do dataset YOLO
    
    Returns:
        None
    """
    
    total_images = int(input("Digite a quantidade total de imagens de cada classe: "))

    images_by_folder = {
        "train": int(total_images * 0.85),
        "val": int(total_images * 0.10),
        "test": int(total_images * 0.05)
    }

    # Percorre as classes obtidas do parâmetro class_map
    for classe in class_map:
        print(f"Processando imagens e labels de {classe}...")

        # Percorre os arquivos CSV para cada pasta
        for i in annotations.keys():
            df = pd.read_csv(annotations[i])
            labels_used_df = df[df["LabelName"] == class_map[classe]]

            # Copia as imagens para as pastas de treinamento, validação e teste
            for image in tqdm(labels_used_df["ImageID"].sample(images_by_folder[i]), desc=f"Gravando imagens para {i}"):
                image_path = os.path.join(images_dir, image + ".jpg")
                destination_path = os.path.join(yolo_dir, "images", i, image + ".jpg")
                shutil.copy(image_path, destination_path)

            # Copia os labels para as pastas de treinamento, validação e teste
            images_path = os.path.join(yolo_dir, "images", i)
            images_names = [os.path.splitext(arq)[0] for arq in os.listdir(images_path)]
            for image_name in tqdm(images_names, desc=f"Gravando labels para {i}"):
                for index, rows in labels_used_df[labels_used_df["ImageID"] == image_name].iterrows():
                    class_id = classe
                    x_center = (rows["XMin"] + rows["XMax"]) / 2
                    y_center = (rows["YMin"] + rows["YMax"]) / 2
                    width = rows["XMax"] - rows["XMin"]
                    height = rows["YMax"] - rows["YMin"]

                    yoloLabel = f"{class_id} {x_center} {y_center} {width} {height}\n"
                    with open(os.path.join(yolo_dir, "labels", i, image_name + ".txt"), "a") as f:
                        f.write(yoloLabel)
