import base64
import inspect
import os
import socket
import subprocess
import sys
import threading
import time

# Create a UDP socket
command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command_sock.bind(('', 9000))
command_address = ('192.168.10.1', 8889)

video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.bind(('', 11111))

cmd_mux = threading.Lock()


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
            if os.stat(filename).st_size > 0:
                p = subprocess.Popen(['ffmpeg', '-framerate', '30', '-i', filename, '-c', 'copy', f'{filename}.mp4'])
                p.wait()
            os.remove(filename)
            break


def battery_ping(debug=False):
    _f = str(inspect.stack()[0][3])

    while True:
        time.sleep(5)
        if debug:
            print(f"{_f}: sent ping")
        if command(b'battery?', debug=debug) is not None:
            break


command_thread = threading.Thread(target=command_receiver)
command_thread.start()

video_thread = threading.Thread(target=video_receiver)
video_thread.start()

keep_alive_thread = threading.Thread(target=battery_ping)
keep_alive_thread.start()

if __name__ == "__main__":
    print("=============================================================================")
    print("This tool has been hack(athon)ed together very quickly, use at your own risk.")
    print("=============================================================================")
    print("welcome")
    while True:
        try:
            msg = input("")
            if not msg:
                continue
            command(bytes(msg, 'utf-8'))

        except KeyboardInterrupt:
            print('closing connections...')
            command_sock.close()
            video_sock.close()

            print('waiting for threads...')
            keep_alive_thread.join()
            command_thread.join()
            video_thread.join()

            print('goodbye')
            break
