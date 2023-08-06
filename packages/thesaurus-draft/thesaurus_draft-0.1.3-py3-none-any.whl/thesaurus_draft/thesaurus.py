class Thesaurus:


  def __init__(self, text):
    self.text = text


  def func(self, text):
    text = ''.join(str(x) for x in text.read().splitlines())

    import spacy
    nlp = spacy.load('en', disable=['parser', 'ner'])
    doc = nlp(text)
    text = " ".join([token.lemma_ for token in doc])

    from gensim.utils import tokenize
    tokens = list(tokenize(text, to_lower=True))

    # Open file with stopwords
    stopwords_file = open('/content/extended_stopwords.txt', 'r')
    # Initialize empty list
    stopwords = []
    # Add stopwords to list
    for line in stopwords_file:
      stopwords.append(line[:-1])

    filtered_tokens = []
    for token in tokens:
      if token not in stopwords:
        filtered_tokens.append(token)

    filtered_tokens = set(filtered_tokens)

    text = " ".join(filtered_tokens)
    embeddings = []

    nlp2 = spacy.load('en_core_web_lg')

    for token in filtered_tokens:
      embeddings.append(nlp2(token).vector)

    return filtered_tokens, embeddings
  

  def visualize(self):
    background = open('background.txt', 'r')

    ft1, e1 = self.func(background)

    ft2, e2 = None, None
    if self.text is not None:

      ft2, e2 = self.func(self.text)

      from sklearn.manifold import TSNE
      import numpy as np

      tsne = TSNE(n_components=2, random_state=0)
      np.set_printoptions(suppress=True)
      Y1 = tsne.fit_transform(e1)
      Y2 = tsne.fit_transform(e2)

      import matplotlib.pyplot as plt

      plt.scatter(Y1[:, 0], Y1[:, 1], c = 'orange')

      plt.scatter(Y2[:, 0], Y2[:, 1], c = 'blue')
      for label, x, y in zip(ft2, Y2[:, 0], Y2[:, 1]):
          plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')

      plt.show()