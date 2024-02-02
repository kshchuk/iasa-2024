all_daily_features = ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                      "sunshine_duration", "precipitation_sum", "precipitation_hours", "wind_speed_10m_max",
                      "wind_gusts_10m_max", "wind_direction_10m_dominant"]

daily_discrete_features = ["weather_code", "wind_direction_10m_dominant"]
daily_regressors = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]

all_hourly_features = ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "surface_pressure",
                       "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]

hourly_discrete_features = ["weather_code", "wind_direction_10m"]
hourly_regressors = ["temperature_2m", "surface_pressure", "wind_speed_10m"]