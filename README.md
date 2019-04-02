## Use it
Just text +1(858) 239 0484 from the texting/SMS app in your phone.

## Inspiration
A large fraction of the populations is still not connected to the internet. Modern web and native apps cater well to the tech savy audience. However, the users with not-so-advanced phones, no internet connection or even the elderly may be left behind.

## What it does
NewsByText leverages the Twilio API and the ubiquitous text messaging feature on mobile phones to provide our users with latest news without the need of internet. We have built a chat bot based service that users can interact with to read latest news. 

The users select their region and are then presented with a list of topics that have been trending in the last 1.5 hours. Upon selecting any of these topics, we scrape related articles from the internet, summarize it using deep learning and send back a short summary of the news as SMS. The users have option to read summaries from more sources and even have it translated to their language (currently supports Hindi)

## How we built it
We used several APIs to put together this hack. We only have a back-end and no front-end, as the user interacts with our service using the stock SMS/text messaging app in their phones.

The SMS infrastructure is provided using Twilio API. Upon receiving an SMS, the Twilio API calls a webhook on our backend. The backend is in Django. We fetch the latest trending topics for the user using the Taboola API. We filter the list of trends and present them to the user. 

Next, upon selecting a topic, we need to fetch its summary. We use some URLs of articles for the selected topic to fetch the article content. This is then converted into a short summary using the DeepAI API and sent back to the user as SMS. In case user has opted for news in Hindi, we use the Google Cloud Translation API to translate the summary into Hindi before sending it back.

All the above is in a Django based backend service.

## Challenges we ran into
Here are some of them:
- Trending topics may have very similar topics because they co-occur in news. We used similarity based heuristics  and a network graph to eliminate them.
- Maintaining state of users in backend

## Accomplishments that we are proud of
- Successfully implemented the chat flow for user interaction using the SMS app
- We need minimal and simple inputs and interactions from user
- Presenting the user only with relevant and non-overlapping trend topics

## What We learned
- Using Twilio to target users using just SMS

## What's next for NewsByText
- Allow users to select categories for news
