import os
import Image
import ImageFilter
import time
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print BASE_DIR
print os.path.join(BASE_DIR, 'media/%s_tmp.jpg' % ("abcdefg"))

def process_image(qfname):
    try:
        tag = qfname.split('/')[-1].strip('.query.done')
        # IMAGE PROCESSING... BEG
        print os.path.join(BASE_DIR, 'media/%s_tmp.jpg' % (tag))
        im = Image.open(os.path.join(BASE_DIR, 'media/%s_tmp.jpg' % (tag)))
        im = im.filter(ImageFilter.BLUR)
        im.save(os.path.join(BASE_DIR, 'media/%s_tmp_out.jpg' % (tag)))
        print 'finish processing %s ' % (tag)
        # IMAGE PROCESSING... END
        open(os.path.join(BASE_DIR, 'media/%s.result.done' % (tag)),'w').close()
    except:
        pass
    os.remove(qfname)

while 1:
    try:
        while 1:
            qfnames = glob.glob(os.path.join(BASE_DIR, 'media/*.query.done'))
            if len(qfnames) == 0:
                time.sleep(1)
                pass
            else:
                break
        print qfnames
        for qfname in qfnames:
            process_image(qfname)
    except:
        pass
