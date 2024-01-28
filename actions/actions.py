import random
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from rasa_sdk.events import EventType

class ActionAskLocation(Action):

    def name(self) -> Text:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # List of possible locations
        locations = ["Rome", "Milan", "Venice", "Florence", "Naples", "Turin", "Bologna", "Genoa", "Palermo", "Verona"]

        location = random.choice(locations)

        response = f"You are in {location}."

        dispatcher.utter_message(text=response)

        return []

def has_non_alphabetic_characters(name):
    return any(not c.isalpha() for c in name)

CHITCHAT_INTENTS = ["bot_challenge", "change_song", "find_gas_station", "ask_location"]

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        chitchat_intents = ["bot_challenge", "find_gas_station", "ask_location"]

        if tracker.latest_message["intent"]["name"] in chitchat_intents:
            intent_name = tracker.latest_message["intent"]["name"]
            dispatcher.utter_template(f"utter_{intent_name}", tracker)
            return {"first_name": None}

        if has_non_alphabetic_characters(slot_value):
            dispatcher.utter_message(
                text=f"Are you sure '{slot_value}' is correct? This did not sound right."
            )
            return {"first_name": None}

        if len(slot_value) < 3:
            dispatcher.utter_message(
                text="There is not such a short name in your contacts."
            )
            return {"first_name": None}

        return {"first_name": slot_value}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        chitchat_intents = ["bot_challenge", "find_gas_station", "ask_location"]

        if tracker.latest_message["intent"]["name"] in chitchat_intents:
            intent_name = tracker.latest_message["intent"]["name"]
            dispatcher.utter_template(f"utter_{intent_name}", tracker)
            return {"last_name": None}

        if has_non_alphabetic_characters(slot_value):
            dispatcher.utter_message(
                text=f"Are you sure '{slot_value}' is correct? This did not sound right."
            )
            return {"last_name": None}

        if len(slot_value) < 3:
            dispatcher.utter_message(
                text="There is not such a short last name in your contacts."
            )
            return {"last_name": None}

        return {"last_name": slot_value}
    
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="please rephrase that")
     
        
        return []


import requests 

class ActionGetNews(Action):
    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        api_key = 'fa015cdf060245468080b87969efc86a'
        endpoint = 'https://newsapi.org/v2/top-headlines'
        country_code = 'us'  

        params = {
            'country': country_code,
            'apiKey': api_key
        }

        response = requests.get(endpoint, params=params)
        news_data = response.json()

        if news_data['status'] == 'ok':
            articles = news_data['articles'][:2]  
            for article in articles:
                title = article['title']
                content = article['content']
                
                if content:
                    dispatcher.utter_message(f"{title}\n{content}")
                else:
                    dispatcher.utter_message(f"{title}\n(No content available)")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch the news at the moment.")

        return []
    
# προσπάθησα να το κάνω με dict αλλά δεν μου έβγαινε με τίποτα , οπότε το έκανα πιο απλοικά με δύο λίστες
ALLOWED_ARTISTS = [
    'Taylor Swift',
    'Morandi',
    'Drake',
    'Billie Eilish',
    'Ed Sheeran',
    'Beyoncé',
    'The Weeknd',
    'Ariana Grande',
    'BTS',
    'Adele',
    'Post Malone'
]

ALLOWED_SONGS = [
    'Love me',
    'Hotline Bling',
    'Bad Guy',
    'Shape of You',
    'Single Ladies (Put a Ring on It)',
    'Blinding Lights',
    'Thank U, Next',
    'Dynamite',
    'Hello',
    'Circles'
]

class ValidateMusicForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_music_form"

    def validate_title(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        chitchat_intents = ["bot_challenge", "find_gas_station", "ask_location"]
        
        if tracker.latest_message["intent"]["name"] in CHITCHAT_INTENTS:
            intent_name = tracker.latest_message["intent"]["name"]
            dispatcher.utter_template(f"utter_{intent_name}", tracker)
            return {"title": None}

        
        if slot_value.lower() not in map(str.lower, ALLOWED_SONGS):
            dispatcher.utter_message(
                text=f"I'm sorry, but I don't recognize that song. Please choose a song from our list."
            )
            return {"title": None}

        dispatcher.utter_message(text=f"Great choice!")
        return {"title": slot_value}

    def validate_artist(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        chitchat_intents = ["bot_challenge", "find_gas_station", "ask_location"]
        
        if tracker.latest_message["intent"]["name"] in CHITCHAT_INTENTS:
            intent_name = tracker.latest_message["intent"]["name"]
            dispatcher.utter_template(f"utter_{intent_name}", tracker)
            return {"artist": None}

        if slot_value.lower() not in map(str.lower, ALLOWED_ARTISTS):
            dispatcher.utter_message(
                text=f"I'm sorry, but I don't recognize that artist."
            )
            return {"artist": None}

        dispatcher.utter_message(text=f"OK!")
        return {"artist": slot_value}