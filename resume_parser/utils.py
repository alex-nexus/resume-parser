from nltk.corpus import stopwords

stop_words = stopwords.words('english')


def clean_text(text):
  return ' '.join([i for i in text.split() if i not in stop_words])
