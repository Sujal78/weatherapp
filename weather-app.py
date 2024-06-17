import dash
from dash import dcc, html, ctx
import requests
import webbrowser

app = dash.Dash(__name__)

# define the layout of the dashboard
app.layout = html.Div( 
    children=[
        html.H1(children='Weather Dashboard', style={'text-align': 'center', 'background-color': '#333333', 'padding': '20px', 'color': 'white'}),
        html.Div(
            children=[
                dcc.Input(id='city-input', type='text', placeholder='Enter a city name', value='Jodhpur',
                          style={'margin-right': '10px', 'align': 'left','font-size': '20px', 'padding': '5px 10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
                html.Button(id='submit-button', n_clicks=0, children='Submit', style={'padding': '5px 10px','align': 'left', 'color': 'white', 'background-color': '#333333', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer', 'font-size': '16px', 'hover': 'background-color: #ddd'}),
                html.Button(id='change-unit',n_clicks=0 ,children='Change Unit', style={'padding': '5px 10px','align': 'left', 'color': 'white', 'background-color': '#424242', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer', 'font-size': '16px', 'hover': 'background-color: #ddd', 'margin-left':'5px'})
            ],
            style={'display': 'flex', 'justify-content': 'left'}
        ),
        html.Div(children=[ html.Div(id='main-weather', style={'flex': '50%','margin': '10px', 'font-size': '16px', 'padding': '5px 10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
                            html.Div(id='weather-table')], style={'display': 'flex', 'justify-content': 'left'}),
        dcc.Graph(id='forecast-graph'),
        html.Div([
            html.Label('Number of Days to Display:', style={'padding' : '20px','font-size': '20px', 'color': '#333333'}),
            dcc.Slider(
                id='date-slider',
                min=1,
                max=5,
                step=1,
                value=3,
                marks={i: str(i) for i in range(1, 11)},
                className='slider-custom',
                included=False
            ),
        ], style={'margin': '20px', 'width': '80%', 'margin': '0 auto','padding': '20px'}),

        html.Div(id='openweathermap-widget', style={'text-align': 'center', 'margin-top': '50px'})   
    ],
    style={'max-width':'1200px','margin': '0 auto', 'font-family': 'Arial, sans-serif', 'background-color': '#f2f2f2', 'padding': '50px', 'text-align': 'center'}
)


# define a callback function to get latitude, longitude, and weather data from the OpenWeatherMap API
@app.callback(
    [dash.dependencies.Output('main-weather', 'children'),
     dash.dependencies.Output('weather-table', 'children'),
     dash.dependencies.Output('forecast-graph', 'figure')],
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.Input('change-unit', 'n_clicks')],
    [dash.dependencies.Input('date-slider', 'value')],
    [dash.dependencies.State('city-input', 'value')]
)
def update_output(n_clicks, btn,date_slider_value, value):


    if btn % 2 == 0:
        unit = 'metric'
        speed_unit = 'mps'
        temp_unit = '°C'
        level_unit = 'ft'
    else:
        unit = 'imperial'
        speed_unit = 'mph'
        temp_unit = '°F'
        level_unit = 'ft'
        
    api_key = "a2054ae789c252fda0b4fb84ee5b2671"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={value}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    
    # make a request to the OpenWeatherMap API to get the current weather data for the input city
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={api_key}"
    weather_response = requests.get(weather_url)
    
    weather_data = weather_response.json()
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    min_temp = weather_data['main']['temp_min']
    max_temp = weather_data['main']['temp_max']
    pressure = weather_data['main']['pressure']
    
    descr = weather_data['weather'][0]['description']
    
    
    # make a request to the OpenWeatherMap API to get the 5-day weather forecast for the input city
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={unit}&appid={api_key}"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    print(forecast_data)
    

    

    dates = []
    temperatures = []
    descriptions = []
    for i in range(0, date_slider_value*8):
        date = forecast_data['list'][i]['dt_txt']
        temperaturee = forecast_data['list'][i]['main']['temp']
        description = forecast_data['list'][i]['weather'][0]['description']
        dates.append(date)
        temperatures.append(temperaturee)
        descriptions.append(description)

    print(descriptions)




    
    
    # create a line chart using the extracted data and return it as the figure for the graph
    figure = {
        'data': [
            {'x': dates, 'y': temperatures, 'type': 'line', 'name': f'Temperature ({temp_unit})'},
        ],
        'layout': {
            'title': f'Weather Forecast for {value}',
            'yaxis': {'title': f'Temperature ({temp_unit})'},
            'xaxis': {'title': 'Date'},
        }
    }
    table_style = {
        'border': '5px solid #ddd',
        'border-collapse': 'collapse',
        'margin': '50px',
        'font-size': '1.2em',
    }

    row_style = {
        'border': '3px solid #ddd',
        'padding': '10px',
        'text-align': 'left',
        'margin': '0 200px 0 20px',
    }
   
    main_weather = html.Div(children=[
        html.H1(style={'color':'#434343'},children=f"{value}"),
        html.H2(children=f"{temp}{temp_unit}"),
        html.H2(style={'color':'#434343'}, children=f"Feels Like: {feels_like}{temp_unit}"),
        html.H3(style={'color':'#434343'}, children=f"Weather: {descr}"),
    ], style={'margin-bottom': '20px', 'align': 'left', 'border' : '5px solid #ddd'})
    
    output = html.Div(children=[
        html.Table(style=table_style, children=[
            html.Tr(children=[
                html.Td("Humidity"),
                html.Td(f"{humidity}%")
            ], style=row_style),
            html.Tr(children=[
                html.Td("Wind speed"),
                html.Td(f"{wind_speed} {speed_unit}")
            ], style=row_style),
            html.Tr(children=[
                html.Td("Min temperature"),
                html.Td(f"{min_temp}{temp_unit}")
            ], style=row_style),
            html.Tr(children=[
                html.Td("Max temperature"),
                html.Td(f"{max_temp}{temp_unit}")
            ], style=row_style)
            
          
        ])
    ])
    return main_weather, output, figure

if __name__ == '__main__':
    app.run_server(debug=False, port=8054)