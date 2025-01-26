"""
Reorganização do Dataset OIDv7-Toolkit para modelo compatível com YOLO

Este script aceita como entrada os caminhos para as pastas de imagens, labels e a pasta de saída.
Ele reorganiza o dataset, criando pastas de treinamento e validação, e divide os arquivos de 
imagens e labels para cada pasta. Além disso, utiliza as funções da pasta "tools" para processar os 
dados e gerar o arquivo de configuração.

Parâmetros de entrada: 
    - images_dir: Caminho para a pasta de imagens 
    - labels_dir: Caminho para a pasta de labels
    - train_count: Quantidade de imagens para treinamento
    - val_count: Quantidade de imagens para validação
    - classes: Lista de nomes das classes
    - output_dir: Caminho para a pasta de saída

Arquivos de saída:
    - Pastas de treinamento e validação com imagens e labels reorganizados
    - Arquivo data.yaml com os caminhos para as pastas de treinamento e validação e 
    as configurações do dataset

Para executar o script, execute o seguinte comando:
    python main.py
"""

from tools import data_processing
from tools import io
from tools import utils

if __name__ == "__main__":

    print("Bem-vindo ao reorganizador de dataset para YOLO!")
    print("Por favor, siga os passos abaixo para obter o dataset reorganizado!")

    images_dir, labels_dir, train_count, val_count, classes = io.get_user_input()
    yolo_dataset_dir, train_images_dir, val_images_dir, train_labels_dir, val_labels_dir = io.create_output_dir()

    path_oiv7 = utils.validate_input_params(images_dir, labels_dir, yolo_dataset_dir)

    data_processing.process_data(images_dir, labels_dir, train_count, val_count, classes, 
                                 yolo_dataset_dir, train_images_dir, val_images_dir, train_labels_dir, 
                                 val_labels_dir
                                 )
