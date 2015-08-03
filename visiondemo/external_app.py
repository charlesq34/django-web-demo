import os
import Image
import ImageFilter
import time
import glob


while 1:
    while len(glob.glob('media/*.query.done')) == 0:
        time.sleep(1)
        pass
    im = Image.open('media/tmp.jpg')
    im = im.filter(ImageFilter.BLUR)
    im.save('media/tmp_out.jpg')
    fname = glob.glob('media/*.query.done')
    print fname
    fname = fname[0].strip('.query.done')
    open(fname+'.result.done','w').close()
    qfnames = glob.glob('media/*.query.done')
    for f in qfnames:
        os.remove(f)
