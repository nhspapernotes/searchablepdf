"""
Other template matching methods:

    [
        'cv2.TM_CCOEFF',
        'cv2.TM_CCOEFF_NORMED',
        'cv2.TM_CCORR',
        'cv2.TM_CCORR_NORMED',
        'cv2.TM_SQDIFF',
        'cv2.TM_SQDIFF_NORMED'
    ]

Test results from different methods and with different templates
for identifying different documents
"""

import cv2

def is_ecg(image_path):
    """
    Takes a jpg (or png) image and return True if image represents an ECG
    Returns False if image represents anything else
    """

    template = cv2.imread('./opencv/ecg_tmplt2.png', 0)
    img = cv2.imread(image_path, 0)

    ccoeff_res = cv2.matchTemplate(img, template, eval('cv2.TM_CCOEFF_NORMED'))
    _, cc_max_val, _, _ = cv2.minMaxLoc(ccoeff_res)

    sqdiff_res = cv2.matchTemplate(img, template, eval('cv2.TM_SQDIFF_NORMED'))
    _, sq_max_val, _, _ = cv2.minMaxLoc(sqdiff_res)

    if cc_max_val > 0.35 and sq_max_val < 1.0:
        return True
    else:
        return False
