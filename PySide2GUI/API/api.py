from .tello import Tello
import sys
import os
from datetime import datetime
import time

start_time = str(datetime.now())

class API:
    def __init__(self):
        self.tello = Tello()

    def _test_run(self):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'command.txt'), 'r') as txt:
            commands = txt.readlines()
            clean_cmds = [w.strip() for w in commands]

            self.run_commands(clean_cmds)

        log = self.tello.get_log()

        out = open('log/' + start_time + '.txt', 'w')
        for stat in log:
            stat.print_stats()
            str = stat.return_stats()
            out.write(str)
    
    def run_commands(self, commands):
        for cmd in commands:
            self.tello.send_command(cmd)

            # if len(cmd.split()) == 1:
            #     # tello.send_command(command(bytes(no_params(cmd), 'utf-8')))
            #     self.tello.send_command(self.no_params(cmd))

            # elif len(cmd.split()) == 2:
            #     cmd, num = cmd.split()
            #     if cmd in ['cw', 'ccw']:
            #         # tello.send_command(command(bytes(angles(cmd, num), 'utf-8')))
            #         self.tello.send_command(self.command_rotation(cmd, num))

            # elif len(cmd.split()) == 5:
            #     cmd, x, y, z, speed = cmd.split()
            #     # tello.send_command(command(bytes(movements(x, y, z, speed), 'utf-8')))
            #     self.tello.send_command(self.command_go(x, y, z, speed))

    @staticmethod
    def command_go(x, y, z, speed):
       return f'go {x} {y} {z} {speed}'

    @staticmethod
    def command_rotation(t_mov, degr):
        """
        If input is string('cw'/'ccw') use var degr
        """
        return {
            'cw': f'cw {degr}',
            'ccw': f'ccw {degr}'
        }.get(t_mov, 'Incorrect command')

    @staticmethod
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

