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
