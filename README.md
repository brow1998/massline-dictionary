# Massline Dictionary Crawler

Este repositório contém um crawler para o site [massline.org](https://massline.org), projetado para capturar todas as entradas do dicionário Marxista, baixar suas imagens e converter os artigos para o formato Markdown, compatível com o Obsidian.

## Requisitos

- **Python**: 3.11+
- **Bibliotecas**: Listadas no arquivo `requirements.txt`

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/massline-dictionary.git
   cd massline-dictionary
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Configuração

Edite o arquivo `settings.py` e ajuste as linhas 25 e 26 para definir onde deseja salvar os artigos e imagens:
```python
ITEMS_OUTPUT_PATH = "caminho/para/salvar/artigos"
FILES_STORE = "caminho/para/salvar/imagens"
```

## Execução

Para rodar o crawler, utilize o comando:
```sh
scrapy crawl massline
```

Os artigos serão salvos no formato `.md` e as imagens serão baixadas para o diretório configurado.

## Licença

Este projeto é distribuído sob a **Licença GPLv3**. Consulte o arquivo `LICENSE` para mais detalhes.

