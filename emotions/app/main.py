import google.auth
from event_processor import process_consumer, process_publisher
import threading

# set up the Google Cloud Default Credentials
credentials, project = google.auth.default()

# Create a thread and excecute the consumer's function
consumer_thread = threading.Thread(target=process_consumer, args=())
consumer_thread.start()