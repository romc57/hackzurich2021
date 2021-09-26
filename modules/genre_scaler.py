import numpy as np
import pandas as pd
import json


ALPHA = 0.1


def convert_int_to_sentiment(int_sent):
    sent_list = ['Sadness', 'Joy', 'Fear', 'Disgust', 'Anger']
    return sent_list[int_sent - 1]


def get_state(stress_lvl, states):
    """
    :param stress_lvl: (float) stress level
    :param states: (dict) maps between ids to intervals
    :return: the id of state for the given stress level
    """
    for s_id, interval in states.items():
        begin, end = interval
        if begin <= int(stress_lvl) < end:
            return s_id


# Example
def get_curr_scores(state):
    df = {'0': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '1': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '2': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '3': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '4': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '5': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '6': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '7': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '8': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '9': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '10': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '11': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '12': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '13': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          '14': {'Sadness': 0, 'Joy': 0, 'Fear': 0, 'Disgust': 0, 'Anger': 0},
          }
    print(json.dumps(df))


def update_score(curr_stress, next_stress, article_mood, states, scores):
    """
    :param curr_stress: (float) current stress level
    :param next_stress: (float) stress level after reading the given article's mood
    :param article_mood: (str) mood of the article
    :param states: dict - keys are ids and the values are their corresponding interval
    :return: updated scores after reading the article
    """
    state = get_state(curr_stress, states)
    scores_state = scores[state]
    reward = curr_stress - next_stress
    article_subject = convert_int_to_sentiment(int(article_mood))
    scores_state[article_subject] = ALPHA * reward + (1 - ALPHA) * scores_state[article_subject]  # Moving avarage
    return scores_state


def get_weights(scores):
    """
    :param scores: dict - (mood,score)
    :return: dict - (mood, mood weight)
    """
    vals = np.array(list(scores.values()))
    vals += abs(min(vals)) + 1  # make sure the values are positive
    vals = vals / vals.sum()
    res = list()
    for i, (k, v) in enumerate(zip(scores, vals)):
        res.append({'name': k, 'size': v, 'id': i + 1})
    return res


def get_bins(stress_levels, q=10):
    """
    :param stress_levels: 1d ndarray or Series
    :param q: int or list-like of float
        Number of quantiles. 10 for deciles, 4 for quartiles, etc. Alternately
        array of quantiles, e.g. [0, .25, .5, .75, 1.] for quartiles.
    :return: dict - keys are ids and the values are their corresponding interval
    """
    _, bins = pd.qcut(stress_levels, q, retbins=True)
    states = dict()
    for i in range(len(bins) - 1):
        states[str(i)] = (bins[i], bins[i + 1])
    return states
