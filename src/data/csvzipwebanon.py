import requests
import zipfile
import io

# URL do arquivo zip
url = 'https://repositorio.dados.gov.br/seges/detru/siconv_convenio.csv.zip'

# Faz o download do arquivo zip
response = requests.get(url)
zip_file = zipfile.ZipFile(io.BytesIO(response.content))

# Extrai o conteúdo do arquivo zip
zip_file.extractall()

# Fecha o arquivo zip
zip_file.close()

print("Arquivo descompactado com sucesso!")
