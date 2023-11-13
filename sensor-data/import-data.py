import csv
from influxdb import InfluxDBClient

# InfluxDB connection details
INFLUXDB_HOST = 'influxdb'
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = 'sensordata'
INFLUXDB_USER = 'root'
INFLUXDB_PASS = 'pass'

# CSV file path
CSV_FILE_PATH = 'sensor.csv'

def read_csv_data(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

def main():
    # Connect to InfluxDB
    client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASS, INFLUXDB_DATABASE)

    # Read data from CSV file
    data = read_csv_data(CSV_FILE_PATH)

    # Prepare data for InfluxDB insertion
    influx_data = []
    for row in data:
        influx_data.append(
            {
                'measurement': 'sensors',
                'tags': {
                    'DeviceID': row['Device ID'],
                    'DeviceName': row['Device Name']
                },
                'time': row['LastUpdateTime'],
                'fields': {
                    'DeviceStatus': row['Device Status'],
                    'SensorType' : row['Sensor Type']
                }
            }
        )

    # Write data to InfluxDB
    client.write_points(influx_data)

if __name__ == '__main__':
    print("Starting importing influx data")
    main()
    print("Done Importing influx data")
