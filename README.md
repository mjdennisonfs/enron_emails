# Project: enron_emails
Analysis of the Enron email dataset.


## Steps to take after cloning this repo

* Setup and activate a Python environment:
```
$ conda env create -f environment.yml
$ source activate enron_emails
```

* Download spacy data
```
$ python -m spacy download en_core_web_sm
$ python -m spacy download en_core_web_lg
```

* Get the Enron email dataset:
```
$ curl https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz --output enron_mail_20150507.tar.gz    (*Mac*)
$ wget https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz -O enron_mail_20150507.tar.gz          (*Linux*)
```
or visit https://www.cs.cmu.edu/~./enron/ to download.

## Running the code

* The repo contains two notebooks:
- `notebooks/analysis.ipynb`: pre-run notebook, contains results
- `notebooks/analysis_blank.ipynb`: same notebook, without any output

* Run `notebooks/analysis_blank.ipynb` to carry out the analysis

## TODO (non-analysis)

* Unit tests + CI tests for code style etc.
