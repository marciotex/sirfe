# -*- coding: utf-8 -*-

"""MakeDatasetApp"""
from pyspark.sql import SparkSession
import requests
#import pandas as pd
#import io



# https://pypi.org/project/charset-normalizer/
#from charset_normalizer import from_path, from_bytes

def main ():

    #base_url_sme = 'https://www.sme.rs.gov.br/sme/projeto-completo/exportar-csv/'
    base_url_sme = 'https://smegov02.hml.rs.gov.br/sme/projeto-completo/exportar-csv/'
    filenumber_export_sme = '15'
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
#    response_file_like = io.BytesIO(response.content)
#    df = pd.read_csv(response_file_like)
#    df.show
# procuro uma forma de conectar o download dos dados
# e passar para o spark sem gravar dados em disco
# o segredo parece estar em transformar o retorno de request.get em um objeto
# file-like, que talvez o panda possa ler como csv (acho que não)
# ou seja como estruturar o retorno de request.get em algo que possa
# ser carregada por pandas ou pyspark? request.raw?
# https://requests.readthedocs.io/en/latest/api/#requests.Response.raw
# se precisar gravar em disco, gravar em parquet, mais eficiente
# https://www.databricks.com/glossary/what-is-parquet
# já chamando o pyspark:
# https://towardsdatascience.com/4-ways-to-write-data-to-parquet-with-python-a-comparison-3c4f54ee5fec
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

    spark = SparkSession.builder.appName("MakeDatasetApp").getOrCreate()
    inputFile = relative_file_path  # Should be some file on your system, o arquivo salvo acima
    df = spark.read.options(delimiter=";", inferSchema="true", header=True).csv(inputFile)
    #df.show()
    # inserir aqui as rotinas de transformação
    outputFile = outuput_dir_path + 'parquetmp'
    df.write.format("parquet").mode('overwrite').save(outputFile)
    print (f'Arquivo gravado em: {outputFile}')
#    df2 = spark.read.options(delimiter=";", inferSchema="true", header=True).parquet(outputFile)
    df2=spark.read.parquet(outputFile)
    df2.createOrReplaceTempView("TmpTable")
    qdf2 = spark.sql("select * from TmpTable where `tmptable`.`IRFE.CODIGO_IRFE` >= 1000")
    qdf2.show()
    #df = spark.read.csv(inputFile).cache()
    #cacheData = spark.read.text(inputFile).cache()

#    numAs = cacheData.filter(cacheData.value.contains('a')).count()
#    numBs = cacheData.filter(cacheData.value.contains('b')).count()

#    print (f'Arquivo processado: {relative_file_path}')
#    print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

    spark.stop()

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
# https://www.alura.com.br/artigos/o-que-significa-if-name-main-no-python
if __name__ == '__main__':
   main()