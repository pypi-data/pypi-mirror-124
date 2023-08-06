import sys,platform
from wspier.core import ConfigX
from wspier.core import RuntimeX
from wspier.core import Logger

log = Logger(isNull=False)

conf = ConfigX(file='E:/app.ini',logger= log)
run = RuntimeX()
print(run.isWindows())