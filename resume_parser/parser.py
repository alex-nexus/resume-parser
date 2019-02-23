from resume_parser import convert
from resume_parser import utils
from resume_parser.extractor import Extractor


import multiprocessing as mp

PROCESSES = 4


def parse_batch(resume_files):
  texts = [convert.convert_to_text(resume_file) for resume_file in resume_files]
  pool = mp.Pool(processes=PROCESSES)
  clean_texts = pool.map(utils.clean_text, texts)
  resumes = pool.map(Extractor().extract, clean_texts)
  print(resumes)
  return resumes
