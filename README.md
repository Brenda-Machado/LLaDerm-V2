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

   ```bash
   pip install --upgrade pip
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   pip install "unsloth[cu118-ampere-torch240] @ git+https://github.com/unslothai/unsloth.git"
   pip install trl pydantic scikit-learn pandas matplotlib seaborn tensorboard
   pip install python-dotenv huggingface_hub Pillow tqdm pyyaml
   ```

   Se tiver erros na instalacao do unsloth, consulte: https://github.com/unslothai/unsloth

4. Configure seu token do Hugging Face

O modelo base precisa ser baixado do Hugging Face. Crie um token em https://huggingface.co/settings/tokens e salve-o:

```
echo "HF_TOKEN=hf_seu_token_aqui" > .env
```

## Fluxo de trabalho

Para entender melhor como funciona cada um dos scripts, o fluxo segue a seguinte lógica:

```
[1] Preparar dataset  -->  [2] Definir modelo base  -->  [3] Treinar
        |                                                      |
        v                                                      v
 build_dataset.ipynb                               fine_tune.ipynb
 OU prepare_custom_dataset.py
 (veja secao 5)

[4] Testar  -->  [5] Analisar resultados
    |                    |
    v                    v
test.ipynb      analyze_tests.ipynb
```

## Uso

