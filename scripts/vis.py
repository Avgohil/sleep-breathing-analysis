import pandas as pd
import matplotlib.pyplot as plt
import argparse 
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import os 

parser  = argparse.ArgumentParser()
parser.add_argument("-name", required=True)
args = parser.parse_args()

folder = args.name

# Load Nasal AirFlow

flow = pd.read_csv(folder + '/Flow - 30-05-2024.txt', sep = ';',skiprows=7,header=None)
flow.columns = ['timestamp', 'flow']

#timestamp format 
flow['timestamp'] =  flow['timestamp'].str.replace(',','.', regex = False)
flow['timestamp'] =pd.to_datetime(flow['timestamp'], dayfirst = True)

#set timestamp as index
flow = flow.set_index('timestamp')

# Load Thoracic 
thorac = pd.read_csv(folder + '/Thorac - 30-05-2024.txt', sep=';',skiprows=7,header=None)
thorac.columns = ['timestamp', 'thorac']
thorac['timestamp'] =  thorac['timestamp'].str.replace(',','.', regex = False)
thorac['timestamp'] =pd.to_datetime(thorac['timestamp'], dayfirst = True)
thorac = thorac.set_index('timestamp')

# Load SpO2
spo2 = pd.read_csv(folder + '/SPO2 - 30-05-2024.txt', sep=';',skiprows=7,header=None)
spo2.columns = ['timestamp', 'spo2']
spo2['timestamp'] =  spo2['timestamp'].str.replace(',','.', regex = False)
spo2['timestamp'] =pd.to_datetime(spo2['timestamp'], dayfirst = True)
spo2 = spo2.set_index('timestamp')

#convert to numeric 
spo2['spo2'] = pd.to_numeric(spo2['spo2'], errors='coerce')

# remove unrealistic values
spo2.loc[spo2["spo2"] < 70, "spo2"] = None

# Interpolate missing values
spo2['spo2'] = spo2['spo2'].interpolate()

# Load Flow Events
events = pd.read_csv(folder + '/Flow Events - 30-05-2024.txt', sep=';',skiprows=5,header=None)
events.columns = ['timestamp', 'duration', 'event_type','sleep_stage']

#Split start and end time 
events[['start','end']] = events['timestamp'].str.split('-', expand=True)
events['start'] = events['start'].str.replace(',','.', regex = False)
events['end'] = events['end'].str.replace(',','.', regex = False)
events['start'] = pd.to_datetime(events['start'], dayfirst = True)
events["end"] = events["start"].dt.date.astype(str) + " " + events["end"]
events["end"] = pd.to_datetime(events["end"])

# print(flow.head())
# print(thorac.head())
# print(spo2.head())
# print(events.head())

# subplots 

fig, axes = plt.subplots(3,1, figsize= (15,10), sharex = True)

# Nasal AirFlow
axes[0].plot(flow.index, flow['flow'], color ='blue')
axes[0].set_title('Nasal AirFlow')
axes[0].set_ylabel('Airflow')

# Thoracic
axes[1].plot(thorac.index, thorac['thorac'], color ='orange')
axes[1].set_title('Thoracic Movement')
axes[1].set_ylabel('Amplitude')

# SpO2
axes[2].plot(spo2.index, spo2['spo2'], color ='green')
axes[2].set_title('SpO2 Levels')
axes[2].set_ylabel('SpO2 (%)')
axes[2].set_xlabel('Time')

for ax in axes:
    ax.grid(True, alpha=0.3)
    # ax.set_xlabel("Time")
    ax.tick_params(axis='x', labelbottom=True)

# Overall title (participant)
fig.suptitle("Sleep Study — Participant AP01 | Full 8-Hour Recording")

axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes[2].xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45)
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45)
plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45)

# Overlay breathing events
for _, row in events.iterrows():

    if row["event_type"] == "Obstructive Apnea":
        color = "red"
    elif row["event_type"] == "Hypopnea":
        color = "purple"
    else:
        color = "gray"

    for ax in axes:
        ax.axvspan(row["start"], row["end"], color=color, alpha=0.25)

legend_elements =[
    Patch(facecolor='red', alpha=0.25, label='Obstructive Apnea'),
    Patch(facecolor='purple', alpha=0.25, label='Hypopnea'),
    Patch(facecolor='gray', alpha=0.25, label='Other Events')
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.02) )
plt.tight_layout()

os.makedirs('visualizations', exist_ok=True)
with PdfPages('visualizations/participant_ap01_full_recording.pdf') as pdf:
    pdf.savefig(fig)
plt.show()