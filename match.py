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
    def _sort(d):
        r = dict()
        for k, lst in d.items():
            s = sorted(lst, key=lambda x: x[1])
            # sort highest to lowest
            s.reverse()
            r[k] = s
        return r

    return _sort(mentor_preferences), _sort(mentee_preferences)

def read_candidates(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return set([Candidate(**v) for v in DictReader(f)])

def read_dei_and_capacity(input_file):
    candidates = read_candidates(input_file)
    dei = {c.token: dei_score(c) for c in candidates if is_mentee(c)}
    capacity = {c.token: int(c.howmanyhours) for c in candidates if is_mentor(c)}

    # munge
    capacity['mattgordon'] = 3
    return dei, capacity

class Match:
    def __init__(self, mentee, score):
        self.mentee = mentee
        self.score = score

class MeMatch:
    def __init__(self, mentee, prefs, dei):
        self.mentee = mentee
        self.dei = dei
        self.prefs = sorted(prefs, key=lambda x: x[1])
        self.prefs.reverse()
        self.proposed = set()
        self.mrmatch = None

    def next_proposal(self):
        pass


class MrMatch:
    def __init__(self, mentor, capacity):
        self.mentor = mentor
        self.matches = set()
        self.capacity = capacity

    def propose(self, match : MeMatch):
        match.proposed.add(self.mentor)
        if self.capacity < len(self.matches):
            self.matches.add(match)
            match.mrmatch = self
            return
        new_matches = self.matches.copy()
        for m in self.matches:
            if match.dei > m.dei:
                new_matches.remove(m)
                m.mrmatch = None
                new_matches.add(match)
                match.mrmatch = self
        self.matches = new_matches


class Matcher:
    def __init__(self, me_pref, capacity, dei):
        self.mematch = {k: MeMatch(k, v, dei[k]) for k, v in me_pref.items()}
        self.mrmatch = {k: MrMatch(k, cap) for k, cap in capacity.items()}

    def unmatched_me(self):
        return {k: v for k, v in self.mematch.items() if v.mrmatch is None}

    def solve(self):
        unmatched = self.unmatched_me()




    # dei, cap = read_dei_and_capacity(INPUT)
# mr_pref, me_pref = read_preferences(INPUT_DIRECTORIES[0], dei)
# g = HospitalResident.create_from_dictionaries(me_pref, mr_pref, cap)
# cdict = {c.token: c for c in read_candidates(INPUT)}
# cdict['mattgordon'] = "Matt Gordon"
# matching = g.solve(optimal='hospital')
# assert g.check_stability()
# assert g.check_validity()
# #print([x for x in matching.items() if '6cjmsu945gzrl210d6ur8d6cjmsux44k' in x[1]])
# sampenrose = 'wqqmq9vk16cg0tbfku46hz4wqqmq9zc7'
#
# def _name(c):
#     if isinstance(c, str):
#         return c
#     return c.firstname + " " + c.lastname
# d = {_name(cdict[k.name]):  [_name(cdict[x.name]) for x in v] for k, v in matching.items()}
# print(d)
