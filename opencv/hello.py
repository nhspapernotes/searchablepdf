import cv2
import numpy as np

template = cv2.imread('ecg_tmplt2.png',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_SQDIFF_NORMED']

for i in range(4):
    #img = cv2.imread(f'{i+1}.jpg',0)
    img = cv2.imread(f'./ecgs/ECG summary-0{i + 1}.jpg',0)
    img2 = img.copy()
    img = img2.copy()
    
    ccoeff_res = cv2.matchTemplate(img,template,eval('cv2.TM_CCOEFF_NORMED'))
    cc_min_val, cc_max_val, cc_min_loc, cc_max_loc = cv2.minMaxLoc(ccoeff_res)

    sqdiff_res = cv2.matchTemplate(img,template,eval('cv2.TM_SQDIFF_NORMED'))
    sq_min_val, sq_max_val, sq_min_loc, sq_max_loc = cv2.minMaxLoc(sqdiff_res)

    if cc_max_val > 0.35 and sq_max_val < 1.0:
        print('Yes this is an ECG')
    else:
        print('Not an ECG')

    print('--------------')