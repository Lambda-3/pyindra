from distutils.core import setup

setup(
  name = 'pyindra',
  packages = ['pyindra'], # this must be the same as the name above
  version = '0.1.2',
  description = 'The official client for the Indra word embedding and semantic relatedness server',
  author = 'Juliano Efson Sales',
  author_email = 'julsal@lambda3.org',
  url = 'https://github.com/Lambda-3/PythonIndraClient',
  download_url = 'https://github.com/Lambda-3/PythonIndraClient/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['semantic', 'relatedness', 'word embedding', 'distributional semantics', 'computational linguistics',
              'natural language processing', 'nlp', 'natural language understanding', 'nlu', 'artificial intelligence',
              'ai', 'nearest neighbors', 'pyindra'], # arbitrary keywords
  classifiers = [],
)