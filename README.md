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

#### Determining Prometheus Queries

To obtain the Prometheus queries required to request relevant quantities takes a bit of troubleshooting. Refer to the [cms-cactus documentation](https://gitlab.cern.ch/cms-cactus/ops/monitoring/prometheus/-/wikis/Trigger-queries) for the basics. Another good way to check if you have a viable query is to test it on the [online console](http://l1ts-prometheus.cms:9090) (provided your P5 tunnel is set up).

Finally, the quickest way to determine a query for a general quantity-of-interest is directly from Grafana (again, provided your P5 tunnel is set up). Shown in in the images below, you can 1) Navigate to any Grafana page with a metric you want. 2) Click the descriptor to get the dropdown menu, then click "Inspect", then "Panel JSON" 3) Navigate to the "expr" portion of the code and copy the value as your query. It may take some further formatting and troubleshooting, but this should give you the values you are interested in.

##### 1) 
<p align="center">
<img width="500" alt="Screen Shot 2023-04-11 at 08 26 12" src="https://user-images.githubusercontent.com/52294237/231077143-a8b87dd3-b694-450a-8599-ce979fa6f263.png">
</p>
 
##### 2) 
<p align="center">
<img width="500" alt="Screen Shot 2023-04-11 at 08 26 48" src="https://user-images.githubusercontent.com/52294237/231077231-06a1492f-47fd-424c-9f6a-c6a259772e3b.png">
</p>

##### 3)
<p align="center">
<img width="500" alt="Screen Shot 2023-04-11 at 08 27 13" src="https://user-images.githubusercontent.com/52294237/231077303-e34f08b6-6815-46a6-ae57-a3d254e5dc21.png">
</p>



