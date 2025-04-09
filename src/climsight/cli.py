import argparse
import logging
import os
import yaml

from terminal_interface import run_terminal

# FIXME the code of the following functions was copied from climsight.py
#  -- to be refactored further
#---

def get_config():
    config = {}
    logger = logging.getLogger(__name__)
    # reading configuration file
    if not config:
       config_path = os.getenv('CONFIG_PATH', 'config.yml')
       logger.info(f"reading config from: {config_path}")
       try:
          with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
       except Exception as e:
          logging.error(f"An error occurred while reading the file: {config_path}")
          raise RuntimeError(f"An error occurred while reading the file: {config_path}") from e
    return config


def setup_logging():
    logging.basicConfig(
       filename='climsight.log',
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       datefmt='%Y-%m-%d %H:%M:%S'
    )


def check_config(config):
    # preliminary check config file   
    try:
       model_name = config['model_name']
       climatemodel_name = config['climatemodel_name']
       llmModeKey = config['llmModeKey'] 
       data_path = config['data_settings']['data_path']
       coastline_shapefile = config['coastline_shapefile']
       haz_path = config['haz_path']
       pop_path = config['pop_path']
       distance_from_event = config['distance_from_event']
       lat_default = config['lat_default']
       lon_default = config['lon_default']
       year_step = config['year_step']
       start_year = config['start_year']
       end_year = config['end_year']
       system_role = config['system_role']
       rag_settings = config['rag_settings']
       embedding_model = rag_settings['embedding_model']
       chroma_path_ipcc = rag_settings['chroma_path_ipcc']
       chroma_path_general = rag_settings['chroma_path_general']
       document_path = rag_settings['document_path']
       chunk_size = rag_settings['chunk_size']
       chunk_overlap = rag_settings['chunk_overlap']
       separators = rag_settings['separators']
       rag_activated = rag_settings['rag_activated']
       rag_template = config['rag_template']
    except KeyError as e:
       logging.error(f"Missing configuration key: {e}")
       raise RuntimeError(f"Missing configuration key: {e}")
    

def get_references():
    logger = logging.getLogger(__name__)
    references = {'references': {}, 'used': []}
    # reading references file
    if not references:
       references_path = 'references.yml'
       logger.info(f"reading references from: {references_path}")
       try:
          with open(references_path, 'r') as file:
                references = yaml.safe_load(file)
                references['used'] = []
       except Exception as e:
          logging.error(f"An error occurred while reading the file: {references_path}")
          raise RuntimeError(f"An error occurred while reading the file: {references_path}") from e
    return references

#---

def parse_arguments(config):
    parser = argparse.ArgumentParser(
        description='ClimSight command-line interface')
    parser.add_argument(
        '--lat', type=float, default=config['lat_default'], help='latitude')
    parser.add_argument(
        '--lon', type=float, default=config['lon_default'], help='longitude')
    parser.add_argument('--msg', default='', help='user message')
    parser.add_argument('-o', '--output-file')
    return parser.parse_args()

def run():

    # FIXME calling the functions with the code copied from climsight.py
    # ---
    setup_logging()
    config = get_config()
    check_config(config)
    chroma_path = [config['rag_settings']['chroma_path_ipcc'],
                   config['rag_settings']['chroma_path_general']]
    references = get_references()
    # ---
    
    args = parse_arguments(config)
    output = run_terminal(config, api_key='', skip_llm_call=False,
                 lon=args.lon, lat=args.lat,
                 user_message=args.msg,
                 show_add_info='n', rag_activated=True, verbose=False,
                 embedding_model=config['rag_settings']['embedding_model'],
                 chroma_path=chroma_path, references=references)
    if args.output_file:
        with open(args.output_file, 'w+') as fp:
            fp.write(output)
    else:
        print(output)

if __name__ == '__main__':
    run()

