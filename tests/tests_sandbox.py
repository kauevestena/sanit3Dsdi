import time

a = ['b.img','b.img','b.img','b.img.xml']


for i,entry in enumerate(a):
    

    print(a,'\n',i,'\n',entry)

    time.sleep(1)

    if i < 20:
       a.append(i)



print('\n\n\n',a)