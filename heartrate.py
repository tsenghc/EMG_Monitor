import heartrate

from heartrate import trace, files



heartrate.trace(browser=True)

trace(files=files.path_contains('realtimeUDP.py'))