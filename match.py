import json
import re
from pathlib import Path
from collections import defaultdict
from pipeline import Candidate, dei_score, is_mentee, is_mentor, INPUT
from csv import DictReader
from matching.games import HospitalResident
INPUT_DIRECTORIES = ['/Users/mgordon/ctan/mentorship_july_2020/matt_apps']
DATA_RE = re.compile('\^DATA\^:\s?(.*)')

def read_preferences(input_dir, dei):
    mentee_preferences = defaultdict(list)
    mentor_preferences = defaultdict(list)
    input_dir = Path(input_dir)

    # read the match forms and generate two dicts
    # for each potential mentor/mentee match:
    # mentor: [(mentee, dei_score)]
    # mentee: [(mentor, match_score)]
    for f in [x for x in input_dir.iterdir() if str(x).endswith('.md')]:
        matches = DATA_RE.findall((input_dir / f).read_text())
        for m in matches:
            j = json.loads(m)
            if j['score'] != 0:
                mentee_preferences[j['metoken']].append((j['mrtoken'], j['score']))
                mentor_preferences[j['mrtoken']].append((j['metoken'], dei[j['metoken']]))

    # now iterate over the dict items and sort by the score column (2nd element of the tuple)
    # this will order the preferences: mentees rank mentors by their match score and mentors preference mentees
    # by their dei score
    # after they've been ordered, we can remove the scores and return just two dicts of sorted preferences
    def _sort_and_strip(d):
        r = dict()
        for k, lst in d.items():
            s = sorted(lst, key=lambda x: x[1])
            # sort highest to lowest
            s.reverse()
            r[k] = [x[0] for x in s]
        return r

    return _sort_and_strip(mentor_preferences), _sort_and_strip(mentee_preferences)

def read_dei_and_capacity(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        candidates = set([Candidate(**v) for v in DictReader(f)])
    dei = {c.token: dei_score(c) for c in candidates if is_mentee(c)}
    capacity = {c.token: c.howmanyhours for c in candidates if is_mentor(c)}
    return dei, capacity


dei, cap = read_dei_and_capacity(INPUT)
mr_pref, me_pref = read_preferences(INPUT_DIRECTORIES[0], dei)
g = HospitalResident.create_from_dictionaries(me_pref, mr_pref, cap)
matching = g.solve()
