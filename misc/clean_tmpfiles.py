import glob,os

desiredfolder = '/home/kaue/data/sanit3d_out/temporary'

for filepath in glob.glob(os.path.join(desiredfolder,'*.tmp')):
    print(filepath)
    os.remove(filepath)