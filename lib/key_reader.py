"""Cross-platform non-blocking key reader for Windows and Linux.

Uses only the Python standard library.
"""

from __future__ import annotations

import os
import queue
import sys
import threading


class KeyReader:
    _key_queue: queue.Queue[str] = queue.Queue()
    _stop_event = threading.Event()
    _thread: threading.Thread | None = None
    _thread_lock = threading.Lock()
    _linux_terminal_lock = threading.Lock()

    @staticmethod
    def _windows_read_key() -> str:
        import msvcrt

        while True:
            key = msvcrt.getch()

            match key:
                case b"\r":
                    return "enter"
                case b"\x08":
                    return "backspace"
                case b"\t":
                    return "tab"
                case b"\x1b":
                    return "escape"
                case b" ":
                    return "space"
                case b"\x03":
                    return "ctrl + c"

            try:
                return key.decode()
            except UnicodeDecodeError:
                if key == b"\xe0":
                    key = msvcrt.getch()
                    if key == b"H":
                        return "up"
                    if key == b"P":
                        return "down"
                    if key == b"K":
                        return "left"
                    if key == b"M":
                        return "right"

    @classmethod
    def _windows_getch(cls) -> str:
        return cls._windows_read_key()

    @classmethod
    def _windows_reader_loop(cls) -> None:
        while not cls._stop_event.is_set():
            key = cls._windows_getch()
            cls._key_queue.put(key)
            if key == "ctrl + c":
                cls._stop_event.set()
                break

    @staticmethod
    def _normalize_key(key: str) -> str:
        match key:
            case "\r" | "\n":
                return "enter"
            case "\x08" | "\x7f":
                return "backspace"
            case "\t":
                return "tab"
            case "\x1b":
                return "escape"
            case " ":
                return "space"
            case "\x03":
                return "ctrl + c"
        return key

    @staticmethod
    def _normalize_linux_arrow(key: str) -> str | None:
        match key:
            case "A":
                return "up"
            case "B":
                return "down"
            case "C":
                return "right"
            case "D":
                return "left"
        return None

    @classmethod
    def _linux_read_key(cls) -> str:
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            next_ch = sys.stdin.read(1)
            if next_ch == "[":
                arrow = cls._normalize_linux_arrow(sys.stdin.read(1))
                if arrow is not None:
                    return arrow
            return "escape"
        return cls._normalize_key(ch)

    @classmethod
    def _linux_getch(cls) -> str:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        with cls._linux_terminal_lock:
            try:
                tty.setcbreak(fd)
                return cls._linux_read_key()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @classmethod
    def _linux_reader_loop(cls) -> None:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        with cls._linux_terminal_lock:
            try:
                tty.setcbreak(fd)
                while not cls._stop_event.is_set():
                    key = cls._linux_read_key()
                    cls._key_queue.put(key)
                    if key == "ctrl + c":
                        cls._stop_event.set()
                        break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @classmethod
    def getch(cls) -> str:
        """Read a single key press and normalize common special keys."""
        if os.name == "nt":
            return cls._windows_getch()
        else:
            return cls._linux_getch()

    @classmethod
    def start(cls) -> None:
        with cls._thread_lock:
            if cls._thread is not None and cls._thread.is_alive():
                return

            cls._stop_event.clear()
            cls._thread = threading.Thread(target=cls._reader_loop, daemon=True)
            cls._thread.start()

    @classmethod
    def stop(cls) -> None:
        cls._stop_event.set()

    @classmethod
    def _reader_loop(cls) -> None:
        if os.name == "nt":
            cls._windows_reader_loop()
            return

        cls._linux_reader_loop()

    @classmethod
    def queue(cls, timeout: float = 0.05):
        cls.start()
        try:
            return cls._key_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    @classmethod
    def drain(cls):
        keys = []
        while True:
            try:
                keys.append(cls._key_queue.get_nowait())
            except queue.Empty:
                return keys

    def demo(self):
        print("Press keys (press 'q' to quit):", flush=True)
        while True:
            key = self.queue(timeout=0.10)
            if key is None:
                continue
            print(f"You pressed: {key}", flush=True)
            if key == "q":
                break


if __name__ == "__main__":
    k = KeyReader()
    k.demo()
