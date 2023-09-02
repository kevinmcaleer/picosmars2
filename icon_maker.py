import tkinter as tk

class IconEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("8x8 Icon Editor")

        self.grid = []
        for row in range(8):
            row_data = []
            for col in range(8):
                canvas = tk.Canvas(self, width=30, height=30, bg='white')
                canvas.grid(row=row, column=col)
                canvas.bind("<Button-1>", self.toggle_pixel)
                row_data.append(canvas)
            self.grid.append(row_data)

        btn = tk.Button(self, text="Generate Code", command=self.generate_code)
        btn.grid(row=9, columnspan=8)

        self.output = tk.Text(self, height=10, width=40)
        self.output.grid(row=10, columnspan=8)

    def toggle_pixel(self, event):
        canvas = event.widget
        bg = canvas["bg"]
        new_color = "black" if bg == "white" else "white"
        canvas["bg"] = new_color

    def generate_code(self):
        rows = []
        for row_canvases in self.grid:
            row_val = 0
            for i, canvas in enumerate(row_canvases):
                if canvas["bg"] == "black":
                    row_val += (1 << (7-i))
            rows.append(f"0b{row_val:08b}")
        code = "face = [\n    " + ",\n    ".join(rows) + ",\n]"
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, code)

if __name__ == "__main__":
    app = IconEditor()
    app.mainloop()
