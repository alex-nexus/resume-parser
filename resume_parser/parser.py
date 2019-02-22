import multiprocessing as mp

from resume_parser.convert import convert_resume_to_text
from resume_parser.extractor import Extractor


class Parser:
  def parse(self, resume_files):
    texts = [convert_resume_to_text(resume_file) for resume_file in resume_files]
    pool = mp.Pool(processes=4)
    return pool.map(Extractor().extract, texts)
