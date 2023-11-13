from influxdb import InfluxDBClient
import os
import json
class SensorFetcher:
    # def __init__(self, host=os.environ.get('INFLUXDB_HOST'), port=os.environ.get('INFLUXDB_PORT'), database=os.environ.get('INFLUXDB_DATABASE'), username=os.environ.get('INFLUXDB_USER'), password=os.environ.get('INFLUXDB_PASS')):
    def __init__(self, host='influxdb', port=8086, database='sensordata', username='root', password='pass'):
    
        self.client = InfluxDBClient(host, port, username=username, password=password, database=database)
        self.database = database
        

    def fetch_query(self, query):
        result = self.client.query(query, database=self.database)
        return result.raw

    def get_sensor_count(self):
        query = f'SELECT COUNT(*) FROM sensors'
        result = self.fetch_query(query)
        return result['series'][0]['values'][0][1]

    def get_running_sensor_count(self):
        query = f'SELECT COUNT(*) FROM sensors WHERE "DeviceStatus" = \'On\''
        result = self.fetch_query(query)
        return result['series'][0]['values'][0][1]

    def get_stopped_sensor_count(self):
        query = f'SELECT COUNT(*) FROM sensors WHERE "DeviceStatus" = \'Off\''
        result = self.fetch_query(query)
        return result['series'][0]['values'][0][1]

    def get_sensor_details(self, sensor_id):
        query = f'SELECT * FROM sensors WHERE "DeviceID" = \'{sensor_id}\''
        result = self.fetch_query(query)
        return result['series'][0]['values']
    def get_all_sensors(self):
        query = f'SELECT * FROM sensors'
        result = self.fetch_query(query)
        return result['series'][0]['values']

        
if __name__ == '__main__':
    sensor_fetcher = SensorFetcher()

    # 1. How many sensors are there?
    sensor_count = sensor_fetcher.get_sensor_count()
    print(f'Total number of sensors: {sensor_count}')

    # 2. How many sensors are turned on/running?
    running_sensor_count = sensor_fetcher.get_running_sensor_count()
    print(f'Total number of sensors turned on/running: {running_sensor_count}')

    # 3. How many sensors are turned off/not running?
    stopped_sensor_count = sensor_fetcher.get_stopped_sensor_count()
    print(f'Total number of sensors turned off/not running: {stopped_sensor_count}')

    # 4. Show me the detail of e8c918d2-95a1-4c4d-9a1a-2e9df2fcd98d sensor
    sensor_id = 'e8c918d2-95a1-4c4d-9a1a-2e9df2fcd98d'
    sensor_details = sensor_fetcher.get_sensor_details(sensor_id)
    print(f'Sensor details for {sensor_id}:')
    for entry in sensor_details:
        print(entry)

    # 5. Show me all sensors
    all_sensors = sensor_fetcher.get_all_sensors()
    print('All sensors:')
    for entry in all_sensors:
        print(entry)
