from datetime import datetime
from datetime import time
from time import perf_counter
import os
import string
from itertools import product
character_set = string.ascii_letters + string.digits + string.punctuation + ' ' # Get character set
def brute_force():
  minimum_length = int(input("Enter the minimum length: ")) # Get minimum and maximum length to generate
  maximum_length = int(input("Enter the maximum length: "))
  current_length = minimum_length
  combination_count = 0
  if minimum_length > maximum_length or minimum_length == 0 or maximum_length == 0: # Exit program in case of user error
    print("Invalid input.")
    os.system("pause")
    exit()
  while current_length <= maximum_length: # Calculate number of possible combinations
    current_count = pow(95, current_length)
    combination_count = combination_count + current_count
    current_length = current_length + 1
  confirmation = input(f"Generate {combination_count} possible combinations? (Y/N): ")
  if confirmation == 'N': # Exit if user input is N
    print("Exiting...")
    exit()
  current_length = minimum_length
  while current_length <= maximum_length:
    combination_counter = 0 # To count how many combinations have been generated
    starting_date_and_time = datetime.now()
    timer_start = perf_counter()
    title = open('generated.txt','a') # Log date and time when program starts
    title.write(f'<< Character generation started on: {starting_date_and_time} for combinations of length {current_length} >>\n')
    title.close()
    print(f"[{starting_date_and_time}] Character generation started.")
    log = open('generated.txt','a')
    for new_combination in (''.join(x) for x in product(character_set, repeat=current_length)): # Generate combination
      combination_counter = combination_counter + 1
      combination_percentage = round(float((combination_counter/combination_count) * 100), 2)
      log.write(f'{new_combination}\n')
      print(f"Time elapsed: [{datetime.now() - starting_date_and_time}] | {new_combination} ({combination_counter}/{combination_count} combinations of length range {minimum_length}-{maximum_length}) ({combination_percentage}%)", end = '\r') # Print combination in terminal
    ending_date_and_time = datetime.now()
    timer_stop = perf_counter()
    log.write(f"<< Combination generation ended on: {ending_date_and_time} for combinations of length {current_length} >>") # Log date and time where program ends
    log.close()
    time_elapsed = timer_stop - timer_start # Get elapsed time for generation.
    print(f"Printed {combination_count} combinations with time elapsed: {time_elapsed}")
    print(f"Started at {starting_date_and_time} and ended at {ending_date_and_time}")
    print(f"Average speed: {int(combination_count/time_elapsed)} words per second")
    current_length = current_length + 1
  log.close()
  redo = input("Generate again? (Y/N): ")
  if redo == 'Y':
    brute_force()
  else:
    os.system("pause")
    exit()
brute_force()
 