import requests

# https://pypi.org/project/charset-normalizer/
#from charset_normalizer import from_path, from_bytes

def main ():

    base_url_sme = 'https://www.sme.rs.gov.br/sme/projeto-completo/exportar-csv/'
    filenumber_export_sme = '14'
    # URL do arquivo zip
    url = base_url_sme + filenumber_export_sme


    # Faz o download do arquivo
    print ('Baixando arquivo...')

    # Parâmetros de cabeçalho
    headers = {
    'Content-type': 'text/csv',
    'Authorization': 'Basic NDMxNTYyMjMwMzQ6RkRqRlRpU2NXVDl5ZHYy'
}

    # Faz a solicitação HTTP GET com os parâmetros de cabeçalho
    response = requests.get(url, headers=headers)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Salva o conteúdo da resposta em um arquivo local
        outuput_dir_path = 'data/interim/'
        relative_file_path = outuput_dir_path + filenumber_export_sme + '.csv'
        with open(relative_file_path, 'wb') as f:
            f.write(response.content)
        print (f'Arquivo baixado e gravado com sucesso como {relative_file_path}')
        print (f'O encoding do arquivo é: {response.encoding}.')
        if response.encoding != 'UTF-8':
        # queremos manter tudo em utf-8 já a partir da ingestão do dado
        # para evitar ter de lidar com complexidades futuras, queremos
        # garantir que tudo seja UTF-8
        # também por isto: 
        # cat, grep and less do not do any encoding transformation, 
        # they will treat your ISO-8859/latin1 file as UTF-8, which will not work.
        # https://zditect.com/blog/2114862.html file e iconv são ferramentas relevantes
        # print encoding of response
            print(f'O encoding do arquivo não é UTF-8. Converteremos para UTF-8 (em desenvolvimento).')
            # inserir aqui a conversão adequada
            # https://gist.github.com/thluiz/4751212 para script simples e não charset-normalizer
    else:
        print("Erro na solicitação HTTP:", response.status_code)

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
# https://www.alura.com.br/artigos/o-que-significa-if-name-main-no-python
if __name__ == '__main__':
   main()