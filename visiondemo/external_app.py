import os
from PIL import Image
from PIL import ImageFilter
import time
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DEFINE YOUR FUNCTION HERE
# this is an example, just to filter the image
def process_image(input_img_filename, output_img_filename):
    im = Image.open(input_img_filename)
    im = im.filter(ImageFilter.CONTOUR)
    im.save(output_img_filename)



# ROUNTINE
def run_external_process(input_img_filename, output_img_filename):
    try:
        process_image(input_img_filename, output_img_filename)
        return 1
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print('****')
        print(message)
        return 0

while 1:
    # WAIT ON DIRECTORY CHANGE (by POLLING)
    while 1:
        qfnames = glob.glob(os.path.join(BASE_DIR, 'media/*.query.done'))
        if len(qfnames) > 0:
            break
        else:
            time.sleep(1)

    # ACT ON QUERIES
    print(qfnames)
    for qfname in qfnames:
        tag = qfname.split('/')[-1].split('.')[-3]
        print("qfname: %s, tag: %s" % (qfname, tag))
        input_img_filename = os.path.join(BASE_DIR, 'media/%s_tmp.jpg' % (tag))
        output_img_filename = os.path.join(BASE_DIR, 'media/%s_tmp_out.jpg' % (tag))

        # IMAGE PROCESSING...
        print('start processing %s' % (tag))
        print('input: %s, output: %s' % (input_img_filename, output_img_filename))
        succeed = run_external_process(input_img_filename, output_img_filename)
        print('finish processing %s , return: %s' % (tag, str(succeed)))
        
        if succeed:
            open(os.path.join(BASE_DIR, 'media/%s.result.done' % (tag)),'w').close()
            os.remove(qfname)
        else:
            open(os.path.join(BASE_DIR, 'media/%s.result.err' % (tag)),'w').close()
            os.remove(qfname)
            
