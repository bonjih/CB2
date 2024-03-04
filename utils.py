import time

import numpy as np
import datetime

from configs import (hsv_lower_l_d, hsv_upper_l_d, hsv_lower_r_d, hsv_upper_r_d, hsv_lower_l_n_blk, hsv_upper_l_n_blk,
                     hsv_lower_r_n_blk, hsv_upper_r_n_blk)


def get_time_period():
    """
    defines time between day and night for different hsv values
    :return: a time period
    """

    current_time = datetime.datetime.now().time()
    h = current_time.hour

    return h


def hsv_values(roi_number):
    """
    returns specific hsv values for left and right trucks and time of day
    :param roi_number:
    :return: hsv values
    """
    h = get_time_period()

    if 5 <= h <= 18:
        if roi_number == 1:
            hsv_lower = np.array(hsv_lower_l_d)
            hsv_upper = np.array(hsv_upper_l_d)
        elif roi_number == 2:
            hsv_lower = np.array(hsv_lower_r_d)
            hsv_upper = np.array(hsv_upper_r_d)
        else:
            raise ValueError("Invalid ROI number")
        return hsv_lower, hsv_upper
    else:
        if roi_number == 1:
            hsv_lower = np.array(hsv_lower_l_n_blk)
            hsv_upper = np.array(hsv_upper_l_n_blk)
        elif roi_number == 2:
            hsv_lower = np.array(hsv_lower_r_n_blk)
            hsv_upper = np.array(hsv_upper_r_n_blk)
        else:
            raise ValueError("Invalid ROI number")
        return hsv_lower, hsv_upper


def calc_area_percent(tl, tr, bl, C):
    """
    calculaes the percentage/area of the bounding box
    for the purpose of excluding small areas
    :param tl: bb coords top left
    :param tr: bb coords top right
    :param bl: bb coords bottom left
    :param C: bb coords bottom right
    :return: BB area percentage contours fill it
    """
    box_area = (tr[0] - tl[0]) * (bl[1] - tl[1])
    topmost = tuple(C[C[:, :, 1].argmin()][0])
    percent = 1 - ((topmost[1] - 340) / 740)
    return box_area, percent
