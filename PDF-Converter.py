import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_path = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_UI()

    def initialize_UI(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Output PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        selected_files = filedialog.askopenfilenames(title="Select Images",
                                                     filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if selected_files:
            self.image_path.extend(selected_files)
            self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_path:
            _, filename = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, filename)

    def convert_images_to_pdf(self):
        if not self.image_path:
            return

        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_path in self.image_path:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawImage(image_path, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    root.geometry("400x500")
    ImageToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
