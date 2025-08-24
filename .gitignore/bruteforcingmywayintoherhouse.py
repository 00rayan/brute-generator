import os
import string
from itertools import product
from time import perf_counter
from datetime import datetime, date
import multiprocessing
import functools
import psutil

CHARACTER_SET = string.ascii_letters + string.digits + string.punctuation + ' '

def get_unit(time):
    units = [(60, 'minutes'), (3600, 'hours'), (86400, 'days'), (31536000, 'years')]
    for unit_time, unit_name in units:
        if time < unit_time:
            return time, unit_name
        time /= unit_time
    return time, 'years'

def run_benchmark(mode, length=3):
    print(f"Benchmark test in {mode} started")
    speed = brute_force(length, length, True, True, 'message', 'Average')
    return speed

def is_performance_mode():
    user_choice = input("Enable live progress display? (Only for high-end systems) (Y/N): ").lower()
    if user_choice == 'y':
        confirmation = input("Are you sure? This is a horrible idea for any length past 3 characters. (Y/N): ").lower()
        if confirmation == 'y':
            print("Starting with live progress display.")
            return False
    print("Starting without live progress display.")
    return True

def get_combination_count(minimum_length, maximum_length):
    return sum(pow(len(CHARACTER_SET), length) for length in range(minimum_length, maximum_length + 1))

def generate_combinations(start_length, end_length, queue, max_memory_percent=80, initial_batch_size=100000):
    # Initialize batch size
    batch_size = initial_batch_size
    characters = CHARACTER_SET * end_length
    
    for current_length in range(start_length, end_length + 1):
        combination_counter = 0
        timer_start = perf_counter()

        # Check if combinations are possible for the current length
        if len(list(batched_combinations(current_length, batch_size, characters))) == 0:
            continue

        file_name = f'combinations_length{current_length}.txt'

        with open(file_name, 'w') as combination_file:
            for batch in batched_combinations(current_length, batch_size, characters):
                for new_combination in batch:
                    combination_file.write(new_combination + '\n')
                    combination_counter += len(new_combination)

                    # Check memory usage and adjust batch size if necessary
                    if combination_counter % 500000 == 0:
                        memory_percent = psutil.virtual_memory().percent
                        if memory_percent > max_memory_percent:
                            batch_size = int(batch_size * 0.9)  # Reduce batch size if memory usage is high
                        elif memory_percent < max_memory_percent - 5:
                            batch_size = int(batch_size * 1.1)  # Increase batch size if memory usage is low

        timer_stop = perf_counter()
        time_elapsed = timer_stop - timer_start

        queue.put((current_length, combination_counter, time_elapsed))

def batched_combinations(length, batch_size, characters):
    batches = [characters[i:i + batch_size] for i in range(0, len(characters), batch_size)]
    return [[''.join(x) for x in product(batch, repeat=length)] for batch in batches]

@functools.lru_cache(maxsize=None)  # Cache previously generated combinations
def get_cached_combinations(length):
    return list(batched_combinations(length, 100000, CHARACTER_SET))

def brute_force(minimum_length, maximum_length, performance_mode, benchmark, message, message_type):
    cores = multiprocessing.cpu_count()

    processes = []
    queue = multiprocessing.Queue()

    for i in range(cores):
        start_length = minimum_length + (i * (maximum_length - minimum_length + 1) // cores)
        end_length = minimum_length + ((i + 1) * (maximum_length - minimum_length + 1) // cores) - 1

        process = multiprocessing.Process(target=generate_combinations, args=(start_length, end_length, queue))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    total_combinations = 0
    total_time_elapsed = 0

    # Process queue until it's empty
    while not queue.empty():
        current_length, combinations_generated, time_elapsed = queue.get()
        total_combinations += combinations_generated
        total_time_elapsed += time_elapsed

    speed = total_combinations / total_time_elapsed if total_time_elapsed > 0 else float('inf')
    print(f"Printed {total_combinations} combinations with time elapsed: {total_time_elapsed} seconds")
    if total_time_elapsed > 0:
        print(f"{message_type} speed: {int(speed)} combinations per second")
    else:
        print(f"{message_type} speed: Infinite combinations per second")
    return speed

def main():
    minimum_length = int(input("Enter the minimum length: "))
    maximum_length = int(input("Enter the maximum length: "))

    if minimum_length >= maximum_length or minimum_length <= 0 or maximum_length <= 0:
        print("Invalid length input.")
        os.system("pause")
        return

    combination_count = get_combination_count(minimum_length, maximum_length)

    perf_speed = run_benchmark('Performance mode', 3)
    live_speed = run_benchmark('Live display mode', 3)

    perf_time_estimate, perf_unit = get_unit(combination_count / perf_speed)
    live_time_estimate, live_unit = get_unit(combination_count / live_speed)

    performance_mode = is_performance_mode()

    estimated_time, unit = (perf_time_estimate, perf_unit) if performance_mode else (live_time_estimate, live_unit)

    confirmation = input(f"Generate {combination_count} possible combinations? This will take approximately {estimated_time} {unit} (Y/N): ")

    if confirmation.lower() == 'y':
        brute_force(minimum_length, maximum_length, performance_mode, False, 'message', 'Average')
    else:
        os.system("pause")
        return

if __name__ == "__main__":
    main()
