#!/usr/bin/python
# -*- coding: utf8 -*-
import pika
import json
import os

def process_publisher(message_body):
    
    """
    This function creates a new connection with the broker and sends a message body
    to the queue established.

    Args:
        message_body (_type_): A JSON objecto containing the employees
        pictures and names.
    """
    host = os.environ['RABBIT_HOST']
    port = os.environ['RABBIT_PORT']
    queue = os.environ['RABBIT_PRODUCER_QUEUE']

    # create a connection to the locally running RabbitMQ Message Broker
    connection_parameters = pika.ConnectionParameters(host=host,port=port)

    connection = pika.BlockingConnection(connection_parameters)

    # A connection can have different channels
    channel = connection.channel() # We don't give a name because we're using the default channel

    # Declaring a queue
    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message_body))

    print("Images sended to the queue...")

    connection.close()
    