# ROADMAP

## Migração Dataflows Power Apps ("solução MICROSOFT") --> "solução PROCERGS" como alternativa, no âmbito do SIRFE: Prova de Conceito

Esta prova de conceito investiga a seguinte questão:

> é possível executar, com suporte de serviços disponibilizados ou disponibilizáveis pela PROCERGS as rotinas básicas de ETL do SIRFE atualmente suportadas por serviços disponibilizados pela MICROSOFT, mais especificamente a tecnologia Dataflows do produto Power Apps (oferecida no âmbito da contratação do Office 365)?

O SIRFE é...???

Esta prova de conceito responde afirmativamente esta questão e identifica algumas formas alternativas de solução (como é possível). Esta prova de conceito não avalia a viabilidade das soluções identificadas, sob nenhum ponto de vista, seja técnico, econômico, de estratégia de TIC ou outro.

### Premissas sobre os serviços disponibilizados ou disponibilizáveis pela PROCERGS

1. Hadoop, Spark, Python e Airflow
2. Hospedagem de máquina virtual, serviços isolados, desenvolvimento da solução completa, etc

### Requisitos da solução alternativa

1. A solução deve ser capaz de:
    1. conectar-se a fontes do tipo web, com e sem autenticação, e sharepoint
    2. ler e carregar dados em formato tabular, com tipos de arquivo csv, csv comprimido (zip) e xlsx
    3. gravar dados em formato e disponibilizar conectores compatíveis com o Power Query (Online? Faz diferença?), todos compatíveis com o modo de conectividade import e direct query (importa ter os 2? custo?)
    4. disponibilizar dados no ambiente Governo do RS (nuvem Microsoft, sem necessidade de gateway)
2. Os datasets consolidados devem ser atualizáveis regularmente mediante rotinas agendadas em tempo de execução (admin - e não devel - do sistema), com log e aviso em caso de rotinas com falha (semelhante ao sistema de agendamento do Power BI)

### Tarefas e/ou milestones

> executar, com Hadoop, Spark, Python e Airflow, as rotinas básicas de ETL automatizadamente a partir dos dados dos tipos de fontes atualmente usadas (arquivos csv zipados via web anônima; arquivos csv via web autenticada no SME e arquivos xlsx via sharepoint ambiente Governo RS), disponbilizando o resultado do processamento dos dados (datasets consolidados) como fonte de dados para datasets do Power BI no ambiente Governo RS

- [ ] csvwebanon.py: carregar csv, web anônima, e armazenar em cache, em formato tabular carregável pelo pyspark (parquet?)
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
