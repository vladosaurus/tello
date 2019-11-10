from .tello import Tello
import os
from datetime import datetime

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

    @staticmethod
    def command_go(x, y, z, speed):
       return f'go {x} {y} {z} {speed}'

    @staticmethod
    def command_rotation(t_mov, degr):
        """
        If input is string('cw'/'ccw') use var degr
        """
        return {
            'cw': f'cw {degr}'
        }.get(t_mov, 'Incorrect command')

    @staticmethod
    def command_no_params(t_mov):
        """
        Input for this function is single param (command, takeoff, land)
        """
        return{
            'command': f'command',
            'takeoff': f'takeoff',
            'land': f'land',
        }.get(t_mov, 'Incorrect command')

    #file_name = sys.argv[1]

