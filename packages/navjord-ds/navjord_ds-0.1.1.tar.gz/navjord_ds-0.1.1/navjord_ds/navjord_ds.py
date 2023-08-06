"""Main module."""

import urllib.request as request
from urllib.parse import urlencode

import numpy as np

class Logger(object):
    # https://shantanum91.github.io/kagglewatch/
    CHANNEL_NAME = 'my-channel'

    def __init__(self):
        self.terminal = sys.stdout

    def write(self, message):
        if message != '\n':
            self.terminal.write(message + '\n')
            payload = {'msg': message}
            quoted = urlencode(payload)
            thr = threading.Thread(target=self.send, args=(quoted,), kwargs={})
            thr.start()

    def flush(self):
        pass

    @staticmethod
    def send(msg):
        msg = 'https://dweet.io/dweet/for/' + Logger.CHANNEL_NAME + '?' + msg
        try:
            request.urlopen(msg).read()
        except Exception as e:
            sys.stdout.terminal.write(e)


def print_shapes(*args):
    for var in vars()["args"]:
        print(var.shape)

def print_channels(img):
    n_channels = img.shape[2]
    fig, ax = plt.subplots(1, n_channels+2, figsize=(12, 12))

    for i in range [n_channels]:
        ax.imshow(img)
        ax.title.set_text(f'Channel {i}')
        ax.set_xticks([])
        ax.set_yticks([])
        
    ax[n_channels].imshow(img)
    ax[n_channels].title.set_text("Full image")

if __name__ == '__main__':

    x = np.array([1, 2, 3])
    y = np.array([[1], [2]])

    print_shapes(x, y)