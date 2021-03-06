from flask import Flask, render_template, request

from resume_parser import parser

app = Flask(__name__)


@app.route('/')
def index():
  app.logger.info('GET index')
  return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  app.logger.info('POST upload')

  if request.method == 'POST':
    keywords = request.form['keywords']
    keywords = [keyword.strip() for keyword in keywords.lower().split(',')]
    resume_files = request.files.getlist("resumes[]")
    resumes = parser.parse_batch(resume_files)
    return render_template('uploaded.html', keywords=keywords, resumes=resumes)
  else:
    return render_template('index.html')
