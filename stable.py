from datetime import datetime
from datetime import time
from time import perf_counter
import os
import string
from itertools import product
character_set = string.ascii_letters + string.digits + string.punctuation + ' ' # Get character set
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
      confirmation = input(f"Generate {combination_count} possible combinations? (Y/N): ") # Display number of combinations to user
      if confirmation == 'Y':
        brute_force(minimum_length, maximum_length)
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
def brute_force(minimum_length, maximum_length):
  combination_count = get_combination_count(minimum_length, maximum_length)  # Get combination count
  current_length = minimum_length
  while current_length <= maximum_length:
    combination_counter = 0 # To count how many combinations have been generated
    starting_date_and_time = datetime.now()
    timer_start = perf_counter()
    title = open('generated.txt','a') # Log and output starting date and time
    title.write(f'<< Combination generation started on: {starting_date_and_time} for combinations of length {current_length} >>\n')
    title.close()
    print(f"[{starting_date_and_time}] Combination generation of length {current_length} started.")
    log = open('generated.txt','a')
    for new_combination in (''.join(x) for x in product(character_set, repeat=current_length)): # Generate combination
      combination_counter = combination_counter + 1
      combination_percentage = round(float((combination_counter/combination_count) * 100), 2)
      log.write(f'{new_combination}\n')
      print(f"Time elapsed: [{datetime.now() - starting_date_and_time}] | {new_combination}  ({combination_percentage}% complete)", end = '\r') # Output progress
    ending_date_and_time = datetime.now() # Output end date and time
    timer_stop = perf_counter()
    log.write(f"<< Combination generation ended on: {ending_date_and_time} for combinations of length {current_length} >>\n") # Log and output ending date and time
    log.close()
    print(f"[{starting_date_and_time}] Combination generaton of length {current_length} ended.")
    time_elapsed = timer_stop - timer_start # Get elapsed time for generation
    current_length = current_length + 1
  print(f"Printed {combination_count} combinations with time elapsed: {time_elapsed}") # Display final results
  print(f"Average speed: {int(combination_count/time_elapsed)} words per second") # Display final speed for benchmarking
  log.close()
  redo = input("Generate again? (Y/N): ")
  if redo == 'Y':
    main()
  else:
    os.system("pause")
    exit()

main()
