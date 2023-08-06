# lib-py-helpu (not stable right now)
Phonetic - *| help juː |*

Library on PYPI that contains some very lazy but safe methods.
It's a tradition I wanted to follow my very first development team. Miss you guys.

I did document this, but I'm not sure how to use auto docs on Python, so this is really just for my usage for now.
I highly doubt anyone would really want to use this besides me.

Use case example:
```
import helpu

data_lists = [["header1", "header2"], ["value1", "value3"]]
file_path = "C:\yourfile.csv"

helpu.write_to_csv(file_path, data_lists)
```

Examples of functions:
```
def write_to_csv(self, file_path, lists):

def timestamp(self, formatting="%Y%m%d"):
```
