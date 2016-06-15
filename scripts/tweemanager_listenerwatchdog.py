# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import psutil
import pprint
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def getConfigFiles(path):
    """
    given a path returns all available configuation files.
    """
    endpatterns = ('.json', '.cfg', '.ini')
    if os.path.isdir(path):
        cfgfilelist = filter(lambda x: x if x.endswith(endpatterns) else False, os.listdir(path))
    else:
        cfgfilelist = []
    return cfgfilelist


def getProcessesByCfgfiles(cfgfiles):
    """
    given a list of configuration files returns process associated to if if any.
    """
    processes = list(psutil.process_iter())
    result = []
    for cfgfile in cfgfiles:
        cfgresult = {'cfgfile': cfgfile, 'cfgfullpath': os.path.abspath(cfgfile), 'cmdline': None, 'running': None, 'pid': None}
        try:
            for proc in processes:
                if any(cfgfile in word for word in proc.cmdline()):
                    cfgresult = {'cfgfile': cfgfile, 'cfgfullpath': os.path.abspath(cfgfile), 'cmdline': proc.cmdline(), 'running': proc.status(), 'pid': proc.pid}
        except:
            pass
        result.append(cfgresult)
    return result


def startProcess(cfgdata):
    """
    cfgdata
    {'cfgfile': cfgfile, 'cfgfullpath': os.path.abspath(cfgfile), 'cmdline': None, 'running': None, 'pid': None}
    """
    cfgfile = cfgdata['cfgfullpath']
    logging.info('process is starting {}'.format(' '.join(['tweemanager', 'listener', '-c', cfgfile, '-o', 'mongodb', '&'])))
    os.system(' '.join(['tweemanager', 'listener', '-c', cfgfile, '-o', 'mongodb', '&']))


def stopProcess(cfgdata):
    """
    """
    # psutil.Process(cfgdata['pid']).terminate()
    logging.info('process id {} is stoping'.format(str(cfgdata['pid'])))
    # os.kill(cfgdata['pid'], signal.SIGTERM)
    psutil.Process(cfgdata['pid']).terminate()


def restartProcess(cfgdata):
    """
    """
    stopProcess(cfgdata)
    startProcess(cfgdata)


class ConfigFilesHandler(PatternMatchingEventHandler):
    patterns = ["*.json", "*.cfg", "*.ini"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        pass
        

    def on_modified(self, event):
        logging.info("Modified")
        cfgdata = getProcessesByCfgfiles([event.src_path])
        logging.info(event.src_path)
        logging.info(cfgdata)
        if len(cfgdata) > 0:
            logging.info('Modified Config file {} restarting process id {}'.format(event.src_path,cfgdata[0]['pid']))
            restartProcess(cfgdata[0])
        time.sleep(1)

    def on_created(self, event):
        # logging.info("Modified")
        cfgdata = getProcessesByCfgfiles([event.src_path])
        # logging.info(event.src_path)
        logging.info(cfgdata)
        if len(cfgdata) > 0:
            logging.info('Created Config file {} starting process id {}'.format(event.src_path,cfgdata[0]['pid']))
            if cfgdata[0]['pid']:
                restartProcess(cfgdata[0])
            else:
                startProcess(cfgdata[0])
        time.sleep(1)

    def on_deleted(self, event):
        # logging.info("Dele")
        cfgdata = getProcessesByCfgfiles([event.src_path])
        # logging.info(event.src_path)
        # logging.info(cfgdata)
        if len(cfgdata) > 0:
            logging.info('Deleted Config file {} stopping process id {}'.format(event.src_path,cfgdata[0]['pid']))
            stopProcess(cfgdata[0])
        time.sleep(1)


if __name__ == '__main__':
    # config logging
    # script must be run on the folder containin
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    )
    args = sys.argv[1:]
    path = args[0] if args else '.'
    path = os.path.abspath(path)
    observer = Observer()
    observer.schedule(ConfigFilesHandler(), path=path)
    observer.start()

    try:
        while True:
            time.sleep(1)
            cfgfiles = getConfigFiles(path)
            status = getProcessesByCfgfiles(cfgfiles)
            for process in status:
                if not process['running']:
                    startProcess(process)
    except KeyboardInterrupt:
        observer.stop()
        cfgfiles = getConfigFiles(path)
        status = getProcessesByCfgfiles(cfgfiles)
        #pprint.pprint(status)
        for process in status:
            stopProcess(process)

    observer.join()