# -*- coding: utf-8 -*-
#import click
import logging
from pathlib import Path
#from dotenv import find_dotenv, load_dotenv
import subprocess


#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
#def main(input_filepath, output_filepath):
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
# execução como subprocesso adaptado daqui:
# https://sparkbyexamples.com/pyspark/run-pyspark-script-from-python-subprocess/
    spark_submit_str= "spark-submit \
    --master local[4] \
    src/data/MakeDatasetApp.py"
    process=subprocess.Popen(spark_submit_str,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    stdout,stderr = process.communicate()
    if process.returncode !=0:
        print(stderr)
    print(stdout)


    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
 #   load_dotenv(find_dotenv())

    main()
