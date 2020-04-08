#coding:utf-8
import os
import subprocess
# import log
import logging

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
script_path = os.path.abspath(os.path.join(file_path, '../uuuScript')).replace('\\', '/')


class ImageDownload(object):
    """docstring for Ser"""
    def __init__(self, tool):
        self.tool = tool

    def generate_script(self, scriptName, device, SDPimage, bootImage1, bootImage2=None):
        script = os.path.join(script_path, scriptName)

        if device == 'sd':
            cmd_device = '''FB[-t 40000]: ucmd mmc dev 1
FB[-t 40000]: ucmd mmc erase 0 0x10000
FB: download -f >{}\n'''.format(bootImage1)
            cmd_device = cmd_device + '''FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x40 0x2000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x2000 0x2000\n'

        if device == 'emmc':
            cmd_device = '''FB[-t 40000]: ucmd mmc dev 0
FB[-t 40000]: ucmd mmc erase 0 0x10000
FB: download -f >{}\n'''.format(bootImage1)
            cmd_device = cmd_device + '''FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x40 0x2000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd mmc write ${fastboot_buffer} 0x2000 0x2000\n'

        if device == 'flexspi':
            cmd_device = '''FB[-t 40000]: ucmd sf probe 0
FB[-t 40000]: ucmd sf erase 0 0x800000
FB: download -f >{}\n'''.format(bootImage1)
            cmd_device = cmd_device + '''FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x0 0x200000\n'''
            #write boot image2 to offset 4M
            if bootImage2:
                cmd_device = cmd_device + '''FB: download -f >{}\n'''.format(bootImage2)
                cmd_device = cmd_device + 'FB[-t 20000]: ucmd sf write ${fastboot_buffer} 0x400000 0x200000\n'

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

    def download_image(self, scriptName, device, SDPimage, bootImage1, bootImage2=None):
        script = self.generate_script(scriptName, device, SDPimage, bootImage1, bootImage2)
        cmd = self.tool + ' -v ' + script
        print cmd
        # print cmd
        process = subprocess.Popen(cmd, shell=True, cwd=script_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(process.communicate()[0])
        # print process.communicate()[0]
        assert process.returncode == 0


if __name__ == "__main__": 
    image = ImageDownload(r'D:\Git_repo\rom_validation\8DXL_Auto\tool\uuu.exe')
    image.download_image('test', 'sd', SDPimage=r'D:\Git_repo\rom_validation\8DXL_Auto\image\unsigned_scfw_uboot.bin', bootImage1 = r'D:\Git_repo\rom_validation\8DXL_Auto\image\unsigned_scfw_uboot.bin')






  