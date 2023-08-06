#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
https://blog.starmeow.cn/detail/6c9882bbac1c7093bd25041881277658/

@Version :   Ver0.1
@Author  :   StarMeow
@License :   (C) Copyright 2018-2020, blog.starmeow.cn
@Contact :   starmeow@qq.com
@Software:   PyCharm
@File    :   starmeow_cryptor.py
@Time    :   2020/2/11 13:50
@Desc    :   加解密文本，生成License文件，客户端校验license.cli，该文件放在客户端上需进行加密，不可支持反编译
"""

import string
import random
import json
import os
import datetime
import socket
import base64
from Crypto.Cipher import AES
import netifaces
from cinirw.cinirw_ import ReadConfigIni

"""
Python库 ：pip install pycrypto netifaces

说明：
1、AES使用的密钥保存在随机变量名中，不易被外部获取。
2、AES加密和解密字符串。
3、根据获取的mac地址明文AES生成密文，使用该密文及其他信息整合到json中，通过AES加密成密文，保存到License文件中。
4、其他程序调用校验License文件，如果校验通过则返回True，否则返回False。
    1、判断硬件信息。
    2、判断授权时间。
5、本文件运行到客户端时，需要对其编译，让其不可读，然后在程序入口非源码文件中放置判断程序。

# 验证license调用方法示例，需要关联starmeow_cryptor.py中的check_license
from starmeow_cryptor import check_license

# 检查生成的License是否正确
if check_license():
    print('程序继续运行！')
else:
    print('程序授权终止，退出！')
