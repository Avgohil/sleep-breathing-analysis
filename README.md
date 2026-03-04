# Sleep Breathing Analysis

Analysis and visualization of physiological signals from sleep study recordings to detect breathing events and create labeled datasets.

## Overview

This project processes polysomnography (sleep study) data to:
- Visualize key signals: Nasal Airflow, Thoracic Movement, and SpO2
- Annotate breathing events: Hypopnea and Obstructive Apnea
- Create labeled datasets for machine learning applications

## Features

✓ **Signal Visualization** – Plot 8-hour sleep recordings with event annotations  
✓ **Signal Preprocessing** – Bandpass filter (0.17–0.4 Hz) for breathing frequencies  
✓ **Windowed Dataset** – 30-second windows with 50% overlap  
✓ **Event Labeling** – Automatic label assignment based on breathing event annotations  
✓ **PDF Export** – Save visualizations as publication-ready PDFs  

## Folder Structure

```
.
├── Data/                      # Raw signal data
│   ├── AP01/                  # Patient 1
│   ├── AP02/                  # Patient 2
│   └── ...
├── Dataset/                   # Processed output
│   └── breathing_dataset.csv  # Labeled windows
├── Visualizations/            # Generated plots (PDFs)
├── scripts/
│   ├── vis.py                 # Signal visualization script
│   └── create_dataset.py      # Preprocessing and dataset creation
└── README.md
```

## Data Format

Each patient folder contains:
- `Flow - [DATE].txt` – Nasal airflow signal
- `Thorac - [DATE].txt` – Thoracic movement signal
- `SPO2 - [DATE].txt` – Blood oxygen saturation
- `Flow Events - [DATE].txt` – Annotated breathing events

## Requirements

- Python 3.7+
- pandas
- numpy
- scipy
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone <https://github.com/Avgohil/sleep-breathing-analysis>
cd sleep-breathing-analysis
```

2. Install dependencies:
```bash
pip install pandas numpy scipy matplotlib
```

## Usage

### 1. Visualize Signals

Run the visualization script to plot signals and breathing events:

```bash
python scripts/vis.py
```

Output: Generates PDF plots in the `Visualizations/` folder

### 2. Create Dataset

Preprocess signals and generate a labeled dataset:

```bash
python scripts/create_dataset.py
```

Output: Creates `Dataset/breathing_dataset.csv` with:
- 30-second signal windows
- 50% overlap between windows
- Event labels based on annotations

## Dataset Output

The generated CSV contains:
- **Signal features** from each 30-second window
- **Labels** (Normal/Hypopnea/Obstructive Apnea) based on event overlap
- Ready for machine learning pipelines

## AI Assistance Disclosure

AI tools such as GitHub Copilot and ChatGPT  were used occasionally to assist with code suggestions, debugging, and documentation formatting.  
However, the implementation, testing, and understanding of the code were carried out by the author.

## Contact
- **Email** : ankitagohil945@gmail.com
