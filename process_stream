import time
import cv2
import numpy as np
import imutils
from ultralytics import YOLO

from process_truck import TruckProcessor
from object_masking import RegionMasking
from object_region import TruckDetector
from utils import hsv_values
from configs import is_truck_area_l, is_truck_area_r, truck_area_l, truck_area_r, truck_area_detect_mask_l, \
    truck_area_detect_mask_r


def define_mask(new_frame, roi_number):
    """

    :param new_frame:
    :param roi_number:
    :return:
    """
    hsv_lower, hsv_upper = hsv_values(roi_number)
    mask = np.zeros_like(new_frame[:, :, 0])

    # defines the region to detect truck is present at crusher
    # HSV/is_truck values define in configs.py
    if roi_number == 1:
        roi_obj = np.array([is_truck_area_l], dtype=np.int32)
        cv2.rectangle(new_frame, (truck_area_l[0]), (truck_area_l[1]), (255, 255, 255), 1)
    elif roi_number == 2:
        roi_obj = np.array([is_truck_area_r], dtype=np.int32)
        cv2.rectangle(new_frame, (truck_area_r[0]), (truck_area_r[1]), (255, 255, 255), 1)
    else:
        raise ValueError("Invalid ROI number")

    cv2.fillPoly(mask, [roi_obj], 255)
    new_frame_hsv = cv2.cvtColor(new_frame, cv2.COLOR_BGR2HSV)
    new_frame_obj = cv2.inRange(new_frame_hsv, hsv_lower, hsv_upper)
    #
    # if roi_number == 1:
    #     hsv_condition_met = np.any(mask != 0)
    #     print(hsv_condition_met)

    new_frame_obj = cv2.bitwise_and(new_frame_obj, mask)
    mask_roi = np.zeros_like(new_frame_obj)
    cv2.fillPoly(mask_roi, [roi_obj], 255)

    new_frame_obj = cv2.bitwise_and(new_frame_obj, mask_roi)
    new_frame_obj = cv2.erode(new_frame_obj, np.ones((3, 3), np.uint8), cv2.BORDER_REFLECT)
    new_frame_obj = cv2.dilate(new_frame_obj, np.ones((3, 3), np.uint8), cv2.BORDER_REFLECT)

    _, thresholded = cv2.threshold(new_frame_obj, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cnts = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts, thresholded, roi_obj


def run_stream(frame_orig, prev_frame):
    """

    :param cap:
    :return:
    """
    # defines region (the extent) the Mask for 'is_truck'
    # values defined in configs.py
    masking_instance_l = RegionMasking(truck_area_detect_mask_l)
    masking_instance_r = RegionMasking(truck_area_detect_mask_r)
    truck_instance = TruckProcessor()

    back = cv2.createBackgroundSubtractorMOG2()
    f_width = frame_orig.shape[1]
    f_height = frame_orig.shape[0]

    model_path = "../model/dust_detect_20231116.pt"
    model = YOLO(model_path)
    model.to('cuda')

    is_empty = None

    if prev_frame is None:
        prev_frame = frame_orig

    # try:

    # truck left
    thresh_min, thresh_max, roi_is_truck_l = masking_instance_l.masking(prev_frame, frame_orig, back)
    thresh_type = masking_instance_l.threshold(thresh_min, thresh_max)
    truck_instance_l = TruckDetector(thresh_type, f_width, f_height, 'Truck L', roi_is_truck_l)
    frame_is_truck_l, exist_truck_l = truck_instance_l.is_truck(frame_orig)
    frame_roi_l = frame_is_truck_l.copy()

    # truck right
    thresh_min_r, thresh_max_r, roi_is_truck_r = masking_instance_r.masking(prev_frame, frame_orig, back)
    thresh_type_r = masking_instance_r.threshold(thresh_min_r, thresh_max_r)
    truck_instance_r = TruckDetector(thresh_type_r, f_width, f_height, 'Truck R', roi_is_truck_r)
    frame_is_truck_r, exist_truck_r = truck_instance_r.is_truck(frame_orig)
    frame_roi_r = frame_is_truck_r.copy()

    if exist_truck_l:
        c1, mask_l, roi_left = define_mask(frame_roi_l, 1)

        result, is_empty = truck_instance.filter_contours(c1, frame_roi_l, mask_l, roi_left )

    elif exist_truck_r:
        c2, mask_r, roi_right = define_mask(frame_roi_r, 2)
        result, is_empty = truck_instance.filter_contours(c2, frame_roi_r, mask_r, roi_right )

    else:
        result = frame_orig

    cv2.putText(result, 'TV401A PC1 ROM North 2023.11.28-13.00.00', (int(10), int(40)),
                cv2.FONT_HERSHEY_SIMPLEX,
                .5, (255, 255, 255), 1)

    return result


    #
    #
    # except Exception as e:
    #     # sleep 30 seconds for resting loop if stream stops
    #     time.sleep(30)


# def main():
#     cap = cv2.VideoCapture(
#         r'C:\Users\hamibenb\Desktop\Crusher\Carryback\(10.114.237.110) - TV401A PC1 ROM North-2023.11.28-13.00.00-30m00s.mkv')
#
#     run_stream(cap)
#
#
# main()
