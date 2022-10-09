import pika
import threading
import json
from vision import analyze_emotion

def on_message_received(ch, method, properties, body):
    """
    This function gets excecuted when the consumer connection receives
    a new message from the load-images queue.

    Args:
        ch (_type_): Not used
        method (_type_): Not used
        properties (_type_): Not used
        body (string): A json object containing the consumers pictures and names.
    """
    print("Receiving employees information....")
    # Load the JSON data received
    received_message = json.loads(body)
    # Create n array to store JSON Objects inside it
    employees_emotions = []
    print("Analyzing employees emotions....")
    # Loop the employees JSON Array and analyze data
    for employee in received_message:
        # Get the exact data from every employee
        emp_name = employee['name']
        emp_image = employee['image']

        # Detect the face emotion from the employee image
        emp_emotion = analyze_emotion(emp_image)
        # Store a JSON objecto in the array
        employees_emotions.append(
            {
                "name": emp_name,
                "emotion": emp_emotion
            }
        )
    print("employees emotions analyzed....")
    # Prepear the employees analyzed data in a JSON array object
    message = json.dumps(employees_emotions)
    # Deliver the results to the next event processor by using the publisher connection
    publisher_thread = threading.Thread(target=process_publisher, args=(message,))
    publisher_thread.start()
def process_consumer():
    """
    This function creates a new connection with the broker and initializes a channel
    to receive messages from the queue.
    The connection keeps running until the program is finished
    """
    # create the Message Broker connection parameters
    connection_parameters = pika.ConnectionParameters('localhost')

    # Create a new connection
    connection = pika.BlockingConnection(connection_parameters)

    # A connection can have different channels
    channel = connection.channel() # We don't give a name because we're using the default channel

    # Declaring a queue
    channel.queue_declare(queue='load-images')

    channel.basic_consume(queue='load-images', auto_ack=True, 
                        on_message_callback=on_message_received)


    print("The service has started consuming.....")
    channel.start_consuming()  
def process_publisher(message_body):
    """
    This function creates a new connection with the broker and sends a message body
    to the queue established.

    Args:
        message_body (_type_): A JSON objecto containing the employees
        pictures and names.
    """
    # create a connection to the locally running RabbitMQ Message Broker
    connection_parameters = pika.ConnectionParameters('localhost')

    connection = pika.BlockingConnection(connection_parameters)

    # A connection can have different channels
    channel = connection.channel() # We don't give a name because we're using the default channel

    # Declaring a queue
    channel.queue_declare(queue='emotions-managment')

    channel.basic_publish(exchange='', routing_key='emotions-managment', body=message_body)

    print("New data published....")

    connection.close()
    