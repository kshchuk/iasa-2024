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
After selecting location, you can choose paramaters for creating weather prediction: start date, end date and format (hourly or daily). Start and end date are restricted by yesterday - so we can actually compare results of our predictions with reality.
![image](https://github.com/kshchuk/iasa-2024/assets/96624185/ae99d80c-ad5a-47df-854a-0c497a0eb884)

After pressing button "Predict" you will see table of results with graphics for each parameter.
![image](https://github.com/kshchuk/iasa-2024/assets/96624185/443b6d81-8767-4881-b52f-5967035fbed7)
![image](![image](https://github.com/kshchuk/iasa-2024/assets/98614059/0c5ef120-856b-4aa8-9c93-3a3c826333a9)
![image](https://github.com/kshchuk/iasa-2024/assets/96624185/12d70c0d-78a3-4940-a153-1b267a39cefd)
