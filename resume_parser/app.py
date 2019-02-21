from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    f = request.files['the_file']
    # parse
    # copy to s3

    return render_template('uploaded.html')
