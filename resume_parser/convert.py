import io
import os
import docx2txt

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def convert_to_text(resume_file):
  '''
  Wrapper function to detect the file extension and call text extraction function accordingly

  :param file_path: path of file of which text is to be extracted
  :param extension: extension of file `file_name`
  '''
  filename = resume_file.filename
  extension = os.path.splitext(resume_file.filename)[1]

  text = ''
  if extension == '.pdf':
    text = convert_pdf_to_text(resume_file)
  elif extension == '.docx' or extension == '.doc':
    text = convert_doc_to_text(resume_file)
  elif extension == '.txt':
    text = convert_txt_to_text(resume_file)

  return ' '.join(text.split())

# private


def convert_pdf_to_text(pdf_file):
  '''
  Helper function to extract the plain text from .pdf files

  :param resume_file: FileStorage of PDF file to be converted
  :return: iterator of string of extracted text
  '''
  # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
  tmp_file_path = '/tmp/' + pdf_file.filename
  pdf_file.save(tmp_file_path)

  text = ''
  with open(tmp_file_path, 'rb') as fh:
    for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
      resource_manager = PDFResourceManager()
      fake_file_handle = io.StringIO()
      converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
      page_interpreter = PDFPageInterpreter(resource_manager, converter)
      page_interpreter.process_page(page)

      page_text = fake_file_handle.getvalue()
      text += page_text

      # close open handles
      converter.close()
      fake_file_handle.close()

  return text


def convert_doc_to_text(doc_file):
  '''
  Helper function to extract plain text from .doc or .docx files

  :param doc_path: path to .doc or .docx file to be extracted
  :return: string of extracted text
  '''
  temp = docx2txt.process(doc_file)
  text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
  return ' '.join(text)


def convert_txt_to_text(txt_file):
  return clean_text(txt_file.stream.read().decode('utf-8'))


def clean_text(text):
  text = [line.replace('\t', ' ') for line in text.split('\n') if line]
  return ' '.join(text)
