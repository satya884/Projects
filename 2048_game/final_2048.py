from tkinter import *
import random as rd
from tkinter import messagebox
import colors as c

class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.move=True
        self.win=True
        self.main_grid=Frame(self,bg=c.GRID_COLOR,bd=3,width=800,height=800)
        self.main_grid.grid(pady=(100,50))
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>",self.left)
        self.master.bind("<Right>",self.right)
        self.master.bind("<Up>",self.up)
        self.master.bind("<Down>",self.down)
        self.mainloop()
        
    def make_GUI(self):
        self.cells=[]
        for i in range(4):
            row=[]
            for j in range(4):
                cell_frame=Frame(self.main_grid,bg=c.EMPTY_CELL_COLOR,width=150,height=150)
                cell_frame.grid(row=i,column=j,padx=5,pady=5)
                cell_number=Label(self.main_grid,bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i,column=j)
                cell_data={"frame":cell_frame,"number":cell_number}
                row.append(cell_data)
            self.cells.append(row)

        self.score_frame=Frame(self)
        self.score_frame.place(relx=0.5,y=45,anchor="center")
        Label(self.score_frame,text="SCORE",font="Verdana",fg="white",bg="black").grid(row=0)
        self.score_label=Label(self.score_frame,text="0",font=c.SCORE_LABEL_FONT)
        self.score_label.grid(row=1)
             
    def generate(self):
         num=rd.randint(1,4)
         randno=rd.choice([2,4])

         randrow=rd.randint(0,3)
         randcol=rd.randint(0,3)

         while self.grid[randrow][randcol]>0:
             randrow=rd.randint(0,3)
             randcol=rd.randint(0,3)

         self.grid[randrow][randcol]=randno
         self.cells[randrow][randcol]["frame"].configure(bg=c.CELL_COLORS[randno])
         self.cells[randrow][randcol]["number"].configure(bg=c.CELL_COLORS[randno],fg=c.CELL_NUMBER_COLORS[randno],font=c.CELL_NUMBER_FONTS[randno],text=str(randno))


    def start_game(self):
         self.grid=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
         self.tGrid=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
         print("This is 2048 game!!!...")
         self.generate()
         self.generate()
         self.score=0

    def merge(self,row1,col1,row2,col2):
         self.grid[row2][col2]=2*self.grid[row1][col1]
         self.score=self.score+self.grid[row2][col2]     

    def clear_f(self):
        self.move=False

    def compareGrid(self):
        for i in range (4):
            for j in range (4):
                if (self.tGrid[i][j] != self.grid[i][j]) : return True
        return False    

    def fill_tg(self):
        self.tGrid=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range (4):
            for j in range (4):
                self.tGrid[i][j]=self.grid[i][j]

    def up(self,event):
        self.fill_tg()
        for col in range(4):
            for row in range(1,4):
                searchrow=row-1
                while self.grid[searchrow][col]==0 and searchrow>0:
                    searchrow-=1
                if searchrow==0 and self.grid[searchrow][col]==0:
                    self.grid[searchrow][col]=self.grid[row][col]
                    self.grid[row][col]=0

                elif self.grid[searchrow][col]==self.grid[row][col]:
                    self.merge(row,col,searchrow,col)
                    self.grid[row][col]=0

                elif searchrow+1 < row :
                    self.grid[searchrow + 1][col]=self.grid[row][col]
                    self.grid[row][col]=0    

        self.move=self.compareGrid()            
        if (self.move==True) : self.generate()
        self.clear_f()
        self.update_gui()
        self.game_over()

    def right(self,event):
        self.fill_tg()
        for row in range(4):
            for col in range(2,-1,-1):
                searchcol=col+1
                while self.grid[row][searchcol]==0 and searchcol<3:
                    searchcol+=1
                if searchcol==3 and self.grid[row][searchcol]==0:
                    self.grid[row][searchcol]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True

                elif self.grid[row][searchcol]==self.grid[row][col]:
                    self.merge(row,col,row,searchcol)
                    self.grid[row][col]=0
                    self.move=True

                elif searchcol-1 > col :
                    self.grid[row][searchcol-1]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True   

        self.move=self.compareGrid()
        if (self.move==True) : self.generate()
        self.clear_f()
        self.update_gui()
        self.game_over()

    def left(self,event):
        self.fill_tg()
        for row in range(4):
            for col in range(1,4):
                searchcol=col-1
                while self.grid[row][searchcol]==0 and searchcol>0:
                    searchcol-=1
                if searchcol==0 and self.grid[row][searchcol]==0:
                    self.grid[row][searchcol]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True
                    
                elif self.grid[row][searchcol]==self.grid[row][col]:
                    self.merge(row,col,row,searchcol)
                    self.grid[row][col]=0
                    self.move=True

                elif searchcol+1 < col :
                    self.grid[row][searchcol+1]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True

        self.move=self.compareGrid()
        if (self.move==True) : self.generate()
        self.clear_f()
        self.update_gui()
        self.game_over()

    def down(self,event):
        self.fill_tg()
        for col in range(4):
            for row in range(2,-1,-1):
                searchrow=row+1
                while self.grid[searchrow][col]==0 and searchrow<3:
                    searchrow+=1
                if searchrow==3 and self.grid[searchrow][col]==0:
                    self.grid[searchrow][col]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True

                elif self.grid[searchrow][col]==self.grid[row][col]:
                    self.merge(row,col,searchrow,col)
                    self.grid[row][col]=0
                    self.move=True

                elif searchrow-1 > row :
                    self.grid[searchrow - 1][col]=self.grid[row][col]
                    self.grid[row][col]=0
                    self.move=True   

        self.move=self.compareGrid()
        if (self.move==True): self.generate()
        self.clear_f()
        self.update_gui()
        self.game_over()                  

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                cell_value=self.grid[i][j]
                if cell_value==0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR,text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value],fg=c.CELL_NUMBER_COLORS[cell_value],font=c.CELL_NUMBER_FONTS[cell_value],text=str(cell_value))
            self.score_label.configure(text=self.score)
            self.update_idletasks()
            
        
    def hor_move(self):
         for i in range(4):
             for j in range(3):
                 if self.grid[i][j]==self.grid[i][j+1]:
                     return True
         return False           

    def ver_move(self):
         for i in range(3):
             for j in range(4):
                 if self.grid[i][j]==self.grid[i+1][j]:
                     return True
         return False  

    def game_over(self):
         if any(2048 in row for row in self.grid):
             game_over_frame=Frame(self.main_grid,borderwidth=2)
             game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
             if(self.win):
                 if messagebox.askyesno('2048', 'You Win! \n Do you still want to continue'): pass
                 else:
                     self.grid=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                     self.update_gui()
                     Label(game_over_frame,text="You Win!",bg=c.WINNER_BG,fg=c.GAME_OVER_FONT_COLOR,font=c.GAME_OVER_FONT).pack()
                              
             self.win=False
                     
          
         elif not any(0 in row for row in self.grid) and not self.hor_move() and not self.ver_move():
             game_over_frame=Frame(self.main_grid,borderwidth=2)
             game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
             Label(game_over_frame,text="You lose!",bg=c.WINNER_BG,fg=c.GAME_OVER_FONT_COLOR,font=c.GAME_OVER_FONT).pack()
             messagebox.showinfo('2048', 'OOPS!!!! You lose!')
                 
             
def main():
     Game()
             
if __name__ == "__main__" :
    main()
    
