# coletaDados
# Sistema de Detalhes dos Pacotes

Este documento descreve um sistema em Python que permite obter informações detalhadas sobre pacotes de dados de várias fontes de dados abertos. 
O sistema usa a biblioteca Tkinter para criar uma interface gráfica de usuário (GUI) e oferece funcionalidades como coletar dados, exportar 
informações para um arquivo Excel e atualizar a lista de resultados na interface. Aqui está uma visão geral do sistema e como usá-lo:

## Requisitos

Para executar este sistema, você precisa ter o Python instalado em seu computador. Certifique-se de que as seguintes bibliotecas também estejam instaladas:
- tkinter
- requests
- json
- shutil
- openpyxl
- os
- filedialog
- xlsxwriter

## Uso

1. **Selecione a Base URL:**
   - Inicie o sistema e selecione uma das URLs base nas opções fornecidas, como:
     - https://dados.fortaleza.ce.gov.br/api/3/action/
     - http://www.dados.df.gov.br/api/3/action/
     - http://dados.recife.pe.gov.br/api/3/action/
     - http://dados.natal.br/api/3/action/
     - https://dadosabertos.poa.br/api/3/action/
   - A URL base determina a fonte de dados que você deseja acessar.

2. **Pesquisar:**
   - Clique no botão "Pesquisar" para buscar informações sobre os pacotes de dados na fonte selecionada.

3. **Exportar para Excel:**
   - Após a pesquisa, você pode exportar os detalhes dos pacotes para um arquivo Excel. Certifique-se de ter pesquisado os pacotes antes de tentar exportar.

4. **Lista de Resultados:**
   - A lista de resultados na interface exibe as cidades de origem dos pacotes de dados disponíveis na fonte selecionada. Cada cidade é exibida apenas uma vez,
   garantindo cidades únicas.

## Funcionalidades

- O sistema coleta detalhes de pacotes de dados de fontes de dados abertos com base na URL fornecida.
- Ele exporta os detalhes dos pacotes de dados para um arquivo Excel.
- Atualiza a lista de resultados na interface, exibindo cidades únicas das fontes de dados abertos.

## Observações

- O sistema usa a biblioteca Tkinter para criar uma interface gráfica simples, permitindo uma interação fácil.
- É importante ter uma conexão com a internet para acessar e coletar informações da fonte de dados selecionada.

**Nota:** 
Este sistema é um exemplo e pode ser estendido e personalizado para atender a diferentes fontes de dados e requisitos específicos. 
Certifique-se de instalar as bibliotecas necessárias antes de executar o sistema.
