import json


def update_graph_by_like(article_id, mood):
    with open('articles_data_reduced.txt') as json_file:
        articles_data = json.load(json_file)
    data = articles_data[mood]['nodes'][article_id]
    data['confidence'] = data['confidence'] + 0.2
    articles_data[mood]['nodes'][article_id] = data
    for edge in articles_data[mood]['links']:
        if edge['source'] == article_id:
            second_article_id = edge['target']
        elif edge['target'] == article_id:
            second_article_id = edge['source']
        else:
            continue
        if len(articles_data[mood]['nodes']) > second_article_id:
            data = articles_data[mood]['nodes'][second_article_id]
            data['confidence'] = data['confidence'] + 0.1
            articles_data[mood]['nodes'][second_article_id] = data
    with open('articles_data_reduced.txt', 'w') as outfile:
        json.dump(articles_data, outfile)


