import subprocess
import os
import sys
import time

filePath = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
mainPath = os.path.abspath(os.path.join(filePath, '..')).replace('\\', '/')
sys.path.append(mainPath) # add application path to env


reportLibPath = os.path.abspath(os.path.join(mainPath, 'testReport')).replace('\\', '/')
sys.path.append(reportLibPath)
import process_test_report


log = os.path.abspath(os.path.join(mainPath, 'log/log.xml')).replace('\\', '/')


class Test(object):
    def __init__(self):
        pass
    def run(self):
        # Call all the unit test cases (The test_xxx.py files)
        pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
        subprocess.call([pytest, '-v' ,  '--junitxml=' + log])

    def generate_report(self, report_log):
        test_report = os.path.join(mainPath, 'log/testReport.html')
        process_test_report.TestReportProcessorTool().run([log ,'-o' + test_report])


if __name__ == '__main__':
    test = Test()
    test.run()
    test.generate_report(log)