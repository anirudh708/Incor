import os
import signal
import time
from watchdog.events import FileSystemEventHandler
from subprocess32 import Popen,PIPE,call

class EventHandler(FileSystemEventHandler):

    # TODO Add docstrings

    # parentpid = None
    p = None
    lastCall = ''
    fw = None
    # existing_Children = None

    def __init__(self, path):

        self.path = path

    def on_modified(self, event):
        # Checks whether the created event is not a directory event
        if not event.is_directory:
            cur_path = event.src_path
            file_extension = cur_path.split('.')[-1]
            if file_extension == 'py':
                try:
                    self.p.terminate()
                    self.fw.close()
                    print self.lastCall
                    self.p = None
                    time.sleep(1)
                except AttributeError:
                    pass
                finally:
                    self.lastCall = 'python ' + cur_path + ' call terminated'
                    call('clear',shell=True)
                    print('issuing system call - python ' + cur_path)
                    self.fw=open("tmpout","wb")
                    self.p = Popen('python ' + cur_path,stdin=PIPE,stdout=self.fw,stderr=self.fw,shell=True,bufsize=1)


    def on_created(self, event):
        cur_path = ''
        if not event.is_directory:
            cur_path = event.src_path
            file_extension = cur_path.split('.')[-1]
            if file_extension in ['py','cpp','c']:
                name = 'template.' + file_extension
                f_created = open(cur_path, 'rw')
                if f_created.read() == '':
                    for root, dirs, files in os.walk(self.path):
                        if name in files:
                            f = open(os.path.join(root, name))
                            f_created.write(f.read())
                            f.close()
                            break
                f_created.close()
