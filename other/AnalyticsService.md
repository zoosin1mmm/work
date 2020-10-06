
# Murano Analytics Service

>Murano Analytics Service for ETL Data Processing and Advanced Analytical APIs


### Operations


#### Analytics
  * [Test123.addressToGPS()](#addresstogps)  - Get approximated GPS longitude and latitude based on address
  * [Test123.dataTrans()](#datatrans)  - Manipulate and transform TSDB export data with a pipeline
  * [Test123.detectAnomalies()](#detectanomalies)  - Detect anomalies from given univariate timeseries data
  * [Test123.forecast()](#forecast)  - Forecast future data points given historical univariate timeseries data
  * [Test123.geoLocation()](#geolocation)  - Get approximated GPS longitude and latitude of an IP address
  * [Test123.gpsToAddress()](#gpstoaddress)  - Get approximated address based on GPS longitude and latitude



## Operations


### Analytics
  ---
### addressToGPS

>Get approximated GPS longitude and latitude based on address

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| **address** | *string* |  Address text |

#### Responses

##### GPS info extracted
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- Get GSP longitude and latitude from address
local out = Analytics.addressToGPS({
  address = "No. 22, Lane 74, Linxi Road, Shilin District, Taipei City, Taiwan 111"
})
response.message = out

```

  ---
### dataTrans

>Manipulate and transform TSDB export data with a pipeline

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| url | *string* |  The download url of remote csv file. |
| pipelines | [ [ *object* ] ] |  A list of pipelines. |

#### Responses

##### Data transformated
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- get download url with filename (assume export job completed)
local expires_in = 3600
local content_id = "export_1d"
local _, out = content.download(content_id, expires_in)

-- execute pipeline operations
local out = Analytics.dataTrans({
  url = out.url,
  pipelines = {
    {
      op = "SELECT",
      value = "city, model, sn, H29"
    },
    {
      op = "GROUP_BY",
      value = "city, model, sn",
      target = "H29",
      ["function"] = "count"
    },
    {
      op = "FILTER",
      value = "count > 0"
    },
    {
      op = "ORDER_BY",
      value = "-count"
    },
    {
      op = "LIMIT",
      value = 10
    }
  }
})
response.message = out

```

  ---
### detectAnomalies

>Detect anomalies from given univariate timeseries data

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| data | [ *nil* ] |  Univariate timerseries data array with unix timestamp and value for each row. |
| direction | *string* |  Directionality of the anomalies to be detected. (Optional)<br />Options: pos (positive only), neg (negative only), both (positive or negative)<br/>Default: "both" |
| max_anoms | *number* |  Maximum number of anomalies to detect as a percentage of the data.<br />Default value is 5%, which means at most 5% of the data points will be considered as anomalies. (Optional)<br/>Default: 0.05 |
| alpha_level | *number* |  The level of statistical significance (the probability of false positive) with which to accept or reject anomalies.<br />Default value is 5%, which means it is acceptable to have a 5% probability of incorrectly false positive detections. (Optional)<br/>Default: 0.05 |
| return_score | *boolean* |  Whether to return anomaly scores. It is computed by the absolute percentage of difference between actual and expected values for each detect anomaly.<br />The higher the score, the greater the deviation of anomaly values. (Optional)<br/>Default: true |
| recent_window | *integer* |  An integer to indicate relative seconds of recent window to return latest detected anomalies.<br />Set -1 as the value to disable this constraint. (Optional)<br/>Default: 5 |
| ignore_level_changes | *boolean* |  Whether to ignore level changes of data when detecting anomalies. (Optional)<br/>Default: true |

#### Responses

##### Anomaly data extracted
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- fetch recent device data points from TSDB service
local metrics = {"humidity"}
local tags = {
  sid = "device001"
}
local ts_data = Tsdb.query({
  metrics = metrics,
  tags = tags,
  relative_start = "-30m",
  epoch = "ms",
  mode = "split",
  sampling_size = "1s",
  fill = "previous",
  limit = 150
})
-- detect anomalies
local out = Analytics.detectAnomalies({
  data = ts_data.values[1],
  recent_window = 5,
  max_anoms = 0.05,
  direction = "both",
  alpha_level = 0.05,
  return_score = true
})
response.message = out

```

  ---
### forecast

>Forecast future data points given historical univariate timeseries data

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| data | [ *nil* ] |  Univariate timerseries data array with unix timestamp and value for each row. |
| method | *string* |  Method to use for forecasting the seasonally adjusted series. (Optional)<br />Options: arima (Autoregressive Integrated Moving Average model), ets (Exponential Smoothing state space model)<br/>Default: "ets" |
| frequency | *integer* |  The number of observation data points per period (or cycle). Period means the time unit of observation windows used for capturing trend and seasonality patterns.<br />For example, for hourly data, the frequency is 24 because the time unit is usually by day. (Optional)<br/>Default: 20 |
| prediction_num | *integer* |  The number of future data points to predict.<br />The interval of predicted data points will be based on the periodicity detected from given data. (Optional)<br/>Default: 20 |
| remove_outliers | *boolean* |  Whether to remove outlier data using IQR technique before training forecasting model. (Optional)<br />It is usually helpful for getting more stable predictions if abnormal spikes and dips in the data can be treated as noises.<br/>Default: true |
| return_confidence | *boolean* |  Whether to return upper and lower bound of confidence intervals for predicted data points.<br />Used together with confidence_level argument.<br/>Default: true |
| confidence_interval | *string* |  Confidence interval (CI) for predictions. 95% or 80% are available options.<br />For example, a confidence interval of 80% mean that we are 80% confident that the true value of the forecasting data is in our confidence interval.<br />Options: 95p (only compute 95% interval), 80p (only compute 80% interval), both (compute 80% and 95% intervals)<br/>Default: "80p" |

#### Responses

##### Forecasting data generated
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- fetch recent device data points from TSDB service
local metrics = {"humidity"}
local tags = {
  sid = "device001"
}
local ts_data = Tsdb.query({
  metrics = metrics,
  tags = tags,
  relative_start = "-1d",
  epoch = "ms",
  mode = "split",
  sampling_size = "1s",
  fill = "previous",
  limit = 180
})
-- forecast future data points
local out = Analytics.forecast({
  data = ts_data.values[1],
  prediction_num = 10,
  frequency = 60,
  remove_outliers = true,
  return_confidence = true
})
response.message = out

```

  ---
### geoLocation

>Get approximated GPS longitude and latitude of an IP address

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| **ip** | *string* |  IP address |

#### Responses

##### Geo-location info extracted
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- Get GPS location info of an IP address
local out = Analytics.geoLocation({
  ip = "8.8.8.8"
})
response.message = out

```

  ---
### gpsToAddress

>Get approximated address based on GPS longitude and latitude

#### Arguments

##### parameters  -  *object*  -  *Object containing service call parameters.*

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| **lon** | *string* |  GPS longitude |
| **lat** | *string* |  GPS latitude |

#### Responses

##### Address info extracted
**Content:**  *nil*

##### Error
**Content:**  *object*
The response to the caller

| Name        | Type          | Description  |
| ----------- |:-------------:| ------------ |
| error | *string* |  Error Message in case of failure |
| result | *object* |  Result message |

#### Example
```lua
-- Get address from GSP longitude and latitude 
local out = Analytics.gpsToAddress({
  lon = 25.094591022301255,
  lat = 121.54939102230125
})
response.message = out

```

