from collections import namedtuple
from csv import DictReader
INPUT = '/Users/mgordon/ctan/mentorship_july_2020/july_2020.csv'
HEADER = ["a","firstname","lastname","email","linkedin","city","role","gender","pronouns","ethnicity","disability","accomodations","mentormentee","howmanyhours","howlong","workin","expertise","networking","interestedin","why","notes","submitted","token"]
Candidate = namedtuple('candidate', HEADER)

def dei_score(c : Candidate) -> int:
    score = 0
    if c.ethnicity != 'White or Caucasian':
        score += 1
    if c.gender != 'Man':
        score += 1
    if c.disability != 'I do not have a disability':
        score += 1
    return score

with open(INPUT, 'r') as f:
    candidates = set([Candidate(**v) for v in DictReader(f)])
    mentees = set([c for c in candidates if c.mentormentee in ['Being mentored', 'Both']])
    mentors = candidates - mentees


