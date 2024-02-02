# Weather Cast

## Local Deployment

### Docker startup

Inside of the repository directory run the following commands:
```shell
docker build --tag weathercast .
docker-compose up --build
```

### Docker shutdown

```shell
docker-compose down
```

### Direct app startup
You also can locally start the app even without docker:
```shell
panel serve src/app.py --autoreload --port 5008
```

### App interface
## Basics
After deploying the app (either directly or using Docker) you will be greeted by the following page.

<img width="1725" alt="Screenshot 2024-02-02 at 17 38 56" src="https://github.com/kshchuk/iasa-2024/assets/96624185/4599cf94-90d7-461c-81db-165f8758cf43">

Your starting point is Kyiv, capital of Ukraine. To choose a new geographic location you can either click on the map or enter its name in search bar, located at the uppermost corner. If you click on the map, searchbar displays closest recorded city/location to it.

## Predictions
After selecting location, you can choose paramaters for creating weather prediction: start date, end date and format (hourly or daily). Start and end date are restricted by yesterday - so we can actually compare results of our predictions with reality (also lower bound is 1985 because of API).

![image](https://github.com/kshchuk/iasa-2024/assets/96624185/ae99d80c-ad5a-47df-854a-0c497a0eb884)

After pressing button "Predict" you will see table of results with graphics for each parameter.
Model is training in runtime.

![image](https://github.com/kshchuk/iasa-2024/assets/96624185/443b6d81-8767-4881-b52f-5967035fbed7)
![image](https://github.com/kshchuk/iasa-2024/assets/98614059/0c5ef120-856b-4aa8-9c93-3a3c826333a9)
![image](https://github.com/kshchuk/iasa-2024/assets/96624185/12d70c0d-78a3-4940-a153-1b267a39cefd)

## Accuracy

The program works with accuracy (for example, for a one-day forecast):

```json
{
  "MAE": {
    "temperature_2m_max": 4.843785274072368,
    "temperature_2m_min": 2.321389825575265,
    "temperature_2m_mean": 0.7550294169010895,
    "sunshine_duration": 10245.870516646848,
    "precipitation_sum": 2.005132634202109,
    "precipitation_hours": 4.810381796158233,
    "wind_speed_10m_max": 2.265034454414431,
    "wind_gusts_10m_max": 5.918261581598748,
    "wind_direction_10m_dominant": 59.57907098209936
  }
}
```

(Tested on data from "2020-12-15" to "2021-01-01" at location (-11.754611883149868, 19.918700267723633))

Day 7 of the forecast:

```json
{
  "MAE": {
    "temperature_2m_max": 1.6072502043560597,
    "temperature_2m_min": 1.2600533888776115,
    "temperature_2m_mean": 1.1235168730263907,
    "sunshine_duration": 1318.5452697882822,
    "precipitation_sum": 1.7391070555115937,
    "precipitation_hours": 3.1401393876967587,
    "wind_speed_10m_max": 2.168524311293046,
    "wind_gusts_10m_max": 5.227003241677727,
    "wind_direction_10m_dominant": 101.68661402304062
  }
}
```

Day 30 of the forecast:

```json
{
  "MAE": {
    "temperature_2m_max": 3.259992719348105,
    "temperature_2m_min": 2.2311398483630356,
    "temperature_2m_mean": 2.1789147348819746,
    "sunshine_duration": 2382.7168698129317,
    "precipitation_sum": 0.9703819437927207,
    "precipitation_hours": 0.22774123298833904,
    "wind_speed_10m_max": 0.9313952349471961,
    "wind_gusts_10m_max": 2.0915679566065393,
    "wind_direction_10m_dominant": 178.23165126448154
  }
}
```

(Tested on data from "2020-01-01" to "2021-01-01" at location (-11.754611883149868, 19.918700267723633))

Day 365 of the forecast:

```json
{
  "MAE": {
    "temperature_2m_max": 0.08072807271954474,
    "temperature_2m_min": 0.1332458425827241,
    "temperature_2m_mean": 0.24579642776241073,
    "sunshine_duration": 2420.093302314308,
    "precipitation_sum": 2.9153344234939556,
    "precipitation_hours": 0.857514525550247,
    "wind_speed_10m_max": 2.3368065659020907,
    "wind_gusts_10m_max": 1.7427424464340149,
    "wind_direction_10m_dominant": 132.0382412575859
  }
}
```

(Tested on data from "2010-01-01" to "2021-01-01" at location (-11.754611883149868, 19.918700267723633))

Variable "weather_code" is predicted using current weather conditions.
