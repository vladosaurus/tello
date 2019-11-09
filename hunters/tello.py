# -*- coding: utf-8 -*-

import threading
import time

import cv2
from easytello.tello import Tello

from .image_processing import find_centroid


class TrackingTello(Tello):
    def __init__(self):
        self.log_file = open("logs.txt", "a+")
        super().__init__()
        self.move_vector = None
        self.known_radius = []

    def __del__(self):
        self.log_file.close()

    def send_command(self, command, query=False):
        """
        :type command: str
        :type query: bool
        """
        try:
            super().send_command(command, query)
            self.log_file.write(f"Command: {command}: {str(self.log[-1].get_response())}\n")
        # Tello library sometimes returns error because it does not handle invalid numeric response properly
        except (ValueError, TypeError) as e:
            print(f"Unexpected error when sending command {command}: {e}")

    def _video_thread_tracking(self):
        capture = cv2.VideoCapture('udp://' + self.tello_ip + ':11111')
        w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(w)
        print(h)
        i = 0
        while True:
            okay, image = capture.read()
            i = i + 1
            if i % 12 == 0:
                cv2.imshow("GreenBallTracker", image)
                if okay:
                    ctr, radius = find_centroid(image)
                    if radius is not None:
                        self.known_radius.append(radius)
                    if not ctr:
                        break
                    if ctr[0] != -1 or ctr[1] != -1:
                        move_x, move_y = w/2-ctr[0], h/2-ctr[1]
                        # print(f"w {ctr[0]}/{w}    h {ctr[1]}/{h}")
                        self.move_vector = (int(move_x), int(move_y))
                        if cv2.waitKey(1) & 0xFF == 27:
                            break
                else:
                    print('Capture failed')
                    break
        capture.release()
        cv2.destroyAllWindows()

    def start_stream(self):
        self.send_command('streamon')
        self.stream_state = True
        self.video_thread = threading.Thread(target=self._video_thread_tracking)
        self.video_thread.daemon = True
        self.video_thread.start()

    def _control_move(self):
        while True:
            if self.move_vector is not None:
                self.move(self.move_vector[0], self.move_vector[1], 0.55)
                self.move_vector = None

    # x: forward
    # y: left
    # z: up
    def move(self, x_pixels: int, y_pixels: int, pixels_to_centimeters_ratio: float):
        x_centimeters = x_pixels * pixels_to_centimeters_ratio
        y_centimeters = y_pixels * pixels_to_centimeters_ratio
        z_centimeters = 0
        if self.known_radius:
            average_radius = sum(self.known_radius) / len(self.known_radius)
            print(f"Average radius: {average_radius}")
            self.known_radius.clear()
            if average_radius < 70:
                z_centimeters = 40 # forward
            elif average_radius > 120:
                z_centimeters = -20 # backwards
        print(f"Move for x {x_centimeters}, y {y_centimeters} and z {z_centimeters}")
        if abs(x_centimeters) < 10:
            x_centimeters = 0
        else:
            x_centimeters = 20 * (x_centimeters / abs(x_centimeters))
        if abs(y_centimeters) < 10:
            y_centimeters = 0
        else:
            y_centimeters = 20 * (y_centimeters / abs(y_centimeters))

        if x_centimeters != 0 or y_centimeters != 0:
            print(f"Move with x{x_centimeters} y{y_centimeters}")
            try:
                height = self.get_height()
                if height is None:
                    return
                if height < 9 and y_centimeters < 0:
                    print(f"Height low and going down: {height} => landing")
                    self.land()
                    return
            except (ValueError, TypeError) as e:
                print(f"Unexpected error when checking height: {e}")

            try:
                self.go(x=z_centimeters, y=x_centimeters, z=y_centimeters, speed=30)
            except (ValueError, TypeError) as e:
                print(f"Unexpected error when moving the drone: {e}")

    # Take off the drone and start streaming
    def takeoff_and_start_streaming(self):
        self.takeoff()
        self.streamoff()
        self.start_stream()
        self.control_thread = threading.Thread(target=self._control_move)
        self.control_thread.start()
        while True:  # Keepalive for the drone
            try:
                battery = self.get_battery()
                if battery is not None:
                    print(f"battery: {battery}")
            except (ValueError, TypeError) as e:
                print(f"Unexpected error when checking battery status: {e}")
            time.sleep(3.0)
