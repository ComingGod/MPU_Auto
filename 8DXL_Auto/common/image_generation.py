#coding:utf-8
import os
import subprocess
# import log
import logging

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')


class ImageGeneration(object):
    """docstring for Ser"""
    def __init__(self, tool):
        self.tool = tool

    def generate_flexspi_image(self,vendor,pad,is_ddr,is_32bit,patch_offset,freq,ifile,ofile):
        #generate image restore folder
        if not os.path.exists(os.path.dirname(ofile)):
            os.makedirs(os.path.dirname(ofile))

        cmd = [self.tool, 'norDeviceInfo=vendor:{},pad:{},is_ddr:{},is_32bit:{} patch_offset={} serialClkFreq={} ifile={} ofile={}'.format(vendor,pad,is_ddr,is_32bit,patch_offset,freq,ifile,ofile)]
        cmd = ' '.join(cmd)
        logging.info(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(process.communicate()[0])
        assert process.returncode == 0


if __name__ == "__main__": 
    tool = r'D:\Git_repo\rom_validation\8DXL_Auto\tool\flexspi_config_util.exe'
    image_file = 'D:/Git_repo/rom_validation/8DXL_Auto/image/flexspi/1M.bin'
    input_file = r'D:\Git_repo\rom_validation\8DXL_Auto\image\unsigned_flexspi_scfw_cm4_flexspi_uboot.bin'
    gen_img = ImageGeneration(tool)
    print gen_img.generate_flexspi_image(vendor='micron', pad='octal', is_ddr=1, is_32bit=1, patch_offset=0x400, freq=1, ifile=input_file, ofile=image_file)





  