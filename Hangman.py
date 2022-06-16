import tkinter as tk
import turtle

class Hangman():
    def __init__(self,master):
        self.master = master

        self.master.geometry("800x600")
        self.master.title("HANGMAN by Vlasta & Lukáš")
        self.canvas = tk.Canvas(self.master, width = 300, height = 300,bg="white")
        self.canvas.pack()

        self.t = turtle.RawTurtle(self.canvas)
        self.t.shape("circle")
        self.t.shapesize(0.08,0.08)
        self.t.pensize(3)
        self.t.pencolor("black")

        self.funkce = [self.kopecek,self.tyc,self.dalsityc,self.podpera,self.provaz,self.hlava,self.krk,self.ruka_l,self.ruka_r,self.telo,self.noha_l,self.noha_r]

        self.frame = tk.Frame(self.master, width=800, height=250)
        self.frame.pack(side=tk.BOTTOM)

        self.ramec_pro_pismenka = tk.Frame(self.master,width=740,height=50)
        self.ramec_pro_pismenka.pack()

        self.VYHRA = tk.Label(self.ramec_pro_pismenka,text="",font="Arial 20",fg="green")
        self.VYHRA.pack()

        self.delka_textu_label = tk.Label(self.frame,font="Arial 12",text="Počet písmen ve slově: ").place(x=20,y=20)

        self.var = tk.StringVar()
        self.delka_textu_entry = tk.Entry(self.frame, width="4", textvariable=self.var).place(x=240,y=24) # ----------INPUT delky----------

        self.otazka = tk.Label(self.frame,font="Arial 12",text="Rozhodněte, zda se ve slově nachází písmeno: ")
        self.otazka.place(x=180,y=100)

        self.ano = tk.Button(self.frame,font="Arial 20", text="Pokračovat",width="10",bg="green",command= self.ano,state="disabled")
        self.ano.place(x=180, y=150)
        self.ne = tk.Button(self.frame,font="Arial 20", text="NE",width="10",bg="red",command= self.ne,state="disabled")
        self.ne.place(x=400, y=150)

        #self.pokr = tk.Button(self.frame,font="Arial 12", text="Pokračovat",width="10",command= self.odentrovani,state="disabled")
        #self.pokr.place(x=600, y=150)

        self.nope = 0

        self.pozice = []

        self.start = tk.Button(self.frame, text = "Start", command = self.start, width="10",font="Arial 18")
        self.start.place(x=20,y=50)

        self.button = {} #prázdný slovník ---------------------- který se potom naplní loopem for i in range dole

        self.pocitadlo = 0 # Počítadlo pro neplatný pokus

    def start(self):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width = 300, height = 300,bg="white")
        self.canvas.pack()
        self.t = turtle.RawTurtle(self.canvas)
        self.t.shape("circle")
        self.t.shapesize(0.08,0.08)
        self.t.pensize(3)
        self.t.pencolor("black")

        self.ano.configure(state="disabled")
        self.ne.configure(state="normal")
        self.VYHRA.destroy()
        self.ramec_pro_pismenka.destroy()
        self.ramec_pro_pismenka = tk.Frame(self.master,width=740,height=50)
        self.ramec_pro_pismenka.pack()

        self.start.configure(state="disabled")

        #for i in self.funkce:
            #i()
        self.stDialog()
        self.pDelky()
        self.char = self.Vyskyt()
        self.otazka.configure(text="Rozhodněte, zda se ve slově nachází písmeno:  {}  \n- Pokud ano, vyklikejte jeho pozice".format(self.char),font="Arial 12",fg="black")
        self.Hadani()

    def ano(self):
        print("HELL YEAH")
        self.ne.configure(state="disabled")
        self.ano.configure(state="disabled")

        self.YN = "y"
        self.Hadani()
        self.char = self.Vyskyt()
        self.otazka.configure(text="Rozhodněte, zda se ve slově nachází písmeno:  {}".format(self.char),font="Arial 12",fg="black")
        self.ne.configure(state="normal")

        if "_" not in self.pole:
            print("PROGRAM TO UHODL")
            self.ramec_pro_pismenka.destroy()
            self.ramec_pro_pismenka = tk.Frame(self.master,width=740,height=50)
            self.ramec_pro_pismenka.pack()
            self.VYHRA = tk.Label(self.ramec_pro_pismenka,text="PROGRAM VYHRÁL",font="Arial 20",fg="green")
            self.VYHRA.pack()
            self.ano.configure(state="disabled")
            self.ne.configure(state="disabled")
            self.start.configure(state="normal")
            self.pocitadlo = 0

    def ne(self):
        self.YN = "n"

        self.ne.configure(state="disabled")
        self.ano.configure(state="disabled")
        print("HELL NO")
        self.funkce[self.pocitadlo]()
        self.pocitadlo += 1

        self.ne.configure(state="normal")
        #self.ano.configure(state="normal")
        if self.pocitadlo == len(self.funkce):
            print("PROGRAM PROHRAL")
            self.ramec_pro_pismenka.destroy()
            self.ramec_pro_pismenka = tk.Frame(self.master,width=740,height=50)
            self.ramec_pro_pismenka.pack()
            self.VYHRA = tk.Label(self.ramec_pro_pismenka,text="PROGRAM PROHRÁL",font="Arial 20",fg="red")
            self.VYHRA.pack()
            self.start.configure(state="normal")
            self.ne.configure(state="disabled")
            self.ano.configure(state="disabled")

            self.pocitadlo = 0
        self.Hadani()
        self.char = self.Vyskyt()
        self.otazka.configure(text="Rozhodněte, zda se ve slově nachází písmeno:  {}".format(self.char),font="Arial 12",fg="black")

    def toggle_text(self,button_number):# funkce která si bere jako proměnnou pořadové číslo buttonu ve slovníku což je "i" , které se potom dá do funkce vyvolnám funkce z buttonu toggle_text pomocí lambdy
        #print(button_number)  # vyprintí číslo i
        self.button_number = button_number

        if (self.button[self.button_number][1] == "_"):    # když se tvoří tlačítko přes for i in loop, tak se mu automaticky přiřadí hodnota "on" což se dá pak vyprintit
            self.button[self.button_number][0].configure(text = str(self.char),state="disabled",font="Arial 12")  #.configure je funkce k in-acttion modifikaci tlačítka, takže tohle jenom mění text v tlačítko a formátuje to číslo přes %
            self.button[self.button_number][1]= str(self.char) #přířadí tomu novou hodnotu "off" , která jde taky printit
            self.pozice.append(self.button_number)
            self.ano.configure(state="normal")
            self.ne.configure(state="disabled")
            print(self.pozice)




        else:
            self.button[self.button_number][0].configure(text = "_")
            self.button[self.button_number][1]='_'

    def stDialog(self):
        #print("Myslete si spisovné české slovo...  (S délkou 4+ písmen)\nMáš slovo? Tak na co čekáš!?")
        #self.delka = int(input("Zadej délku svého slova: "))
        self.delka = int(self.var.get())
        print(self.delka)
        self.ABC = {"a" : 0, "á" : 0, "b" : 0, "c" : 0, "č" : 0, "d" : 0, "ď" : 0, "e" : 0, "é" : 0, "ě" : 0, "f" : 0, "g" : 0, "h" : 0, "ch" : 0, "i" : 0, "í" : 0, "j" : 0, "k" : 0, "l" : 0, "m" : 0, "n" : 0, "ň" : 0, "o" : 0, "ó" : 0, "p" : 0, "q" : 0, "r" : 0, "ř" : 0, "s" : 0, "š" : 0, "t" : 0, "ť" : 0, "u" : 0, "ú" : 0, "ů" : 0, "v" : 0, "w" : 0, "x" : 0, "y" : 0, "ý" : 0, "z" : 0, "ž" : 0}
        self.pole = list(self.delka * "_") #vytvoří pole xčlenů podle délky


        for i in range(0,self.delka):
            self.button[i]  = [tk.Button(self.ramec_pro_pismenka,state="normal",font="Arial 12", text="_" , width=2, command=lambda i=i: self.toggle_text(i)), "_"] #přiřadí do slovníku
            self.button[i][0].pack(side=tk.LEFT)

    def pDelky(self):
        self.dict = open("Czech.3-2-5.dic", encoding = "windows-1250")
        self.slova = []
        for Element in self.dict:
            Element = Element[:-1]
            if len(Element) == self.delka:
                self.slova.append(Element)

    def Hadani(self):

        #while "_" in self.pole:
            #tisk = ""

            #for i in self.pole:
                #tisk += i + " "

            #print(tisk)

        self.ABC.pop(list(self.ABC)[self.hodnoty.index(max(self.hodnoty))])

        for key,value in self.ABC.items():
            self.ABC[key] = 0
        print("tohle je pole: ",self.pole)

        if self.YN == "y":
            for place in self.pozice:
                print(place)
                self.pole[place] = self.char
                print(self.pole)
            self.pozice = []

        else:
            self.pozice = []

    def Vyskyt(self):
        for word in self.slova:
            check = None

            for pismeno, charakter in zip(self.pole, word):
                if pismeno != "_":
                    if pismeno == charakter:
                        check = True
                    else:
                        check = False
                        break
                else:
                    check = True
            if check == True:
                for index, char in enumerate(word):
                    try:
                        self.ABC[char] += 1
                    except:
                        pass
        self.hodnoty = list(self.ABC.values())
        return(list(self.ABC)[self.hodnoty.index(max(self.hodnoty))])

    def kopecek(self):
        self.t.penup()
        self.t.goto(-100,-150)
        self.t.pendown()
        self.t.speed(2)
        self.t.left(90)
        self.t.circle(-115/2,180)
        self.t.right(90)
        self.t.forward(115)
        self.t.right(180)
        self.t.forward(115/2)
        self.t.penup()
        self.t.left(90)
        self.t.forward(115/2)
        self.t.pendown()

    def tyc(self):
        self.t.speed(2)
        self.t.forward(160)

    def dalsityc(self):
        self.t.right(90)
        self.t.forward(120)

    def podpera(self):
        self.t.penup()
        self.t.left(180)
        self.t.forward(80)
        self.t.left(45)
        self.t.pendown()
        self.t.forward((40**2+40**2)**(1/2))
        self.t.penup()
        self.t.left(180)
        self.t.forward((40**2+40**2)**(1/2))
        self.t.right(45)
        self.t.forward(80)
        self.t.pendown()

    def provaz(self):
        self.t.right(90)
        self.t.forward(30)

    def hlava(self):
        self.t.right(90)
        self.t.circle(15)

    def krk(self):
        self.t.left(90)
        self.t.penup()
        self.t.forward(30)
        self.t.pendown()
        self.t.forward(15)

    def ruka_l(self):
        self.t.right(35)
        self.t.forward(40)
        self.t.penup()
        self.t.right(180)
        self.t.forward(40)
        self.t.right(-35+180)
        self.t.pendown()

    def ruka_r(self):
        self.t.left(35)
        self.t.forward(40)
        self.t.penup()
        self.t.right(180)
        self.t.forward(40)
        self.t.left(-35+180)
        self.t.pendown()

    def telo(self):
        self.t.forward(50)

    def noha_l(self):
        self.t.right(35)
        self.t.forward(55)
        self.t.penup()
        self.t.right(180)
        self.t.forward(55)
        self.t.right(-35+180)
        self.t.pendown()

    def noha_r(self):
        self.t.left(35)
        self.t.forward(55)
        self.t.penup()
        self.t.right(180)
        self.t.forward(55)
        self.t.left(-35+180)
        self.t.penup()

root = tk.Tk()

klasa = Hangman(root)
#klasa.stDialog()
#klasa.pDelky()
#klasa.Hadani()
root.mainloop()
