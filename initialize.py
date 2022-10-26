import webview

def print_hi(name):
    window = webview.create_window(name, 'http://127.0.0.1:8000/admin', fullscreen=False, resizable=False,
                                   height=900, width=1200, confirm_close=True)
    webview.start()

if __name__ == '__main__':
    print_hi('Versat Y')
