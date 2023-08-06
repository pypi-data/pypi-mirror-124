from firemember import lisensi


def testFunction():
    base = 'https://projectname.firebaseio.com'
    l = lisensi.Lisensi(base)
    assert l
    # if not l.check():
    #     k = input("Kode lisensi: ")
    #     if l.new_device(k):
    #         print("Sukses")
    #     else:
    #         print("new device failed")
    # else:
    #     print("sukses login")
    
    # assert l.check()