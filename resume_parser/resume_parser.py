import multiprocessing as mp
import spacy
from spacy.matcher import Matcher

from resume_parser.convert import convert_resume_to_text
from resume_parser.extract import *


class ResumeParser:
  def __init__(self):
    self.__nlp = spacy.load('en_core_web_sm')
    self.__matcher = Matcher(self.__nlp.vocab)

  def parse(self, resumes):
    return [self.parse_one(resume) for resume in resumes]
    # pool = mp.Pool(mp.cpu_count())
    # jobs = [pool.apply_async(self.parse_one, args=(resume_path,)) for resume_path in resume_paths]
    # return [job.get() for job in jobs]

  def parse_one(self, resume):
    text = convert_resume_to_text(resume)
    doc = self.__nlp(text)
    noun_chunks = list(doc.noun_chunks)

    return {
        'name': extract_name(doc, matcher=self.__matcher),
        'email': extract_email(text),
        'mobile': extract_mobile_number(text),
        'skills': extract_skills(doc, noun_chunks),
        'education': extract_education([sent.string.strip() for sent in doc.sents]),
        'experience': extract_experience(text)
    }
