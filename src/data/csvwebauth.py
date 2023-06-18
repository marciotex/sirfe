# -*- coding: utf-8 -*-

"""MakeDatasetApp"""
import os
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from dotenv import load_dotenv
from pyspark.sql.types import IntegerType, StringType, DateType, DoubleType



def main ():

    # produção:
    #base_url_sme = 'https://www.sme.rs.gov.br/sme/projeto-completo/exportar-csv/'
    # devel: 
    base_url_sme = 'https://smegov02.hml.rs.gov.br/sme/projeto-completo/exportar-csv/'

    # Define exportação dos irfes
    filenumber_export_sme = '14'
    filename = 'irfes_sme'

    # Define a URL do arquivo CSV
    url = base_url_sme + filenumber_export_sme



    # Parâmetros de cabeçalho
    # precisamos antes carregar as variáveis de ambiente a partir de .env
    load_dotenv()
    headers = {
        "Content-type": "text/csv",
        "Authorization": os.environ.get('AUTHORIZATION_HEADER_SME')
    }

    # Faz a solicitação HTTP para obter o conteúdo do CSV
    print(f'Baixando conteúdo csv de {url}')
    response = requests.get(url, headers=headers)
    csv_content = response.text

    # se precisar gravar em disco, gravar em parquet, mais eficiente
    # https://www.databricks.com/glossary/what-is-parquet
    # já chamando o pyspark:
    # https://towardsdatascience.com/4-ways-to-write-data-to-parquet-with-python-a-comparison-3c4f54ee5fec

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # outuput_dir_path = 'data/interim/'
        print('Conteúdo baixado com sucesso.')
    else:
        print("Interrupção por erro na solicitação HTTP:", response.status_code)
        exit()


    print ('Criando a sessão spark e o dataframe.')
    # Cria a sessão Spark
    spark = SparkSession.builder.getOrCreate()
    # não foi preciso salvar como arquivo e carregar
    # solução limpa, direta
    # Lê o conteúdo CSV como um DataFrame do PySpark
    df = spark.read.csv(spark.sparkContext.parallelize(csv_content.splitlines()), header=True, sep=";", encoding="cp1252")

    # Renomeia as colunas
    columns_to_rename = {
        "IRFE.CODIGO_IRFE": "ID_IRFE_SME",
        "IRFE.Convenente": "NM_PROPONENTE",
        "IRFE.Concedente": "NM_CONCEDENTE",
        "IRFE.CPF_Usuario": "ID_SETORIALISTA",
        "IRFE.Nome_Usuario": "NM_SETORIALISTA",
        "IRFE.Data_Inicio_Vigencia": "DATA_INIC_VIGENC_CONV",
        "IRFE.Data_Termino_Vigencia": "DATA_FIM_VIGENC_CONV",
        "IRFE.Prazo_Limite_Prestacao_Contas": "DIAS_PREST_CONTAS",
        "IRFE.Data_Limite_Prestacao_Contas": "DATA_LIMITE_PREST_CONTAS",
        "IRFE.Data_Final_Original": "DATA_FIM_VIGENC_ORIGINAL_CONV",
        "IRFE.Data_Limite_Retirada_Suspensiva": "DATA_SUSPENSIVA",
        "IRFE.Modalidade_Instrumento_Repasse": "MODALIDADE",
        "IRFE.Status_Operacional": "SIT_CONVENIO",
        "IRFE.Valor_Contrapartida": "VL_CONTRAPARTIDA_CONV",
        "IRFE.Valor_Global": "VL_GLOBAL_CONV",
        "IRFE.Valor_Repasse": "VL_REPASSE_CONV",
        "IRFE.Publico_Alvo": "PUBLICO_ALVO",
        "IRFE.Clausula_Suspensiva": "TEM_SUSPENSIVA_Q",
        "IRFE.Transferencia_Valor_Original": "VL_REPASSE_ORIGINAL_CONV",
        "IRFE.Contrapartida_Valor_Original": "VL_CONTRAPARTIDA_ORIGINAL_CONV",
        "IRFE.CODIGO_PROJETO": "ID_PROJETO_SME",
        "IRFE.Objeto": "OBJETO_PROPOSTA",
        "IRFRE.Identificador_Transfergov": "ID_IRFE_PMBR",
        "IRFE.Identificador_Outro_Sistema_Federal": "ID_IRFE_OUTRO_SF",
        "IRFE.Tipo_Repasse": "TIPO_TRANSFERENCIA",
        "IRFE.Valor_Rendimento_Autorizado": "VL_RENDIMENTO_AUTORIZADO"
    }

    for old_name, new_name in columns_to_rename.items():
        df = df.withColumnRenamed(old_name, new_name)

    # Define os tipos de coluna necessários
    column_types = {
        "ID_IRFE_SME": IntegerType(),
        "DATA_INIC_VIGENC_CONV": DateType(),
        "DATA_FIM_VIGENC_CONV": DateType(),
        "DIAS_PREST_CONTAS": IntegerType(),
        "DATA_LIMITE_PREST_CONTAS": DateType(),
        "VL_REPASSE_CONV": DoubleType(),
        "VL_CONTRAPARTIDA_CONV": DoubleType(),
        "VL_GLOBAL_CONV": DoubleType(),
        "ID_IRFE_PMBR": IntegerType(),
        "ID_SETORIALISTA": IntegerType(),
        "VL_RENDIMENTO_AUTORIZADO": DoubleType()
    }

    # Converte os tipos das colunas conforme necessário
    for col_name, col_type in column_types.items():
        df = df.withColumn(col_name, df[col_name].cast(col_type))

    # # forma alternativa de fazer a conversão
    # # testar desempenho
    # # Converte os tipos das colunas conforme necessário
    # df = df.withColumn("ID_IRFE_SME", df["ID_IRFE_SME"].cast("integer"))
    # df = df.withColumn("DATA_INIC_VIGENC_CONV", df["DATA_INIC_VIGENC_CONV"].cast("date"))
    # df = df.withColumn("DATA_FIM_VIGENC_CONV", df["DATA_FIM_VIGENC_CONV"].cast("date"))
    # df = df.withColumn("DIAS_PREST_CONTAS", df["DIAS_PREST_CONTAS"].cast("integer"))
    # df = df.withColumn("DATA_LIMITE_PREST_CONTAS", df["DATA_LIMITE_PREST_CONTAS"].cast("date"))
    # df = df.withColumn("VL_REPASSE_CONV", df["VL_REPASSE_CONV"].cast("double"))
    # df = df.withColumn("VL_CONTRAPARTIDA_CONV", df["VL_CONTRAPARTIDA_CONV"].cast("double"))
    # df = df.withColumn("VL_GLOBAL_CONV", df["VL_GLOBAL_CONV"].cast("double"))
    # df = df.withColumn("ID_IRFE_PMBR", df["ID_IRFE_PMBR"].cast("integer"))
    # df = df.withColumn("ID_SETORIALISTA", df["ID_SETORIALISTA"].cast("integer"))
    # df = df.withColumn("VL_RENDIMENTO_AUTORIZADO", df["VL_RENDIMENTO_AUTORIZADO"].cast("double"))

    # Adiciona a coluna de índice
    df = df.withColumn("INDICE_IRFES_SME", monotonically_increasing_id() + 1)
    outuput_dir_path = 'data/interim/'
    outputFile = outuput_dir_path + filename
    df.write.format("parquet").mode('overwrite').save(outputFile)
    print (f'Arquivo parquet gravado em: {outputFile}')

    # Exibe o DataFrame resultante
    df.show()

    # Encerra a sessão Spark
    spark.stop()

    #df2 = spark.read.options(delimiter=";", inferSchema="true", header=True).parquet(outputFile)
    #df2=spark.read.parquet(outputFile)
    #df2.createOrReplaceTempView("TmpTable")
    #qdf2 = spark.sql("select * from TmpTable where `tmptable`.`IRFE.CODIGO_IRFE` >= 1000")
    #qdf2.show()

# Execute a função main() definida acima se o script tiver sido chamado para execução, e não apenas tiver sido
# importado como módulo em outro script, caso em que não queremos executar main ()
# https://www.alura.com.br/artigos/o-que-significa-if-name-main-no-python
if __name__ == '__main__':
   main()
