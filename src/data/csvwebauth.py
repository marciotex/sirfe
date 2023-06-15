import requests

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
        with open(outuput_dir_path + filenumber_export_sme + '.csv', 'wb') as f:
            f.write(response.content)
        print (f'Arquivo baixado e gravado com sucesso em {outuput_dir_path}')
#        print ('Arquivo baixado e gravado com sucesso em ?')
    else:
        print("Erro na solicitação HTTP:", response.status_code)

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
# https://www.alura.com.br/artigos/o-que-significa-if-name-main-no-python
if __name__ == '__main__':
   main()