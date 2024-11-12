import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
import requests
import datetime

import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather():
    weather_data = None
    graph_filename = None
    if request.method == 'POST':
        city = request.form['city']
        
        # Geocoding to get latitude and longitude for the city using Open-Meteo's location API
        geocoding_response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}')
        
        if geocoding_response.status_code == 200 and geocoding_response.json().get('results'):
            location = geocoding_response.json()['results'][0]
            latitude, longitude = location['latitude'], location['longitude']
            
            # Fetch hourly forecast data for temperature
            weather_response = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,visibility&timezone=auto'
            )
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                graph_filename = generate_temperature_graph(weather_data)
            else:
                weather_data = {'error': 'Unable to retrieve weather data.'}
        else:
            weather_data = {'error': 'City not found'}
            
    return render_template('dash.html', weather_data=weather_data, graph_filename=graph_filename)

def generate_temperature_graph(weather_data):
    # Parse hourly temperature data
    times = weather_data['hourly']['time'][:24]  # Take data for the next 24 hours
    temperatures = weather_data['hourly']['temperature_2m'][:24]
    humidity = weather_data['hourly']['relative_humidity_2m'][:24]
    precipitation = weather_data['hourly']['precipitation_probability'][:24]
    visibility = weather_data['hourly']['visibility'][:24]

    time_labels = [datetime.datetime.fromisoformat(time).strftime('%H:%M') for time in times]

    # Plot temperature graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, temperatures, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Forecast for the Next 24 Hours')
    plt.tight_layout()
    graph_filename = './static/temperature_plot.png'
    plt.savefig(graph_filename)

    # Humidity Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, humidity, marker='o', linestyle='-', color='g', label='Humidity (%)')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Relative Humidity (%)')
    plt.title('Humidity Forecast for the Next 24 Hours')
    plt.tight_layout()
    plt.show()
    graph_filename = './static/humidity_plot.png'
    plt.savefig(graph_filename)

    # Precipitation Probability Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, precipitation, marker='o', linestyle='-', color='purple', label='Precipitation Probability (%)')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Precipitation Probability (%)')
    plt.title('Precipitation Probability for the Next 24 Hours')
    plt.tight_layout()
    plt.show()
    graph_filename = './static/precipitation_plot.png'
    plt.savefig(graph_filename)

    # Visibility Graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, visibility, marker='o', linestyle='-', color='orange', label='Visibility (km)')
    plt.xticks(rotation=45)
    plt.xlabel('Time (24 hours)')
    plt.ylabel('Visibility (km)')
    plt.title('Visibility Forecast for the Next 24 Hours')
    plt.tight_layout()
    plt.show()
    graph_filename = './static/visibility_plot.png'
    plt.savefig(graph_filename)

    # Save plot as image
    # Ensure the static directory exists
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists('static'):
        os.mkdir('static')
    graph_filename = './static/temperature_plot.png'
    graph_filename = './static/humidity_plot.png'
    graph_filename = './static/precipitation_plot.png'
    graph_filename = './static/visibility_plot.png'
    plt.savefig(graph_filename)
    plt.close()
    
    return graph_filename


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.mkdir('static')
    app.run(debug=True)