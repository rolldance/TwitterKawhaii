import twitter
import json
from collections import Counter
from prettytable import PrettyTable
CONSUMER_KEY = 'XXXXXXXX'
CONSUMER_SECRET = 'XXXXXXX'
OAUTH_TOKEN = 'XXXXXXXX'
OAUTH_TOKEN_SECRET = 'XXXXXXXX'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                              CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


#Query Analysis
q= '@spurs'
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']
# print statuses
for _ in range(10):
    # print 'Length of statuses', len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e:
        break

    kwargs = dict([kv.split('=') for kv in next_results[1:].split('&')])

    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

status_texts = [status['text']
               for status in statuses]
screen_names = [user_mention['screen_name']
                for status in statuses
                   for user_mention in status['entities']['user_mentions']]
hashtags = [hashtag['text']
            for status in statuses
                for hashtag in status['entities']['hashtags']]

words = [w for t in status_texts
            for w in t.split()]


#frequency Analysis
for label, data in(('Word',words),
                   ('Screen_name', screen_names),
                   ('Hashtags',hashtags)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:15]]
    pt.align[label], pt.align['Count'] = 'l', 'r'
    print pt

#lexical diversity
def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)

def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.*total_words/len(statuses)
print lexical_diversity(words)
print lexical_diversity(screen_names)
print lexical_diversity(hashtags)
print average_words(status_texts)