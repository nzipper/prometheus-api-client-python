# prometheus-api-client

A Python wrapper for the Prometheus http api and some tools for metrics processing. This fork is modified to use a proxy, such that one can tunnel to the P5 CMS network and query the prometheus server there. Make sure your tunnel is set up and remember which port on your local machine you are using for forwarding.

### Usage
[Prometheus](https://prometheus.io/), a Cloud Native Computing Foundation project, is a systems and service monitoring system. It collects metrics (time series data) from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true. The raw time series data obtained from a Prometheus host can sometimes be hard to interpret. To help better understand these metrics we have created a Python wrapper for the Prometheus http api for easier metrics processing and analysis.

The `prometheus-api-client` library consists of multiple modules which assist in connecting to a Prometheus host, fetching the required metrics and performing various aggregation operations on the time series data.

#### Connecting and Collecting Metrics from a Prometheus host
The `PrometheusConnect` module of the library can be used to connect to a Prometheus host. This module is essentially a class created for the collection of metrics from a Prometheus host. It stores the following connection parameters:

-   **url** - (str) url for the prometheus host
-   **proxy** - (dict) A dictionary that maps protocols to proxy urls
-   **headers** – (dict) A dictionary of http headers to be used to communicate with the host. Example: {“Authorization”: “bearer my_oauth_token_to_the_host”}
-   **disable_ssl** – (bool) If set to True, will disable ssl certificate verification for the http requests made to the prometheus host

```python
from prometheus_api_client import PrometheusConnect

p5_proxy = {'http' : 'socks5h://localhost:1080'}
prom = PrometheusConnect(url="http://l1ts-prometheus.cms:9090", proxy=p5_proxy, disable_ssl=True)
```

You can then access the prometheus server with PromQL formatted queries to get CMS monitoring information, giving a dersired time range and resolution.

```python
import datetime

start = now - datetime.timedelta(minutes=300)
stop = datetime.datetime.now()
step = 20 # timestep in seconds
query = prom.custom_query_range(<Query String>, start, stop, step)
```

#### Getting Data as pandas DataFrames


```python
from prometheus_api_client import MetricRangeDataFrame
query_df = MetricRangeDataFrame(query)
```

For more functions included in the `prometheus-api-client` library, please refer to this [documentation.](https://prometheus-api-client-python.readthedocs.io/en/master/source/prometheus_api_client.html)
