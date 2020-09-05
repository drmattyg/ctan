import json
import re
from pathlib import Path
from collections import defaultdict
from pipeline import Candidate, dei_score, is_mentee, is_mentor, INPUT, read_candidates
from csv import DictReader
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

        # turn this into a dict of capacities?  Or read capacity further down?
        # move proposed/capacity into Matcher?
        self.proposed = defaultdict(int) # number of times we've proposed
        self.mrmatch = None

    def next_proposal(self, mrmatch):
        d = [mr for mr in self.prefs if mrmatch[mr[0]].capacity > self.proposed[mr[0]]]
        if not d:
            return None
        else:
            return d[0][0]

class MrMatch:
    def __init__(self, mentor, capacity):
        self.mentor = mentor
        self.matches = set()
        self.capacity = capacity

    def propose(self, match : MeMatch):
        match.proposed[self.mentor] += 1
        if self.capacity > len(self.matches):
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
        return {k: v for k, v in self.mematch.items() if v.mrmatch is None and v.next_proposal(self.mrmatch) is not None}

    def solve_iter(self):
        unmatched = self.unmatched_me()
        for me in unmatched.values():
            self.mrmatch[me.next_proposal(self.mrmatch)].propose(me)

    def can_match(self):
        for me in self.unmatched_me().values():
            if me.next_proposal(self.mrmatch) is not None:
                return True
        return False

    def solve(self):
        i = 1
        while(self.can_match()):
            print('round {}: {} unmatched'.format(i, len(self.unmatched_me())))
            self.solve_iter()
            i += 1

    @property
    def solution(self):
        # mentor/mentees
        return {k: set([x.mentee for x in v.matches]) for k, v in self.mrmatch.items()}

    @property
    def unmatched_mentees(self):
        return {k for k, v in self.mematch.items() if v.mrmatch is None}

MATCH_HEADER = ['mr_first', 'mr_last', 'mr_email', 'me_first', 'me_last', 'me_email']
def solution_to_csv(solution, candidates, file=None):

    cdict = {c.token: c for c in candidates}
    print(",".join(MATCH_HEADER), file=file)
    for mrk, mentees in solution.items():
        for mek in mentees:
            mec = cdict[mek]
            mrc = cdict[mrk]
            print("{}, {}, {}, {}, {}, {}".format(mrc.firstname, mrc.lastname, mrc.email, mec.firstname, mec.lastname, mec.email), file=file)




if __name__ == '__main__':
    dei, cap = read_dei_and_capacity(INPUT)
    mr_pref, me_pref = read_preferences(INPUT_DIRECTORIES[0], dei)
    m = Matcher(me_pref, cap, dei)
    m.solve()
    solution_to_csv(m.solution, read_candidates())

# def _name(c):
#     if isinstance(c, str):
#         return c
#     return c.firstname + " " + c.lastname
# d = {_name(cdict[k.name]):  [_name(cdict[x.name]) for x in v] for k, v in matching.items()}
# print(d)
