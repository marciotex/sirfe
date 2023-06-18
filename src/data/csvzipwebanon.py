# -*- coding: utf-8 -*-

"""MakeDatasetApp"""
#import os
import requests
import zipfile
from io import BytesIO
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
#from dotenv import load_dotenv
from pyspark.sql.types import IntegerType, DateType, StringType, DoubleType

def main():

    # Carrega as variáveis de ambiente a partir do arquivo .env
    #load_dotenv()

    base_url_tbr = 'https://repositorio.dados.gov.br/seges/detru/'
#    filename_tbr = 'siconv_proposta.csv.zip'
#    filename = 'propostas_tbr'
    filename_tbr = 'siconv_convenio.csv.zip'
    filename = 'irfes_tbr'
    # Define a URL do arquivo CSV zipado
    url = base_url_tbr + filename_tbr

    # Faz a solicitação HTTP para obter o conteúdo do arquivo ZIP
    print(f'Baixando conteúdo zip de {url}')
    response = requests.get(url)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # outuput_dir_path = 'data/interim/'
        print ('Conteúdo baixado com sucesso.')
    else:
        print("Interrupção por erro na solicitação HTTP:", response.status_code)
        exit()

    print('Descomprimindo o csv zipado baixado.')
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    # Extrai o arquivo CSV do ZIP
    csv_filename = zip_file.namelist()[0]
    csv_content = zip_file.read(csv_filename).decode('utf8')
    print('Descompressão concluída.')
 
    # Cria a sessão Spark
    print ('Criando a sessão spark e o dataframe.')
    spark = SparkSession.builder.getOrCreate()

    # Lê o conteúdo CSV como um DataFrame do PySpark
    df = spark.read.csv(spark.sparkContext.parallelize(csv_content.splitlines()), header=True, sep=";", encoding="utf8")

    # Renomeia as colunas
    columns_to_rename = {
        "DIA_ASSIN_CONV": "DATA_ASSIN_CONV",
        "DIA_FIM_VIGENC_CONV": "DATA_FIM_VIGENC_CONV",
        "DIA_FIM_VIGENC_ORIGINAL_CONV": "DATA_FIM_VIGENC_ORIGINAL_CONV",
        "DIA_INIC_VIGENC_CONV": "DATA_INIC_VIGENC_CONV",
        "DIA_LIMITE_PREST_CONTAS": "DATA_LIMITE_PREST_CONTAS",
        "DIA_PUBL_CONV": "DATA_PUBL_CONV",
        "QTD_PRORROGA": "QTD_PRORROGA_OFIC",
        "QTDE_CONVENIOS": "QTD_CONVENIOS",
        "SITUACAO_CONTRATACAO": "SIT_CONTRATACAO",
        "SITUACAO_PUBLICACAO": "SIT_PUBLICACAO",
        "SUBSITUACAO_CONV": "SUBSIT_CONV",
        "VALOR_GLOBAL_ORIGINAL_CONV": "VL_GLOBAL_ORIGINAL_CONV",
        "ID_PROPOSTA": "ID_PROPOSTA_PMBR"
    }

    for old_name, new_name in columns_to_rename.items():
        df = df.withColumnRenamed(old_name, new_name)

    # Define os tipos de coluna necessários
    column_types = {
        "NR_CONVENIO": IntegerType(),
        "ID_PROPOSTA_PMBR": IntegerType(),
        "DATA_ASSIN_CONV": DateType(),
        "SIT_CONVENIO": StringType(),
        "SUBSIT_CONV": StringType(),
        "SIT_PUBLICACAO": StringType(),
        "INSTRUMENTO_ATIVO": StringType(),
        "IND_OPERA_OBTV": StringType(),
        "NR_PROCESSO": StringType(),
        "DATA_PUBL_CONV": DateType(),
        "DATA_INIC_VIGENC_CONV": DateType(),
        "DATA_FIM_VIGENC_CONV": DateType(),
        "DATA_FIM_VIGENC_ORIGINAL_CONV": DateType(),
        "DIAS_PREST_CONTAS": IntegerType(),
        "DATA_LIMITE_PREST_CONTAS": DateType(),
        "DATA_SUSPENSIVA": DateType(),
        "DATA_RETIRADA_SUSPENSIVA": DateType(),
        "DIAS_CLAUSULA_SUSPENSIVA": StringType(),
        "SIT_CONTRATACAO": StringType(),
        "IND_ASSINADO": StringType(),
        "MOTIVO_SUSPENSAO": StringType(),
        "IND_FOTO": StringType(),
        "QTD_CONVENIOS": IntegerType(),
        "QTD_TA": IntegerType(),
        "QTD_PRORROGA_OFIC": IntegerType(),
        "VL_GLOBAL_CONV": DoubleType(),
        "VL_REPASSE_CONV": DoubleType(),
        "VL_CONTRAPARTIDA_CONV": DoubleType(),
        "VL_EMPENHADO_CONV": DoubleType(),
        "VL_DESEMBOLSADO_CONV": DoubleType(),
        "VL_SALDO_REMAN_TESOURO": DoubleType(),
        "VL_SALDO_REMAN_CONVENENTE": DoubleType(),
        "VL_RENDIMENTO_APLICACAO": DoubleType(),
        "VL_INGRESSO_CONTRAPARTIDA": DoubleType(),
        "VL_SALDO_CONTA": DoubleType(),
        "VL_GLOBAL_ORIGINAL_CONV": DoubleType()
    }

    # Converte os tipos das colunas conforme necessário
    for col_name, col_type in column_types.items():
        df = df.withColumn(col_name, df[col_name].cast(col_type))

    # Adiciona a coluna de índice
    df = df.withColumn("INDICE_IRFES_TBR", monotonically_increasing_id() + 1)
    outuput_dir_path = 'data/interim/'
    outputFile = outuput_dir_path + filename
    df.write.format("parquet").mode('overwrite').save(outputFile)
    print (f'Arquivo parquet gravado em: {outputFile}')

    # Exibe o DataFrame resultante
    df.show()

    # Encerra a sessão Spark
    spark.stop()

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
if __name__ == '__main__':
   main()
