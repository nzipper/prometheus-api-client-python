import datetime
import pandas as pd
import prometheus_api_client

def df_from_query(query_string, timerange, label):
    query = prom.custom_query_range(query_string, *timerange)
    df = prometheus_api_client.MetricRangeDataFrame(query).loc[:, ['value']].rename(columns={'value': label})
    return df

def append_query(query_string, df, timerange, label):
    query = prom.custom_query_range(query_string, *timerange)
    df = df.join(prometheus_api_client.MetricRangeDataFrame(query)['value']).rename(columns={'value': label})
    return df

if __name__ == '__main__':
    p5_proxy = {'http' : 'socks5h://localhost:1080'}
    prom = prometheus_api_client.PrometheusConnect(url="http://l1ts-prometheus.cms:9090", proxy=p5_proxy, disable_ssl=True)

    # For given time range
    oms_data_format = '%Y-%m-%d %H:%M:%S'
    start = datetime.datetime.strptime('2023-04-09 08:35:27', oms_data_format)
    stop = datetime.datetime.strptime('2023-04-09 17:36:19', oms_data_format)
    # For recent update
    # stop = datetime.datetime.now()
    # start = now - datetime.timedelta(minutes=300)
    step = 20 # timestep in seconds (20s is minimum based on prometheus system refresh)
    timerange = (start, stop, step)

    # Suffix to query requiring active UGT systems (given by L1 TC)
    query_suffix = ' AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                   'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                   'AND ON() runsession_parameters{trg_state="Running"}'

    # Make Dataframe with Run Number, L1 Physics Rate, and all L1AD Rates
    query_df = df_from_query('runnumber{job="sql-exporter"}'+query_suffix, timerange, 'runnumber')
    query_df = append_query('rate_l1a_hz'+query_suffix, query_df, timerange, 'l1a_physics_rate')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_108"}'+query_suffix, query_df, timerange, 'l1_adt_80_rate')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_103"}'+query_suffix, query_df, timerange, 'l1_adt_400_rate')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_095"}'+query_suffix, query_df, timerange, 'l1_adt_4000_rate')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_094"}'+query_suffix, query_df, timerange, 'l1_adt_20000_rate')

    # Print and save
    print(query_df)
    query_df.to_pickle('L1AD_Monitoring.pkl')

    # For testing: just print query results
    # query = prom.custom_query_range('trg_run_info{job="sql-exporter"} AND ON() runsession_parameters{trg_state="Running"}', 
    #                                 *timerange)
    # print(query)