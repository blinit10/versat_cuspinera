# import multiprocessing
# import os
#
# import webview
# import wmi
#
#
# def on_closing(thread):
#     pass
#
#
# if __name__ == '__main__':
#     process = multiprocessing.Process(target=os.system('start cmd /k "cd /d C:\\venv\\scripts & activate & cd /d C:\\Users\\Blinit10\\PycharmProjects\\versat_cuspinera & python manage.py runserver 0.0.0.0:9595"'), args=[])
#     process.start()
#     pid = process.pid
#     window = webview.create_window('Versat Y', 'http://127.0.0.1:9595/admin', fullscreen=True, frameless=False,
#                                    confirm_close=True)
#     window.events.closing += on_closing(os.system('"taskkill /pid ' + str(pid) + ' /F /T"'))
#
#     webview.start()
import os
import sys
import time
from threading import Thread
import webview
from screeninfo import get_monitors


def start_webview():
    # window = webview.create_window('Versat Y', 'http://localhost:9595/admin', confirm_close=True, width=900, height=600)
    window = webview.create_window('Versat Y', 'http://localhost:9595/admin', confirm_close=True, fullscreen=False,
                                   frameless=False, width=get_monitors()[0].width, height=get_monitors()[0].height - 50)
    webview.start()
    window.closed = os._exit(0)


def start_startdjango():
    if sys.platform in ['win32', 'win64']:
        os.system("python manage.py runserver {}:{}".format('127.0.0.1', '9595'))
        # time.sleep(10)
    else:
        os.system("python3 manage.py runserver {}:{}".format('127.0.0.1', '9595'))
        # time.sleep(10)


if __name__ == '__main__':
    Thread(target=start_startdjango).start()
    start_webview()