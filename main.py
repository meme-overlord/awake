import argparse
from enum import Enum
import time
from datetime import datetime

import pyautogui

pyautogui.FAILSAFE = False
DEFAULT_MINUTES_WAKEUP = 3


class State(Enum):
    IDLE = 0
    MOVE = 1
    EXIT = 2


class WakeUp:

    def __init__(self, minutes_to_wait: int, verbose: bool):
        self.state = State.IDLE
        self.timer_seconds = 0
        self.minutes_to_wait = minutes_to_wait or DEFAULT_MINUTES_WAKEUP
        self.exit = False
        self.verbose = verbose or False

    def check_state(self):
        next_state = State.IDLE

        if self.exit is True:
            next_state = State.EXIT

        elif self.state == State.IDLE and self.timer_seconds >= self.minutes_to_wait * 60:
            next_state = State.MOVE

        if self.verbose:
            print(
                f'State: {self.state} - '
                f'Counter: {self.timer_seconds} - '
                f'Timeout: {self.minutes_to_wait * 60} - '
                f'Next State: {next_state}'
            )

        self.state = next_state

    def exec_state(self):
        if self.state == State.EXIT:
            print('Terminating program...')
            exit(0)
        elif self.state == State.MOVE:
            self.move()
            self.timer_seconds = 0

    def move(self):
        if self.verbose:
            print(f'Movement made at {datetime.now().time()}')

        for _ in range(0, 5):
            pyautogui.moveTo(0, _ * 5)
        pyautogui.moveTo(1, 1)
        for _ in range(0, 3):
            pyautogui.press('shift')

    def run(self):
        while True:
            try:
                self.check_state()
                self.exec_state()
                time.sleep(1)
                self.timer_seconds += 1
            except KeyboardInterrupt:
                print('Received exit signal')
                self.exit = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--min', help='Number of minutes between each movement.', type=int)
    parser.add_argument('-v', help='Enables maximum verbosity', action='store_true')
    args = parser.parse_args()
    seconds = 0

    print("Ah, I see that you're based and sleep-on-the-job-pilled as well.")
    print(f"This program will now execute and wake up your computer every {args.min or DEFAULT_MINUTES_WAKEUP} minutes.")
    print('To exit this program just type CTRL+C.')

    wake_up = WakeUp(args.min, args.v)
    wake_up.run()


if __name__ == '__main__':
    main()
