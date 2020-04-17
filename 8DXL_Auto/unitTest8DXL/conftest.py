import pytest
import yaml
import os
import sys

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\', '/')
sys.path.append(main_path)



@pytest.fixture(scope = 'module')
def cfg():
	config_file = os.path.join(file_path, 'config.yaml')
	with open(config_file, 'r') as f:
		cfg = yaml.safe_load(f)
		os.environ['PRODUCT'] = cfg['Product']
		return cfg

# @pytest.fixture(scope = 'function')
# def bl():
#     # target_conf = configure()
#     print('this is bl function form conftest')
#     bl = bltest.BootloaderDevice(blhostTool = target_conf['Tool']['Blhost'] , peripheral = 'uart', speed = '57600', port = 'com10')
#     return bl

if __name__ == '__main__':
	pass



