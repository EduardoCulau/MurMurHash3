import numpy as np
import sys
import csv
import mmh3

############ VARIÁVEIS PARA ALTERAR ############

# Modo Debug
_DEBUG_ = False
_INFO_  = True

# AllowList sendo de 1 até 100%
ALLOWLIST = 10

# Seed do MurMurHash
_SEED_ = 0

# Arquivo CSV de entrada no qual teremos os UUIDs na primeira coluna chamada 'uuid' como string e sem headers (só uma lista de UUIDs)
input_csv_full_path = "C:\\Users\\eduar\\Desktop\\Pyhton\\MurMurHash3\\uuids.csv"

# Arquivo de saída com somente os UUIDs que estão dentro da allowlist pelo algorítimo murmurhas_v3
output_csv_full_path = "C:\\Users\\eduar\\Desktop\\Pyhton\\MurMurHash3\\uuids_filtrados.csv"

########################## NÃO ALTERAR ##########################

# CONSTANTE MAX_UINT PARA DENOMINADOR DA PORCENTAGEM
MAX_UINT_32 = np.iinfo(np.uint32).max #(2**32 - 1) = 4294967295

# Checar se o realmente está como 32 bits
print(f'Nesse sistema o UINT32 realmente possui {sys.getsizeof(MAX_UINT_32)} bits')
print(f'Valor do MAX_UINT_32 = {MAX_UINT_32} sendo em Hex = {hex(MAX_UINT_32)}')

# Define o métodos do murmurhash_x86_32
def murmurhash_x86_32(string, seed=0):
    
    # Converte a string para representação binária bruta
    bit_representation = string.encode('ascii') # força o encode a usar ascii sendo 1 byte por caractere 
    
    if _DEBUG_:
        print(f'Calculando o MurMurHash para a string = {string}')
        print(f'A string representada em bits = {bit_representation}')
    
    hash_value_32 = mmh3.hash(bit_representation, seed, signed=False)
    percentage = hash_value_32 / MAX_UINT_32  # Normaliza baseado no max_int, assim criando a porcentagem
    
    if _DEBUG_:
        print(f'Output do murmurhas = {hash_value_32}')
        print(f'Porcentagem = {percentage*100:.4}%') #Print com a % correta e 4 casas decimais
    
    return percentage

# Usado para imprimir a barra de progresso
def print_progress_bar(iteration, total, bar_length=50):
    progress = iteration / total
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    percent = round(progress * 100)
    bar = f"[{arrow}{spaces}] {percent}%"
    sys.stdout.write(f"\r{bar}")  # \r moves the cursor to the beginning of the line
    sys.stdout.flush()  # Flush the buffer to ensure the progress bar is displayed

try:
    import pandas as pd
    _HAS_PANDAS_ = True
    print('Módulo Pandas localizado, o mesmo será utilizado para ler e escrever o CSV')
except ImportError: 
    _HAS_PANDAS_ = False
    print('Módulo Pandas não localizado, seguindo com o Módulo CSV')

# Lê os UUIDs de um arquivo csv
def read_uuids_from_csv(file_path):
    """Reads UUIDs from a CSV file and returns a list of UUID strings."""
    uuids = []
    
    if _INFO_:
        print('Lendo arquivo de entrada')
    
    if _HAS_PANDAS_:
        df = pd.read_csv(file_path, header=None)
        uuids = df.iloc[:,0].tolist()
    else:
        with open(file_path, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row:  # Ensure row is not empty
                    uuids.append(row[0])  # Assume UUIDs are in the first column
    return uuids
    
# Escreve os UUIDs em um arquivos
def write_uuids_to_csv(uuid_list, file_path):
    """Write UUIDs to a CSV file."""
    if _INFO_:
        print('Escrevendo arquivo de saída')
    
    if _HAS_PANDAS_:
        df = pd.DataFrame(uuid_list)
        #df.columns = [None] #remove o header do csv
        df.to_csv(file_path, index=False, header=False)
    else:
        with open(file_path, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            #writer.writerow(["UUID"])  # Sem Heade
            for uuid in uuid_list:
                writer.writerow([uuid])

def filtra_uuids (uuid_lista, threshold):
    
    uuid_lista_filtrada = []
    
    # Quantidade do processamento
    qtd_total = len(uuid_lista)
    qtd_processados = 0
    
    if _INFO_:
        print(f'Iniciando filtregem de {qtd_total} uuids')
    
    for uuid in uuid_lista:
        porcentagem = murmurhash_x86_32(uuid , _SEED_)
        
        if porcentagem <= threshold:
            uuid_lista_filtrada.append(uuid)
        
        qtd_processados += 1
        
        if _INFO_:
            if (qtd_processados / qtd_total * 100) % 1 == 0:
                print_progress_bar(qtd_processados, qtd_total)
    
    if _INFO_:
        print(f'\nFim da filtragem, retornando {len(uuid_lista_filtrada)} uuid dentro da Allow-List')
    
    return uuid_lista_filtrada

########################## MAIN ##########################

#Lê o arquivo
uuid_lista  = read_uuids_from_csv(input_csv_full_path)

# Exemplos para teste
_UUIDS_  = ['b1e06607-0883-40cf-bee5-561058ae3832', 
            '4059061a-ba72-48ad-97d0-7e13169f21e7', 
            'd936c1f6-a68b-4d29-aeed-466a8bfd7ccf', 
            '2364b31e-7482-4c4c-959c-4311cc772292',
            'acc934b3-2284-411b-a1dd-e1d09aca76c8',
            '34c44f41-9ceb-4dad-a21f-89fcedb99342',
            'de09e0b4-5153-4456-a4dc-762174663d4d',
            '5a1471dd-6185-4b93-9422-993fb830a349',
            'a96e4e3e-fad2-4aad-a4c6-47cea5d1639a',
            '3db65d21-98f6-4638-a23a-945d9540217e']
            
# Filtra os UUIDs        
uuid_lista_filtrada = filtra_uuids(uuid_lista, ALLOWLIST/100)

# Exporta os arquivos para o arquivo de destino
write_uuids_to_csv(uuid_lista_filtrada, output_csv_full_path)
