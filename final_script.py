import os
import time
import subprocess
import configparser 
from datetime import datetime

# Initialize configuration
config = configparser.ConfigParser()
config.read('config.ini')

processed_files = set()

# Read configuration parameters
resultsFilePath = config.get('General', 'resultsFilePath')
monitoredFilePath = config.get('General', 'monitoredFilePath')
log_file_path = config.get('General', 'log_file_path')
targetWord = config.get('General', 'targetWord')

# Function to get the full path for the log file based on the date
def get_fullpath(date):
  file_name = f'CDRs-{date}.txt'
  fullpath = os.path.join(monitoredFilePath, file_name)
  
  # Create the file if it doesn't exist
  if not os.path.exists(fullpath):
    with open(fullpath,'a') as new_file:
      pass  # Creating an empty file

  return fullpath

# Function for monitoring the log files
def monitoring(): 
   now = datetime.now()
   hour = now.hour 
   minute = now.minute 
  
  # Determine the time interval
   if 0 <= minute <= 14: 
     i= 1 
   elif 15<= minute <= 29:
     i = 2 
   elif 30<= minute <=44: 
     i = 3 
   else:
     i = 4 
     
   date = now.strftime('%Y%m%d') 
   fullpath = get_fullpath(date) #CDRs_20230807.txt
   
   initial_size = os.path.getsize(fullpath)
   
   with open(fullpath, 'r',encoding = 'utf-8',errors='replace') as f:  
      file_lines = f.readlines()
      num_of_lines = len(file_lines) #0
      
   while True:     
   
      now = datetime.now()
      current_date = now.strftime('%Y%m%d')
      
      if current_date != date:
        fullpath = get_fullpath(current_date)
        num_of_lines = 0
        date = current_date
           
      current_size = os.path.getsize(fullpath)
   
      if current_size != initial_size :
         initial_size = current_size
         time.sleep(5)
         current_size = os.path.getsize(fullpath)
                
         if current_size == initial_size:
           print('FILE STOPPED UPDATING!')
           hour_str = "{:02d}".format(hour)
         
           split_file(date,i,hour_str,num_of_lines+1,fullpath) 
         
           with open(fullpath, 'r',encoding = 'utf-8',errors='replace') as file_to_monitor:
             file_lines = file_to_monitor.readlines()
             new_lines = len(file_lines)
             num_of_lines = new_lines
                  
           i += 1 

           if i == 5:
             i = 1
             hour += 1
            
           if hour == 24:
             hour = 0
            
   time.sleep(60)

# Function to split log files based on patterns
def split_file(date,i,hour_str,num_of_lines,fullpath): 
   patterns = {
             1:'([0-1][0-4]:[0-5][0-9].[0-999999])',
             2:'(1[5-9]|2[0-9]):[0-5][0-9].[0-999999]',
             3:'(3[0-9]|4[0-4]):[0-5][0-9].[0-999999]',
             4:'(4[5-9]|5[0-9]):[0-5][0-9].[0-999999]'
           }

   files = {
            1:f'{date}_{hour_str}_Q1.txt',
            2:f'{date}_{hour_str}_Q2.txt',
            3:f'{date}_{hour_str}_Q3.txt',
            4:f'{date}_{hour_str}_Q4.txt'
           }
  
   result_file = os.path.join(resultsFilePath, files[i])
   pattern = patterns[i]
   
   if f'{targetWord}' == '' :
     comm = subprocess.Popen(
                r"tail -n +{} {} | awk -F '|' '$4 ~ /{}:{}/ {{print}}' > {}".format(num_of_lines,fullpath,hour_str,pattern,result_file),
                shell=True,
                stdout=subprocess.PIPE,
                encoding='utf-8',
                errors='replace')  
                
     # Wait for the subprocess to finish before proceeding
     comm.communicate()  
     
   else:
     keywords = f'{targetWord}'
     
     comm = subprocess.Popen(
       r"tail -n +{} {} | awk -F '|' '$4 ~ /{}:{}/ {{print}}' | awk '/{}/' > {}".format(num_of_lines,fullpath,hour_str,pattern,keywords,result_file),
                shell=True,
                stdout=subprocess.PIPE,
                encoding='utf-8',
                errors='replace')  
                
     # Wait for the subprocess to finish before proceeding
     comm.communicate()   
   time.sleep(3)
   
   write_on_log(files[i])

# Function to write log file statistics
def write_on_log(file_name):
    filename = file_name
    filepath = os.path.join(resultsFilePath, filename) 
    with open (filepath,'r',encoding = 'utf-8',errors='replace') as f:
      if f'{targetWord}' == '':
        lines = f.readlines()
        num_lines= len(lines) 
        with open(log_file_path, 'a') as log: 
           log.write(f'number of lines in {filename} = {num_lines}' + '\n')
      else:
        # Count the occurrences of the word 
        contents = f.read() 
        count = contents.count(f'{targetWord}') 
        with open(log_file_path, 'a') as log: 
          log.write(f'{targetWord} is repeated {count} times in {file}' + '\n') 
                
    # Add the file to the set of processed files
    processed_files.add(filename)          

def main():
  monitoring()

if __name__ == "__main__":
  main()
