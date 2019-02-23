import os
import re
import nltk
import spacy
import pandas as pd


from spacy.matcher import Matcher
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from resume_parser import data
import resume_parser.constants as cs

nlp = spacy.load('en_core_web_sm')
schools = data.load_schools()
majors = data.load_majors()


class Extractor:
  def extract(self, text):
    self.text = text
    return {
        'name': self.extract_name(),
        'email': self.extract_email(),
        'educations': self.extract_educations(),
        'experiences': self.extract_experiences(),
        'github_url': self.extract_github_url(),
        'linkedin_url': self.extract_linkedin_url(),
        'phone': self.extract_phone(),
        'skills': self.extract_skills()
    }

  # private

  def extract_github_url(self):
    match = re.search(r"(github.com\/[\d\-\w]+)", self.text)
    return match[0] if match else None

  def extract_linkedin_url(self):
    match = re.search(r"(linkedin.com\/in\/[\w\-\d]+)", self.text)
    return match[0] if match else None

  def extract_email(self):
    match = re.search(r'[\w\.-]+@[\w\.-]+',  self.text)
    return match[0] if match else None

  def extract_name(self):
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    '''
    nlp_text = nlp(self.text)
    matcher = Matcher(nlp.vocab)
    pattern = [cs.NAME_PATTERN]

    matcher.add('NAME', None, *pattern)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
      span = nlp_text[start:end]
      return span.text

  def extract_phone(self):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    # Found this complicated regex on : https://zapier.com/blog/extract-links-email-phone-regex/
    phone = re.findall(re.compile(
        r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), self.text)
    if phone:
      number = ''.join(phone[0])
      if len(number) > 10:
        return '+' + number
      else:
        return number

  def extract_skills(self):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    nlp_text = nlp(self.text)
    noun_chunks = list(nlp_text.noun_chunks)
    tokens = [token.text for token in nlp_text if not token.is_stop]

    skills_data = pd.read_csv('data/skills.csv')
    skills = list(skills_data.columns.values)
    # check for one-grams
    skillset = [token for token in tokens if token.lower() in skills]
    # check for bi-grams and tri-grams
    skillset += [token.text.lower().strip() for token in noun_chunks if token.text in skills]
    return [skill.capitalize() for skill in set(skillset)]

  def extract_educations(self):
    '''
    Helper function to extract education from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found else only returns education degree
    '''
    nlp_text = nlp(self.text)
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
      for tex in text.split():
        tex = re.sub(r'[?|$|.|!|,]', r'', tex)
        if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
          edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
      year = re.search(re.compile(cs.YEAR), edu[key])
      if year:
        education.append((key, ''.join(year.group(0))))
      else:
        education.append(key)
    return education

  def extract_experiences(self):
    '''
    Helper function to extract experience from resume text

    :param resume_text: Plain resume text
    :return: list of experience
    '''
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization
    word_tokens = nltk.word_tokenize(self.text)

    # remove stop words and lemmatize
    filtered_sentence = [
        w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)

    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)

    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label() == 'P')):
      test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x
