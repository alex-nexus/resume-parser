import csv


def load_schools():
  with open('data/world-universities.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    schools = []
    for row in csv_reader:
      schools += row[1]
  return schools


def load_majors():
  return []


load_schools()
