from matplotlib import pyplot as plt
import numpy as np
if __name__ == '__main__':
    f=open("avrage.txt","r")
    x=f.read()
    array=x.split()
    print(len(array))
    t=np.arange(len(array)/3)
    bests=[]
    worsts=[]
    avg=[]
    for i in range(int(len(array)/3)):
            bests.append(float(array[i*3]))
            worsts.append(float(array[i*3+1]))
            avg.append(float(array[i*3+2]))
    plt.plot(t,bests)
    plt.plot(t,worsts)
    plt.plot(t,avg)
    plt.show()