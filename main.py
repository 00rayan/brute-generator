from datetime import datetime
from datetime import date
from time import perf_counter
import os
import string
import math
from itertools import product

character_set = string.ascii_letters + string.digits + string.punctuation + ' ' # Get character set

def convert(seconds):
  time = [] # time[0] = quantity, time[1] = units. eg. time[5,"hours"] represents 5 hours
  minutes = math.floor(seconds/60)
  hours = math.floor(minutes/60)
  days = math.floor(hours/24)
  years = math.floor(days/365)
  if years >= 1:
    time.append(years)
    time.append("years")
  elif days >= 1:
    time.append(days)
    time.append("days")
  elif hours >= 1:
    time.append(hours)
    time.append("hours")
  elif hours <= 1:
    time.append(minutes)
    time.append("minutes")
  elif minutes <= 1:
    time.append(seconds)
    time.append("seconds")
  str_time = f"{time[0]} {time[1]}"
  return str_time 

def is_performance_mode():
  performance_mode = True
  user_choice = input("Enable live progress display? (Only for high end systems) (Y/N): ")
  if user_choice == 'Y':
    confirmation = input("Are you sure? This is a horrible idea for any length past 3 characters. (Y/N): ")
    if confirmation == 'Y':
      print("Starting with live progress display.")
      performance_mode = False
    elif confirmation == 'N':
      print("Starting without live progress display.")
      performance_mode = True
  elif user_choice == 'N':
    print("Starting without live progress display.")
    performance_mode = True
  else:
    print("Invalid input.")
  return performance_mode
def main():
    combination_count = 0
    minimum_length = int(input("Enter the minimum length: ")) # Get minimum and maximum length to generate
    maximum_length = int(input("Enter the maximum length: "))
    if minimum_length > maximum_length: # Error check length
      print("Invalid.")
      os.system("pause")
    if minimum_length == 0 or maximum_length == 0:
      print("Length cannot be 0.")
      os.system("pause")
    else:
      combination_count = get_combination_count(minimum_length, maximum_length)
      is_benchmark = input("Run a benchmark to get estimated time? (Y/N): ") # Check if user wants to benchmark or not
      if is_benchmark == 'Y':
        perf_speed = brute_force(minimum_length,maximum_length,True,True)
        live_speed = brute_force(minimum_length,maximum_length,True,False)
        estimated_perf_time = convert(combination_count/perf_speed) #  Get estimated time in performance mode
        estimated_live_time = convert(combination_count/live_speed) # Get estimated time in live display mode
        t1 = f"{estimated_perf_time}"
        t2 = f"{estimated_live_time}"
        print(f"Estimated time in performance mode: {t1}")
        print(f"Estimated time in live display mode: {t2}")
      confirmation = input(f"Generate {combination_count} possible combinations? (Y/N): ") # Display number of combinations to user
      if confirmation == 'Y':
        brute_force(minimum_length, maximum_length, False,False)
      else:
        os.system("pause")
        exit()
def get_combination_count(minimum_length, maximum_length):
  current_length = minimum_length
  combination_count = 0
  while current_length <= maximum_length:
    current_count = pow(95, current_length) # Calculate combination count per length
    combination_count = combination_count + current_count # Total combination count
    current_length = current_length + 1
  return combination_count
def brute_force(minimum_length, maximum_length, benchmark, benchmark_mode):
  log_count = 1
  combination_count = get_combination_count(minimum_length, maximum_length)  # Get combination count
  if benchmark:
    combination_count = 100*((maximum_length-minimum_length)+1)
  if benchmark:
    performance_mode = benchmark_mode
  else:
    performance_mode = is_performance_mode()
  current_length = minimum_length

  while current_length <= maximum_length:
    combination_counter = 0 # To count how many combinations have been generated
    starting_date_and_time = datetime.now()
    timer_start = perf_counter()
    log_date = date.today()
    log_name = f"{log_date}"
    log = open(f'{log_name}.txt','a') # Log and output starting date and time
    log.write(f'<< Combination generation started on: {starting_date_and_time} for combinations of length {current_length} >>\n')
    print(f"[{starting_date_and_time}] Combination generation of length {current_length} started.")
    for new_combination in (''.join(x) for x in product(character_set, repeat=current_length)): # Generate combination
      log_name = f"{log_date}-log{log_count}"
      combination_counter = combination_counter + 1
      combination_percentage = round(float((combination_counter/combination_count) * 100), 2)
      log.write(f'{new_combination}\n')
      if performance_mode == False:
        print(f"Time elapsed: [{datetime.now() - starting_date_and_time}] | {new_combination}  ({combination_percentage}% complete)", end = '\r') # Output progress
      if benchmark and combination_counter == 100:
        break
    ending_date_and_time = datetime.now() # Output end date and time
    timer_stop = perf_counter()
    log.write(f"<< Combination generation ended on: {ending_date_and_time} for combinations of length {current_length} >>\n") # Log and output ending date and time
    log.close()
    print(f"[{starting_date_and_time}] Combination generaton of length {current_length} ended.")
    time_elapsed = timer_stop - timer_start # Get elapsed time for generation
    current_length = current_length + 1
  print(f"Printed {combination_count} combinations with time elapsed: {time_elapsed}") # Display final results
  speed = int(combination_count/time_elapsed)
  print(f"Average speed: {speed} combinations per second") # Display final speed for benchmarking
  log.close()
  if not benchmark:
    redo = input("Generate again? (Y/N): ")
    if redo == 'Y':
      main()
    else:
      os.system("pause")
      exit()
  return speed

while True: 
  main()