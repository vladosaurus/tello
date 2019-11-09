from datetime import datetime


class Stats:
    def __init__(self, command, _id):
        self.command = command
        self.response = None
        self.id = _id

        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None

    def add_response(self, response):
        self.response = response
        self.end_time = datetime.now()
        self.duration = self.get_duration()
        # self.print_stats()

    def get_duration(self):
        diff = self.end_time - self.start_time
        return diff.total_seconds()

    def print_stats(self):
        print(f'\nid: {self.id}')
        print(f'command: {self.command}')
        print(f'response: {self.response}')
        print(f'start time: {self.start_time}')
        print(f'end_time: {self.end_time}')
        print(f'duration: {self.duration}\n')

    def got_response(self):
        return self.response is not None

    def return_stats(self):
        stats_msg = f'\nid: {self.id}\n' \
            f'command: {self.command}\n' \
            f'response: {self.response}\n' \
            f'start time: {self.start_time}\n' \
            f'end_time: {self.end_time}\n' \
            f'duration: {self.duration}\n'
        return stats_msg
