# -*- coding: utf-8 -*-

import cv2
import numpy as np

GREEN_LOWER_THRESHOLD = [50, 35, 15]
GREEN_UPPER_THRESHOLD = [80, 255, 255]


def find_centroid(image, color_lower_threshold=None, color_upper_threshold=None, show_image=True, show_mask=False):
    """
    Accepts BGR image as Numpy array

    :type image: numpy.array
    :type color_lower_threshold: None | list[int]
    :type color_upper_threshold: None | list[int]
    :type show_image: bool
    :type show_mask: bool
    :rtype: None | tuple[int, int]
    :returns:
        (x, y) coordinates of centroid if found
        (-1, -1) if no centroid was found
        None if user hit ESC
    """
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    if color_lower_threshold is None:
        color_lower_threshold = GREEN_LOWER_THRESHOLD
    if color_upper_threshold is None:
        color_upper_threshold = GREEN_UPPER_THRESHOLD

    color_lower_threshold = np.array(color_lower_threshold)
    color_upper_threshold = np.array(color_upper_threshold)

    # Threshold the HSV image to get only given colors
    mask = cv2.inRange(hsv, color_lower_threshold, color_upper_threshold)
    bmask = cv2.GaussianBlur(mask, (5, 5), 5)
    circles = cv2.HoughCircles(bmask, cv2.HOUGH_GRADIENT, 3, 10)  # [[Xpos, Ypos, Radius], ...]
    # Assume no centroid
    centroid_coords = (-1, -1)
    radius = None
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # show the first circle
        x, y, radius = circles[0]
        cv2.circle(image, (x, y), radius, (0, 255, 0), 4)

        moments = cv2.moments(bmask)
        m00 = moments['m00']
        centroid_x, centroid_y = None, None
        if m00 != 0:
            centroid_x = int(moments['m10']/m00)
            centroid_y = int(moments['m01']/m00)

        # Use centroid if it exists
        if centroid_x != None and centroid_y != None:
            centroid_coords = (centroid_x, centroid_y)

            # Put black circle in at centroid in image
            cv2.circle(image, centroid_coords, 4, (0, 0, 0))

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (255, 255, 255)
            line_type = 2

            cv2.putText(
                image,
                f"x: {centroid_x}, y: {centroid_y}",
                centroid_coords,
                font,
                font_scale,
                font_color,
                line_type,
            )

    if show_image:
        # Display full-color image
        cv2.imshow("GreenBallTracker", image)
    if show_mask:
        # Display image mask
        cv2.imshow("Image mask", bmask)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        centroid_coords = None

    # Return coordinates of centroid
    return centroid_coords, radius
