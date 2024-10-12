import requests
import json
import time
from datetime import datetime, time as dt_time  # Importing time as dt_time to avoid conflict

# Replace with the actual IP address of your Flask server
SERVER_URL = 'http://127.0.0.1:5000/send_data'  # Change to your server IP if needed

def get_current_shift():
    current_time = datetime.now().time()

    # Define shift times
    shift_1_start = dt_time(6, 0)  # 6:00 AM
    shift_1_end = dt_time(14, 0)    # 2:00 PM

    shift_2_start = dt_time(14, 0)  # 2:00 PM
    shift_2_end = dt_time(22, 0)    # 10:00 PM

    shift_3_start = dt_time(22, 0)  # 10:00 PM
    shift_3_end = dt_time(6, 0)     # 6:00 AM (next day)

    # Determine the current shift based on the time
    if shift_1_start <= current_time < shift_1_end:
        return 1
    elif shift_2_start <= current_time < shift_2_end:
        return 2
    elif shift_3_start <= current_time or current_time < shift_3_end:
        return 3
    else:
        return None  # No active shift

def simulate_raspberry_pi(pi_id):
    product_count = 0  # Initialize product count
    not_ok_count = 0    # Initialize Not OK count

    while True:
        # Increment counts by 1 for testing
        product_count += 1  # Increment product count
        not_ok_count += 1 if product_count % 10 == 0 else 0  # Increment Not OK count every 10 products

        shift = get_current_shift()  # Get the current shift based on time

        # Prepare the data to send
        data = {
            'pi_id': pi_id,
            'product_count': product_count,
            'not_ok_count': not_ok_count,
            'shift': shift
        }

        # Send the data to the server
        headers = {'Content-Type': 'application/json'}
        response = requests.post(SERVER_URL, data=json.dumps(data), headers=headers)
        print(response.json())

        time.sleep(5)  # Wait for 5 seconds before sending the next data

# Simulate Raspberry Pi 1
simulate_raspberry_pi('Side RH India 2.5/Octavia')
