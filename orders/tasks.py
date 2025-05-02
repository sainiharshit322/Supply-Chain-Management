from celery import shared_task
from time import sleep

@shared_task
def process_order_file(filename):
    # Simulated processing
    sleep(5)
    return f"Processed {filename}"

