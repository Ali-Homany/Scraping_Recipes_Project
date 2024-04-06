import subprocess
import time
import os
import sys
import math


# Replace 'script.py' with the name of the Python file you want to run
SCRIPT_NAME = 'Crawler.py'
OUTPUT_PATH = lambda i: f'logs/iteration_{i}.txt'
DONE_PER_ITERATION = 10


def display_progress(n, total):
    '''
    This function calculates the percentage finished, and displays the progress of the process on the console
    
    Args:
        - n (int): number of finished items
        - total (int): number of total items to be done
    '''
    percentage = n/total * 100
    msg = f'{percentage:.2f}% ({n} recipes out of {total}) scraped till now'
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


total = find_total()
i = 0
stdout_output = ''
while i < total or total == 0:
    # measure time consumed
    start_time = time.time()
    result = subprocess.run(['python', SCRIPT_NAME], capture_output=True)
    total_time = time.time() - start_time

    # save result state
    if result.returncode == 0:
        stdout_output += f"Script executed successfully ({i} recipes) in {total_time:.2f} seconds.\n\n"
    else:
        stdout_output += f"Script encountered an error in {total_time:.2f} seconds.\n\n"

    # add process output to save it to file
    if result.stdout:
        stdout_output += result.stdout.decode('utf-8')
        # count scraped and failed
        i += result.stdout.decode('utf-8').count('Done')
        total -= result.stdout.decode('utf-8').count('An error')
    elif result.stderr:
        stdout_output += result.stderr.decode('utf-8')
    stdout_output += '\n'
    
    # if condition true, then recipes_links file didn't exist before, now it does
    if total <= 0:
        total += find_total() + i
    display_progress(i, total=total)

    # write all output and error to log file
    with open(OUTPUT_PATH(i), 'w') as file:
        file.write(stdout_output)
