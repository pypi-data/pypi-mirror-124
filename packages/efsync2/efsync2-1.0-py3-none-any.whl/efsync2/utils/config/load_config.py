import os
from efsync2.utils.config.get_boto3_client import get_boto3_client
from efsync2.utils.config.load_args_from_yaml import load_args_from_yaml
from efsync2.utils.config.validate_config import validate_config


def load_config(input_args):
    try:
       # efsync2 -cf efsync2.yaml
        if isinstance(input_args, dict) and 'config_file' in input_args and os.path.isfile(input_args['config_file']):
            args = load_args_from_yaml(input_args['config_file'])
        # efsync2('efsync2.yaml')
        elif isinstance(input_args, str) and os.path.isfile(input_args):
            args = load_args_from_yaml(input_args)
        # efsync2 -e -> using clie
        elif isinstance(input_args, dict):
            args = input_args
        # efsync2 -e -> using cli
        else:
            args = input_args
        
        # validate config
        validate_config(args)
        
        args = get_boto3_client(args)
        return args
    except Exception as e:
        print(e)
        raise(e)
