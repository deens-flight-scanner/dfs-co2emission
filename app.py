from math import radians, sin, cos, asin, sqrt

from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS
from pymysql.cursors import DictCursor

app = Flask(__name__)
CORS(app)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_USER'] = 'b68cef34044509'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ac42c229'
app.config['MYSQL_DATABASE_DB'] = 'heroku_7958580bc9bdd70'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-05.cleardb.net'

mysql.init_app(app)


@app.route('/')
def hello():
    return "calculate-co2"


@app.route('/calculate-co2', methods=['GET'])
def calculate_co2():
    # get arguments
    departure_code = request.args.get('departure')
    arrival_code = request.args.get('arrival')

    # connect to mysql db
    conn = mysql.connect()
    cursor = conn.cursor()

    # execute query to find departure arrival
    cursor.execute("SELECT id, code, lat, lon from airports WHERE code = '" + departure_code + "'")
    departure_airport = cursor.fetchone()
    # return None if airport is not in db
    if departure_airport is None:
        return jsonify(None)
        # return NotFound(departure_airport)

    departure_airport_lon = departure_airport['lon']
    departure_airport_lat = departure_airport['lat']

    # execute query to find arrival arrival
    cursor.execute("SELECT id, code, lat, lon from airports WHERE code = '" + arrival_code + "'")
    arrival_airport = cursor.fetchone()
    # return None if airport is not in db
    if arrival_airport is None:
        return jsonify(None)
        # return NotFound(departure_airport)

    arrival_airport_lon = arrival_airport['lon']
    arrival_airport_lat = arrival_airport['lat']

    # calculate distance between two points https://www.geeksforgeeks.org/program-distance-two-points-earth/
    departure_lon = radians(departure_airport_lon)
    departure_lat = radians(departure_airport_lat)
    arrival_lon = radians(arrival_airport_lon)
    arrival_lat = radians(arrival_airport_lat)

    difference_in_lon = arrival_lon - departure_lon
    difference_in_lat = arrival_lat - departure_lat

    distance = 6371 * 2 * asin(sqrt(sin(difference_in_lat / 2) ** 2 + cos(departure_lat) * cos(arrival_lat) * sin(
        difference_in_lon / 2) ** 2))  # radius of earth in kilometers = 6371

    # calculate average time of the flight from departure to arrival
    avg_time = distance * 850  # avg of 850 km/h in typical commercial passenger jet

    # calculate the amount of emission for the flight
    co2_emission = avg_time * 134  # kg CO2 per hour kg -> UK DfT source

    # close db connection
    conn.close()

    # return relevant information and the co2 emission in json format
    return \
        {"flight":
            {
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "distance": distance,
                "avg_time": avg_time,
                "co2_emission": co2_emission
            }
        }


if __name__ == '__main__':
    app.run(debug=False)

# if __name__ == '__main__':
#     conn = mysql.connect()
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT * from airports")
#     data = cursor.fetchone()
#
#     conn.close()
#
#     print(data)
