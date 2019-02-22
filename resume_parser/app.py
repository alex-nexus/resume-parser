from flask import Flask, render_template, request

from resume_parser.parse import parse_batch

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
    resume_files = request.files.getlist("resumes[]")
    resumes = parse_batch(resume_files, keywords)
    app.logger.info(resumes)
    return render_template('uploaded.html', keywords=keywords, resumes=resumes)