"""

# __all__属性，可用于模块导入时限制，如：from module import *，此时被导入模块若定义了__all__属性，
# 则只有__all__内指定的属性、方法、类可被导入。若没定义，则导入模块内的所有公有属性，方法和类 。
__all__ = ['check_license']


def generate_random_str(num):
    # 生成随机字母数字字符串
    key = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return key


# secret_key = generate_random_str(32)
# print('KEY：', secret_key, '（妥善保管，勿泄露！）')

# 添加一段随机字符串的含义：代码加密后，导入包时不会自动显示该变量，防止从其他文件中import猜测获取该值
__random_str = generate_random_str(5)  # 生成一个随机字符串
exec('__{0}_secret_key_{0} = "{1}"'.format(__random_str, "nctd7PpjhSkTHEmfOaxyZKsVY5M0IgXD"))  # 使用随机字符串作为变量名，不易猜测的变量名
# 使用该变量： globals().get('__{0}_secret_key_{0}'.format(__random_str)) ，如果要替换变量名，本文件全文替换 __{0}_secret_key_{0} 字符串

lic_dir = os.getcwd()  # 指定包含license的目录
lic_file = os.path.join(lic_dir, 'starmeow_license.lic')


# 字符串补位
def add_to_16(v):
    # 不足16位并返回bytes
    while len(v) % 16 != 0:
        v = v + "\0"
    # return v.encode('utf-8')
    return v


# 字符串AES加解密
class AESEncryptDecrypt(object):
    def __init__(self, key):
        self.__key = key
        self.__mode = AES.MODE_ECB

    # AES加密
    def encrypt(self, data):
        """
        str =(aes编码)=> bytes =(base64编码)=> bytes =(utf-8解码)=> str
        :param data:
        :return:
        """
        data = add_to_16(data)  # 字符串补位 <class 'str'>
        # print('补位：', data, '|end')
        cipher = AES.new(self.__key, self.__mode)

        encrypt_data = cipher.encrypt(data)  # encrypt_data:<class 'bytes'>  AES编码
        encrypt_data = base64.b64encode(encrypt_data)  # encrypt_data:<class 'bytes'>  base64编码，参数为bytes类型
        encrypt_data = encrypt_data.decode('utf-8')  # encrypt_data:<class 'str'>  使用utf-8解码成字符串
        return encrypt_data

    # AES解密
    def decrypt(self, encrypt_data):
        """
        str =(base64解码)=> bytes =(aes解码)=> bytes =(utf-8编码)=> str
        :param encrypt_data:
        :return:
        """
        cipher = AES.new(self.__key, self.__mode)

        encrypt_data = base64.b64decode(encrypt_data)  # <class 'bytes'>
        decrypt_data = cipher.decrypt(encrypt_data)  # <class 'bytes'>
        decrypt_data = decrypt_data.decode('utf-8')  # <class 'str'>
        decrypt_data = decrypt_data.rstrip('\0')
        return decrypt_data


# MAC地址管理，返回明文的mac地址
class GetMacAddress(object):
    def __init__(self):
        self.ip = ''
        self.__mac = ''

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('114.114.114.114', 80))
            self.ip = s.getsockname()[0]
        finally:
            s.close()

    def get_mac_address(self):
        # 根据指定的ip地址获取mac：00:50:56:c0:00:08
        for i in netifaces.interfaces():
            # print(i)
            addrs = netifaces.ifaddresses(i)
            try:
                # print(addrs[netifaces.AF_LINK], addrs[netifaces.AF_INET])
                if_mac = addrs[netifaces.AF_LINK][0]['addr']
                if_ip = addrs[netifaces.AF_INET][0]['addr']
                if if_ip == self.ip:
                    self.__mac = if_mac
                    break
            except KeyError:
                pass

    def mac(self):
        self.get_ip_address()
        self.get_mac_address()
        return self.__mac


# license管理工具，传递dict数据，生成密文到文件；校验密文返回True、False
class LicenseManager(object):
    def __init__(self, lic_file, key, dict_data=None):
        if dict_data is None:
            dict_data = {}
        self.lic_file = lic_file
        self.dict_data = dict_data  # 需要加密的dict类型数据
        self.aes_crypt = AESEncryptDecrypt(key=key)

    def generator(self):
        data = json.dumps(self.dict_data)
        # print('原文json：', data, type(data))

        encrypt_data = self.aes_crypt.encrypt(data)
        # print('加密：', encrypt_data)

        with open(self.lic_file, "w+") as lic:
            lic.write(encrypt_data)
            lic.close()
            print('生成License完成！请将生成的 {} 复制到客户端。'.format(os.path.basename(self.lic_file)))

    def calibrator(self):
        obj = GetMacAddress()
        mac = obj.mac()  # 明文的mac地址
        encrypt_code = self.aes_crypt.encrypt(mac)  # AES加密后的mac

        if os.path.exists(self.lic_file):
            with open(self.lic_file) as lic:
                encrypt_data = lic.read()
                lic.close()
        else:
            print('Error......license.lic文件不存在！如未获取License，请将   {}   发给管理员获取授权。'.format(encrypt_code))
            return False

        try:
            decrypt_data = self.aes_crypt.decrypt(encrypt_data)
            # print('解密：', decrypt_data)
        except Exception as e:
            # print(e)
            decrypt_data = '{}'
        dict_data = json.loads(decrypt_data)
        # print('原文dict：', dict_data, type(dict_data))

        # 验证是否是本机mac的授权

        if dict_data.get('unique_code') != encrypt_code:
            print('Error......非本机授权！请检查是否更换硬件，将   {}   发给管理员重新获取授权。'.format(encrypt_code))
            return False

        # 终生授权
        if dict_data.get('life_time') is True:
            return True
        # 非终生授权，在指定日期中可用
        try:
            today_date = datetime.datetime.today()
            start_date = datetime.datetime.strptime(dict_data['start_date'], "%Y-%m-%d")
            end_date = datetime.datetime.strptime(dict_data['end_date'], "%Y-%m-%d")
            if dict_data.get('life_time') is False and start_date < today_date < end_date:
                return True
            else:
                print('Error......程序未在授权时间内使用！')
                return False
        except Exception as e:
            pass
        return False


# 其他程序调用license校验
def check_license():
    """
    专用于其他程序调用
    :return: True or Flase，表明license是否检测通过
    """
    lic_manager = LicenseManager(lic_file, globals().get('__{0}_secret_key_{0}'.format(__random_str)))
    return lic_manager.calibrator()


if __name__ == '__main__':
    # mac = '11:22:33:44:55'  # 用户所在计算机的mac地址

    # encrypt_code = 'lXJ45GPb5n23peNLSS0EkJOlBHlZdCDSZZwSnLbTvSs='  # 用户发来的是加密后的唯一识别码（mac、主板ID、硬盘ID、CPU ID等），用于生成license
    # encrypt_code = 'AwT+qvY3nXuRJFQfs8dszhonEmaeQb2vatHqcxGRryw='  # USER

    pathdlicense = "." + os.sep + "CADP_license_" + ".ini"

    DoConfigIni = ReadConfigIni(pathdlicense)
    LicenseEC = DoConfigIni.getConfigValue("License", "encrypt_code")
    print("LicenseEC: ", LicenseEC)

    LicenseSD = DoConfigIni.getConfigValue("License", "start_date")
    print("LicenseSD: ", LicenseSD)
    LicenseED = DoConfigIni.getConfigValue("License", "end_date")
    print("LicenseED: ", LicenseED)

    data = {
        'unique_code': LicenseEC,
        'name': 'ProjectName',
        'life_time': False,  # 终生有效，如果为False，首先开始---结束时间
        'start_date': LicenseSD,  # 开始时间
        'end_date': LicenseED,   # 结束时间
        'create_date': datetime.datetime.now().strftime('%Y-%m-%d'),  # 生成时间
    }

    # 生成license
    lic_manager = LicenseManager(lic_file, globals().get('__{0}_secret_key_{0}'.format(__random_str)), data)  # 生成license文件
    lic_manager.generator()
    print('---' * 20)

    # 验证license
    lic_manager = LicenseManager(lic_file, globals().get('__{0}_secret_key_{0}'.format(__random_str)))
    print('验证解密过程，程序是否运行：', lic_manager.calibrator())

