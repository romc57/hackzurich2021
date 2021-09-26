import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


df_articles = pd.read_csv('articles_dataset_1k.csv')
# Prep TF-IDF Matrix for Word Clouds
# data = df_articles.transpose()
# data.columns = ['unnamed', 'title', 'publication', 'author', 'date', 'year', 'month', 'url', 'content']
print(df_articles.head())
wordcloud = WordCloud().generate_from_frequencies(df_articles['content'])
plt.imshow(wordcloud)