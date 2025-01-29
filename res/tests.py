import os
import glob

from k_means import *

# correct convertation
def fir():
    path = '..\\temp\\*.jpg'
    resp = []
    for file in glob.glob(path, recursive=True):
        resp.append(processing(file))
    return resp

# correct save img
def sec():
    resp = fir()
    k = 0
    print(os.getcwd())
    for i in resp:
        cv2.imwrite(os.getcwd() + f'\\{k}.jpg', i[1])
        k += 1

sec()