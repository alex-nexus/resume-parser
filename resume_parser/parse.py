from resume_parser.extractor import Extractor
from resume_parser.convert import convert_to_text

import multiprocessing as mp
import nltk
from nltk.corpus import stopwords

stop_words = stopwords.words('english')


PROCESSES = 4


def parse_batch(resume_files, keywords):
  texts = [convert_to_text(resume_file) for resume_file in resume_files]
  texts = [clean_text(text) for text in texts]
  pool = mp.Pool(processes=PROCESSES)
  resumes = pool.map(Extractor().extract, texts)
  print(resumes)
  return resumes


def clean_text(text):
  return ' '.join([i for i in text.split() if i not in stop_words])
