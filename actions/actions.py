from typing import Any, Text, Dict, List, Union
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sensorfetcher import SensorFetcher

class ActionRetrieveSensor(Action):
    def name(self) -> Text:
        return "action_retrieve_sensor"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) ->List[Dict[Text, Any]]:
        prediction = tracker.latest_message
        print(prediction)
        fetcher = SensorFetcher()
        # For fetch-sensor-details intent
        if prediction['intent']['name'] == 'fetch-all-sensors':
            response= fetcher.get_all_sensors()
            
            dispatcher.utter_message(text=json.dumps(response))
        elif prediction['intent']['name'] == 'count-sensors':
            response= fetcher.get_sensor_count()
            dispatcher.utter_message(text="There are total of "+str(response)+" sensors in the inventory.")
        elif prediction['intent']['name'] == 'fetch-running-sensors':
            response= fetcher.get_running_sensor_count()
            dispatcher.utter_message(text="There are total of "+str(response)+" sensors in the inventory which are running.")
        elif prediction['intent']['name'] == 'fetch-stopped-sensors':
            response= fetcher.get_stopped_sensor_count()
            dispatcher.utter_message(text="There are total of "+str(response)+" sensors in the inventory which are turned off.")
        elif prediction['intent']['name'] == 'fetch-sensor-details':
            entities = [entity['entity'] for entity in prediction['entities']]
            if 'sensor-id' in entities:
                sensor_id = [entity for entity in prediction['entities'] if entity['entity']=='sensor-id'][0]['value']
                try:
                    response= fetcher.get_sensor_details(sensor_id)[0]
                    keys= ["Last Update Time", "Sensor ID", "Device Name", "Sensor Status", "Sensor type"]
                    values = list(zip(keys, response))
                    message = "\n".join([": ".join(v) for v in values])
                    dispatcher.utter_message(text="We found results for the sensor:")
                    dispatcher.utter_message(text=str(message))
                except IndexError:
                    dispatcher.utter_message(text="Sorry! We can not find any sensor with id "+str(sensor_id)+".")
                    
            else:
                dispatcher.utter_message(text="Sorry You have not provided the Sensor device id.")
        else:
            dispatcher.utter_message(text="I apologize for not understanding your query. Could you please rephrase it. Thanks! ")
        
        return []
