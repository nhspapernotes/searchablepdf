"""
Takes a jpg (or png) image and return True if image represents an ECG
Returns False if image represents anything else
"""

import cv2

def is_ecg(image_path):

    TEMPLATE = cv2.imread('./opencv/ecg_tmplt2.png', 0)

    img = cv2.imread(image_path, 0)
    img2 = img.copy()
    img = img2.copy()

    ccoeff_res = cv2.matchTemplate(img, TEMPLATE, eval('cv2.TM_CCOEFF_NORMED'))
    cc_min_val, cc_max_val, cc_min_loc, cc_max_loc = cv2.minMaxLoc(ccoeff_res)

    sqdiff_res = cv2.matchTemplate(img, TEMPLATE, eval('cv2.TM_SQDIFF_NORMED'))
    sq_min_val, sq_max_val, sq_min_loc, sq_max_loc = cv2.minMaxLoc(sqdiff_res)

    if cc_max_val > 0.35 and sq_max_val < 1.0:
        return True
    else:
        return False
