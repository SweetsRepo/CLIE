from PIL import Image, ImageFilter, ImageDraw, ImageFont
import textwrap
import glob, os

__author__ = 'Chris'

'''
Master Class for the Command Line Image Editor. Handles opening and saving image edits,
taking in user input, and includes commands for various operations possible with PIL.
'''
class CLIE:

    def __init__(self, filename):
        folderDir = "./Album Covers/Originals/"
        self.image = Image.open(folderDir + filename + ".jpg")
        self.stack = []

    def showImage(self):
        '''
        Show the image in it's current edited state
        '''
        print("Displaying Image")
        self.image.show()

    def applyFilter(self):
        '''
        Allow for the application of a filter to the image
        '''
        #Add the image in it's current state to the stack
        self.addToStack()
        #User input to choose filter
        choice = input("Select a filter from below \n 1.) Blur \n 2.) Contour \n 3.) Edge Enhance \n 4.) Emboss \n 5.) Find Edges \n 6.) Sharpen \n 7.) Smooth \n 8.) Monochrome \n 9.) Black and White \n")
        filtered = self.image
        if choice == "1":
            filtered = self.image.filter(ImageFilter.BLUR)
        elif choice == "2":
            filtered = self.image.filter(ImageFilter.CONTOUR)
        elif choice == "3":
            filtered = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif choice == "4":
            filtered = self.image.filter(ImageFilter.EMBOSS)
        elif choice == "5":
            filtered = self.image.filter(ImageFilter.FIND_EDGES)
        elif choice == "6":
            filtered = self.image.filter(ImageFilter.SHARPEN)
        elif choice == "7":
            filtered = self.image.filter(ImageFilter.SMOOTH_MORE)
        #Fix These - Type Cast ?
        elif choice == "8":
            filtered = self.MONOCHROME()
        elif choice == "9":
            filtered = self.BLACK_AND_WHITE()
        self.image = filtered
        #self.image.show()

    def addText(self):
        '''
        Adds text to the image (Rough approximation of center)
        '''
        #Add the image in it's current state to the stack
        self.addToStack()
        #Create objects needed to work with text and images
        quote = input("Type a quote you'd like to have centered: ")
        para = textwrap.wrap(quote, width=30)
        #Make a deep copy of the image
        self.image.save("./tempText.jpg")
        copy = Image.open("./tempText.jpg")
        #Make Image Drawn and Font Instances
        draw = ImageDraw.Draw(copy)
        W, H = self.image.size
        font = ImageFont.truetype("palace-script.ttf", int(H/7.5)) #Scale text to image size
        w, h = draw.textsize(quote, font)
        #Select Scale Factor to determine where the quote is placed.
        sf = input("Enter value between -10 and 10 to determine Vertical Scale \n")
        #Pick the Color based off user input
        color = 0,0,0
        choice = input("Select a color from below \n 1.) Black \n 2.) White \n")
        if(choice == "1"):
            color = 0,0,0
        elif(choice == "2"):
            color = 255,255,255
        #Add the text, wrap if need be, and show the user
        current_h, pad = (H-float(sf)*h)/2, 10
        for line in para:
            w, h = draw.textsize(line, font)
            draw.text((((W-w)/2), current_h), line, color, font)
            current_h += h + pad
        self.image = copy
        #self.image.show()

    ''''''''''''''"""Additional Filter Options Do not add text after these right now"""''''''''''''''
    def MONOCHROME(self):
        gray = self.image.convert('L')
        bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
        return bw

    def BLACK_AND_WHITE(self):
        gray = self.image.convert('L')
        bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
        return bw

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def addToStack(self):
        '''
        Adds item to the stack, limits the stack to size of 10 in order to minimize memory usage
        '''
        if len(self.stack) < 10:
            self.stack.append(self.image)
        else:
            #Remove the least recent action
            del self.stack[0]
            self.stack.append(self.image)

    def undo(self):
        '''
        Undoes the last operation by taking the previous state off the top of the stack
        If no previous state, returns a message alerting the user.
        '''
        if not self.stack:
            print("No operations to undo")
        else:
            self.image = self.stack.pop()
            print("Last Action Undone")

    def saveImage(self):
        '''
        Save the edited image with a new name
        '''
        newName = input("Specify name for image: ")
        self.image.save("./Album Covers/Edits/" + newName + ".jpg")
        print("Saving Image")

    def chooseAction(self):
        '''
        Method which allows for user operations to occur.
        '''
        choice = 0
        while (choice != "6"):
            choice = input(" 1.) Show Image in it's current state. \n 2.) Apply a filter to the image. \n 3.) Add text to the image. \n 4.) Save Image. \n 5.) Undo \n 6.) Exit \n")
            if(choice == "1"):
                self.showImage()
            elif(choice == "2"):
                self.applyFilter()
            elif(choice == "3"):
                self.addText()
            elif(choice == "4"):
                self.saveImage()
            elif(choice == "5"):
                self.undo()
            elif(choice == "6"):
                print("Exiting")
            #Hidden Functions for tesing purposes
            elif(choice == "7"):
                print("Stack size: " + str(len(self.stack)))
            elif(choice == "8"):
                print((type(self.image)))
            elif (choice == "9"):
                self.MONOCHROME()
            elif (choice == "10"):
                self.BLACK_AND_WHITE()
            else:
                print("Please select one of the given functions")

def Main():
    file = input("Enter name of the image to edit: ")
    editor = CLIE(file)
    editor.chooseAction()

if __name__ == '__main__':
    Main()