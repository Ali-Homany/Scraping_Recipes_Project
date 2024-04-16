import subprocess
import time
import os
import sys
import math


# Replace 'script.py' with the name of the Python file you want to run
SCRIPT_NAME = 'Crawler.py'
OUTPUT_PATH = lambda i: f'logs/iteration_{i}.txt'
DONE_PER_ITERATION = 10


def display_progress(n, total, elapsed_time):
    '''
    This function calculates the percentage finished, and displays the progress of the process on the console
    Args:
        - n (int): number of finished items
        - total (int): number of total items to be done
        - elapsed_time (int): duration of curr progress
    '''
    percentage = n/total * 100
    time_left = (100 - percentage) * elapsed_time/percentage
    msg = f'{percentage:.2f}% ({n} recipes out of {total}) scraped till now in {elapsed_time/60:.2f} mins. Estimated {time_left/60:.2f} mins left'
    length = len(msg)
    sys.stdout.write('\b'*length + ' '*length + '\b'*length)
    sys.stdout.flush()
    sys.stdout.write(msg)
    sys.stdout.flush()


def find_total():
    '''
    Returns:
        total (int): total number of recipes that need to be scraped, 0 returned when an error occurs
    '''
    try:
        with open('recipes_links.txt') as file:
            total = len(file.readlines())
    except:
        total = 0
    return total


start = time.time()
accumulated_duration = 0
total = find_total()
num_finished = 0
curr_finished = 0
i = 0
while num_finished < total or total == 0:
    # measure time consumed
    curr_start_time = time.time()
    result = subprocess.run(['python', SCRIPT_NAME], capture_output=True)
    curr_duration = time.time() - curr_start_time
    accumulated_duration += curr_duration

    # save result state
    stdout_output = ''

    # add process output to save it to file
    if result.stdout:
        stdout_output += result.stdout.decode('utf-8')
        # count scraped and failed
        curr_finished = result.stdout.decode('utf-8').count('Done')
        num_finished += curr_finished
        total -= result.stdout.decode('utf-8').count('An error')
    elif result.stderr:
        stdout_output += result.stderr.decode('utf-8')
    stdout_output += '\n'

    if result.returncode == 0:
        stdout_output = f"Script executed successfully ({curr_finished} recipes) in {curr_duration:.2f} seconds.\n\n" + stdout_output
    else:
        stdout_output = f"Script encountered an error in {curr_duration:.2f} seconds.\n\n" + stdout_output

    # if condition true, then recipes_links file didn't exist before, now it does
    if total <= 0:
        total += find_total() + num_finished
    display_progress(num_finished, total=total, elapsed_time=accumulated_duration)

    # write all output and error to log file
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
    with open(OUTPUT_PATH(i), 'w') as file:
        file.write(stdout_output)
        i += 1
