from .models import UserInfo

HELP_CMD = 'H'
NEWS_TOPICS_CMD = 'news'
PLACES = ["US","UK","India","Australia","Israel","Germany","Mexico","Japan","Korea","France"]

def get_help_text():
    return """Welcome to SMSNews! Enter
- "news" for latest topics"""

def get_new_user_text():
    return """Hey, welcome to SMSNews! Let's get to know you better..."""

def get_trending_topics(country_idx):
    return ["Modi", "Trump", "LA Hacks"]

def get_greeting(u):
    return "Hi, %s!" % u.name

def get_country_prompt():
    msg = """Enter the # for the region you want to learn about %s"""

    places = ['\n' + str(i+1) + ') ' + t for i, t in enumerate(PLACES)]
    places = "".join(places)


    return msg % places

def get_topics_list(u):
    topic_list = get_trending_topics(int(u.country))

    topics_str = ["\n" + str(i+1) + ") " + t for i, t in enumerate(topic_list)]
    topics_str = "".join(topics_str)

    country = PLACES[int(u.country)]
    return "Here is what's trending in " + country + topics_str + "\nSelect a topic by entering its #"

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
