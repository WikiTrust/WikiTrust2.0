import yaml
import os

config = {}
secrets = {}

def norm(path):
    if not path.startswith('/'):
        path = os.path.join(os.path.dirname(__file__), path)
    return path

def setup(config_filename='config_test.yaml', **override):
    global Log
    config.update(yaml.load(open(norm(config_filename))))
    config.update(override)
    secrets.update(yaml.load(open(norm(config['secrets_filename']))))

if __name__ == '__main__':
    setup(config_filename='config_test.yaml')
