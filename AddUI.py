from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
from tkinter import messagebox

#open tk window
root = Tk() 
root.geometry('845x500') 

###########################################################################
#stores the list with the images to be send. Needs 10
images_bytearray_list=[]

#label list
label_list=[]
  
#open file and store it
def open_file(): 
    file = askopenfile(mode ='rb', filetypes =[('Image files', '.jpg .jpeg .img .png .gif .bmp')]) 
    if file is not None: 
        image_readed = file.read()
        image_bytearray = bytearray(image_readed)
        images_bytearray_list.append(image_bytearray)
        if(len(images_bytearray_list)<=10):
            label_list[len(images_bytearray_list)-1].config(text=file.name)
        else:
            messagebox.showwarning(title=None, message='Solo se pueden introducir 10 imágenes') 
        
        

def send_files():
    return 0

###########################################################################
#GUI

#title frame
title_frame = Frame(root)
title_frame.pack(side=TOP)

title=Label(title_frame, text="Add UI", font=("Arial Bold", 30))
title.pack(side=TOP)


#instructions on how to use the app
instructions=Label(title_frame, text="Por favor, agrega 10 imagenes para enviar", font=("Arial Bold", 12))
instructions.pack(side=LEFT)




#frame with the images names

images_names_frame = Frame(root, height=350)
images_names_frame.pack(side=TOP)

#label for the 10 images
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
search_btn = Button(buttons_frame, text ='Seleccionar imagen', command = open_file) 
search_btn.pack(side=LEFT,padx=10) 

search_btn = Button(buttons_frame, text ='Enviar imagenes', command = send_files) 
search_btn.pack(side=LEFT,padx=5) 



#keeps the GUI loop  
mainloop() 