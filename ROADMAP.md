# ROADMAP

## Migração Dataflows Power Apps (MICROSOFT) --> Hadoop, Spark, Python e Airflow (PROCERGS): Prova de Conceito

> executar, com Hadoop, Spark, Python e Airflow, as rotinas básicas de ETL automatizadamente a partir dos dados dos tipos de fontes atualmente usadas (arquivos csv zipados via web anônima; arquivos csv via web autenticada no SME e arquivos xlsx via sharepoint ambiente Governo RS), disponbilizando o resultado do processamento dos dados como fonte de dados para Datasets do Power BI no ambiente Governo RS

- [ ] carregar das fontes (todas) e salvar os arquivos (todos os tipos) com Python, no disco local
- [ ] carregar das fontes (todas) e salvar os arquivos (todos os tipos) com Python, no Hadoop (com Spark? possível sem? convém sem?)
- [ ] carregar do Hadoop e salvar no Hadoop tabelas (qual formato usar para o processamento? Spark determina?)
- [ ] disponibilizar tabelas carregadas do Hadoop e conectar como fonte de dados para Datasets do Power BI no ambiente Governo RS (Hive? Json? Outro formato? Tecnologia?)

## Suporte parcial à análise e conciliação

> visualização em página web dos dados combinados inicialmente para efeitos de análise e conciliação (atual relatório Análise e Conciliação DMC)

- [ ] implementar blueprint aec (análise e conciliação), adaptando a partir do blog blueprint (<https://flask.palletsprojects.com/en/2.3.x/tutorial/blog/>)
- blog --> aec

O usuário acessará uma tela contendo referências a todas as análises possíveis. Cada campo comparado é uma análise possível. Postergar.

## Suporte integral à análise e conciliação

> inserção de dados auxiliares resultantes da análise e conciliação (correções e avaliações de pertinência ao escopo, atuais planilhas auxiliares)

## Consolidação da análise de negócio

> visualização em página web dos dados consolidados, tanto para efeitos de suporte operacional quanto para efeitos de análise de negócio (visualizações prototipadas e inicialmente acessadas no Power BI e, quando amadurecidas, migradas para o SIRFE, de modo a aumentar o controle sobre aplicações críticas e a reduzir a dependência das tecnologias proprietárias)

## Algumas tarefas e notas soltas

- ajustar web/schema.sql para novo modelo de dados

A modelagem relacional dos dados será feita no PBI, nos respectivos datasets. Portanto, é suficiente a disponibilização dos dados em formato tabular. Não é necessário um banco de dados relacional. Questões para avaliar: há alguma vantagem em trazer a modelagem relacional para fora, antes do PBI?

Alternativas de saída (qualquer coisa que me entregue dados no formato tabular, que prescinda do gateway?, ambos modos de conexão?):

- Hadoop
- Spark
- ODBC
- HIVE (LLAP)

Para concluir web/src, falta:
adaptar blog para aec <https://flask.palletsprojects.com/en/2.3.x/tutorial/blog/>
testes <https://flask.palletsprojects.com/en/2.3.x/tutorial/tests/>
simular implantação em produção <https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/>
