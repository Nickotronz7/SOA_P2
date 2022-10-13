#!/usr/bin/python
# -*- coding: utf8 -*-
import pika
import json


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
    channel.queue_declare(queue='load-images')

    channel.basic_publish(exchange='', routing_key='load-images', body=json.dumps(message_body))

    print("Images sended to the queue...")

    connection.close()
    