"""Scripts to extract metadata and email body from emails."""

import re
import string
from typing import Dict, List

import pandas as pd
import spacy
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


def get_metadata(contents: List) -> Dict:
    """Returns the metadata from an email.
    
    Metadata is returned as a dictionary, where the key-value pairs are the metadata labels
    and corresponding entries.
    
    Args:
        contents: List containing the lines in the email.
    
    Returns:
        A dicionary containing the metadata.
    """
    meta_keys = [
        "Bcc",
        "Cc",
        "Content-Transfer-Encoding",
        "Content-Type",
        "Date",
        "From",
        "Message-ID",
        "Mime-Version",
        "Subject",
        "To",
        "X-FileName",
        "X-Folder",
        "X-From",
        "X-Origin",
        "X-To",
        "X-bcc",
        "X-cc"
    ]
    contents_meta = {}
    key = ""
    # the last row of the metadata is at X-FileName:
    final_index = [idx for idx, c in enumerate(contents) if "X-FileName:" in c][0] + 1
    for c in [c for c in contents[:final_index]]:
        if (c[0] != "\t") and (c[0] != " "):
            # if a line does not start with a tab or a space, it is a new metadata line
            try:
                key, value = c.split(":", 1)
                if (key in meta_keys) and (key not in contents_meta.keys()):
                    # is a new metadata key, if not already in the dict and in the keys list
                    # we check this since some subjects have e.g. "Date:" in them
                    contents_meta[key] = value.strip()
                else:
                    # is not a new metadata key
                    key = key_old
                    contents_meta[key] += (" " + c.strip())
            except ValueError:
                # did not split, it is not a new line
                contents_meta[key] += (" " + c.strip())
        else:
            # if a line starts with a tab, add it to the previous line
            contents_meta[key] += (" " + c.strip())
        key_old = key
    return contents_meta


def get_email_body(contents: List) -> str:
    """Returns the body of an email.
    
    Args:
        contents: List containing the lines in an email.
    
    Returns:
        A string with all email metadata removed.
    """
    # first index of the email body, after X-FileName
    first_index = [idx for idx, c in enumerate(contents) if "X-FileName:" in c][0] + 1
    # join to get the message
    msg = "".join(contents[first_index:])
    # strip out any e.g. html and replace all white spaces with a single space
    soup = BeautifulSoup(msg)
    return re.sub("\s+", " ", soup.get_text()).strip()


def strip_string(msgs: List) -> List:
    """Strips links, emails, punctuation and numbers from a list of strings.
    
    Args:
        msgs: List of messages.
    
    Returns:
        A list of messages with links, puntuaction and numbers removed.
    """
    # replace web-links and email address with placeholder
    msgs_strip = [
        re.sub(r"^https?:\/\/.*[\r\n]*", "web_link ", m, flags=re.MULTILINE) for m in msgs
    ]
    msgs_strip = [
        re.sub(r"\S*@\S*\s?", "email_address ", m, flags=re.MULTILINE) for m in msgs_strip
    ]
    # remove [IMAGE]
    msgs_strip = [re.sub(r"\[(IMAGE)\]", " ", m) for m in msgs_strip]
    # remove punctuation
    msgs_strip = [
        m.translate(str.maketrans("", "", string.punctuation)) for m in msgs_strip
    ]
    # remove numbers
    msgs_strip = [re.sub(r"\d+", " ", m) for m in msgs_strip]
    # replace any extra white-space
    msgs_strip = [re.sub("\s+", " ", m) for m in msgs_strip]
    return msgs_strip


def stem_text(msgs: List) -> List:
    """Applies a porter stemmer to messages in a list.
    
    Args:
        msgs: List of messages.

    Returns:
        A list of messages with stemmed text.
    """
    # set stemmer
    ps = PorterStemmer()
    # apply to the text
    msgs_stem = [ps.stem(m) for m in msgs]
    return msgs_stem


def remove_named_entities(msgs: List) -> List:
    """Replace named entities in a message with their type.
    
    Args:
        msgs: A list of messages.
        
    Returns:
        A list of messgages with replaced named entities.
    """
    nlp = spacy.load('en_core_web_lg')
    nlp.add_pipe("merge_entities")

    output = []
    # loop over all messages in input, extract nouns and append.
    for i, doc in enumerate(nlp.pipe(msgs)):
        noun_text = " ".join([t.text if not t.ent_type_ else t.ent_type_ for t in doc])
        output.append(noun_text)
    return output


def extract_message_nouns(msgs: pd.Series) -> List:
    """Extracts nouns from a series of email messages.
    
    Args:
        msgs: Pandas series containing the messages.
    Returns:
        List containing messages with nouns removed.
    """
    # disable parser and named entity rec to speed up processing
    nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
    output = []
    # loop over all messages in input, extract nouns and append.
    for i, doc in enumerate(nlp.pipe(msgs)):
        noun_text = " ".join(token.lemma_ for token in doc if token.pos_ == 'NOUN')
        output.append(noun_text)
    return output
