import pandas as pd
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EmotionOptions, KeywordsOptions

IAM_KEY = 'nd2d2Wqk5_HpoJfiRzbqZIy0c3FBaeBnmJkPgqJbGsza'
SERVICE_URL = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/d41851c7-bee4-4afa-812a-d818adfe5401'

authenticator = IAMAuthenticator(IAM_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(version='2020-08-01', authenticator=authenticator)
natural_language_understanding.set_service_url(SERVICE_URL)

df = pd.read_csv('articles_dataset_1k.csv')
df.head()

res = []
for i, (index, row) in enumerate(df.iterrows()):
    response = natural_language_understanding.analyze(text=row['content'], features=Features(
        keywords=KeywordsOptions(limit=5, sentiment=True, emotion=True)))
    res.append(response)
    print(i)
pass
