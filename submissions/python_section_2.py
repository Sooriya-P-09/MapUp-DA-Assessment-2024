import pandas as pd
import networkx as nx
import datetime as dt
df = pd.read_csv(r"C:/Users/soori/Downloads/dataset-2.csv")
print(df)


def calculate_distance_matrix(file_path):
    df = pd.read_csv(file_path)
    G = nx.Graph()
    for index, row in df.iterrows():
        location_a = row['id_start']
        location_b = row['id_end']
        distance = row['distance']
        G.add_edge(location_a, location_b, weight=distance)
    locations = sorted(G.nodes())
    distance_matrix = pd.DataFrame(0, index=locations, columns=locations)
    for location_a in locations:
        for location_b in locations:
            if location_a != location_b:
                try:
                    shortest_distance = nx.shortest_path_length(G, source=location_a, target=location_b, weight='weight')
                    distance_matrix.loc[location_a, location_b] = shortest_distance
                    distance_matrix.loc[location_b, location_a] = shortest_distance
                except nx.NetworkXNoPath:
                    distance_matrix.loc[location_a, location_b] = float('inf')
    return distance_matrix
file_path =(r"C:/Users/soori/Downloads/dataset-2.csv")
result = calculate_distance_matrix(file_path)
result.head()


def unroll_distance_matrix(distance_matrix):
    unrolled_data = []
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                unrolled_data.append([id_start, id_end, distance_matrix.loc[id_start, id_end]])
    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df
unrolled_result = unroll_distance_matrix(result)
unrolled_result.head()


def find_ids_within_ten_percentage_threshold(unrolled_df, reference_value):
    reference_distances = unrolled_df[unrolled_df['id_start'] == reference_value]
    average_distance = reference_distances['distance'].mean()
    lower_threshold = average_distance * 0.90
    upper_threshold = average_distance * 1.10
    avg_distances_by_id = unrolled_df.groupby('id_start')['distance'].mean()
    ids_within_threshold = avg_distances_by_id[(avg_distances_by_id >= lower_threshold) & 
                                               (avg_distances_by_id <= upper_threshold)].index.tolist()
    return sorted(ids_within_threshold)
reference_value = unrolled_result['id_start'].iloc[0]
res=find_ids_within_ten_percentage_threshold(unrolled_result, reference_value)
res


def calculate_toll_rate(unrolled_df):
    rate_coefficients={
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6}
    unrolled_df['moto'] = unrolled_df['distance'] * rate_coefficients['moto']
    unrolled_df['car'] = unrolled_df['distance'] * rate_coefficients['car']
    unrolled_df['rv'] = unrolled_df['distance'] * rate_coefficients['rv']
    unrolled_df['bus'] = unrolled_df['distance'] * rate_coefficients['bus']
    unrolled_df['truck'] = unrolled_df['distance'] * rate_coefficients['truck']
    return unrolled_df
toll_rates_df = calculate_toll_rate(unrolled_result)
toll_rates_df.head()




def calculate_time_based_toll_rates(toll_rates_df):
    weekdays_intervals=[
    (datetime.time(0, 0), datetime.time(10, 0)),
    (datetime.time(10, 0), datetime.time(18, 0)),
    (datetime.time(18, 0), datetime.time(23, 59, 59))]
    weekdays_discount_factors = [0.8, 1.2, 0.8]
    weekends_discount_factor = 0.7
    toll_rates_df['start_day'] = 'Monday'
    toll_rates_df['start_time'] = datetime.time(0, 0)
    toll_rates_df['end_day'] = 'Sunday'
    toll_rates_df['end_time'] = datetime.time(23, 59, 59)
    for i in range(len(weekdays_intervals)):
        start_time, end_time = weekdays_intervals[i]
        discount_factor = weekdays_discount_factors[i]
        mask = (toll_rates_df['start_day'] >= 'Monday') & (toll_rates_df['start_day'] <= 'Friday') & (toll_rates_df['start_time'] >= start_time) & (toll_rates_df['end_time'] >= start_time) & (toll_rates_df['end_time'] <= end_time)
        toll_rates_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor

    mask = (toll_rates_df['start_day'] == 'Saturday') | (toll_rates_df['start_day'] == 'Sunday')
    toll_rates_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekends_discount_factor
    return toll_rates_df
time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rates_df)
time_based_toll_rates_df


