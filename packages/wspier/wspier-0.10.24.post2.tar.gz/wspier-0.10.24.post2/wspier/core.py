import pathlib
import sys,os,time,platform
from wspier.io import FileInfo, Directory

'''
日志引擎
'''
class Logger:

    __isNull = False
    @property
    def isEnable(self):
        if self.__isNull:
            return False
        return True

    @property
    def Null(self):
        return Logger(isNull= False)

    def info(self, v):
        if not self.__isNull:
            v = '\n[I] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1;32m {v}\033[0m',end=' ')
            self.__writer.write(v)

    def warn(self, v):
        if not self.__isNull:
            v = '\n[W] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1:33m {v} \033[0m',end=' ')
            self.__writer.write(v)

    def error(self, v):
        if not self.__isNull:
            v = '\n[E] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1:33m {v} \033[0m',end=' ')
            self.__writer.write(v)

    def fatal(self, v):
        if not self.__isNull:
            v = '\n[F] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1;31m {v}\033[0m',end=' ')
            self.__writer.write(v)
            self.__release()
        sys.exit(-1)

    def __release(self):
        self.__writer.flush()
        self.__writer.close()

    def __init__(self,folder = '', isNull = False, banner = False):
        if len(folder) <= 0:
            folder = 'logs'
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.__isNull = isNull
        self.__currentFile = '{}/{}.log'.format(folder,time.strftime('%Y%m%d', time.localtime()))
        self.__writer = open(self.__currentFile, 'a', encoding='UTF-8')
        if banner:
            print('''
$$\  $$\  $$\  $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\  $$$$$$$\  
$$ | $$ | $$ |$$  __$$\ $$  __$$\$$  _____|$$  __$$\ $$  __$$\ $$  __$$\ 
$$ | $$ | $$ |$$ /  $$ |$$ |  \__\$$$$$$\  $$ /  $$ |$$ /  $$ |$$ |  $$ |
$$ | $$ | $$ |$$ |  $$ |$$ |      \____$$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |
\$$$$$\$$$$  |\$$$$$$  |$$ |     $$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |  $$ |
 \_____\____/  \______/ \__|     \_______/  \______/  \______/ \__|  \__|''',end=' ')

'''
配置文件引擎
'''
class ConfigX:
    __data = {}
    __fileInfo = FileInfo()
    def get(self,key):
        return self.__data.get(key=key,default='')
    def set(self,key,value):
        self.__data.update(key=key,value=value)

    def __init__(self, file, provider = 'ini', loadOnce = True, logger = Logger().Null):
        self.__logger = logger
        if len(file) <= 0:
            if self.__logger.isEnable:
                self.__logger.error('致命错误！未找到配置文件，检查配置文件是否存在！')
            else:
                print('致命错误！未找到配置文件，检查配置文件是否存在！')
            exit(-1)

        if not pathlib.Path(file).exists():
            self.__fileInfo.create(v= file, c= "")
        else:
            self.__logger.info('配置文件已存在！')

        self.configFile = file
        self.provider = provider
        self.__logger = logger
'''
扩展
'''
class Convert:
    @classmethod
    def toBase64(self, str, encoding='utf-8'):
        pass

'''
运行时组件
'''
class RuntimeX:
    __info = {}
    @property
    def Runtime(self):
        return self.__info

    def isLinux(self):
        return self.__info['os'] == 'linux'
    def isWindows(self):
        return self.__info['os'] == 'windows'
    def isAmd64(self):
        return self.__info['os'] == 'arm64'
    def isX86(self):
        return self.__info['os'] == 'arm64'
    def isArm(self):
        return False
    def isArm64(self):
        return False

    def __init__(self):
        self.__info['os'] = platform.system().lower()
        self.__info['version'] = platform.version()