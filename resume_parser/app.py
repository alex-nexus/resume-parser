from flask import Flask, render_template, request

from resume_parser.parser import Parser

app = Flask(__name__)


@app.route('/')
def index():
  app.logger.info('GET index')
  return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  app.logger.info('POST upload')

  if request.method == 'POST':
    resume_files = request.files.getlist("resumes[]")
    resumes = Parser().parse(resume_files)
    app.logger.info(resumes)
    return render_template('uploaded.html', resumes=resumes)
