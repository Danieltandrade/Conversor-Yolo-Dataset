# Dataset Personalizado para YOLO

[![Build Status](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/Danieltandrade/Conversor-Yolo-Dataset/actions)
[![OS Compatibility](https://img.shields.io/badge/OS-Windows%20|%20Linux%20|%20macOS-blue.svg)](https://github.com/Danieltandrade/Conversor-Yolo-Dataset)
[![Python Version](https://img.shields.io/badge/Python-3.10|3.11|3.12-blue.svg)](https://www.python.org/downloads/)
[![Code Size](https://img.shields.io/github/languages/code-size/Danieltandrade/Conversor-Yolo-Dataset.svg)](https://github.com/Danieltandrade/Conversor-Yolo-Dataset)
[![Last Update](https://img.shields.io/github/last-commit/Danieltandrade/Conversor-Yolo-Dataset.svg)](https://github.com/Danieltandrade/Conversor-Yolo-Dataset)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este projeto cria um dataset personalizado a partir do Dataset OIDv7-Toolkit para uso com o framework YOLO.

## Introdução

Open Images Dataset V7 (OIDv7) é um conjunto de dados criado pelo Google para fins de aprendizado de máquina. Contém um conjunto de aproximadamente 9 Milhoes de imagens anotadas com rótulos de imagem, caixas delimitadoras de objetos, máscaras de segmentação de objetos, relações visuais e narrativas localizadas.
Mais informações podem ser obtidas em [Open Images Dataset V7](https://storage.googleapis.com/openimages/web/index.html)

O dataset OIDv7-Toolkit pode ser obtido no GitHub através do link: [EdgeOfAI/oidv7-Toolkit](https://github.com/EdgeOfAI/oidv7-Toolkit)


## Descrição

Este projeto cria um novo dataset personalizado a partir do Dataset OIDv7-Toolkit para uso com o framework YOLO. Ele cria pastas de treinamento e validação, divide os arquivos de imagens e labels para cada pasta e gera um arquivo de configuração data.yaml com os caminhos para as pastas de treinamento e validação.

## Requisitos

__Python 3.10+__

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Danieltandrade/Conversor-Yolo-Dataset.git
```

## Uso

Execute o script:

```bash
python main.py
```
> [!NOTE]
> Após execução de "main.py", o script irá perguntar os caminhos para as pastas de imagens, labels e saída.

O script criará um novo dataset personalizado com pastas de treinamento e validação, dividindo os arquivos de imagens e labels para cada pasta e reorganizando. Também será criado o arquivo de configuração data.yaml.
Para as imagens de treinamento e validação, o script irá perguntar a quantidade de imagens de cada classe, sendo dividdo da seguinte forma:
- 85% para treinamento
- 10% para validação
- 05% para teste

> [!WARNING]
> Caso deseje formar um dataset com uma quantidade de imagens muito grande, primeiramente confira a quantidade de imagens de cada classe no Dataset OIDv7-Toolkit.

- Estrtura de Diretórios:
```
yolo_dataset
    ├── dataset
    │   ├── images
    │   │   ├── train
    │   │   └── val
    │   └── labels
    │       ├── train
    │       └── val
    └── data.yaml
```

## Contribuição

Contribuições são bem-vindas! Se você encontrar um erro ou tiver uma sugestão, por favor abra uma issue ou envie um pull request.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Conclusão

Este projeto apresentou o comprotamento esperados nos testes realizados. O dataset personalizado criado com base no OIDv7-Toolkit pode ser utilizado com o framework YOLO para treinamento de modelos de detecção de objetos.