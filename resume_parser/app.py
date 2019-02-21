from flask import Flask, render_template, request

from resume_parser.resume_parser import ResumeParser

app = Flask(__name__)


@app.route('/')
def index():
  app.logger.info('GET index')
  return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  app.logger.info('POST upload')

  if request.method == 'POST':
    resumes = request.files.getlist("resumes[]")
    resumes_data = ResumeParser().parse(resumes)
    app.logger.info(resumes_data)
    return render_template('uploaded.html', resumes_data=resumes_data)
