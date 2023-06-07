import datetime
import pandas as pd
import prometheus_api_client

def df_from_query(prom, query_string, timerange, label):
    query = prom.custom_query_range(query_string, *timerange)
    df = prometheus_api_client.MetricRangeDataFrame(query).loc[:, ['value']].rename(columns={'value': label})
    return df

def append_query(prom, query_string, df, timerange, label):
    query = prom.custom_query_range(query_string, *timerange)
    df = df.join(prometheus_api_client.MetricRangeDataFrame(query)['value']).rename(columns={'value': label})
    return df

def make_axol1tl_query(start=None,stop=None,step=None,save=True):
    p5_proxy = {'http' : 'socks5h://localhost:1080'}
    prom = prometheus_api_client.PrometheusConnect(url="http://l1ts-prometheus.cms:9090", proxy=p5_proxy, disable_ssl=True)

    # For given time range
    oms_data_format = '%Y-%m-%d %H:%M:%S'

    # Time range
    start = now - datetime.timedelta(minutes=start) if isinstance(start, int) else datetime.datetime.strptime('2023-05-24 14:50:05' if start is None else start, oms_data_format)
    stop = datetime.datetime.now() if 'now' in stop else datetime.datetime.strptime('2023-05-24 14:50:05' if stop is None else stop, oms_data_format)
    step = 20 if step is None else step # timestep in seconds (20s is minimum based on prometheus system refresh)
    timerange = (start, stop, step)

    # Suffix to query requiring active UGT systems (given by L1 TC)
    query_suffix = ' AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                   'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                   'AND ON() runsession_parameters{trg_state="Running"}'

    # Make Dataframe with Run Number, L1 Physics Rate, and all L1AD Rates
    query_df = df_from_query(prom, 'runnumber{job="sql-exporter"}'+query_suffix, timerange, 'runnumber')
    query_df = append_query(prom, 'rate_l1a_hz'+query_suffix, query_df, timerange, 'l1a_physics_rate')
    query_df = append_query(prom, 'swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_108"}'+query_suffix, query_df, timerange, 'l1_adt_80_rate')
    query_df = append_query(prom, 'swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_103"}'+query_suffix, query_df, timerange, 'l1_adt_400_rate')
    query_df = append_query(prom, 'swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_095"}'+query_suffix, query_df, timerange, 'l1_adt_4000_rate')
    query_df = append_query(prom, 'swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_094"}'+query_suffix, query_df, timerange, 'l1_adt_20000_rate')

    # Print and save
    if save:
        print(query_df)
        query_df.to_pickle('AXOL1TL_Monitoring.pkl')
    else:
        #For testing: just print query results
        query = prom.custom_query_range('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_095" ' \
                                        'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                                        'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                                        'AND ON() runsession_parameters{trg_state="Running"}', *timerange)
        query = prom.custom_query('runsession_parameters{trg_state=~\"Configured|Running\"}')
        print(query)

def make_topo_query(start=None,stop=None,step=None,save=True):
    p5_proxy = {'http' : 'socks5h://localhost:1080'}
    prom = prometheus_api_client.PrometheusConnect(url="http://l1ts-prometheus.cms:9090", proxy=p5_proxy, disable_ssl=True)

    # Time range
    start = now - datetime.timedelta(minutes=start) if isinstance(start, int) else datetime.datetime.strptime('2023-05-24 14:50:05' if start is None else start, oms_data_format)
    stop = datetime.datetime.now() if 'now' in stop else datetime.datetime.strptime('2023-05-24 14:50:05' if stop is None else stop, oms_data_format)
    step = 20 if step is None else step # timestep in seconds (20s is minimum based on prometheus system refresh)
    timerange = (start, stop, step)

    # Suffix to query requiring active UGT systems (given by L1 TC)
    query_suffix = ' AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="luminositySegmentNumber"} > 1 '\
                   'AND ON() swatch_metric_value{subsystem="UGT", board="Finor_slot07", metric="oc0Counter"} > 0 '\
                   'AND ON() runsession_parameters{trg_state="Running"}'

    # Make Dataframe with Run Number, L1 Physics Rate, and all L1AD Rates
    query_df = df_from_query('runnumber{job="sql-exporter"}'+query_suffix, timerange, 'runnumber')
    query_df = append_query('rate_l1a_hz'+query_suffix, query_df, timerange, 'l1a_physics_rate')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_000"}'+query_suffix, query_df, timerange, 'L1_TOPO_25')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_001"}'+query_suffix, query_df, timerange, 'L1_TOPO_154')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_002"}'+query_suffix, query_df, timerange, 'L1_TOPO_904')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_003"}'+query_suffix, query_df, timerange, 'L1_TOPO_1007')
    query_df = append_query('swatch_metric_value{subsystem="SPARE_UGT", metric=~"BPRATE_004"}'+query_suffix, query_df, timerange, 'L1_TOPO_1023')

    # Print and save
    if save:
        print(query_df)
        query_df.to_pickle('TOPO_Monitoring.pkl')
    else:
        #For testing: just print query results
        query = prom.custom_query('runsession_parameters{trg_state=~\"Configured|Running\"}')
        print(query)

if __name__ == '__main__':
    make_axol1tl_query()
    make_topo_query()