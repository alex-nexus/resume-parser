import multiprocessing as mp

from resume_parser.convert import convert_resume_to_text
from resume_parser.extract import *


class ResumeParser:
  def parse(self, resume_files):
    texts = [convert_resume_to_text(resume_file) for resume_file in resume_files]
    pool = mp.Pool(processes=4)
    return pool.map(self.parse_one, texts)

  def parse_one(self, text):
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'educations': extract_education(text),
        'experiences': extract_experience(text),
        'github_url': '',
        'linkedin_url': '',
        'mobile': extract_mobile_number(text),
        'skills': extract_skills(text)
    }
