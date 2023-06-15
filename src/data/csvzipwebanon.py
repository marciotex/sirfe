import requests
import zipfile
import io

def main ():

    base_url_tbr = 'https://repositorio.dados.gov.br/seges/detru/'
    filename_tbr = 'siconv_proposta.csv.zip'
    # URL do arquivo zip
    url = base_url_tbr + filename_tbr


    # Faz o download do arquivo zip
    print ('Baixando arquivo...')
    response = requests.get(url)
    print ('Arquivo baixado com sucesso. Agora vamos tentar descomprimi-lo...')
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    # Extrai o conteúdo do arquivo zip
    outuput_dir_path = 'data/interim/'
    zip_file.extractall(path=outuput_dir_path)

    # Fecha o arquivo zip
    zip_file.close()

    print (f'Arquivo baixado, descomprimido e gravado com sucesso em {outuput_dir_path}')

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
# https://www.alura.com.br/artigos/o-que-significa-if-name-main-no-python
if __name__ == '__main__':
   main()