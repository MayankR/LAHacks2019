from .models import UserInfo

HELP_CMD = 'h'
NEWS_TOPICS_CMD = 'news'

def get_help_text():
    return """Welcome to SMSNews! Enter
- "news" for latest topics"""

def get_new_user_text():
    return """Hi, Welcome to SMSNews! Let's get to know you better... What is your name? :)"""

def get_trending_topics():
    return ["Modi", "Trump", "LA Hacks"]

def get_country_prompt(u):
    msg = """Hi %s, Enter the # for the region you want to learn about
1) IN
2) US
3) UK"""

    return msg % u.name

def get_topics_list():
    topic_list = get_trending_topics()

    topics_str = ["\n" + str(i+1) + ") " + t for i, t in enumerate(topic_list)]
    topics_str = "".join(topics_str)
    return "Select a topic by entering its #" + topics_str

def get_current_user(from_num):
    try:
        u = UserInfo.objects.get(number=from_num)
        print("Found user: " + u.number)
    except UserInfo.DoesNotExist:
        print("New user")
        u = UserInfo(number=from_num,country='*',name='*')
        u.save()

    return u
