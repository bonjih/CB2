
# defines region (the extent) the Mask for is_truck
truck_area_detect_mask_l = [450, 400], [450, 200], [500, 200], [500, 400]
truck_area_detect_mask_r = [950, 350], [940, 130], [1000, 130], [1250, 350]

# defines the region to detect truck is present at crusher
is_truck_area_l = [130, 420], [130, 200], [500, 200], [500, 350]
is_truck_area_r = [950, 350], [940, 130], [1250, 130], [1250, 350]

# defines the region of the truck for HSV to detect empty or not
truck_area_l = [450, 400], [500, 200]
truck_area_r = [950, 350], [1000, 130]

# HSV truck right day
hsv_lower_l_d = [0, 38, 0]
hsv_upper_l_d = [179, 255, 255]
# HSV truck left day
hsv_lower_r_d = [0, 35, 0]
hsv_upper_r_d = [179, 255, 255]

# HSV truck right night
hsv_lower_l_n = [0, 0, 0]
hsv_upper_l_n = [179, 58, 255] #[179, 255, 84]
# HSV truck left day
hsv_lower_r_n = [26, 0, 81]
hsv_upper_r_n = [179, 62, 86]

# HSV truck right night full black
hsv_lower_l_n_blk = [0, 0, 0]
hsv_upper_l_n_blk = [86, 255, 255]
# HSV truck left day
hsv_lower_r_n_blk = [26, 0, 81]
hsv_upper_r_n_blk = [179, 62, 86]

