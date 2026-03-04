import pandas as pd 
import numpy as np 
import argparse
import os
from scipy.signal import butter, filtfilt

parser  = argparse.ArgumentParser()
parser.add_argument("-in-dir", required=True)
parser.add_argument("-out-dir", required=True)

args = parser.parse_args()

data_folder = args.in_dir
output_folder = args.out_dir

os.makedirs(output_folder, exist_ok=True)

# Load Nasal AirFlow

flow = pd.read_csv(data_folder + r'\AP01\Flow - 30-05-2024.txt', sep = ';',skiprows=7,header=None)
flow.columns = ['timestamp', 'flow']
#timestamp format
flow['timestamp'] =  flow['timestamp'].str.replace(',','.', regex = False)
flow['timestamp'] =pd.to_datetime(flow['timestamp'], dayfirst = True)
#set timestamp as index
flow = flow.set_index('timestamp')

def bandpass_filter(signal, lowcut, highcut, fs):

    nyquist = 0.5*fs
    low = lowcut/nyquist
    high = highcut/nyquist
    b, a = butter(4, [low, high], btype='band')

    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

fs = 32

flow['filtered_flow'] = bandpass_filter(flow['flow'], 0.17, 0.4, fs)

window_size = 30
step_size = 15

windows = []

start_time = flow.index.min()
end_time = flow.index.max()
current_start = start_time

while current_start + pd.Timedelta(seconds=window_size) <= end_time:
    current_end = current_start + pd.Timedelta(seconds=window_size)
    window_data =flow.loc[current_start:current_end]

    if len(window_data) > 0:
        flow_mean = window_data['filtered_flow'].mean()

        windows.append({
            'start': current_start,
            'end': current_end,
            'flow_mean': flow_mean
        })
    current_start += pd.Timedelta(seconds=step_size)
windows_df = pd.DataFrame(windows)
# print(windows_df.head())   

events = pd.read_csv(data_folder + r'\AP01\Flow Events - 30-05-2024.txt', sep=';',skiprows=5,header=None)
events.columns = ['timestamp', 'duration', 'event_type','sleep_stage']
events[['start','end']] = events['timestamp'].str.split('-', expand=True)
events['start'] = events['start'].str.replace(',','.', regex = False)
events['end'] = events['end'].str.replace(',','.', regex = False)
events['start'] = pd.to_datetime(events['start'], dayfirst = True)
events["end"] = events["start"].dt.date.astype(str) + " " + events["end"]
events["end"] = pd.to_datetime(events["end"])

labels = []

for _, window in windows_df.iterrows():
    label = 'normal'
    for _, event in events.iterrows():
        overlap_start = max(window['start'], event['start'])
        overlap_end = min(window['end'], event['end'])

        overlap = (overlap_end - overlap_start).total_seconds()

        if overlap > 15:
            label = event['event_type']
            break
    labels.append(label)
windows_df['label'] = labels

output_path = os.path.join(output_folder, "breathing_dataset.csv")

windows_df.to_csv(output_path, index=False)

print("Dataset saved to:", output_path)