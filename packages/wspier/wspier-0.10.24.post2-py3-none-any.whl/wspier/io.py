import logging
import os,sys,shutil
import pathlib

class FileInfo:
    def remove(self,v):
        pass
    def exist(self,v):
        return pathlib.Path(v).exists()
    def create(self,v,c):
        if exit(v):
            return
        with open(v) as writer:
            writer.write(c)
            writer.flush()

'''
文件夹操作方法
'''
class Directory:
    def setLog(self,log):
        self.log = log

    def remove(self,force = False):
        if not os.path.exists(self.BASE_URL):
            return

        self.log.info('删除操作目录 {}'.format(self.BASE_URL))
        if force :
            shutil.rmtree(self.BASE_URL)
        else:
            os.removedirs(self.BASE_URL)

    def rename(self, dist):
        shutil.move(self.BASE_URL, dist)
        self.BASE_URL = dist

    def compress(self, dist, tools = '7zip'):
        zip = Ziper()
        zip.compress(dist, tools= tools)

    def __init__(self, dir):
        self.BASE_URL = dir

'''
压缩解压
'''
class Ziper:
    @classmethod
    def compress(raw, save_dir, tools = '7zip'):
        pass

    @classmethod
    def depress(raw, save_dir, tools='7zip'):
        pass
