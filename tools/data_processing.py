"""
Arquivo data_processing.py contendo funções para processamento de dados.

Modulos:
- process_data
"""

import os
import shutil
import random

def process_data(images_dir, labels_dir, train_count, val_count, classes, 
                 yolo_dataset_dir, train_images_dir, val_images_dir, train_labels_dir, val_labels_dir
                 ):
    """
    Função para processamento de dados.

    Args:
        images_dir (str): Caminho para a pasta de imagens.
        labels_dir (str): Caminho para a pasta de rótulos.
        train_count (int): Quantidade de imagens para treino.
        val_count (int): Quantidade de imagens para validação.
        classes (list): Lista de nomes das classes.
        output_dir (str): Caminho para a pasta de saída.
        train_images_dir (str): Caminho para a pasta de imagens de treino.
        val_images_dir (str): Caminho para a pasta de imagens de validação.
        train_labels_dir (str): Caminho para a pasta de rótulos de treino.
        val_labels_dir (str): Caminho para a pasta de rótulos de validação.

    Returns:
        None
    """

    # Dicionário de mapeamento de classes
    class_map = {class_name: i for i, class_name in enumerate(classes)}

    # Função para processar uma classe específica
    def process_class_and_fix_labels(class_name):
        """
        Função para processar uma classe especifica.

        Args:
            class_name (str): Nome da classe.

        Returns:
            None
        """
        # Listar arquivos da classe nos rótulos
        all_labels = [f for f in os.listdir(labels_dir) if f.endswith(".txt")]

        # Filtrar arquivos que pertencem à classe
        class_files = []
        for label_file in all_labels:
            label_path = os.path.join(labels_dir, label_file)
            with open(label_path, "r") as f:
                content = f.read()
                if content.startswith(class_name):  # Verificar se a classe está no início
                    class_files.append(label_file)

        # Embaralhar os arquivos
        random.shuffle(class_files)

        # Dividir entre treino e validação
        train_files = class_files[:train_count]
        val_files = class_files[train_count:train_count + val_count]

        # Função para copiar e corrigir rótulos
        def copy_and_fix(file, dest_images_dir, dest_labels_dir):
            # Copiar imagem correspondente
            image_file = file.replace(".txt", ".jpg")
            shutil.copy(os.path.join(images_dir, image_file), dest_images_dir)
            # Corrigir e copiar rótulo correspondente
            label_path = os.path.join(labels_dir, file)
            with open(label_path, "r") as f:
                lines = f.readlines()
            with open(os.path.join(dest_labels_dir, file), "w") as f:
                for line in lines:
                    f.write(line.replace(class_name, str(class_map[class_name])))

        # Copiar e corrigir rótulos para treino e validação
        for file in train_files:
            copy_and_fix(file, train_images_dir, train_labels_dir)
        for file in val_files:
            copy_and_fix(file, val_images_dir, val_labels_dir)

    # Processar cada classe
    for class_name in classes:
        process_class_and_fix_labels(class_name)

    # Criar arquivo data.yaml
    yaml_content = f"""
        train: {os.path.join(yolo_dataset_dir, 'dataset/images/train')}
        val: {os.path.join(yolo_dataset_dir, 'dataset/images/val')}
        nc: {len(classes)}
        names: {list(range(len(classes)))}
        """
    with open(os.path.join(yolo_dataset_dir, "data.yaml"), "w") as f:
        f.write(yaml_content)

    print("Processamento concluido com sucesso!")
