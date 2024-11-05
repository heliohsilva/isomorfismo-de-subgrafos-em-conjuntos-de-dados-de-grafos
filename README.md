## Estrutura do Projeto
```
root/
├── bzr/
│ ├── input_exemplos/
│ │ ├── tamanho_100/
│ │ │ ├── input.png
│ │ │ ├── resultado_1.png
│ │ │ ├── ...
│ │ └── resultados/
│ │ ├── desempenho_batch_size.csv
│ │ ├── ...
│ └── ...
├── cuneiform/
│ └── ...
├── mutag/
│ └── ...
├── tudataset/
│ ├── ...
├── compute.py
├── in_out_data.py
├── main.py
├── media+intervalo.py
├── requirements.txt
├── run.sh
└── speedup+eficiencia.py
```
## Descrição das Pastas e Arquivos

- **bzr, cuneiform, mutag:** Pastas que contém os dados e resultados para cada algoritmo.
  - **input_exemplos:**
    - **tamanho_100:** Pasta contendo exemplos de entrada (input.png) e os 5 primeiros resultados obtidos para um determinado tamanho de entrada.
    - **resultados:** Pasta contendo os resultados das execuções, como arquivos CSV com dados de desempenho para diferentes configurações de parâmetros.
- **tudataset:** Contém scripts e dados relacionados à transformação dos conjuntos de dados em objetos `nx.Graph`.
- **compute.py:** Script responsável por processar os dados, dividindo-os em batches e executando o teste de isomorfismo em paralelo.
- **in_out_data.py:** Script utilizado para gerar as entradas utilizadas nos testes.
- **main.py:** Script principal que controla a execução do programa.
- **media+intervalo.py:** Script para calcular a média e o intervalo de confiança dos resultados obtidos.
- **requirements.txt:** Lista as bibliotecas Python necessárias para o projeto.
- **run.sh:** Script de shell para automatizar as execuções, variando os parâmetros como tamanho do batch, número de processos e tamanho da entrada.
- **speedup+eficiencia.py:** Script para calcular o speedup e outras métricas de eficiência.

## Como Executar o Projeto

1. **Criar um ambiente virtual:**

   a. **Utilizando venv**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   b. **Utilizando conda**

   ```bash
   conda create -n my-env
   conda activate my-env
   ```

2. **Instalar as dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar projeto**
   ```bash
   sh run.sh
   ```
