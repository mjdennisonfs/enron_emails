"""Scripts for fitting models to email data."""

from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer


def fit_tf_idf(
    msgs: List,
    max_features: int = 10000,
    max_df: float = 0.95,
    min_df: int = 2
) -> TfidfVectorizer:
    """Fits a TF-IDF vectorizer to a list of messages.
    
    TF-IDF: Term frequency - inverse document frequency.
    
    Args:
        msgs: List of messages.
        max_features: Maximum number of elements in the feature vector, corresponds
                      to taking the most frequent max_features words (given the below
                      constraints). Default is 10,000. 
        max_df: Term must occur in at most this fraction of documents, default is 0.95.
        min_df: Term must occur in at least this many documents, default is 2.
        
    Returns:
        The vectorizer object that is used for the conversion.
    """
    # make sure min/max df are in range
    max_df = np.clip(max_df, 1e-6, 1.0)
    min_df = int(np.clip(min_df, 1, len(msgs)))
    # fit tf-idf vectorizer to the dataset
    vec = TfidfVectorizer(
        stop_words="english", 
        max_features=max_features,
        max_df=max_df,
        min_df=min_df
    )
    vec.fit(msgs)
    
    return vec
