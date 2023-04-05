import datetime
import importlib
import pandas as pd
import prometheus_api_client

def append_query(query_string, df, timerange, label):
    start, stop, step = timerange
    query = prom.custom_query_range(query_string, start, stop, step)
    df = df.join(prometheus_api_client.MetricRangeDataFrame(query)['value']).rename(columns={'value': label})
    return df

if __name__ == '__main__':
    p5_proxy = {'http' : 'socks5h://localhost:1080'}
    prom = prometheus_api_client.PrometheusConnect(url="http://l1ts-prometheus.cms:9090", proxy=p5_proxy, disable_ssl=True)

    now = datetime.datetime.now()
    hourago = now - datetime.timedelta(minutes=60)
    timedelta = 30 # timestep in seconds
    timerange = (hourago, now, timedelta)

    runnumber_query = prom.custom_query_range('runnumber{job="sql-exporter"} '\
                                              'AND ON() runsession_parameters{trg_state="Running"}',
                                    hourago,
                                    now,
                                    timedelta)
    query_df = prometheus_api_client.MetricRangeDataFrame(runnumber_query).loc[:, ['value']].rename(columns={'value': 'runnumber'})

    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_108"} '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                            'AND ON() runsession_parameters{trg_state="Running"}',
                            query_df, timerange, 'l1_adt_80_rate')

    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_103"} '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                            'AND ON() runsession_parameters{trg_state="Running"}',
                            query_df, timerange, 'l1_adt_400_rate')

    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_095"} '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                            'AND ON() runsession_parameters{trg_state="Running"}',
                            query_df, timerange, 'l1_adt_4000_rate')

    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_094"} '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                            'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                            'AND ON() runsession_parameters{trg_state="Running"}',
                            query_df, timerange, 'l1_adt_20000_rate')

    print(query_df)
    query_df.to_pickle('L1AD_Monitoring.pkl')
