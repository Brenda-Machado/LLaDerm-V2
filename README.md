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

   Estou trabalhando em cima das outras dependências, mas até o fine-tuning é para não haver nenhuma qu eo VLAB vai ter pedir.

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

## Instruções para treino e teste do modelo

   ### Fine-tuning

   Agora é para estar tudo pronto para iniciar o fine-tuning. Rode o Jupyter Notebook ```fine_tune.ipynb```. Ele irá pedir pela GPU que você quer utilizar (rode ```nvidia-smi``` no terminal antes de escolher). Também pedirá pelo seu token do HuggingFace. Após preenchido, o fine-tuning iniciará.

   Quando o fine-tuning tiver finalizado, alguns arquivos .json serão salvos, como o ```models.json```, ```adapter_wheights.json```, ```training_hyperparameters.json```, etc. Assim como checkpoints na pasta ```notebooks/outputs```.

   ### Teste

   Antes de iniciar o teste, você precisa definir o modelo base para treino, isso é feito rodando o Jupyter Notebook ```define_base_model.ipynb```. Se ele der algum erro, provavelmente houve um problema no salvamento dos dados do seu modelo. Ele irá pedir a GPU e o seu token da mesma forma que o Fine-tuning.

   Quando o teste tiver finalizado, novamento alguns arquivos serão gerados, mas eles estarão na pasta ```/results``` na raiz do projeto.

## Instruções para análise dos dados obtidos 

   Para gerar os plots e as métricas em cima do treinamento e do treino, os notebooks ```analyse_trainings.ipynb``` e ```analyse_tests.ipynb```, respectivamente, deverão ser rodados. Antes de rodar, é necessário especificar alguns detalhes. Importante, pode ser necessário criar a pasta ```plots``` dentro da pasta ```results``` na raiz do projeto. Verifique se ela existe.

   ### Plots da loss

   No primeiro, ```analyse_trainings.ipynb```, você precisará preencher o ```MODEL_NAME``` e o ```EVENT_FILE_NAME``` com o nome do modelo e o nome do arquivo de checkpoint que você tá utilizando, o qual vai estar na pasta ```notebooks/outputs/runs```. Um exemplo de como preencher a seguir:

   ```
   MODEL_NAME = 'Llama'
   EVENT_FILE_NAME = 'Apr23_15-12-21_a7d2d29c04e2'
   ```
   Rodando o notebook você verá o plot da loss e estatísticas dela.

   ### Plots e métricas do teste

   No segundo, ```analyse_tests.ipynb```, você precisará preencher o ```TEST_NAME```, ```SKIN_LESIONS_CONFUSION_MATRIX_NAME``` e o ```RISK_CONFUSION_MATRIX_NAME``` com os nomes que você quiser ´}pôr nos testes e titulos. Um exemplo de como preencher a seguir:

   ```
   TEST_NAME = 'Llama.json' 
   SKIN_LESIONS_CONFUSION_MATRIX_NAME = 'Acurácia do Llama-3.2-11B na classificação de lesões de pele'
   RISK_CONFUSION_MATRIX_NAME = 'Acurácia do Llama-3.2-11B na classificação de risco'
   ```
   Rodando o notebook você verá o plot da matriz de confusão, métricas como precision, acurácia, BLEU, ROUGE, etc.

