from logging import RootLogger
from tkinter import * 
import base64
from tkinter.filedialog import askopenfile 
from tkinter import messagebox
from event_processor import process_publisher
from datetime import datetime
import os

#open tk window
root = Tk() 
root.geometry('600x500') 
root.title('AddUI')

###########################################################################
#stores the list with the images to be send. Needs 10
images_bytearray_list=[]

#label list
label_list=[]
  
#open file and store it
def open_file(): 
    #only images can be uploaded
    file = askopenfile(mode ='rb', filetypes =[('Image files', '.jpg .jpeg .img .png .gif .bmp')]) 
    if file is not None: 
        #read the file, convert to byte arrae and add it to the UI list if len(list)<=10
        image_readed = file.read()
        #file name without path
        clean_name=os.path.split(file.name)[1]
        employee_name = clean_name.split('.')[0]
        encoded_image = base64.encodebytes(image_readed).decode('utf-8')
        images_bytearray_list.append(
            {
                "name": employee_name,
                "image": encoded_image
            }
        )
        if(len(images_bytearray_list)<=10):
            label_list[len(images_bytearray_list)-1].config(text=clean_name)
        else:
            messagebox.showwarning(title=None, message='Solo se pueden introducir 10 imágenes') 
        
        
#sends the file to the broker
def send_files():
    if(len(images_bytearray_list)<10):
        messagebox.showwarning(title=None, message='Se deben introducir 10 imágenes')
        return 0
    # If the expected number of images is satisfied, then publish the data to the Broker
    print("Preparing the images...")
    # Get the current date
    now = datetime.now() # current date and time
    date = now.strftime("%m/%d/%Y")
    
    # Prepare a JSON Object with the necessary data
    json_object = {
        "date": date,
        "employees": "imagen"
    }
                           
    process_publisher(json_object)
    

###########################################################################
#GUI

#title frame
title_frame = Frame(root)
title_frame.pack(side=TOP)

#title
title=Label(title_frame, text="Add UI", font=("Arial Bold", 30), width=600, bg= '#0066CC', fg='white')
title.pack(pady=3)


#instructions on how to use the app
instructions=Label(title_frame, text="Por favor, agrega 10 imágenes para enviar", font=("Arial Bold", 12))
instructions.pack(pady=3)

#label that indicate current images
added_images=Label(title_frame, text="Imágenes agreagadas:", font=("Arial ", 12))
added_images.pack(pady=3)


#frame with the images names

images_names_frame = Frame(root, height=350)
images_names_frame.pack(side=TOP)

#labels for the 10 images
label1=Label(images_names_frame, text='' , font=("Arial", 12))
label1.pack(side=TOP)

label2=Label(images_names_frame, text='' , font=("Arial", 12))
label2.pack(side=TOP)

label3=Label(images_names_frame, text='' , font=("Arial", 12))
label3.pack(side=TOP)

label4=Label(images_names_frame, text='' , font=("Arial", 12))
label4.pack(side=TOP)

label5=Label(images_names_frame, text='' , font=("Arial", 12))
label5.pack(side=TOP)

label6=Label(images_names_frame, text='' , font=("Arial", 12))
label6.pack(side=TOP)

label7=Label(images_names_frame, text='' , font=("Arial", 12))
label7.pack(side=TOP)

label8=Label(images_names_frame, text='' , font=("Arial", 12))
label8.pack(side=TOP)

label9=Label(images_names_frame, text='' , font=("Arial", 12))
label9.pack(side=TOP)

label10=Label(images_names_frame, text='' , font=("Arial", 12))
label10.pack(side=TOP)

buttons_frame = Frame(root)
buttons_frame.pack(side=LEFT)

#add references to list
label_list.append(label1)
label_list.append(label2)
label_list.append(label3)
label_list.append(label4)
label_list.append(label5)
label_list.append(label6)
label_list.append(label7)
label_list.append(label8)
label_list.append(label9)
label_list.append(label10)

#trigers the open file function
search_btn = Button(buttons_frame, text ='Seleccionar imagen', command = open_file, font=("Arial ", 12), bd=4, bg= '#1e91fe', fg='white') 
search_btn.pack(side=LEFT,padx=10) 

#trigers the send files function
search_btn = Button(buttons_frame, text ='Enviar imágenes', command = send_files, font=("Arial ", 12), bd=4, bg= '#1e91fe', fg='white') 
search_btn.pack(side=LEFT,padx=5) 



#keeps the GUI loop  
mainloop() 