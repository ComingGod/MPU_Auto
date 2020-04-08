import pytest
import os
import sys
import logging
import Tkinter as tk

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\', '/')
sys.path.append(main_path)


from common import log
from common import serialspawn
from common import image_download
import subprocess


def messagebox():
    top = tk.Tk()
    top.mainloop()
    print '111111'

class TestemmcBoot:
    @pytest.fixture(autouse=True)
    def setup(self, request, cfg):
        #sall the paramaters got from config.yaml
        self.config = cfg
        self.image = image_download.ImageDownload(self.config['UUU']['path'])

        def teardown():
            pass
        request.addfinalizer(teardown)
        
    def test_emmc_boot_image_cm4_ddr(self):
        messagebox()
        #download image
        self.image.download_image('test_emmc_boot_image_cm4_ddr', 'emmc', SDPimage = self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['cm4_ddr'])
        messagebox()
        #checking boot expectation
        spawn = serialspawn.SerialSpawn(self.config['COM']['CM4'], self.config['COM']['CM4_baudrate'])
        spawn.find('hello', timeout = 10)
        spawn.close()

    def test_emmc_boot_image_cm4_tcm(self):
        messagebox()
        #download image
        self.image.download_image('test_emmc_boot_image_cm4_tcm', 'emmc', SDPimage = self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['cm4_tcm'])
        messagebox()
        #checking boot expectation
        spawn = serialspawn.SerialSpawn(self.config['COM']['CM4'], self.config['COM']['CM4_baudrate'])
        spawn.find('hello', timeout = 10)
        spawn.close()

    def test_emmc_boot_image1_invalid_SECO_container_image2_uboot(self):
        messagebox()
        #download image
        self.image.download_image('test_emmc_boot_image1_invalid_SECO_container_image2_uboot', 'emmc', SDPimage = self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['invalid_seco_container'], bootImage2 = self.config['Image']['serial_download'])
        messagebox()
        #checking boot expectation
        spawn = serialspawn.SerialSpawn(self.config['COM']['uBoot'], self.config['COM']['uBoot_baudrate'])
        spawn.find('Hit any key to stop autoboot', timeout = 5)
        spawn.close()


if __name__ == '__main__':
      # pytest.main(['-v', '-s'])
    import subprocess
    pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
    subprocess.call([pytest, '-v' ,'-s', 'test_emmc_boot.py::TestemmcBoot::test_emmc_boot_image_cm4_ddr' ])
    # pytest.main(['-v', '-s'])

