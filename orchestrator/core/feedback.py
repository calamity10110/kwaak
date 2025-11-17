
import asyncio
import itertools
import sys

class ConsoleFeedback:
    def __init__(self):
        self.spinner_task = None

    async def _spinner(self, message: str):
        for char in itertools.cycle(['|', '/', '-', '\\']):
            sys.stderr.write(f'\r{message} {char}')
            sys.stderr.flush()
            await asyncio.sleep(0.1)

    def start_spinner(self, message: str):
        self.spinner_task = asyncio.create_task(self._spinner(message))

    def stop_spinner(self, success: bool, final_message: str):
        if self.spinner_task:
            self.spinner_task.cancel()
            sys.stderr.write('\r')
            if success:
                sys.stderr.write(f"✅ {final_message}\n")
            else:
                sys.stderr.write(f"❌ {final_message}\n")
            sys.stderr.flush()

    def print_message(self, message: str):
        sys.stderr.write(f"{message}\n")
        sys.stderr.flush()
