import tkinter as tk
from PIL import Image
from PIL import ImageTk
from PyScripts import HeightToBuildingType
from PyScripts import HeightToFloors
from PyScripts import Polygon_To_Centroid
from PyScripts import Foundation_Year
from PyScripts import Directional_9

window = tk.Tk()
window.title("Main Function")
window.geometry('1000x500')

# imgPath = r'C:\Users\Shaked Chen\Desktop\Geo NLG\background.png'
# label = tk.Label(window)
# img = Image.open(imgPath)
# img = img.resize((1000, 500))
# label.img = ImageTk.PhotoImage(img)
# label['image'] = label.img
#
# label.grid(linestyle='dashed')

# building path

building_frame= tk.Frame(window)
building_frame.grid(sticky="W")

Mbuilding_lbl = tk.Label(building_frame, text="------- Building Details -------",font=("Arial Bold", 14),fg='brown')
Mbuilding_lbl.grid(row=0,column=0,sticky='S',rowspan=3)

buildings_path_lbl = tk.Label(building_frame, text="Please Enter Polygon layer path(for instance: layer.shp): ",font=("Arial Bold", 11))
buildings_path_lbl.grid(row=5,column=0,sticky="W")

folder_path_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
folder_path_txt.grid(row=5,column=1,sticky="W")

def buildings_func():
    return folder_path_txt.get()

# height field
height_lbl = tk.Label(building_frame, text="Please Enter HEIGHT field name (for instance, building_height): ",font=("Arial Bold", 11))
height_lbl.grid(row=6,column=0,sticky="W")

height_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
height_txt.grid(row=6,column=1,sticky="W")

def height_func():
    return height_txt.get()


# building FID

fid_lbl = tk.Label(building_frame, text="Please Enter building FID from source layer (for instance, 1): ",font=("Arial Bold", 11))
fid_lbl.grid(row=7,column=0,sticky='W')

fid_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
fid_txt.grid(row=7,column=1,sticky="W")

# Founding year
founding_lbl = tk.Label(building_frame, text="Please Enter founding year field from source layer (if exist): ",font=("Arial Bold", 11))
founding_lbl.grid(row=8,column=0,sticky='W')

founding_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
founding_txt.grid(row=8,column=1,sticky="W")

def founding_year_func():
    return founding_txt.get()

MinsideY_lbl = tk.Label(building_frame, text="------- Inside Building Point -------",font=("Arial Bold", 14),fg='brown')
MinsideY_lbl.grid(row=9,column=0,sticky='S',rowspan=3)

def insideX_func():
    return (insideX_txt.get())

insideX_lbl = tk.Label(building_frame, text="Please Enter X value of point inside of the building (for instance, 0.114): ",font=("Arial Bold", 11))
insideX_lbl.grid(row=13,column=0,sticky='W')

insideX_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
insideX_txt.grid(row=13,column=1,sticky="W")




def insideY_func():
    return (insideX_txt.get())


insideY_lbl = tk.Label(building_frame, text="Please Enter Y value of point inside of the building (for instance, 0.184): ",font=("Arial Bold", 11))
insideY_lbl.grid(row=14,column=0,sticky='W')

insideY_txt = tk.Entry(building_frame,font=("Arial Bold", 11), width=50,fg='brown')
insideY_txt.grid(row=14,column=1,sticky="W")




def fid_func():
    fid1= int(fid_txt.get())
    print("fid: ",fid1)
    building_path= buildings_func()
    print("building_path: ", building_path)
    height= height_func()
    print("height: ", height)
    # finding building type
    building_type= HeightToBuildingType.HeightToBuildingType(input_layer_path=building_path,Height_Field_Name=height,fid=fid1)
    print("building_type: ",building_type)
    floors_number=  HeightToFloors.HeightToFloors(input_layer_path=building_path,Height_Field_Name=height,fid=fid1)
    print("floors number: ", floors_number)

    # inner point
    x= float(insideX_func())
    print("x: ", x)

    y= float(insideY_func())
    print("y: ", y)

    relative_location= Directional_9.Directional_9(input_layer_path=building_path, pointX=x,pointY=y,fid=fid1)
    print("relative_location: ", relative_location)


    if (founding_year_func() != '') or (founding_year_func() != None):
        year= founding_year_func()
        print("year: ",year)
        building_foundation_year= int(Foundation_Year.Foundation_Year(input_layer_path=building_path,founding_Field_Name=year,fid=fid1))
        print("building_foundation_year: ", building_foundation_year)
fid_btn = tk.Button(building_frame, text="Submit",fg='brown',font=("Arial Bold", 11),command=fid_func)
fid_btn.grid(row=15,column=1,sticky="S")




window.mainloop()