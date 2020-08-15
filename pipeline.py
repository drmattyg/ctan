import os
from collections import namedtuple
from csv import DictReader
import jinja2 as j2
import os
INPUT = '/Users/mgordon/ctan/mentorship_july_2020/july_2020.csv'
OUTDIR = '/Users/mgordon/ctan/mentorship_july_2020/'
HEADER = ["a","firstname","lastname","email","linkedin","city","role","gender","pronouns","ethnicity","disability","accomodations","mentormentee","howmanyhours","howlong","workin","expertise","networking","interestedin","why","notes","submitted","token"]
Candidate = namedtuple('candidate', HEADER)
TEMPLATE = os.path.join(os.path.dirname(__file__), 'profile.md')
with open(TEMPLATE, 'r') as f:
    TEMPLATE_STR = f.read()
def dei_score(c : Candidate) -> int:
    score = 0
    if c.ethnicity != 'White or Caucasian':
        score += 1
    if c.gender != 'Man':
        score += 1
    if c.disability != 'I do not have a disability':
        score += 1
    return score

def interest_overlap_score(mentee: Candidate, mentor: Candidate):
    me = set([x.strip() for x in mentee.interestedin.split(',')])
    mr = set([x.strip() for x in mentor.workin.split(',')])
    return len(me.intersection(mr))

def career_score(me: Candidate, mr: Candidate):
    categories = ["", "Less than a year", "One to three years", "Longer than three years"]
    mr_long = categories.index(mr.howlong)
    me_long = categories.index(me.howlong)
    return mr_long - me_long

def match(me: Candidate, mr: Candidate) -> bool:
    if career_score(me, mr) < 0:
        return False
    if interest_overlap_score(me, mr) < 1:
        return False
    return True

with open(INPUT, 'r') as f:
    candidates = set([Candidate(**v) for v in DictReader(f)])
    mentees = set([c for c in candidates if c.mentormentee in ['Being mentored', 'Both']])
    mentors = candidates - mentees

    matches = {
        me: [mr for mr in mentors if match(me, mr)]
        for me in mentees
    }

    me = list(matches)[0]


    t = j2.Template(TEMPLATE_STR)
    r = t.render({'me': me, 'mentors': matches[me]})
    print(r)