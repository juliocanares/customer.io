import sys


def read_arguments():
    num_of_args = len(sys.argv)

    config_filename = sys.argv[1] if num_of_args > 1 else 'configuration.json'
    data_filename = sys.argv[2] if num_of_args > 2 else 'data.json'

    return (config_filename, data_filename)