# LogQuarterSplitter

**LogQuarterSplitter** is a Python script designed for real-time log monitoring and analysis in Linux environments. It uses Linux commands and split log files into quarter-hour intervals. Additionally, it can search for a specific target word within the logs.

## Features

- Real-time monitoring of log files.
- Automatic splitting of logs into quarter-hour intervals.
- Search for a specific target word within the logs.
- Detailed logging and statistics generation.

## Prerequisites

Before using **LogQuarterSplitter**, ensure you have the following:

- Python 3.x installed.
- A Linux environment.
- A `config.ini` file configured with the appropriate paths and settings.

## Configuration

1. Clone this repository or download the script.
2. Configure the `config.ini` file with your settings:

   - `resultsFilePath`: The path where split log files will be saved.
   - `monitoredFilePath`: The path to the monitored log files.
   - `log_file_path`: The path to the log file where statistics will be logged.
   - `targetWord`: The specific word you want to search for in the logs (leave empty for no search).

## Usage

1. Run the script.
This will start real-time monitoring and log analysis.

2. The script will continuously monitor log files and split them into quarter-hour intervals based on time patterns.

3. If a `targetWord` is specified, the script will also search for and log occurrences of that word.

4. The script will create log files with statistics and update them as logs are analyzed.
Happy log monitoring!
