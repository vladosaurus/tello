from .tello import Tello
import sys
from datetime import datetime
import time

start_time = str(datetime.now())

def movements(x, y, z, speed):
    return f'go {x} {y} {z} {speed}'

def angles(t_mov, degr):
    """
    If input is string('cw'/'ccw') use var degr
    """
    return {
            'cw': f'cw {degr}',
            'ccw': f'ccw {degr}'
    }.get(t_mov, 'Incorrect command')

def no_params(t_mov):
    """
    Input for this function is single param (command, takeoff, land)
    """
    return{
            'command': f'command',
            'takeoff': f'takeoff',
            'land': f'land',
    }.get(t_mov, 'Incorrect command')

#file_name = sys.argv[1]

tello = Tello()
with open('command.txt', 'r') as txt:
    commands = txt.readlines()
    clean_cmds = [w.strip() for w in commands]

    for clean_cmd in clean_cmds:
        if len(clean_cmd.split()) == 1:
            # tello.send_command(command(bytes(no_params(clean_cmd), 'utf-8')))
            tello.send_command(no_params(clean_cmd))

        elif len(clean_cmd.split()) == 2:
            cmd, num = clean_cmd.split()
            if cmd in ['cw', 'ccw']:
                # tello.send_command(command(bytes(angles(cmd, num), 'utf-8')))
                tello.send_command(angles(cmd, num))

        elif len(clean_cmd.split()) == 5:
            cmd, x, y, z, speed = clean_cmd.split()
            # tello.send_command(command(bytes(movements(x, y, z, speed), 'utf-8')))
            tello.send_command(movements(x, y, z, speed))

log = tello.get_log()

out = open('log/' + start_time + '.txt', 'w')
for stat in log:
    stat.print_stats()
    str = stat.return_stats()
    out.write(str)
