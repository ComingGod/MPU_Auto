#coding:utf-8
import os
import subprocess
# import log
import logging

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
script_path = os.path.abspath(os.path.join(file_path, '../uuuScript')).replace('\\', '/')
#all the UUU scripts will be stored into the product named foleder, the product name is derived from yaml file
script_path = script_path + '/' + os.environ['PRODUCT'] + '/'
if not os.path.exists(os.path.dirname(script_path)):
    os.makedirs(os.path.dirname(script_path))
else:
    pass


class ImageDownload(object):
    """docstring for Ser"""
    def __init__(self, tool):
        self.tool = tool

    def generate_script(self, scriptName, fuc, SDPimage, bootImage1=None, bootImage2=None):
        script = os.path.join(script_path, scriptName)

        if fuc == 'sd':
            cmd_device = '''FB[-t 40000]: ucmd mmc dev 1
FB[-t 40000]: ucmd mmc erase 0 0x10000\n'''
            if bootImage1:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage1)
                cmd_device = cmd_device + '''FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x40 0x2000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x2000 0x2000\n'

        if fuc == 'emmc':
            cmd_device = '''FB[-t 40000]: ucmd mmc dev 0
FB[-t 40000]: ucmd mmc erase 0 0x10000\n'''
            if bootImage1:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage1)
                cmd_device = cmd_device + '''FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x40 0x2000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x2000 0x2000\n'

        if fuc == 'flexspi':
            cmd_device = '''FB[-t 40000]: ucmd sf probe 0
FB[-t 40000]: ucmd sf erase 0 0x800000\n'''
            if bootImage1:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage1)
                cmd_device = cmd_device + '''FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x0 0x400000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x400000 0x400000\n'

            if bootImage2 and (not bootImage1):
                #for the secondary boot, if image 1 is not exist, need to burn FCB to offset 0x400
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x0 0x1000\n'
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x400000 0x400000\n'

        if fuc == 'flexspi_performance':
            cmd_device = '''FB[-t 40000]: ucmd sf probe 0
FB[-t 40000]: ucmd sf erase 0 0x800000\n'''
            if bootImage1:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage1)
                cmd_device = cmd_device + '''FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x0 0x800000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x400000 0x800000\n'

            if bootImage2 and (not bootImage1):
                #for the secondary boot, if image 1 is not exist, need to burn FCB to offset 0x400
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x0 0x1000\n'
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x400000 0x800000\n'

        if fuc == 'clear':
            cmd_device = '''FB[-t 40000]: ucmd mmc dev 0
FB[-t 40000]: ucmd mmc erase 0 0x10000
FB[-t 40000]: ucmd mmc dev 1
FB[-t 40000]: ucmd mmc erase 0 0x10000
FB[-t 40000]: ucmd sf probe 0
FB[-t 40000]: ucmd sf erase 0 0x800000\n'''

        with open(script, 'w') as f:
            cmd = '''uuu_version 1.2.39
SDPS: boot -f >{}\n'''.format(SDPimage)
            f.write(cmd) 
            f.write('{\n')
            f.write('FB: ucmd setenv fastboot_buffer ${loadaddr}\n')
            f.write(cmd_device)
            f.write('FB: done\n')
            f.write('}')

        return scriptName

    def download_image(self, scriptName, fuc, SDPimage, bootImage1=None, bootImage2=None):
        script = self.generate_script(scriptName, fuc, SDPimage, bootImage1, bootImage2)
        cmd = self.tool + ' -v ' + script
        logging.info(cmd)
        process = subprocess.Popen(cmd, shell=True, cwd=script_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(process.communicate()[0])
        # print process.communicate()[0]
        assert process.returncode == 0


if __name__ == "__main__": 
    image = ImageDownload(r'D:\Git_repo\rom_validation\8DXL_Auto\tool\uuu.exe')
    image.download_image('test', 'sd', SDPimage=r'D:\Git_repo\rom_validation\8DXL_Auto\image\unsigned_scfw_uboot.bin', bootImage1 = r'D:\Git_repo\rom_validation\8DXL_Auto\image\unsigned_scfw_uboot.bin')






  