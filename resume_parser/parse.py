import multiprocessing as mp

from resume_parser.convert import convert_to_text
from resume_parser.extractor import Extractor

PROCESSES = 4


def parse_batch(resume_files):
  texts = [convert_to_text(resume_file) for resume_file in resume_files]
  pool = mp.Pool(processes=PROCESSES)
  return pool.map(Extractor().extract, texts)
