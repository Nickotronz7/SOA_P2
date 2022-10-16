from google.cloud import vision


def analyze_emotion(image_bytes):
    """
    This function analyze the emotion from a picture using the Google Vision API
    Args:
        image_bytes (string): An image in bytes format
    Returns:
        costumer_emotion (string): The emotion detected from the bytes image
    """
    # Instance of the vision client
    vision_client = vision.ImageAnnotatorClient()
    # Create an image object from bytes
    image = vision.Image(content=image_bytes)
    # Using the face detection method from the Google Vision API to get the face annotations
    face_detection = vision_client.face_detection(image=image).face_annotations
    # Get the first face annotation found (There must be only one person in the picture)
    response = face_detection[0] 
    costumer_emotion = "Unknown" # The emotion result in case the used emotions don't match
    if (response.joy_likelihood >= 3) and (response.joy_likelihood <= 5):
        costumer_emotion = "Happy"
    elif (response.anger_likelihood >= 3) and (response.anger_likelihood <= 5):
        costumer_emotion = "Angry"
    elif (response.sorrow_likelihood >= 3) and (response.sorrow_likelihood <= 5):
        costumer_emotion = "Sad"
    elif (response.surprise_likelihood >= 3) and (response.surprise_likelihood <= 5):
        costumer_emotion = "Surprised"
    return costumer_emotion