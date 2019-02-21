import multiprocessing as mp

from resume_parser.convert import convert_resume_to_text
from resume_parser.extract import *


class ResumeParser:
  def parse(self, resumes):
    texts = [convert_resume_to_text(resume) for resume in resumes]
    pool = mp.Pool(processes=4)
    return pool.map(self.parse_one, texts)

  def parse_one(self, text):
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'mobile': extract_mobile_number(text),
        'skills': extract_skills(text),
        'education': extract_education(text),
        'experience': extract_experience(text)
    }
