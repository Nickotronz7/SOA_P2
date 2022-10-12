import tkinter as tk
import base64
from tkinter.filedialog import askopenfile 
from tkinter import messagebox
from event_processor import process_publisher
from datetime import datetime
import os

#open tk window
root = tk.Tk() 
root.geometry('600x500') 
root.title('AddUI')

###########################################################################
#stores the list with the images to be send. Needs 10
images_bytearray_list=[]

#tk.Label list
tk.Label_list=[]
  
#open file and store it
def open_file(): 
    #only images can be uploaded
    file = askopenfile(mode ='rb', filetypes =[('Image files', '.jpg .jpeg .img .png .gif .bmp')]) 
    if file is not None: 
        #read the file, convert to byte arrae and add it to the UI list if len(list)<=10
        image_readed = file.read()
        #file name without path
        clean_name=os.path.split(file.name)[1]
        encoded_image = base64.encodebytes(image_readed).decode('utf-8')
        images_bytearray_list.append(
            {
                "name": clean_name,
                "image": encoded_image
            }
        )
        if(len(images_bytearray_list)<=10):
            tk.Label_list[len(images_bytearray_list)-1].config(text=clean_name)
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
        "employees": images_bytearray_list
    }
                             
    process_publisher(json_object)
    

###########################################################################
#GUI

#title frame
title_frame = tk.Frame(root)
title_frame.pack(side='top')

#title
title=tk.Label(title_frame, text="Add UI", font=("Arial Bold", 30), width=600, bg= '#0066CC', fg='white')
title.pack(pady=3)


#instructions on how to use the app
instructions=tk.Label(title_frame, text="Por favor, agrega 10 imágenes para enviar", font=("Arial Bold", 12))
instructions.pack(pady=3)

#tk.Label that indicate current images
added_images=tk.Label(title_frame, text="Imágenes agreagadas:", font=("Arial ", 12))
added_images.pack(pady=3)


#frame with the images names

images_names_frame = tk.Frame(root, height=350)
images_names_frame.pack(side='top')

#tk.Labels for the 10 images
tk.Label1=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label1.pack(side='top')

tk.Label2=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label2.pack(side='top')

tk.Label3=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label3.pack(side='top')

tk.Label4=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label4.pack(side='top')

tk.Label5=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label5.pack(side='top')

tk.Label6=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label6.pack(side='top')

tk.Label7=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label7.pack(side='top')

tk.Label8=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label8.pack(side='top')

tk.Label9=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label9.pack(side='top')

tk.Label10=tk.Label(images_names_frame, text='' , font=("Arial", 12))
tk.Label10.pack(side='top')

buttons_frame = tk.Frame(root)
buttons_frame.pack(side='left')

#add references to list
tk.Label_list.append(tk.Label1)
tk.Label_list.append(tk.Label2)
tk.Label_list.append(tk.Label3)
tk.Label_list.append(tk.Label4)
tk.Label_list.append(tk.Label5)
tk.Label_list.append(tk.Label6)
tk.Label_list.append(tk.Label7)
tk.Label_list.append(tk.Label8)
tk.Label_list.append(tk.Label9)
tk.Label_list.append(tk.Label10)

#trigers the open file function
search_btn = tk.Button(buttons_frame, text ='Seleccionar imagen', command = open_file, font=("Arial ", 12), bd=4, bg= '#1e91fe', fg='white') 
search_btn.pack(side='left',padx=10) 

#trigers the send files function
search_btn = tk.Button(buttons_frame, text ='Enviar imágenes', command = send_files, font=("Arial ", 12), bd=4, bg= '#1e91fe', fg='white') 
search_btn.pack(side='left',padx=5) 



#keeps the GUI loop  
tk.mainloop() 