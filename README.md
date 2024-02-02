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
After deploying the app (either directly or using Docker) you will be greeted by the following page.
<img width="1725" alt="Screenshot 2024-02-02 at 17 38 56" src="https://github.com/kshchuk/iasa-2024/assets/96624185/4599cf94-90d7-461c-81db-165f8758cf43">

Your starting point is Kyiv, capital of Ukraine. To choose a new geographic location you can either click on the map or enter its name in search bar, located at the uppermost corner. If you click on the map, searchbar displays closest recorded city/location to it.
