import csv
from nltk.corpus import stopwords


def load_schools():
  with open('data/world-universities.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    schools = []
    for row in csv_reader:
      schools += [row[1]]
  return schools


def load_majors():
  with open('data/majors-list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    majors = []
    for row in csv_reader:
      majors += [row[1].lower()]
  return majors


# print(load_schools())
STOPWORDS = set(stopwords.words('english'))
MAJORS = load_majors()
SCHOOLS = load_schools()

DEGREES = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'BTECH', 'MTECH',
    'SSC', 'HSC', 'CBSE', 'ICSE', 'PHD'
]
