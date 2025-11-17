
import asyncio
import itertools
import sys
import time

class ConsoleFeedback:
    def __init__(self):
        self.spinner_task = None

    async def _spinner(self, message: str):
        for char in itertools.cycle(['|', '/', '-', '\\']):
            sys.stdout.write(f'\r{message} {char}')
            sys.stdout.flush()
            await asyncio.sleep(0.1)

    def start_spinner(self, message: str):
        self.spinner_task = asyncio.create_task(self._spinner(message))

    def stop_spinner(self, success: bool, final_message: str):
        if self.spinner_task:
            self.spinner_task.cancel()
            sys.stdout.write('\r')
            if success:
                print(f"✅ {final_message}")
            else:
                print(f"❌ {final_message}")
            sys.stdout.flush()

    def print_message(self, message: str):
        print(message)
