"""
Arquivo io.py contendo funções para criação de pastas de saída e obtenção de inputs do usuário.

Modulos:
- get_user_input
- create_output_dir

Parâmetros de entrada:
    - images_dir: Caminho para a pasta de imagens
    - labels_dir: Caminho para a pasta de labels
    - output_dir: Caminho para a pasta de saída
    - train_count: Quantidade de imagens para treinamento
    - val_count: Quantidade de imagens para validação
    - classes: Lista de nomes das classes
"""

import os

def get_user_input():
    """
    Função para obtenção de inputs do usuário.

    Args:
        None

    Returns:
        images_dir (str): Caminho para a pasta de imagens.
        labels_dir (str): Caminho para a pasta de rótulos.
        train_count (int): Quantidade de imagens para treino.
        val_count (int): Quantidade de imagens para validação.
        classes (list): Lista de nomes das classes.
    """

    images_dir = input("Digite o caminho para a pasta de imagens: ")
    labels_dir = input("Digite o caminho para a pasta de labels: ")
    train_count = int(input("Digite a quantidade de imagens para treinamento: "))
    val_count = int(input("Digite a quantidade de imagens para validação: "))
    num_classes = int(input("Digite a quantidade de classes: "))
    classes = []

    for i in range(num_classes):
        class_name = input(f"Digite o nome da classe {i+1}: ")
        classes.append(class_name)

    return images_dir, labels_dir, train_count, val_count, classes

def create_output_dir():
    """
    Função para criação de pastas de saída.

    Args:
        None

    Returns:
        output_dir (str): Caminho para a pasta de saída.
        train_images_dir (str): Caminho para a pasta de imagens de treino.
        val_images_dir (str): Caminho para a pasta de imagens de validação.
        train_labels_dir (str): Caminho para a pasta de rótulos de treino.
        val_labels_dir (str): Caminho para a pasta de rótulos de validação.
    """

    output_dir = input("Digite o caminho para a pasta de saída: ")
    yolo_dataset_dir = os.path.join(output_dir, "yolo_dataset")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    else:
        # Criar pastas de saída
        train_images_dir = os.path.join(yolo_dataset_dir, "dataset/images/train")
        val_images_dir = os.path.join(yolo_dataset_dir, "dataset/images/val")
        train_labels_dir = os.path.join(yolo_dataset_dir, "dataset/labels/train")
        val_labels_dir = os.path.join(yolo_dataset_dir, "dataset/labels/val")
        os.makedirs(train_images_dir, exist_ok=True)
        os.makedirs(val_images_dir, exist_ok=True)
        os.makedirs(train_labels_dir, exist_ok=True)
        os.makedirs(val_labels_dir, exist_ok=True)

    return yolo_dataset_dir, train_images_dir, val_images_dir, train_labels_dir, val_labels_dir
