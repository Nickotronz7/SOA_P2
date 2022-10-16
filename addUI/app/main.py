from flask import Flask
from flask import request
from flask import redirect
from event_processor import process_publisher
from datetime import datetime
import base64
from index_strings import *

app = Flask(__name__)

#store images
images_bytearray_list=[]

#store names
images_names_list=["","","","","","","","","",""]

#current image being uploaded

current_image_cont=0

'''
#open html file
text_file1 = open("index1.html", "r")
#read whole file to a string
index_string1 = text_file1.read()

text_file2 = open("index2.html", "r")
#read whole file to a string
index_string2 = text_file2.read()'''

index_string1=index1()
index_string2=index2()
  

def open_file(file): 
    global current_image_cont
    #only images can be uploaded
    #read the file, convert to byte arrae and add it to the UI list if len(list)<=10
    image_readed = file.stream.read()
    #file name without path
    employee_name = file.filename
    employee_name = employee_name.split('.')[0]
    encoded_image = base64.encodebytes(image_readed).decode('utf-8')
    images_bytearray_list.append(
        {
            "name": employee_name,
            "image": encoded_image
        }
    )
    print(images_bytearray_list)

    if(len(images_bytearray_list)<=10):
        images_names_list[current_image_cont]=employee_name
        current_image_cont+=1
    else:
        return (index_string1 
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[0] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[1] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[2] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[3] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[4] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[5] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[6] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[7] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[8] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[9] + '</h3>'
        +index_string2+"""
        <script>
        function myFunction() {
        alert('Solo se pueden introducir 10 imágenes');
        }
        window.setTimeout(myFunction, 500);
        </script>"""
        )

#when image is uploaded to be seen in the GUI
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        open_file(f)
        return redirect('/')

#send images to broker
@app.route('/send_to_broker', methods = ['GET', 'POST'])
def send_files():
    if(len(images_bytearray_list)<10):
        return (index_string1 
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[0] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[1] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[2] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[3] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[4] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[5] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[6] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[7] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[8] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[9] + '</h3>'
        +index_string2+"""
        <script>
        function myFunction() {
        alert('Se deben introducir 10 imágenes');
        }
        window.setTimeout(myFunction, 500);
        </script>"""
        )

    # If the expected number of images is satisfied, then publish the data to the Broker
    print("Preparing the images...")
    # Get the current date
    now = datetime.now() # current date and time
    date = now.strftime("%d/%m/%Y")
    
    # Prepare a JSON Object with the necessary data
    json_object = {
        "date": date,
        "employees": images_bytearray_list
    }
                           
    process_publisher(json_object)


    return (index_string1 
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[0] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[1] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[2] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[3] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[4] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[5] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[6] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[7] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[8] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[9] + '</h3>'
        +index_string2+"""
        <script>
        function myFunction() {
        alert('Imágenes enviadas con éxito');
        }
        window.setTimeout(myFunction, 500);
        </script>"""
        )


#main page
@app.route("/")
def index():
    return (index_string1 
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[0] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[1] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[2] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[3] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[4] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[5] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[6] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[7] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[8] + '</h3>'
        + '<h3 style="text-align:center; font-family:Arial; font-weight: bold;">'+ images_names_list[9] + '</h3>'
        +index_string2
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
