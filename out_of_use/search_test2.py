from src.app.viewer.search import Searcher
from src.localization.my_tags import tags_init,TagManager
from src.app.share.recipe_repository import myRepository

import logging

# Clear logfile before start
with open('log_file.log', 'w'):
    pass
logging.basicConfig(filename='log_file.log', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

tags_init()
searcher = Searcher(myRepository)
# Create default tags
TagManager.set_search_columns(["name"])
#result = searcher.search("'Kuchen' vegetarian:true or duration: < 2 h author:'misp'")

try:
    test_query = 'random: 1'
    result = searcher.search(test_query)
    # result = searcher.search("'Kuchen' vegetarian:true or duration: < 2 h author:'misp'")
    for r in result:
        print(r.name)
except Exception as exp:
    print(exp)


