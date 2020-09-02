import json
import os
import re
from pathlib import Path
from collections import defaultdict

INPUT_DIRECTORIES = ['/Users/mgordon/ctan/mentorship_july_2020/matt_apps']
DATA_RE = re.compile('\^DATA\^:\s?(.*)')

def read_match_files(input_dir):
    match_data = defaultdict(dict)
    input_dir = Path(input_dir)
    for f in [x for x in input_dir.iterdir() if str(x).endswith('.md')]:
        print(f)
        matches = DATA_RE.findall((input_dir / f).read_text())
        for m in matches:
            j = json.loads(m)
            if j['score'] != 0:
                match_data[j['metoken']][j['mrtoken']] = j['score']
    return match_data
print(read_match_files(INPUT_DIRECTORIES[0]))
