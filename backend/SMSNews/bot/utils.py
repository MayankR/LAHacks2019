from .models import UserInfo
from .taboola import get_taboola_json

import json
import requests
import operator
import numpy as np

TOPICS_PER_PAGE = 7
HELP_CMD = ['h', 'help']
NEWS_TOPICS_CMD = ['news', 'n', 't', 'topics', 'topic']
COUNTRY_CMD = ['c', 'country', 'r', 'region']
PLACES = ["US","UK","India","Australia","Israel","Germany","Mexico","Japan","Korea","France"]

def get_help_text():
    return """Welcome to SMSNews! Enter
- "news" for latest topics
- "c" for changing region """

def get_new_user_text():
    return """Hey, welcome to SMSNews! Let's get to know you better..."""

def get_trending_topics(country_idx, start_idx=0, only_one=False):
    # return ['trump', 'samantha josephson', 'mick jagger', 'usc', 'university']
    # url = "https://us-central1-vision-migration.cloudfunctions.net/la_hacks_2019?country_code="+str(country_idx)
    # print("requesting")
    # req = requests.get(url)
    # print("got request")
    # json1 = json.loads(req.content.decode('utf-8'))

    json1 = get_taboola_json(country_idx)

    buckets = 3
    traffic_names = {}
    for i in range(buckets):
        report = json1['buckets'][i]['report']
        rollups = report['rollups']
        for j in range(len(rollups)):
            name = rollups[j]['name'] 
            similarity = rollups[j]['similarity']
            if name not in traffic_names:
                traffic_names[name] = rollups[j]['traffic']['totalTraffic']
            else:
                traffic_names[name] += rollups[j]['traffic']['totalTraffic']
            
    sorted_traffic_names = sorted(traffic_names.items(),key=operator.itemgetter(1),reverse=True)

    name_mapping = {}
    for bucket in range(buckets):
        report = json1['buckets'][bucket]['report']
        rollups = report['rollups']
        for topic in rollups:
            name = topic['name']
            similarity = topic['similarity']
            urls_temp = topic['top_articles_on_network']
            urls = []
            for temp in urls_temp:
                urls = list(set(urls))+list(temp.keys())
            if name not in name_mapping:
                name_mapping[name] = {'urls':urls,'similarity':{}}
            else:
                for key in similarity:
                    if key not in name_mapping[name]['similarity']:
                        name_mapping[name]['similarity'][key] = [similarity[key]]
                    else:
                        name_mapping[name]['similarity'][key].append(similarity[key])
                
    for key in name_mapping:
        similarity_list = name_mapping[key]['similarity']
        for neighbour in similarity_list:
            similarity_list[neighbour] = np.mean(similarity_list[neighbour])
            
    threshold = 0.2
    neighbor_set = set()
    final_top = []

    for name, no in sorted_traffic_names:
        if name not in neighbor_set:
            dictx = name_mapping[name]
            final_top.append({name:dictx})
            
            for key, val in dictx['similarity'].items():
                if val >= threshold:
                    neighbor_set.add(key)


    # print(final_top[:2])

    # sorted_traffic_names = [t[0] for t in sorted_traffic_names]
    sorted_traffic_names = [list(t.keys())[0] for t in final_top]
    print("returned stuff")

    if only_one:
        if start_idx < len(sorted_traffic_names) and start_idx >= 0:
            return final_top[start_idx]

    end_idx = start_idx + TOPICS_PER_PAGE
    if start_idx >= len(sorted_traffic_names):
        return [], False

    if end_idx >= len(sorted_traffic_names):
        return sorted_traffic_names[start_idx:end_idx], False

    return sorted_traffic_names[start_idx:end_idx], True

    # print(sorted_traffic_names[:5])
    # return sorted_traffic_names[:5]
    # return ["Modi", "Trump", "LA Hacks"]

def get_greeting(u):
    return "Hi, %s!" % u.name

def get_country_prompt():
    msg = """Enter the # for the region you want to learn about %s"""

    places = ['\n' + str(i+1) + '  ' + t for i, t in enumerate(PLACES)]
    places = "".join(places)


    return msg % places

def get_topics_list(u):
    topic_list, more_topics = get_trending_topics(int(u.country), u.topic_idx)

    if len(topic_list) == 0:
        return "No more topics to show. Select one from above."

    topics_str = ["\n" + str(i+1+u.topic_idx) + ". " + t for i, t in enumerate(topic_list)]
    if more_topics:
        topics_str.append('\n"M"  ... for more topics')
    topics_str = "".join(topics_str)

    if u.topic_idx == 0:
        country = PLACES[int(u.country)]
        begin = "Here is what's trending in " + country
    else:
        begin = ""


    u.topic_idx = u.topic_idx + len(topic_list)
    u.save()

    
    return begin + topics_str + "\nSelect a topic by entering its #"

def get_topic_news(u, topic_idx):
    topic_info = get_trending_topics(int(u.country), topic_idx, only_one=True)
    print(topic_info)

def get_current_user(from_num):
    try:
        u = UserInfo.objects.get(number=from_num)
        print("Found user: " + u.number)
    except UserInfo.DoesNotExist:
        print("New user")
        u = UserInfo(number=from_num,country='*',name='*')
        u.save()

    return u

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def check_if_num_in_range(num, start=1, end=1000000):
    num = num.strip()
    if num[-1] == ')':
        num = num[:-1]

    if representsInt(num):
        if int(num) < start:
            return False
        if int(num) > end:
            return False
        return True
    return False
