import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import json
import shutil
import openpyxl
import os
from tkinter import filedialog
import xlsxwriter

# Variável global para armazenar os detalhes dos pacotes
data_to_save = []
data = []
format_variables = []  # Lista para armazenar as variáveis de controle
content_text = None  # Declaração global da variável content_text

def collect_data(file_paths):
    for file_path in file_paths:
        file_type = file_path.split('.')[-1].lower()
        if file_type == 'zip':
            contents = list_zip_contents(file_path)
        elif file_type == 'rar':
            contents = list_rar_contents(file_path)
        else:
            contents = [{"Arquivo": "Tipo de arquivo não suportado", "Tamanho": 0}]
        
        data.extend(contents)

# Função para gerar arquivo xlsx com os dados coletados
def generate_xlsx(file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    # Escreva os cabeçalhos das colunas
    worksheet.write(0, 0, "Arquivo", bold)
    worksheet.write(0, 1, "Tamanho (bytes)", bold)

    # Preencha os dados nas células
    for row, item in enumerate(data, start=1):
        worksheet.write(row, 0, item["Arquivo"])
        worksheet.write(row, 1, item["Tamanho"])

    workbook.close()

# Função para obter detalhes de um pacote (conjunto de dados)
def get_package_details(package_id):
    response = requests.get(base_url + f'package_show?id={package_id}')
    if response.status_code == 200:
        package_details = response.json()['result']

        # Remove formatos duplicados
        seen_formats = set()
        unique_formats = []
        for resource in package_details.get('resources', []):
            format = resource['format']
            if format not in seen_formats:
                seen_formats.add(format)
                unique_formats.append(format)

        package_details['resources'] = [{'format': format, 'url': resource['url']} for format, resource in zip(unique_formats, package_details.get('resources', []))]

        return package_details

    return None

# Função para exportar para Excel
def export_to_excel(data_to_save):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Detalhes dos Pacotes"

    headers = ["Pacote", "Organização", "Grupos", "Formatos disponíveis", "Caminho de Download"]
    ws.append(headers)

    for package in data_to_save:
        package_name = package["Pacote"]
        package_organization = package.get("Organização", "")
        package_groups = ", ".join([group["name"] for group in package["Grupos"]])
        package_formats = ", ".join([resource['format'] for resource in package["Formatos disponíveis"]])
        package_paths = ", ".join([resource['url'] for resource in package["Formatos disponíveis"]])
        ws.append([package_name, package_organization, package_groups, package_formats, package_paths])

    url_domain = base_url.split("://")[1].replace("/", "_")

    excel_filename = f"{url_domain}_detalhes_pacotes.xlsx"
    try:
        wb.save(excel_filename)
        messagebox.showinfo("Sucesso", f"Arquivo {excel_filename} exportado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao exportar para Excel: {e}")

# Função para atualizar os detalhes na interface
def update_details():
    selected_base_url = base_url_selector.get()
    if selected_base_url:
        global base_url
        base_url = selected_base_url
        package_list_response = requests.get(base_url + 'package_list')
        package_list = package_list_response.json()['result']

        filename = selected_base_url.replace("://", "_").replace("/", "_")
        with open(f"{filename}.json", "w") as json_file:
            data_to_save.clear()
            for package_id in package_list:
                package_details = get_package_details(package_id)
                if package_details:
                    package_data = {
                        "Pacote": package_details['title'],
                        "Organização": package_details.get('organization', {}).get('title', ''),
                        "Grupos": package_details.get('groups', []),
                        "Formatos disponíveis": package_details.get('resources', []),
                    }
                    data_to_save.append(package_data)
                    
                else:
                    print(f"Falha ao obter detalhes do pacote: {package_id}")

            json.dump(data_to_save, json_file, indent=4)

        shutil.copy(f"{filename}.json", "resultados")

        update_results()
        export_button.config(state=tk.NORMAL)

def map_url_to_city(url):
    if 'dados.fortaleza.ce.gov.br' in url:
        return 'Fortaleza'
    elif 'dados.df.gov.br' in url:
        return 'Brasília'
    elif 'dados.recife.pe.gov.br' in url:
        return 'Recife'
    elif 'dados.natal.br' in url:
        return 'Natal'
    elif 'dadosabertos.poa.br' in url:
        return 'Porto Alegre'
    else:
        return 'Cidade Desconhecida'  # Caso não seja reconhecida nenhuma das cidades

# Função para atualizar a lista de resultados na interface
def update_results():
    results_listbox.delete(0, tk.END)
    unique_cities = set()  # Usamos um conjunto para garantir cidades únicas
    for package in data_to_save:
        for resource in package["Formatos disponíveis"]:
            city = map_url_to_city(resource["url"])
            if city not in unique_cities:
                results_listbox.insert(tk.END, city)
                unique_cities.add(city)

# Criação da janela principal
root = tk.Tk()
root.title("Detalhes dos Pacotes")

window_width = 800  # Ajustei o tamanho da janela
window_height = 600
root.geometry(f"{window_width}x{window_height}")

element_width = int(window_width * 0.3)
element_height = int(window_height * 0.3)

base_url_label = tk.Label(root, text="Selecione a base_url:", width=element_width)
base_url_label.pack()

base_url_options = ['https://dados.fortaleza.ce.gov.br/api/3/action/', 'http://www.dados.df.gov.br/api/3/action/','http://dados.recife.pe.gov.br/api/3/action/','http://dados.natal.br/api/3/action/','https://dadosabertos.poa.br/api/3/action/']
base_url_selector = ttk.Combobox(root, values=base_url_options, width=int(element_width * 0.24))
base_url_selector.pack()

update_button = tk.Button(root, text="Pesquisar", command=update_details, width=int(element_width * 0.21))
update_button.pack()

results_listbox = tk.Listbox(root, width=int(element_width * 0.25), height=int(element_height * 0.1), selectmode=tk.SINGLE)
results_listbox.pack()

export_button = tk.Button(root, text="Exportar para Excel", command=lambda: export_to_excel(data_to_save), width=int(element_width * 0.21), state=tk.DISABLED)
export_button.pack()

root.mainloop()
