import customtkinter as ctk
import math
from datetime import datetime

ctk.set_appearance_mode("dark")


class Calculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Student Calculator")
        self.geometry("900x650")
        self.minsize(420,500)
        self.resizable(True,True)

        self.create_ui()
        self.clock()

        self.bind("<Return>", self.calculate)
        self.bind("<Escape>", lambda e:self.clear())


    def create_ui(self):

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.time=ctk.CTkLabel(
            self,
            font=("Segoe UI",16)
        )

        self.time.grid(
            row=0,
            column=0,
            pady=10
        )


        self.display=ctk.CTkEntry(
            self,
            height=70,
            font=("Consolas",35),
            justify="right"
        )

        self.display.grid(
            row=1,
            column=0,
            padx=20,
            sticky="ew"
        )


        self.tabs=ctk.CTkTabview(self)

        self.tabs.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        self.calc=self.tabs.add("Calculator")
        self.commerce=self.tabs.add("Commerce")
        self.his=self.tabs.add("History")


        self.make_calc()
        self.make_commerce()


        self.history=ctk.CTkTextbox(
            self.his,
            font=("Consolas",14)
        )

        self.history.pack(
            fill="both",
            expand=True
        )


        try:
            with open("history.txt") as f:
                self.history.insert(
                    "end",
                    f.read()
                )

        except:
            pass



    def make_calc(self):

        buttons=[

        ["AC","⌫","√","/"],
        ["7","8","9","*"],
        ["4","5","6","-"],
        ["1","2","3","+"],
        ["0",".","^","="],
        ["sin","cos","tan","log"]

        ]


        for r,row in enumerate(buttons):

            self.calc.grid_rowconfigure(
                r,
                weight=1
            )


            for c,text in enumerate(row):

                self.calc.grid_columnconfigure(
                    c,
                    weight=1
                )


                ctk.CTkButton(

                    self.calc,

                    text=text,

                    font=("Segoe UI",20),

                    corner_radius=20,

                    command=lambda x=text:self.press(x)

                ).grid(

                    row=r,
                    column=c,

                    padx=8,
                    pady=8,

                    sticky="nsew"

                )



    def make_commerce(self):

        items={

        "GST 18%" : self.gst,
        "Profit %" : self.profit,
        "Loss %" : self.loss,
        "Simple Interest" : self.si,
        "Compound Interest" : self.ci,
        "Discount" : self.discount

        }


        for name,func in items.items():

            ctk.CTkButton(

                self.commerce,

                text=name,

                height=50,

                font=("Segoe UI",18),

                command=func

            ).pack(

                fill="x",

                padx=30,

                pady=10

            )



    def press(self,key):

        if key=="=":
            self.calculate()


        elif key=="AC":
            self.clear()


        elif key=="⌫":

            value=self.display.get()

            self.clear()

            self.display.insert(
                0,
                value[:-1]
            )


        elif key=="√":

            self.display.insert(
                "end",
                "sqrt("
            )


        else:

            self.display.insert(
                "end",
                key
            )



    def calculate(self,event=None):

        try:

            exp=self.display.get()


            final=(

            exp.replace("^","**")
            .replace("sqrt","math.sqrt")
            .replace("sin","math.sin")
            .replace("cos","math.cos")
            .replace("tan","math.tan")
            .replace("log","math.log10")

            )


            ans=eval(final)


            self.clear()

            self.display.insert(
                0,
                ans
            )


            self.save(
                f"{exp} = {ans}"
            )


        except:

            self.display.delete(
                0,
                "end"
            )

            self.display.insert(
                0,
                "ERROR"
            )



    def save(self,text):

        self.history.insert(
            "end",
            text+"\n"
        )


        with open(
            "history.txt",
            "a"
        ) as file:

            file.write(
                text+"\n"
            )



    def gst(self):

        n=float(self.display.get())

        self.save(
            f"GST = {n*1.18}"
        )



    def profit(self):

        cp=float(input("Cost Price: "))

        sp=float(input("Selling Price: "))

        self.save(
            f"Profit % = {((sp-cp)/cp)*100}"
        )



    def loss(self):

        cp=float(input("Cost Price: "))

        sp=float(input("Selling Price: "))

        self.save(
            f"Loss % = {((cp-sp)/cp)*100}"
        )



    def si(self):

        p=float(input("Principal: "))
        r=float(input("Rate: "))
        t=float(input("Time: "))

        self.save(
            f"SI = {(p*r*t)/100}"
        )



    def ci(self):

        p=float(input("Principal: "))
        r=float(input("Rate: "))
        t=float(input("Time: "))


        self.save(

            f"CI = {p*((1+r/100)**t)-p}"

        )



    def discount(self):

        price=float(input("Price: "))

        d=float(input("Discount: "))

        self.save(

            f"Final Price = {price-price*d/100}"

        )



    def clear(self):

        self.display.delete(
            0,
            "end"
        )



    def clock(self):

        self.time.configure(

            text=datetime.now()
            .strftime(
                "%d %b %Y  |  %I:%M:%S %p"
            )

        )


        self.after(
            1000,
            self.clock
        )



app=Calculator()

app.mainloop()