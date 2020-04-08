import logging
import logging.config
import os
import time

# logFile_name = os.environ['logFile_name']
# log_file = main_path + '/Log/' + logFile_name + '_log.txt'


current_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\','/')
log_file = main_path + '/Log/' + current_time +'_log.txt'
log_conf = file_path + '/Config/logging.conf'


if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))
else:
    pass

logging.config.fileConfig(log_conf, defaults=dict(log_file=log_file))


