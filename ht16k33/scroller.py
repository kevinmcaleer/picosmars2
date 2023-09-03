from .font import font
from time import sleep
import math

class Scroller():
 
    def __init__(self,matrix):
        self.matrix = matrix

    offset = 0
    gap = 1
    brightness = 1.0
    num_cols = 5
    num_rows = 5

    def clear(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self.matrix.pixel(col, row, 0, )
        
    def __str__(self):
        return f"rows: {self.num_rows}, cols: {self.num_cols}"
        
    def display_character(self, character,pos):

        # Initialize y to 0
        y = 0

        # Iterate over each row in the character
        for row_idx in range(0,self.num_rows):
            # Determine the length of the current row
            row_len = len(character[0])
            
            # Iterate over each column in the current row
            for col_idx in range (row_len):
                
                # Determine the x coordinate for the current pixel

                x = self.num_rows - row_idx -1
                y = self.num_cols - (col_idx + self.offset + pos) - 1
                if 0 <=x < self.num_rows and 0 <= y < self.num_cols:
               
                  
                    if 0 <= x < self.num_rows and 0 < y < self.num_cols:
                        if character[row_idx][col_idx] == '1':
                            self.matrix.reverse_pixel(x, y, 1)
                        else:
                            self.matrix.reverse_pixel(x, y, 0)
        # Update the offset
        self.offset += len(character[0]) + self.gap
        
    def show_message(self, message, position):
        """ Shows the message on the display, at the
            position provided"""
    
        for character in message:
            self.display_character(font.get(character), position)
        
        # Update the offset
        self.offset = 0
    



        

    