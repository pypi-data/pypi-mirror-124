from .enc import *
from .help import *


class Lisensi():
    path = "key.enc"
    activation = ""
    lisensi = ""
    base_url = 'https://teak-fin-138114.firebaseio.com'

    def __init__(self,  base_url, key='<ENKRIPSI-KEY>', key_path='lisensi.dat'):
        self.ae = AESCipher(key)
        self.path = key_path
        self.base_url = base_url
        self.load()

    def load(self):
        try:
            with open(self.path, "rb") as fb:
                self.data: str = self.ae.decrypt(fb.read())
                self.lisensi, self.activation = self.data.split("\n")
        except:
            pass

    def save(self):
        data = "%s\n%s" % (self.lisensi, self.activation)
        r = self.ae.encrypt(data)
        with open(self.path, "wb") as fb:
            fb.write(r)
            print(r)

    def check(self):
        if self.activation and self.lisensi:
            if check_offline(self.activation):
                if check_online(self.base_url, self.lisensi, self.activation):
                    return True
        return False

    def new_device(self, lisensi):
        self.activation = get_id()
        self.lisensi = lisensi
        if add_device(self.base_url, self.lisensi, self.activation):
            self.save()
            return True
        return False
