import argparse


class InvalidTimeFormat(argparse.ArgumentError):
    def __init__(self, timestring: str):
        super().__init__(f"Invalid time format '{timestring}'. Must be in the format: %H:%M:%S")


class InvalidIntervalFormat(argparse.ArgumentError):
    def __init__(self, intervalstring: str):
        super().__init__(f"Invalid interval format '{intervalstring}'. Must be in the format: %H:%M:%S/%H:%M:%S")
