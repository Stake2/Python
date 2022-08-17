from tkinter import *

# A subclass of Canvas for dealing with resizing of windows
class Resizing_Canvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)

        self.bind("<Configure>", self.On_Resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def On_Resize(self,event):
        # Determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height

        # Resize the canvas 
        self.config(width=self.width, height=self.height)

        # Rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

def main():
    root = Tk()

    my_frame = Frame(root)
    my_frame.pack(fill=BOTH, expand=YES)

    my_canvas = Resizing_Canvas(my_frame,width=850, height=400, bg="red", highlightthickness=0)
    my_canvas.pack(fill=BOTH, expand=YES)

    # Add some widgets to the canvas
    my_canvas.create_line(0, 0, 200, 100)
    my_canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    my_canvas.create_rectangle(50, 25, 150, 75, fill="blue")

    # Tag all of the drawn widgets
    my_canvas.addtag_all("all")
    root.mainloop()

if __name__ == "__main__":
    main()