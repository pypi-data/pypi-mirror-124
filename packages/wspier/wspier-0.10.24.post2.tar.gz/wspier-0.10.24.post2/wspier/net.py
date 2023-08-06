import os

from wspier.core import Logger

class Piper:
    log = Logger(isNull=True)
    def doubanInstall(self, v):
        if len(v) <= 0:
            self.log.error('安装插件为空！')
            return
        mirror = 'https://pypi.douban.com/simple/'
        self.log.info('正在安装插件： {}'.format(v))
        os.system('pip install {} -i {}'.format(v, mirror))
        self.log.info('安装插件完毕： {}'.format(v))