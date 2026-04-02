# LLaDerm-V2

O trabalho avaliou o uso de um MLLM para classificar lesões de pele e gerar laudos, realizando fine-tuning do modelo LLaMA 3.2 11B com as técnicas QLoRA e LoRA, baseadas em PEFT.

O desenvolvimento ocorreu em duas etapas:

- Classificação de lesões: foi utilizado o conjunto de imagens dermatoscópicas HAM10000. O melhor modelo, treinado com QLoRA, alcançou 87,4% de acurácia.

- Classificação e geração de laudos: utilizou-se um conjunto de imagens de aproximação do STT/SC. O modelo com QLoRA obteve 45,2% de acurácia, e o com LoRA, 44,5%.

Links úteis:
- [Repositório original;](https://github.com/ErFer7/LLaDerm)
- [TCC do Eric.](https://repositorio.ufsc.br/handle/123456789/266618)

## Instruções de instalação

Utilize os seguintes comandos para a instalação. Recomendo você utilizar o ambiente [VLAB](https://jupyter.vlab.ufsc.br/) ou semelhante.

1. Clone

   ```bash
   git clone https://github.com/Brenda-Machado/LLaDerm-V2.git
   cd LLaDerm-V2
   ```

2. Ambiente virtual (recomendado)
   ```bash
   python -m venv .venv
   source .venv/bin/activate 
   ```

3. Instalação das dependências

   A princípio, você irá precisar instalar apenas o unsloth.

   ```bash
   pip install unsloth
   ```

   Se tiver erros na instalacao do unsloth, consulte: https://github.com/unslothai/unsloth

   Estou trabalhando em cima das outras dependências, mas até o fine-tuning é para não haver nenhum. [TO-DO]

## Instruções de preparação do dataset

### ISIC 2019

   Os dados não estarão inclusos no repositório, então é necessário baixá-los utilizando ```wget``` e descompactá-los. 
   
   ### Download
   
   Primeiro, crie o caminho correto para a aplicação, dentro da raiz do projeto, isto é, a pasta LLaDerm:

   ```
   mkdir data/isic2019
   ```

   Em seguinda, baixe o repositório de imagens na pasta correspondente:

   ```
   cd data/isic2019
   wget https://isic-challenge-data.s3.amazonaws.com/2019/ISIC_2019_Training_Input.zip
   ```

   É um dataset de mais ou menos 9GB, então vai levar algum tempo. Agora é preciso baixar as labels:

   ```
   wget https://isic-challenge-data.s3.amazonaws.com/2019/ISIC_2019_Training_GroundTruth.csv
   ```

   e os metadados:

   ```
   wget https://isic-challenge-data.s3.amazonaws.com/2019/ISIC_2019_Training_Metadata.csv
   ```

   Agora, é necessário descompactar o .zip que foi baixado:

   ```
   unzip ISIC_2019_Training_Input.zip
   ```

   Isso resulta em uma pasta contendo muitas imagens.

   ### Formatação para o pipeline

   Como o ISIC não tem textos de laudo, é necessário formatar o dataset antes de iniciar o fine-tuning do modelo.

   Dentro da pasta ```src/notebooks/```, rode o seguinte comando o Jupyter Notebook ```build_isic_dataset.ipynb```.

   Em alguns minutos ele terá gerado os arquivos no formato correto.

   ### Fine-tuning

   Agora é para estar tudo pronto para iniciar o fine-tuning. Rode o Jupyter Notebook ```fine_tune.ipynb```. Ele irá pedir pela GPU que você quer utilizar (rode ```nvidia-smi``` no terminal antes de escolher). Também pedirá pelo seu token do HuggingFace. Após preenchido, o fine-tuning iniciará.

   [mais detalhes em breve]...

