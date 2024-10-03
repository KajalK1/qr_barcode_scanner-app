import tkinter as tk
from tkinter import filedialog, messagebox, Text
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk, ImageDraw
import webbrowser


class QRBarcodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("QR and Barcode Scanner")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Select an image to scan", font=("Arial", 24))
        self.label.pack(pady=20)

        self.scan_button = tk.Button(root, text="Open Image", command=self.open_image, font=("Arial", 16))
        self.scan_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 16), fg="green")
        self.result_label.pack(pady=20)

        self.link_button = tk.Button(root, text="", command=self.open_link, font=("Arial", 16), fg="blue")
        self.link_button.pack(pady=10)

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(pady=20)

        self.link = ""

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.scan_image(file_path)

    def scan_image(self, file_path):
        try:

            image = Image.open(file_path)
            decoded_objects = decode(image)

            if decoded_objects:
                result = ""
                for obj in decoded_objects:
                    result += f"Type: {obj.type}, Data: {obj.data.decode('utf-8')}\n"
                    self.link = obj.data.decode('utf-8')  
                  
                    points = obj.polygon
                    if len(points) == 4: 
                        self.draw_rectangle(image, points)

                self.result_label.config(text=result)
                self.link_button.config(text="Open Link", state=tk.NORMAL) 
            else:
                self.result_label.config(text="No QR/Barcode found.")
                self.link_button.config(text="", state=tk.DISABLED)

         
            image.thumbnail((600, 400))
            image_tk = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image = image_tk 

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load or scan image: {e}")

    def draw_rectangle(self, image, points):

        draw = ImageDraw.Draw(image)
        draw.line([points[0], points[1], points[2], points[3], points[0]], fill="green", width=3)

    def open_link(self):
        if self.link:
            webbrowser.open(self.link) 


if __name__ == "__main__":
    root = tk.Tk()
    app = QRBarcodeScanner(root)
    root.mainloop()
