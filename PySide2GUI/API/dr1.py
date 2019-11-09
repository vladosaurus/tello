#!/usr/bin/env python3
import base64
import inspect
import os
import socket
import subprocess
import sys
import threading
import time

# SDK docs: https://terra-1-g.djicdn.com/2d4dce68897a46b19fc717f3576b7c6a/Tello%20%E7%BC%96%E7%A8%8B%E7%9B%B8%E5%85%B3/For%20Tello/Tello%20SDK%20Documentation%20EN_1.3_1122.pdf
# Create a UDP socket
command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command_sock.bind(('', 9000))
command_address = ('192.168.10.1', 8889)

video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.bind(('', 11111))

cmd_mux = threading.Lock()

# Command sender
def command(msg: bytes, debug=False):
	_f = str(inspect.stack()[0][3])
	cmd_mux.acquire()
	try:
		command_sock.sendto(msg, command_address)
		if debug:
			print(f"{_f}: sent '{msg}'")
	
	except Exception as e:
		print(f"{_f}: error: {e}")
		cmd_mux.release()
		return e
	
	cmd_mux.release()
	return None


# Command receiver
def command_receiver(debug=False):
	_f = str(inspect.stack()[0][3])
	if debug:
		print(f"{_f}: ready")
	
	while True:
		try:
			data = command_sock.recv(32)
			if debug:
				print(f"{_f}: drone response: {data}")
		except Exception as e:
			print(f"{_f}: error: {e}")
			break


# Receive video data from the drone
def video_receiver():
	_f = str(inspect.stack()[0][3])
	print(f"{_f}: ready")
	video_file = None
	filename = f"video-{time.time()}.tmp"
	video_file = open(filename, 'wb')
	while True:
		try:
			data = video_sock.recv(4096)
			video_file.write(data)
		
		except Exception as e:
			print(f"{_f}: error: {e}")
			video_file.close()
		
			# Some video players have trouble playing the file as-is from the drone, so ffmpeg is used to mux it to an mp4 file
			if os.stat(filename).st_size > 0:
					p = subprocess.Popen(['ffmpeg', '-framerate', '30', '-i', filename, '-c', 'copy', f'{filename}.mp4'])
					p.wait()
			os.remove(filename)
			break


# While in command mode, the drone safely lands on its own after not receiving any commands for 15 seconds - this ping prevents that from happenning
def battery_ping(debug=False):
<<<<<<< HEAD
	_f = str(inspect.stack()[0][3])
	while True:
		time.sleep(5)
			if debug:
				print(f"{_f}: sent ping")
			if command(b'battery?', debug=debug) is not None:
				break


=======
    _f = str(inspect.stack()[0][3])
    while True:
        time.sleep(5)
        if debug:
            print(f"{_f}: sent ping")
        if command(b'battery?', debug=debug) is not None:
            break

# VAR. I
>>>>>>> 12ee1ee0533e6d9a28b2edb509f45f7303f734cd
def movements(t_mov, dst):
	"""
	Surprise motherf*cker...
	"""
	return {
		'up': f'up {dst}',
		'down': f'down {dst}',
		'left': f'left {dst}',
		'right': f'right {dst}',
		'forward': f'forward {dst}',
		'back': f'back {dst}',
		'takeoff': f'takeoff',
		'land': f'land'
	}.get(t_mov, 'Incorrect command')
<<<<<<< HEAD


def angles(type_n, degr):
	"""
	If input is string('cw'/'ccw') use var degr
	"""
	return {
			'cw': f'cw {degr}',
			'ccw': f'ccw {degr}'
	}.get(type_n, 'Incorrect command')


def no_params(cmd):
	"""
	Input for this function is single param (command, takeoff, land)
	"""
	return{
			'command': f'command',
			'takeoff': f'takeoff',
			'land': f'land',
	}.get(cmd, 'Incorrect command')
=======
>>>>>>> 12ee1ee0533e6d9a28b2edb509f45f7303f734cd

def angles(type_n, degr):
    """
    Surprise motherf*cker...
    """
    return {
        'cw': f'cw {degr}',
        'ccw': f'ccw {degr}'
    }.get(type_n, 'Incorrect command')

def no_params(cmd):
    return{
        'command': f'command',
        'takeoff': f'takeoff',
        'land': f'land',

    }.get(cmd, 'Incorrect command')

command_thread = threading.Thread(target=command_receiver)
command_thread.start()

video_thread = threading.Thread(target=video_receiver)
video_thread.start()

keep_alive_thread = threading.Thread(target=battery_ping)
keep_alive_thread.start()

if __name__ == "__main__":
<<<<<<< HEAD
	print("=============================================================================")
	print("This tool has been hack(athon)ed together very quickly, use at your own risk.")
	print("=============================================================================")
	print("welcome")

	with open("../../Single_Tello_Test/command.txt", "r") as txt:
		commands = txt.readlines()

		try:
			for task in commands:
				if len(task.split()) == 1:
					command(bytes(no_params(task.strip()), 'utf-8'))
				elif len(task.split()) == 2:
					tmv, prop = task.split()
					if tmv == "cw" or "ccw":
						command(bytes(angles(tmv, prop), 'utf-8'))
					command(bytes(movements(tmv, prop), 'utf-8'))
				else:
					continue

		except KeyboardInterrupt:
				print('closing connections...')
				command_sock.close()
				video_sock.close()
=======
   print("=============================================================================")
   print("This tool has been hack(athon)ed together very quickly, use at your own risk.")
   print("=============================================================================")
   print("welcome")
   # while True:
   #     try:
   #         msg = input("")
   #         if not msg:
   #             continue
   #         # command(bytes(msg, 'utf-8'))
   #         command(bytes(movements(type_m, dist1), 'utf-8'))
   #     except KeyboardInterrupt:
   #         print('closing connections...')
   #         command_sock.close()
   #         video_sock.close()
   #         print('waiting for threads...')
   #         keep_alive_thread.join()
   #         command_thread.join()
   #         video_thread.join()
   #         print('goodbye')
   #         break

f = open("../../Single_Tello_Test/command.txt", "r")
commands = f.readlines()

try:
    for task in commands:
        if len(task.split()) == 1:
            command(bytes(no_params(task.strip()), 'utf-8'))
        elif len(task.split()) == 2:
            tmv, prop = task.split()
            if tmv == "cw" or "ccw":
                command(bytes(angles(tmv, prop), 'utf-8'))
            command(bytes(movements(tmv, prop), 'utf-8'))
        else:
            continue

except KeyboardInterrupt:
    print('closing connections...')
    command_sock.close()
    video_sock.close()

>>>>>>> 12ee1ee0533e6d9a28b2edb509f45f7303f734cd
