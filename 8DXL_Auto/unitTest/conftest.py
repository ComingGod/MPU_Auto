import pytest
import yaml
import os
import sys
import logging

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\', '/')
print main_path
sys.path.append(main_path)



@pytest.fixture(scope = 'module')
def cfg():
	logging.info('-------------------------conftest-cfg---------------------------------- ')
	config_file = os.path.join(main_path, 'config.yaml')
	with open(config_file, 'r') as f:
		return yaml.safe_load(f)

# @pytest.fixture(scope = 'function')
# def bl():
#     # target_conf = configure()
#     print('this is bl function form conftest')
#     bl = bltest.BootloaderDevice(blhostTool = target_conf['Tool']['Blhost'] , peripheral = 'uart', speed = '57600', port = 'com10')
#     return bl

if __name__ == '__main__':
    target_conf = configure()
    print('--- ' * 30)
    bl = bltest.BootloaderDevice(blhostTool = target_conf['Tool']['Blhost'] , peripheral = 'uart', speed = '57600', port = 'com10')
    bl.fill_memory(0x1c000, 0x10, 0xfe)
    print locals()
    print('x' * 20)
    print (globals())



