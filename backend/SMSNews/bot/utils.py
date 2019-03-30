HELP_CMD = 'h'
NEWS_TOPICS_CMD = 'news'

def get_help_text():
	return """Welcome to SMSNews! Enter
- "news" for latest topics"""

def get_trending_topics():
	return ["Modi", "Trump", "LA Hacks"]

def get_topics_list():
	topic_list = get_trending_topics()

	topics_str = ["\n" + str(i+1) + ") " + t for i, t in enumerate(topic_list)]
	topics_str = "".join(topics_str)
	return "Select a topic by entering its #" + topics_str