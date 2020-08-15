from collections import namedtuple
from csv import DictReader
INPUT = '/Users/mgordon/ctan/mentorship_july_2020/july_2020.csv'
HEADER = ["a","firstname","lastname","email","linkedin","city","role","gender","pronouns","ethnicity","disability","accomodations","mentormentee","howmanyhours","howlong","workin","expertise","networking","interestedin","why","notes","submitted","token"]
Candidate = namedtuple('candidate', HEADER)
with open(INPUT, 'r') as f:
    candidates = [Candidate(**v) for v in DictReader(f)]
    print(candidates[0])
