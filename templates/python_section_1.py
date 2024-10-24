from typing import Dict, List

import pandas as pd


def reverse_by_n_elements(lst, n):
    output=[]
    for i in range(0,len(lst),n):
        rev=[]
        for j in range(i, min(i + n, len(lst))):
            rev.insert(0, lst[j])
        output.extend(rev)
    return output
print(reverse_by_n_elements([1, 2, 3, 4, 5, 6, 7, 8], 3))  
print(reverse_by_n_elements([1, 2, 3, 4, 5], 2))           
print(reverse_by_n_elements([10, 20, 30, 40, 50, 60, 70], 4))


def group_strings_by_length(lst):
    d = {}
    for char in lst:
        ln = len(char)  
        if ln not in d: 
            d[ln] = [char]
        else:
            d[ln].append(char)
    return d
print(group_strings_by_length(["apple", "bat", "car", "elephant", "dog", "bear"])) 

print(group_strings_by_length(["one", "two", "three", "four"]))

def flatten_dict(nested_dict):
    dic= {}
    dic["road.name"] = nested_dict["road"]["name"]
    dic["road.length"] = nested_dict["road"]["length"]
    dic["road.sections[0].id"] = nested_dict["road"]["sections"][0]["id"]
    dic["road.sections[0].condition.pavement"] = nested_dict["road"]["sections"][0]["condition"]["pavement"]
    dic["road.sections[0].condition.traffic"] = nested_dict["road"]["sections"][0]["condition"]["traffic"]
    return dic
nested_dict = {
    "road": {
        "name": "Highway 1",
        "length": 350,
        "sections": [
            {
                "id": 1,
                "condition": {
                    "pavement": "good",
                    "traffic": "moderate"
                }
            }
        ]
    }
}
dic = flatten_dict(nested_dict)
print(dic)


lst=[1, 1, 2]
lst.sort()
result=[]
def permute(current,remaining):
    if not remaining:
        result.append(current[:])
    else:
        for i in range(len(remaining)):
            if i > 0 and remaining[i] == remaining[i - 1]:
                continue
            permute(current + [remaining[i]], remaining[:i] + remaining[i + 1:])
permute([],lst)
print(result)


import re
#text="I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
text=input('')
date_pattern = r'\b\d{2}-\d{2}-\d{4}\b|\b\d{2}/\d{2}/\d{4}\b|\b\d{4}\.\d{2}\.\d{2}\b'
dates = re.findall(date_pattern, text)
print(dates)

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """
    return pd.Dataframe()


def rotate_and_transform(matrix):
    n = len(matrix)
    rotated_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n-1-i] = matrix[i][j]
        final_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i]) - rotated_matrix[i][j]
            col_sum = sum(rotated_matrix[k][j] for k in range(n)) - rotated_matrix[i][j]
            final_matrix[i][j] = row_sum + col_sum
    return final_matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
result = rotate_and_transform(matrix)
for row in result:
    print(row)


df = pd.read_csv(r"C:\Users\soori\Downloads\dataset-1.csv")
df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')
df_invalid_timestamps = df[df['start'].isna() | df['end'].isna()]
print(df_invalid_timestamps)
df = df.dropna(subset=['start', 'end'])
full_week = pd.date_range(start='00:00:00', end='23:59:59',freq='1H')
grouped = df.groupby(['id', 'id_2'])
result = pd.Series(index=grouped.groups.keys(), dtype=bool)
for (id_val, id_2_val), group in grouped:
    time_ranges = [pd.date_range(start=row['start'], end=row['end'], freq='1H') for _, row in group.iterrows()]
    combined_times = pd.concat([pd.Series(time) for time in time_ranges]).drop_duplicates().sort_values()
    result[(id_val, id_2_val)] = full_week.isin(combined_times).all()
result.head()

