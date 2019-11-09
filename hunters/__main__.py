# -*- coding: utf-8 -*-

"""
Program demonstrating drone movement based on processing its video feed.

Usage:
    hunters battery
    hunters start
    hunters stop
    hunters graylog
"""

from docopt_dispatch import dispatch

from . import logger_service
from .tello import TrackingTello


@dispatch.on("battery")
def battery(**kwargs):
    drone = TrackingTello()
    print(f"Remaining battery: {drone.get_battery()}")


@dispatch.on("start")
def start(**kwargs):
    drone = TrackingTello()
    drone.takeoff_and_start_streaming()
    print("Drone started")


@dispatch.on("stop")
def stop(**kwargs):
    drone = TrackingTello()
    drone.land()
    print("Drone stopped")


@dispatch.on("graylog")
def upload_to_graylog(**kwargs):
    with open("logs.txt", "r") as log_file:
        lines = log_file.read().split("\n")

    logger = logger_service.extra_logger()
    for line in lines[:-1]:
        split_line = line.split(": ")
        task_type = split_line[1].split(" ")[0]
        response = split_line[2]
        logger.info(line, extra={"task_type": task_type, "response": response})


if __name__ == "__main__":
    dispatch(__doc__)
