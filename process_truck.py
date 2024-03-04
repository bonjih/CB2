import time
import cv2
import imutils
from imutils import perspective

from utils import calc_area_percent


class TruckProcessor:
    def __init__(self):
        self.empty_count = 0
        self.not_empty_count = 0
        self.start_time = time.time()

    def filter_contours(self, conts, frame_roi, mask, roi_obj):
        is_empty = False  # Flag to indicate if the truck is empty

        for c in conts:
            if cv2.contourArea(c) < 3000:
                continue

            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            box_area, percent = calc_area_percent(tl, tr, bl, c)

            if box_area > 30000:
                cv2.drawContours(frame_roi, [box.astype("int")], -1, (0, 255, 255), 1)
                cv2.putText(frame_roi, 'Empty', (int(tr[0]), int(tr[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (36, 255, 12), 1)
                self.empty_count += 1
                is_empty = True  # Set flag to True if the box_area is greater than 30000

            else:
                cv2.drawContours(frame_roi, [box.astype("int")], -1, (0, 255, 255), 1)
                cv2.putText(frame_roi, 'Not Empty', (int(tr[0]), int(tr[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (36, 255, 12), 1)
                self.not_empty_count += 1

        overlay_l = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        overlay_l[:, :, 1] = 0
        result = cv2.addWeighted(frame_roi, 1, overlay_l, 0.5, 0)
        cv2.polylines(result, [roi_obj], True, (0, 0, 255), 2)

        # Check if 3 seconds have elapsed
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 3:
            # print("Total Empty count in last 5 seconds:", self.empty_count, roi_number)
            # print("Total Not Empty count in last 5 seconds:", self.not_empty_count, roi_number)
            # Reset counters and timer
            self.empty_count = 0
            self.not_empty_count = 0
            self.start_time = time.time()

        return result, is_empty  # Return result and the flag indicating if the truck is empty
