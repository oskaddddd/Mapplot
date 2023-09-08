import PIL.Image
import numpy as np
import tkinter as tk
import PIL.ImageTk



#raise the threshold not the entire region is green and lower it if pixels outside the region are green
#If inverse = True, will select the above the threashold (lighter regions), if False will select bellow threashold (Darker regions)
inverse = False
threashhold = 0
imageName = ''
with open('ImageName.txt', 'r') as f:
    imageName = f.read()


image = PIL.Image.open(imageName).convert('RGBA')
defImageArr = np.array(image)
print(defImageArr)
threashhold *=4

print("Coloring region... this might take abit")


def color():
    global image
    if inverse:
        mask = np.sum(defImageArr, axis=2) > threashhold
    else:
        mask = np.sum(defImageArr, axis=2) < threashhold
        print('colored')
    #print(mask)
      # Set RGB channels to zero
    imArray = np.zeros_like(defImageArr)
    imArray[mask, 3] = 255  # Set alpha channel based on the mask

    image2 = PIL.Image.fromarray(imArray.astype(np.uint8))
    image = image2
    return image2




root = tk.Tk()
root.title("Preapere mask")

imTK = PIL.ImageTk.PhotoImage(color())

ImageLabel = tk.Label(root, image=imTK)
ImageLabel.pack(side='bottom')

label = tk.Label(root, text="Threashold: 0")
label.pack(side='top')

def InverseToggle():
    global inverse
    global ImageLabel
    global imTK
    inverse = check.get()
    imTK = PIL.ImageTk.PhotoImage(color())
    ImageLabel["image"] = imTK
    ImageLabel.pack(side="bottom")
    
    

check = tk.BooleanVar()
checkbutton = tk.Checkbutton(root, text = "Inverse", command=InverseToggle, variable=check, onvalue=True, offvalue=False)
checkbutton.pack(side='top')

def SliderChange(x):
    global threashhold
    global imTK
    label.config(text=f"Threashold: {x}")
    threashhold = int(x)*4
    #print(threashhold)
    imTK = PIL.ImageTk.PhotoImage(color())
    ImageLabel["image"] = imTK

slider = tk.Scale(root, from_=0, to=255, orient="horizontal", command=SliderChange)
slider.pack(side='top')

def SaveImage():
    image.save(imageName[:imageName.index('.')+1]+'png' \
    if imageName[imageName.index('.')+1:] != 'png' \
    else imageName)
    print("SavedImage")
    root.quit()
button = tk.Button(root, text="save image if the main part of the map is black", command=SaveImage)
button.pack(side='top')

root.mainloop()


