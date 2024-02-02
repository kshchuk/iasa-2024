# Hourly Parameter Definition

The parameter `&hourly=` accepts the following values. Most weather variables are given as an instantaneous value for the indicated hour. Some variables, like precipitation, are calculated from the preceding hour as an average or sum.

| Variable | Valid time | Unit | Description |
|----------|------------|------|-------------|
| temperature_2m | Instant | °C (°F) | Air temperature at 2 meters above ground |
| relative_humidity_2m | Instant | % | Relative humidity at 2 meters above ground |
| dew_point_2m | Instant | °C (°F) | Dew point temperature at 2 meters above ground |
| apparent_temperature | Instant | °C (°F) | Apparent temperature is the perceived feels-like temperature combining wind chill factor, relative humidity, and solar radiation |
| pressure_msl / surface_pressure | Instant | hPa | Atmospheric air pressure reduced to mean sea level (msl) or pressure at the surface. Typically, pressure on mean sea level is used in meteorology. Surface pressure gets lower with increasing elevation. |
| precipitation | Preceding hour sum | mm (inch) | Total precipitation (rain, showers, snow) sum of the preceding hour. Data is stored with a 0.1 mm precision. If precipitation data is summed up to monthly sums, there might be small inconsistencies with the total precipitation amount. |
| rain | Preceding hour sum | mm (inch) | Only liquid precipitation of the preceding hour including local showers and rain from large scale systems. |
| snowfall | Preceding hour sum | cm (inch) | Snowfall amount of the preceding hour in centimeters. For the water equivalent in millimeters, divide by 7. E.g. 7 cm snow = 10 mm precipitation water equivalent |
| cloud_cover | Instant | % | Total cloud cover as an area fraction |
| cloud_cover_low | Instant | % | Low-level clouds and fog up to 2 km altitude |
| cloud_cover_mid | Instant | % | Mid-level clouds from 2 to 6 km altitude |
| cloud_cover_high | Instant | % | High-level clouds from 6 km altitude |
| shortwave_radiation | Preceding hour mean | W/m² | Shortwave solar radiation as an average of the preceding hour. This is equal to the total global horizontal irradiation |
| direct_radiation / direct_normal_irradiance | Preceding hour mean | W/m² | Direct solar radiation as an average of the preceding hour on the horizontal plane and the normal plane (perpendicular to the sun) |
| diffuse_radiation | Preceding hour mean | W/m² | Diffuse solar radiation as an average of the preceding hour |
| global_tilted_irradiance | Preceding hour mean | W/m² | Total radiation received on a tilted pane as an average of the preceding hour. The calculation assumes a fixed albedo of 20% and an isotropic sky. Please specify tilt and azimuth parameters. Tilt ranges from 0° to 90° and is typically around 45°. Azimuth should be close to 0° (0° south, -90° east, 90° west). If azimuth is set to "nan", the calculation assumes a horizontal tracker. If tilt is set to "nan", it is assumed that the panel has a vertical tracker. If both are set to "nan", a bi-axial tracker is assumed. |
| sunshine_duration | Preceding hour sum | Seconds | Number of seconds of sunshine in the preceding hour per hour calculated by direct normalized irradiance exceeding 120 W/m², following the WMO definition. |
| wind_speed_10m / wind_speed_100m | Instant | km/h (mph, m/s, knots) | Wind speed at 10 or 100 meters above ground. Wind speed at 10 meters is the standard level. |
| wind_direction_10m / wind_direction_100m | Instant | ° | Wind direction at 10 or 100 meters above ground |
| wind_gusts_10m | Instant | km/h (mph, m/s, knots) | Gusts at 10 meters above ground of the indicated hour. Wind gusts in CERRA are defined as the maximum wind gusts of the preceding hour. Please consult the ECMWF IFS documentation for more information on how wind gusts are parameterized in weather models. |
| et0_fao_evapotranspiration | Preceding hour sum | mm (inch) | ET₀ Reference Evapotranspiration of a well-watered grass field. Based on FAO-56 Penman-Monteith equations, ET₀ is calculated from temperature, wind speed, humidity, and solar radiation. Unlimited soil water is assumed. ET₀ is commonly used to estimate the required irrigation for plants. |
| weather_code | Instant | WMO code | Weather condition as a numeric code. Follow WMO weather interpretation codes. See the table below for details. Weather code is calculated from cloud cover analysis, precipitation, and snowfall. As barely no information about atmospheric stability is available, estimation about thunderstorms is not possible. |
| snow_depth | Instant | meters | Snow depth on the ground. Snow depth in ERA5-Land tends to be overestimated. As the spatial resolution for snow depth is limited, please use it with care. |
| vapour_pressure_deficit | Instant | kPa | Vapor Pressure Deficit (VPD) in kilopascal (kPa). For high VPD (>1.6), water transpiration of plants increases. For low VPD (<0.4), transpiration decreases |
| soil_temperature_0_to_7cm / soil_temperature_7_to_28cm / soil_temperature_28_to_100cm / soil_temperature_100_to_255cm | Instant | °C (°F) | Average temperature of different soil levels below ground. |
| soil_moisture_0_to_7cm / soil_moisture_7_to_28cm / soil_moisture_28_to_100cm / soil_moisture_100_to_255cm | Instant | m³/m³ | Average soil water content as volumetric mixing ratio at 0-7, 7-28, 28-100, and 100-255 cm depths. |

# Daily Parameter Definition

Aggregations are a simple 24-hour aggregation from hourly values. The parameter `&daily=` accepts the following values:

| Variable | Unit | Description |
|----------|------|-------------|
| weather_code | WMO code | The most severe weather condition on a given day |
| temperature_2m_max / temperature_2m_min | °C (°F) | Maximum and minimum daily air temperature at 2 meters above ground |
| apparent_temperature_max / apparent_temperature_min | °C (°F) | Maximum and minimum daily apparent temperature |
| precipitation_sum | mm | Sum of daily precipitation (including rain, showers, and snowfall) |
| rain_sum | mm | Sum of daily rain |
| snowfall_sum | cm | Sum of daily snowfall |
| precipitation_hours | hours | The number of hours with rain |
| sunrise / sunset | iso8601 | Sun rise and set times |
| sunshine_duration | seconds | The number of seconds of sunshine per day is determined by calculating direct normalized irradiance exceeding 120 W/m², following the WMO definition. Sunshine duration will consistently be less than daylight duration due to dawn and dusk. |
| daylight_duration | seconds | Number of seconds of daylight per day |
| wind_speed_10m_max / wind_gusts_10m_max | km/h (mph, m/s, knots) | Maximum wind speed and gusts on a day |
| wind_direction_10m_dominant | ° | Dominant wind direction |
| shortwave_radiation_sum | MJ/m² | The sum of solar radiation on a given day in Megajoules |
| et0_fao_evapotranspiration | mm | Daily sum of ET₀ Reference Evapotranspiration of a well-watered grass field |
