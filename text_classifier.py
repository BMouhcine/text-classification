from flask import Flask, request
from operator import itemgetter
import json
from elasticsearch import Elasticsearch
app = Flask(__name__)

es = Elasticsearch("http://es01:9200")






def get_best_category(response):
     categories = {}
     for hit in response['hits']['hits']:
         score = hit['_score']
         category = hit['_source']['category']
         if category not in categories:
            categories[category] = score
         else:
            categories[category] += score
     if len(categories) > 0:
         sortedCategories = sorted(categories.items(), key=itemgetter(1), reverse=True)
         category = sortedCategories[0]
     return category


@app.route("/", methods=['POST'])
def classify_text():
    content = request.form['content']
    res = es.search(index="sample", body={"query": {"more_like_this": {"fields":["category","content"], "like": content, "min_term_freq":1, "max_query_terms":20}}})
    best_category = get_best_category(json.loads(json.dumps(res))) 
    return {"category": best_category[0], "score":best_category[1]}
    
@app.route("/test")
def hello():
  with open("response") as res:
    best_category = get_best_category(json.loads(res.read()))
    print(json.dumps(best_category))
    return json.dumps(best_category)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5001)

