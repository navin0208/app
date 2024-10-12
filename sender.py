import time
import requests
import json
from datetime import datetime, time as dt_time

SERVER_URL = 'http://navin0208.pythonanywhere.com/send_data'  # Update to your URL

def get_current_shift():
    current_time = datetime.now().time()
    shift_1_start = dt_time(6, 0)  
    shift_1_end = dt_time(14, 0)    
    shift_2_start = dt_time(14, 0)  
    shift_2_end = dt_time(22, 0)    
    shift_3_start = dt_time(22, 0)  
    shift_3_end = dt_time(6, 0)     

    if shift_1_start <= current_time < shift_1_end:
        return 1
    elif shift_2_start <= current_time < shift_2_end:
        return 2
    elif shift_3_start <= current_time or current_time < shift_3_end:
        return 3
    else:
        return None

def simulate_raspberry_pi(pi_id):
    product_count = 0  
    not_ok_count = 0    

    while True:
        product_count += 1  
        not_ok_count += 1 if product_count % 10 == 0 else 0  
        shift = get_current_shift()

        data = {
            'pi_id': pi_id,
            'product_count': product_count,
            'not_ok_count': not_ok_count,
            'shift': shift
        }

        headers = {'Content-Type': 'application/json'}

        try:
            start_time = time.time()  # Start timing the request
            response = requests.post(SERVER_URL, data=json.dumps(data), headers=headers, timeout=10)
            response.raise_for_status()
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            print(f"Response received in {elapsed_time:.2f} seconds: {response.json()}")
        except requests.exceptions.RequestException as e:
            print("Error sending data:", e)

        time.sleep(5)  # Wait for 5 seconds before sending the next data

simulate_raspberry_pi('Side LH India 2.5/Octavia')
