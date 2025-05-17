from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import csv
import datetime
import os
from validation.validators import is_valid_password


def start_app():
    root = tk.Tk()
    root.title("Kozmetički salon")
    root.geometry("700x500")
    root.resizable(True, True)


    # Učitavanje pozadinske slike
    bg_image = Image.open("slike/pozadina.png")
    bg_image = bg_image.resize((700, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo 
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Dobrodošlica
    welcome_label = Label(
        root, 
        text="Dobro došli u kozmetički salon",
        font=("Helvetica", 20, "bold"),
        fg="black"
)
    welcome_label.place(relx=0.5, rely=0.4, anchor="center")

    # Gumbi -> Signup i login
    def show_buttons():
        welcome_label.place_forget()
        signup_btn.place(relx=0.3, rely=0.6, anchor='center')
        login_btn.place(relx=0.7, rely=0.6, anchor='center')

    signup_btn = Button(
        root, 
        text="Sign up", 
        font=("Helvetica", 14), width=12,
        command=lambda: open_signup()
)
    login_btn = Button(
        root, 
        text="Login", 
        font=("Helvetica", 14), 
        width=12,
        command=lambda: open_login()
)

#----------------------------------------------------------------------------------------------------

    def open_signup():
        signup_btn.place_forget()
        login_btn.place_forget()

        # Centriranje signup prozora
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Signup frame
        signup_frame = Frame(root, padx=20, pady=20, bg="light salmon")
        signup_frame.grid(row=1, column=1)

        labels = [
            "Ime", 
            "Prezime", 
            "Broj mobitela", 
            "Nadimak", 
            "Lozinka", 
            "Potvrdi lozinku"
]
        
        entries = []

        for i, label_text in enumerate(labels):
            label = Label(signup_frame, text=label_text)
            label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

            entry = Entry(
            signup_frame,
            width=30, 
            show="*" if "lozink" in label_text.lower() else "")

            entry.grid(row=i, column=1, pady=10)
            entries.append(entry)

    
        def save_user():
            ime_korisnika, prezime_korisnika, broj_korisnika, nadimak_korsinika, lozinka_korsinika, potvrda_korisnika = [e.get() for e in entries]

            if not all([ime_korisnika, prezime_korisnika, broj_korisnika, nadimak_korsinika, lozinka_korsinika, potvrda_korisnika]):
                messagebox.showerror("Greška", "Sva polja su obavezna.")
                return False
            
            if lozinka_korsinika != potvrda_korisnika:
                messagebox.showerror("Greška", "Lozinke se ne podudaraju.")
                return False

            if not is_valid_password(lozinka_korsinika):
                messagebox.showerror("Greška", "Lozinka mora imati veliko slovo, broj i poseban znak.")
                return False

            filepath = "data/korisnici.csv"
            os.makedirs("data", exist_ok=True)
            file_exists = os.path.isfile(filepath)

            with open(filepath, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(
                        ["Ime", 
                         "Prezime", 
                         "Broj", 
                         "Nadimak", 
                         "Lozinka"]
)
                    
                writer.writerow([ime_korisnika, prezime_korisnika, broj_korisnika, nadimak_korsinika, lozinka_korsinika])

            messagebox.showinfo("Uspješno", "Registracija je uspješna!")
            open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)
            return True

        # Gumb za registraciju
        register_btn = Button(
            signup_frame, 
            text="Registriraj se", 
            command=lambda: [signup_frame.destroy() if save_user() else True] 
    )
        register_btn.grid(row=len(labels), columnspan=2, pady=20)

            # Gumb za nazad
        back_signup = Button(
            signup_frame, 
            text="Nazad",
            command=lambda: [signup_frame.destroy(), show_buttons()]
    )
        
        back_signup.grid(row=6, column=3, pady=20)

#----------------------------------------------------------------------------------------------------------
    def open_login():
        signup_btn.place_forget()
        login_btn.place_forget()

        # Centriranje login prozora
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Login frame
        login_frame = Frame(root, padx=20, pady=20, bg="light salmon")
        login_frame.grid(row=1, column=1)

        # Label i unos za Nadimak
        Label(login_frame, text="Nadimak").grid(
            row=0, 
            column=0, 
            pady=10, 
            padx=10, 
            sticky="e"
)
        
        username_entry = Entry(login_frame, width=30)
        username_entry.grid(row=0, column=1, pady=10)

        # Labela i unos za Lozinku
        Label(login_frame, text="Lozinka").grid(
            row=1, 
            column=0, 
            pady=10, 
            padx=10, 
            sticky="e"
)
        
        password_entry = Entry(login_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            # ADMIN provjera
            if username == "Caskey" and password == "#Caskey123":
                open_admin_dashboard("Antonio", "Šiljac")
                return

            # Provjera korisnika
            user_filepath = "data/korisnici.csv"
            if os.path.isfile(user_filepath):
                with open(user_filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Nadimak"] == username and row["Lozinka"] == password:
                            ime_korsinika = row["Ime"]
                            prezime_korisnika = row["Prezime"]
                            broj_korisnika = row["Broj"]
                            open_user_dashboard(ime_korsinika, prezime_korisnika, broj_korisnika)
                            return

            # Provjera zaposlenika
            zaposlenik_filepath = "data/zaposlenici.csv"
            if os.path.isfile(zaposlenik_filepath):
                with open(zaposlenik_filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Nadimak"] == username and row["Lozinka"] == password:
                            ime_zaposlenika = row["Ime"]
                            prezime_zaposlenika = row["Prezime"]
                            open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)
                            return

            # Ako nitko nije pronađen
            messagebox.showerror("Greška", "Pogrešan nadimak ili lozinka.")
            return False
            
        # Gumb za potvrdu
        potvrdi_btn = Button(
            login_frame, 
            text="Potvrdi", 
            command=lambda:[login_frame.destroy() if login() else True]
)
        potvrdi_btn.grid(row=2, columnspan=2, pady=20)

        back_login = Button(
            login_frame, 
            text="Nazad", 
            command=lambda:[login_frame.destroy(), show_buttons()]
)
        back_login.grid(row=6, column=3, pady=20)

#--------------------------------------------------------------------------------------------------------

    def open_admin_dashboard(ime_admin, prezime_admin):
        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, Frame):
                    widget.destroy()

        clear_root()

        admin_frame = Frame(root, padx=20, pady=20, bg="light salmon")
        admin_frame.grid(row=1, column=1)

        Label(
            admin_frame, 
            text=f"ADMIN: {ime_admin} {prezime_admin}", 
            font=("Helvetica", 16, "bold")).pack(pady=10)


        def ucitaj_usluge_iz_csv(putanja):
            usluge_lista = []
            with open(putanja, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for red in reader:
                    naziv = red["Usluga"]
                    cijena = red["Cijena"]
                    usluge_lista.append(f"{naziv} -> {cijena}")
            return usluge_lista

        def zakazi_termin_admin():
            clear_root()

            radno_vrijem_label = tk.Label(
                    root,
                    text="Radno vrijeme:\nPon - Pet: 08:00 - 16:00\nSub: 08:00 - 13:00",
                    font=("Arial", 12),
                    fg="black",
                    bg="light salmon",
                )
            radno_vrijem_label.grid(row=0, column=0, columnspan=3)

            zakazi_frame_admin = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            zakazi_frame_admin.grid(row=1, column=1)

            vrijeme_var = tk.StringVar()
            usluga_var = tk.StringVar()

            result_label = tk.Label(zakazi_frame_admin, text="", font=("Arial", 12), fg="black", bg="light salmon")
            result_label.grid(row=4, column=0, columnspan=3)

            today = datetime.datetime.now().date()
            
            today = datetime.datetime.now().date()
            cal = Calendar(zakazi_frame_admin, selectmode='day', date_pattern='dd-mm-yyyy', mindate=today)
            cal.grid(row=0, column=0, columnspan=3, pady=(10, 20))


            # Učitaj zauzeta vremena iz CSV-a za odabrani datum
            def ucitaj_zauzeta_vremena(selected_date):
                zauzeta_vremena = set()
                termini_path = "data/zakazani_termini.csv"
                if os.path.isfile(termini_path):
                    with open(termini_path, mode="r", encoding="utf-8") as file:
                        reader = csv.reader(file)
                        next(reader)
                        for row in reader:
                            if len(row) >= 5 and row[3] == selected_date:
                                vrijeme = row[4].split(':')[0]
                                zauzeta_vremena.add(vrijeme)
                return zauzeta_vremena


            def update_vremena(event=None):
                selected_date_str = cal.get_date()
                day, month, year = map(int, selected_date_str.split('-'))
                selected_date = datetime.date(year, month, day)
                
                zauzeta_vremena = ucitaj_zauzeta_vremena(selected_date_str)
                
                # Odredi radno vrijeme ovisno o danu
                if selected_date.weekday() == 5:  # Subota
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 14)] 
                else:  # Radni dan
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 16)] 
                
                dostupna_vremena = [v for v in sva_vremena if v.split(':')[0] not in zauzeta_vremena]
                
                hour_dropdown['values'] = ["Vrijeme"] + dostupna_vremena
                hour_dropdown.current(0)
                vrijeme_var.set("Vrijeme")

            hour_dropdown = ttk.Combobox(
                zakazi_frame_admin, 
                textvariable=vrijeme_var,
                values=["Vrijeme"], 
                state="readonly"  # Zabrani ručno unos
            )
            hour_dropdown.current(0)
            hour_dropdown.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            
            # Osiguraj da se ažuriraju dostupna vremena kad se promijeni datum
            cal.bind("<<CalendarSelected>>", update_vremena)

            # Ucitaj usluge iz CSV
            usluge = ucitaj_usluge_iz_csv("data/usluge.csv")

            intervention_dropdown = ttk.Combobox(
                zakazi_frame_admin, 
                textvariable=usluga_var,
                values=["Zahvat"] + usluge,
                state="readonly"  # Zabrani ručno unos
            )
            intervention_dropdown.current(0)
            intervention_dropdown.grid(row=2, column=0, columnspan=3, pady=(0, 10))

            def spremi():
                selected_date = cal.get_date()
                selected_hour = vrijeme_var.get()
                selected_usluga = usluga_var.get()

                if selected_hour == "Vrijeme" or not selected_hour:
                    result_label.config(text="Odaberite vrijeme.")
                elif selected_usluga == "Zahvat" or not selected_usluga:
                    result_label.config(text="Odaberite uslugu.")
                else:
                    unos_prozor = tk.Toplevel(root)
                    unos_prozor.title("Unos podataka")
                    unos_prozor.geometry("300x200")
                    unos_prozor.resizable(False, False)

                    tk.Label(unos_prozor, text="Ime:").pack(pady=5)
                    ime_entry = tk.Entry(unos_prozor)
                    ime_entry.pack()

                    tk.Label(unos_prozor, text="Prezime:").pack(pady=5)
                    prezime_entry = tk.Entry(unos_prozor)
                    prezime_entry.pack()

                    tk.Label(unos_prozor, text="Broj:").pack(pady=5)
                    broj_entry = tk.Entry(unos_prozor)
                    broj_entry.pack()

                    def potvrdi_unos():
                        ime = ime_entry.get().strip()
                        prezime = prezime_entry.get().strip()
                        broj = broj_entry.get().strip()

                        if not ime or not prezime or not broj:
                            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")
                            return

                        # Spremi u CSV
                        file_path = "data/zakazani_termini.csv"
                        zaglavlje = ["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"]
                        file_exist = os.path.isfile(file_path)

                        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            if not file_exist:
                                writer.writerow(zaglavlje)
                            writer.writerow([ime, prezime, broj, selected_date, selected_hour, selected_usluga])

                        unos_prozor.destroy()
                        zakazi_frame_admin.destroy()

                        # Kreiraj novi frame za potvrdu
                        potvrda_frame = Frame(root, padx=20, pady=20, bg="light salmon")
                        potvrda_frame.grid(row=1, column=1)

                        potvrda_label = Label(
                            potvrda_frame,
                            text=f"Termin zakazan za {selected_date} u {selected_hour}\nZahvat: {selected_usluga}\nZa: {ime} {prezime}",
                            font=("Arial", 12),
                            fg="black",
                            bg="light salmon",
                            justify="left"
                        )
                        potvrda_label.pack(pady=20)

                        back_pot_termin = tk.Button(
                            potvrda_frame, 
                            text="Nazad", 
                            command=lambda:[potvrda_frame.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]
                        )
                        back_pot_termin.pack(pady=20)

                    potvrdi_btn = tk.Button(unos_prozor, text="Potvrdi", command=potvrdi_unos)
                    potvrdi_btn.pack(pady=10)

            submit_btn = tk.Button(zakazi_frame_admin, text="Zakazi termin",command=lambda: [radno_vrijem_label.destroy(), spremi()])
            submit_btn.grid(row=3, column=1, pady=(0, 10))

            back_zak_termin = tk.Button(
                zakazi_frame_admin, 
                text="Nazad", 
                command=lambda:[zakazi_frame_admin.destroy(),radno_vrijem_label.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]
            )
            back_zak_termin.grid(row=6, column=1, pady=20)


        def otkazi_termin():
            clear_root()
            otkazi_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            otkazi_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_admin_dashboard(ime_admin, prezime_admin)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = list(csv.DictReader(file))
                if not reader:
                    messagebox.showinfo("Prazno", "Nema zakazanih termina.")
                    return open_admin_dashboard(ime_admin, prezime_admin)

            lista = Listbox(otkazi_frame, width=80, height=20)
            lista.pack(pady=10)

            termini = []
            for i, row in enumerate(reader):
                tekst = f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']} ({row['Zahvat']})"
                lista.insert(i, tekst)
                termini.append(row)

            def otkazi():
                index = lista.curselection()
                if not index:
                    messagebox.showerror("Greška", "Odaberite termin za otkazivanje.")
                    return
                del termini[index[0]]
                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                    writer.writeheader()
                    writer.writerows(termini)
                messagebox.showinfo("Uspjeh", "Termin je otkazan.")
                otkazi_frame.destroy()
                open_admin_dashboard(ime_admin, prezime_admin)

            Button(otkazi_frame, text="Otkaži odabrani termin", command=otkazi).pack(pady=10)
            Button(otkazi_frame, text="Natrag", command=lambda: [otkazi_frame.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]).pack(pady=5)


        def prikazi_termine():
            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return

            tekst = ""
            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tekst += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']}\n"

            clear_root()
            
            termini_frame = Frame(
                root, 
                padx=20, 
                pady=20, 
                bg="light salmon"
)
            termini_frame.grid(row=1, column=1)

            Label(
                termini_frame, 
                text="Zakazani termini", 
                font=("Helvetica", 14, "bold")).pack(pady=10)
            
            text_box = Text(termini_frame, wrap="word", height=15, width=50)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.pack()

            Button(
                termini_frame, 
                text="Nazad", 
                command=lambda: [termini_frame.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]).pack(pady=10)


        def dodaj_zaposlenika():
            clear_root()

            dodaj_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            dodaj_frame.grid(row=1, column=1)

            labels = [
                "Ime", 
                "Prezime", 
                "Pozicija", 
                "Broj", 
                "Nadimak", 
                "Lozinka"
]
            entries = []

            for i, label_text in enumerate(labels):
                label = Label(dodaj_frame, text=label_text)
                label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

                entry = Entry(
                    dodaj_frame, 
                    width=30, 
                    show="*" if "lozinka" in label_text.lower() else ""
)
                entry.grid(row=i, column=1, pady=10)
                entries.append(entry)


            def spremi():
                values = [e.get() for e in entries]

                if not all(values):
                    messagebox.showerror("Greška", "Sva polja su obavezna.")
                    return

                filepath = "data/zaposlenici.csv"
                os.makedirs("data", exist_ok=True)

                with open(filepath, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if os.stat(filepath).st_size == 0:
                        writer.writerow(["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"])
                    writer.writerow(values)

                messagebox.showinfo("Uspjeh", "Zaposlenik dodan.")
                open_admin_dashboard(ime_admin, prezime_admin)

            spremi_admin = Button(
                dodaj_frame, 
                text="Spremi", 
                command=spremi
)
            spremi_admin.grid(row=len(labels), columnspan=2,pady=20 )

            nazad_admin = Button(
                dodaj_frame, 
                text="Nazad", 
                command=lambda: [dodaj_frame.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]
)
            nazad_admin.grid(row=6, column=3, pady=20)


        def ukloni_zaposlenika():
            filepath = "data/zaposlenici.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Info", "Nema zaposlenika.")
                return

            clear_root()
            ukloni_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            ukloni_frame.grid(row=1, column=1)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                zaposlenici = list(reader)

            Label(
                ukloni_frame, 
                text="Ukloni zaposlenika", 
                font=("Helvetica", 16, "bold")).pack(pady=10)

            lista = Listbox(ukloni_frame, height=10, width=50)
            entries = [f"{z['Ime']} {z['Prezime']} ({z['Nadimak']}) - {z['Pozicija']}" for z in zaposlenici]
                
            for entry in entries:
                lista.insert("end", entry)
            lista.pack(pady=10)


            def obrisi():
                idx = lista.curselection()
                if not idx:
                    messagebox.showerror("Greška", "Odaberi zaposlenika.")
                    return

                del zaposlenici[idx[0]]

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(
                        file, 
                        fieldnames=["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"]
)
                    writer.writeheader()
                    writer.writerows(zaposlenici)

                messagebox.showinfo("Uspjeh", "Zaposlenik uklonjen.")
                open_admin_dashboard(ime_admin, prezime_admin)

            Button(
                ukloni_frame, 
                text="Ukloni", 
                command=obrisi).pack(pady=5)

            Button(
                ukloni_frame, 
                text="Nazad", 
                command=lambda: [ukloni_frame.destroy(), open_admin_dashboard(ime_admin, prezime_admin)]).pack(pady=5)

        # Glavni gumbi
        Button(
            admin_frame, 
            text="Dodaj zaposlenika", 
            width=25, 
            command=dodaj_zaposlenika).pack(pady=10)
        
        Button(
            admin_frame, 
            text="Ukloni zaposlenika", 
            width=25, 
            command=ukloni_zaposlenika).pack(pady=10)
        
        Button(
            admin_frame, 
            text="Zakaži termin",
            width=25, 
            command=zakazi_termin_admin).pack(pady=10)
        
        Button(
            admin_frame,
            text="Otkaži termin",
            width=25,
            command=otkazi_termin).pack(pady=10)

        Button(
            admin_frame, 
            text="Zakazani termini", 
            width=25, 
            command=prikazi_termine).pack(pady=10)
        
        Button(
            admin_frame, 
            text="Logout", 
            width=25, 
            command=lambda: [admin_frame.destroy(), show_buttons()]).pack(pady=10)

#-----------------------------------------------------------------------------------------------------------------------------------------------
    def open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika):
        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, Frame):
                    widget.destroy()

        zaposlenik_frame = Frame(root, padx=20, pady=20, bg="light salmon")
        zaposlenik_frame.grid(row=1, column=1)

        Label(
            zaposlenik_frame, 
            text=f"Zaposlenik: {ime_zaposlenika} {prezime_zaposlenika}", font=("Helvetica", 16, "bold")).pack(pady=20)


        def ucitaj_usluge_iz_csv(putanja):
            usluge_lista = []
            with open(putanja, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for red in reader:
                    naziv = red["Usluga"]
                    cijena = red["Cijena"]
                    usluge_lista.append(f"{naziv} -> {cijena}")
            return usluge_lista

        def zakazi_termin_zaposlenik():
            clear_root()

            radno_vrijem_label = tk.Label(
                    root,
                    text="Radno vrijeme:\nPon - Pet: 08:00 - 16:00\nSub: 08:00 - 13:00",
                    font=("Arial", 12),
                    fg="black",
                    bg="light salmon",
                )
            radno_vrijem_label.grid(row=0, column=0, columnspan=3)


            zakazi_frame_zaposlenik = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            zakazi_frame_zaposlenik.grid(row=1, column=1)

            vrijeme_var = tk.StringVar()
            usluga_var = tk.StringVar()

            result_label = tk.Label(zakazi_frame_zaposlenik, text="", font=("Arial", 12), fg="black", bg="light salmon")
            result_label.grid(row=4, column=0, columnspan=3)

            # Kalendar - postavljamo mindate na danas i onemogućavamo nedjelje
            today = datetime.datetime.now().date()
            
            # Kalendar - postavljamo mindate na danas (ne može se odabrati prošli datum)
            today = datetime.datetime.now().date()
            cal = Calendar(zakazi_frame_zaposlenik, selectmode='day', date_pattern='dd-mm-yyyy', mindate=today)
            cal.grid(row=0, column=0, columnspan=3, pady=(10, 20))

            # Učitaj zauzeta vremena iz CSV-a za odabrani datum
            def ucitaj_zauzeta_vremena(selected_date):
                zauzeta_vremena = set()
                file_path = "data/zakazani_termini.csv"
                if os.path.isfile(file_path):
                    with open(file_path, mode="r", encoding="utf-8") as file:
                        reader = csv.reader(file)
                        next(reader)  # Preskoči zaglavlje
                        for row in reader:
                            if len(row) >= 5 and row[3] == selected_date:
                                vrijeme = row[4].split(':')[0]  # Uzmi samo sat (npr. "08" iz "08:00")
                                zauzeta_vremena.add(vrijeme)
                return zauzeta_vremena


            ## Generiraj dostupna vremena (08:00 - 16:00) i filtriraj zauzeta
            def update_vremena(event=None):
                selected_date_str = cal.get_date()
                day, month, year = map(int, selected_date_str.split('-'))
                selected_date = datetime.date(year, month, day)
                
                zauzeta_vremena = ucitaj_zauzeta_vremena(selected_date_str)
                
                # Odredi radno vrijeme ovisno o danu
                if selected_date.weekday() == 5:  # Subota
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 14)]  
                else:  # Radni dan
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 16)]  
                
                dostupna_vremena = [v for v in sva_vremena if v.split(':')[0] not in zauzeta_vremena]
                
                hour_dropdown['values'] = ["Vrijeme"] + dostupna_vremena
                hour_dropdown.current(0)
                vrijeme_var.set("Vrijeme")

            # Postavi Combobox za vrijeme
            hour_dropdown = ttk.Combobox(
                zakazi_frame_zaposlenik, 
                textvariable=vrijeme_var,
                values=["Vrijeme"], 
                state="readonly"  # Zabrani ručno unos
            )
            hour_dropdown.current(0)
            hour_dropdown.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            
            # Osiguraj da se ažuriraju dostupna vremena kad se promijeni datum
            cal.bind("<<CalendarSelected>>", update_vremena)

            # Ucitaj usluge iz CSV
            usluge = ucitaj_usluge_iz_csv("data/usluge.csv")

            intervention_dropdown = ttk.Combobox(
                zakazi_frame_zaposlenik, 
                textvariable=usluga_var,
                values=["Zahvat"] + usluge,
                state="readonly"  # Zabrani ručno unos
            )
            intervention_dropdown.current(0)
            intervention_dropdown.grid(row=2, column=0, columnspan=3, pady=(0, 10))

            def spremi():
                selected_date = cal.get_date()
                selected_hour = vrijeme_var.get()
                selected_usluga = usluga_var.get()

                if selected_hour == "Vrijeme" or not selected_hour:
                    result_label.config(text="Odaberite vrijeme.")
                elif selected_usluga == "Zahvat" or not selected_usluga:
                    result_label.config(text="Odaberite uslugu.")
                else:
                    unos_prozor = tk.Toplevel(root)
                    unos_prozor.title("Unos podataka")
                    unos_prozor.geometry("300x200")
                    unos_prozor.resizable(False, False)

                    tk.Label(unos_prozor, text="Ime:").pack(pady=5)
                    ime_entry = tk.Entry(unos_prozor)
                    ime_entry.pack()

                    tk.Label(unos_prozor, text="Prezime:").pack(pady=5)
                    prezime_entry = tk.Entry(unos_prozor)
                    prezime_entry.pack()

                    tk.Label(unos_prozor, text="Broj:").pack(pady=5)
                    broj_entry = tk.Entry(unos_prozor)
                    broj_entry.pack()

                    def potvrdi_unos():
                        ime = ime_entry.get().strip()
                        prezime = prezime_entry.get().strip()
                        broj = broj_entry.get().strip()

                        if not ime or not prezime or not broj:
                            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")
                            return

                        # Spremi u CSV
                        file_path = "data/zakazani_termini.csv"
                        zaglavlje = ["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"]
                        file_exist = os.path.isfile(file_path)

                        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            if not file_exist:
                                writer.writerow(zaglavlje)
                            writer.writerow([ime, prezime, broj, selected_date, selected_hour, selected_usluga])

                        unos_prozor.destroy()
                        zakazi_frame_zaposlenik.destroy()

                        # Kreiraj novi frame za potvrdu
                        potvrda_frame = Frame(root, padx=20, pady=20, bg="light salmon")
                        potvrda_frame.grid(row=1, column=1)

                        potvrda_label = Label(
                            potvrda_frame,
                            text=f"Termin zakazan za {selected_date} u {selected_hour}\nZahvat: {selected_usluga}\nZa: {ime} {prezime}",
                            font=("Arial", 12),
                            fg="black",
                            bg="light salmon",
                            justify="left"
                        )
                        potvrda_label.pack(pady=20)

                        back_pot_termin = tk.Button(
                            potvrda_frame, 
                            text="Nazad", 
                            command=lambda:[potvrda_frame.destroy(), open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)]
                        )
                        back_pot_termin.pack(pady=20)

                    potvrdi_btn = tk.Button(unos_prozor, text="Potvrdi", command=potvrdi_unos)
                    potvrdi_btn.pack(pady=10)

            submit_btn = tk.Button(zakazi_frame_zaposlenik, text="Zakazi termin", command=lambda:[radno_vrijem_label.destroy(), spremi()])
            submit_btn.grid(row=3, column=1, pady=(0, 10))

            back_zak_termin = tk.Button(
                zakazi_frame_zaposlenik, 
                text="Nazad", 
                command=lambda:[zakazi_frame_zaposlenik.destroy(),radno_vrijem_label.destroy(), open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)]
            )
            back_zak_termin.grid(row=6, column=1, pady=20)

            

        def prikazi_termine():
            clear_root()
            prikaz_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            prikaz_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                tekst = ""
                for row in reader:
                    tekst += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']} -> {row['Zahvat']}\n"

            text_box = Text(prikaz_frame, wrap="word", height=20)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.pack(expand=True, fill="both", padx=10, pady=10)

            Button(
                prikaz_frame, 
                text="Natrag", 
                command=lambda:[prikaz_frame.destroy(), open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)]).pack(pady=10)


        def otkazi_termin():
            clear_root()
            otkazi_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            otkazi_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = list(csv.DictReader(file))
                if not reader:
                    messagebox.showinfo("Prazno", "Nema zakazanih termina.")
                    return open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)

            lista = Listbox(otkazi_frame, width=80, height=20)
            lista.pack(pady=10)

            termini = []
            for i, row in enumerate(reader):
                tekst = f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']} ({row['Zahvat']})"
                lista.insert(i, tekst)
                termini.append(row)

            def otkazi():
                index = lista.curselection()
                if not index:
                    messagebox.showerror("Greška", "Odaberite termin za otkazivanje.")
                    return
                del termini[index[0]]
                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                    writer.writeheader()
                    writer.writerows(termini)
                messagebox.showinfo("Uspjeh", "Termin je otkazan.")
                otkazi_frame.destroy()
                open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)

            Button(otkazi_frame, text="Otkaži odabrani termin", command=otkazi).pack(pady=10)
            Button(otkazi_frame, text="Natrag", command=lambda: [otkazi_frame.destroy(), open_zaposlenik_dashboard(ime_zaposlenika, prezime_zaposlenika)]).pack(pady=5)



        Button(
            zaposlenik_frame, 
            text="Zakaži termin",
            width=25, 
            command=zakazi_termin_zaposlenik).pack(pady=10)

        Button(
            zaposlenik_frame,
            text="Otkaži termin",
            width=25,
            command=otkazi_termin).pack(pady=10)


        Button(
            zaposlenik_frame, 
            text="Zakazani termini",
            width=25, 
            command=prikazi_termine).pack(pady=10)
        
        Button(
            zaposlenik_frame, 
            text="Logout",
            width=25, 
            command=lambda: [zaposlenik_frame.destroy(), show_buttons()]).pack(pady=10)
#---------------------------------------------------------------------------------------------------------

    def open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika):
        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, Frame):
                    widget.destroy()

        clear_root()

        user_frame = Frame(root, padx=20, pady=20, bg="light salmon")
        user_frame.grid(row=1, column=1, sticky="nsew")

        welcome_text = f"Korisnik: {ime_korisnika} {prezime_korisnika}"
        Label(
            user_frame, 
            text=welcome_text, 
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, pady=30, columnspan=2)

        def ucitaj_usluge_iz_csv(putanja):
            usluge_lista = []
            with open(putanja, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for red in reader:
                    naziv = red["Usluga"]
                    cijena = red["Cijena"]
                    usluge_lista.append(f"{naziv} -> {cijena}")
            return usluge_lista

        def zakazi_termin_korisnik():
            clear_root()

            radno_vrijem_label = tk.Label(
                    root,
                    text="Radno vrijeme:\nPon - Pet: 08:00 - 16:00\nSub: 08:00 - 13:00",
                    font=("Arial", 12),
                    fg="black",
                    bg="light salmon",
                )
            radno_vrijem_label.grid(row=0, column=0, columnspan=3)

            zakazi_frame_korisnik = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            zakazi_frame_korisnik.grid(row=1, column=1)

            vrijeme_var = tk.StringVar()
            usluga_var = tk.StringVar()

            # Kalendar - postavljamo mindate na danas (ne može se odabrati prošli datum)
            today = datetime.datetime.now().date()
            cal = Calendar(zakazi_frame_korisnik, selectmode='day', date_pattern='dd-mm-yyyy', mindate=today)
            cal.grid(row=0, column=0, columnspan=3, pady=(10, 20))

            # Učitaj zauzeta vremena iz CSV-a za odabrani datum
            def ucitaj_zauzeta_vremena(selected_date):
                zauzeta_vremena = set()
                file_path = "data/zakazani_termini.csv"
                if os.path.isfile(file_path):
                    with open(file_path, mode="r", encoding="utf-8") as file:
                        reader = csv.reader(file)
                        next(reader)  # Preskoči zaglavlje
                        for row in reader:
                            if len(row) >= 5 and row[3] == selected_date:
                                vrijeme = row[4].split(':')[0]  # Uzmi samo sat (npr. "08" iz "08:00")
                                zauzeta_vremena.add(vrijeme)
                return zauzeta_vremena

            # Generiraj dostupna vremena (08:00 - 16:00) i filtriraj zauzeta
            def update_vremena(event=None):
                selected_date_str = cal.get_date()
                day, month, year = map(int, selected_date_str.split('-'))
                selected_date = datetime.date(year, month, day)
                
                zauzeta_vremena = ucitaj_zauzeta_vremena(selected_date_str)
                
                # Odredi radno vrijeme ovisno o danu
                if selected_date.weekday() == 5:  # Subota
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 14)]  # 08:00 - 13:00
                else:  # Radni dan
                    sva_vremena = [f"{i:02d}:00" for i in range(8, 16)]  # 08:00 - 16:00
                
                dostupna_vremena = [v for v in sva_vremena if v.split(':')[0] not in zauzeta_vremena]
                
                hour_dropdown['values'] = ["Vrijeme"] + dostupna_vremena
                hour_dropdown.current(0)
                vrijeme_var.set("Vrijeme")

            # Postavi Combobox za vrijeme
            hour_dropdown = ttk.Combobox(
                zakazi_frame_korisnik, 
                textvariable=vrijeme_var,
                values=["Vrijeme"], 
                state="readonly"  # Zabrani ručno unos
            )
            hour_dropdown.current(0)
            hour_dropdown.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            
            # Osiguraj da se ažuriraju dostupna vremena kad se promijeni datum
            cal.bind("<<CalendarSelected>>", update_vremena)

            # Ucitaj usluge iz CSV
            usluge = ucitaj_usluge_iz_csv("data/usluge.csv")

            intervention_dropdown = ttk.Combobox(
                zakazi_frame_korisnik, 
                textvariable=usluga_var,
                values=["Zahvat"] + usluge,
                state="readonly"  # Zabrani ručno unos
            )
            intervention_dropdown.current(0)
            intervention_dropdown.grid(row=2, column=0, columnspan=3, pady=(0, 10))


            def spremi():
                selected_date = cal.get_date()
                selected_hour = vrijeme_var.get()
                selected_usluga = usluga_var.get()

                if selected_hour == "Vrijeme" or not selected_hour:
                    messagebox.showwarning("Greška", "Odaberite vrijeme.")
                    return
                if selected_usluga == "Zahvat" or not selected_usluga:
                    messagebox.showwarning("Greška", "Odaberite uslugu.")
                    return

                # Spremi u zakazani_termini.csv
                file_path = "data/zakazani_termini.csv"
                zaglavlje = ["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"]
                fajl_postoji = os.path.isfile(file_path)
                with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if not fajl_postoji:
                        writer.writerow(zaglavlje)
                    writer.writerow([ime_korisnika, prezime_korisnika, broj_korisnika, selected_date, f"{selected_hour}", selected_usluga])

                zakazi_frame_korisnik.destroy()

                potvrda_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
                potvrda_frame.grid(row=1, column=1)

                potvrda_label = tk.Label(
                    potvrda_frame,
                    text=f"Termin zakazan za {selected_date} u {selected_hour}\nZahvat: {selected_usluga}\nZa: {ime_korisnika} {prezime_korisnika}",
                    font=("Arial", 12),
                    fg="black",
                    bg="light salmon",
                    justify="left"
                )
                potvrda_label.pack(pady=20)

                def ispisi_racun():
                    os.makedirs("računi", exist_ok=True)
                    naziv_racuna = f"račun_{ime_korisnika}_{prezime_korisnika}_{selected_date}.txt".replace(" ", "_")
                    putanja_racuna = os.path.join("računi", naziv_racuna)

                    if "->" in selected_usluga:
                        naziv_usluge, cijena = map(str.strip, selected_usluga.split("->"))
                    else:
                        naziv_usluge = selected_usluga
                        cijena = "Nepoznato"

                    with open(putanja_racuna, "w", encoding="utf-8") as file:
                        file.write("         Račun\n")
                        file.write("------------------------------\n")
                        file.write("------------------------------\n")
                        file.write(f"Ime: {ime_korisnika} \n")
                        file.write(f"Prezime: {prezime_korisnika}\n")
                        file.write(f"Datum: {selected_date}\n")
                        file.write(f"Vrijeme: {selected_hour}\n")
                        file.write(f"Usluga: {naziv_usluge}\n")
                        file.write(f"Cijena: {cijena}\n")
                        file.write("------------------------------\n")
                        file.write("------------------------------\n")
                        file.write("\n   Hvala na povjerenju!   \n")

                    messagebox.showinfo("Račun", f"Račun je uspješno isprintan.")
                    potvrda_frame.destroy()
                    open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)

                ispisi_btn = tk.Button(potvrda_frame, text="Ispiši račun", command=ispisi_racun)
                ispisi_btn.pack(pady=10)

            submit_btn = tk.Button(zakazi_frame_korisnik, text="Zakazi termin", command=lambda:[radno_vrijem_label.destroy(), spremi()])
            submit_btn.grid(row=3, column=1, pady=(0, 10))

            back_zak_termin = tk.Button(
                zakazi_frame_korisnik,
                text="Nazad",
                command=lambda: [zakazi_frame_korisnik.destroy(),radno_vrijem_label.destroy(), open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)]
            )
            back_zak_termin.grid(row=6, column=1, pady=20)


        def otkazi_termin_korisnik(ime, prezime, broj):
            clear_root()

            otkazi_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            otkazi_frame.grid(row=1, column=1)

            Label(
                otkazi_frame,
                text=f"Korisnik: {ime} {prezime} ",
                font=("Helvetica", 16, "bold")
            ).grid(row=0, column=0, pady=10)

            filepath = "data/zakazani_termini.csv"
            listbox = Listbox(otkazi_frame, width=60, height=10)
            listbox.grid(row=1, column=0, pady=10)

            # Učitaj sve termine
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                svi_termini = list(reader)

            korisnik_termini = [
                row for row in svi_termini
                if row["Ime"] == ime and row["Prezime"] == prezime and row["Broj"] == broj
            ]

            for t in korisnik_termini:
                listbox.insert(END, f"{t['Datum']} u {t['Vrijeme']} - {t['Zahvat']}")

            def otkazi_termin():
                selected = listbox.curselection()
                if not selected:
                    messagebox.showerror("Greška", "Odaberite termin za otkazivanje.")
                    return

                index = selected[0]
                termin_za_brisanje = korisnik_termini[index]
                svi_termini.remove(termin_za_brisanje)

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                    writer.writeheader()
                    writer.writerows(svi_termini)

                messagebox.showinfo("Uspješno", "Termin je otkazan.")
                otkazi_frame.destroy()
                otkazi_termin_korisnik(ime, prezime, broj)

            if korisnik_termini:
                Button(
                    otkazi_frame,
                    text="Otkaži odabrani termin",
                    command=otkazi_termin
                ).grid(row=2, column=0, pady=10)
            else:
                Label(otkazi_frame, text="Nemate zakazanih termina.").grid(row=2, column=0, pady=10)

            Button(
                otkazi_frame,
                text="Natrag",
                command=lambda: [otkazi_frame.destroy(), open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)]
            ).grid(row=3, column=0, pady=10)

        def prikazi_termine(ime, prezime, broj):
            clear_root()

            prikaz_frame = Frame(root, padx=20, pady=20, bg="light salmon")
            prikaz_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                tekst = ""
                for row in reader:
                    if row["Ime"] == ime and row["Prezime"] == prezime and row["Broj"] == broj:
                        tekst += f"{row['Datum']} u {row['Vrijeme']} -> {row['Zahvat']} (Kontakt: {row['Broj']})\n"

            text_box = Text(prikaz_frame, wrap="word", height=20)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.grid(row=1, column=0, padx=10, pady=10)

            Button(
                prikaz_frame,
                text="Natrag",
                command=lambda: [prikaz_frame.destroy(), open_user_dashboard(ime_korisnika, prezime_korisnika, broj_korisnika)]
            ).grid(row=2, column=0, pady=10)

        # Gumbi za termine
        Button(
            user_frame,
            text="Zakaži termin",
            width=25,
            command=lambda: zakazi_termin_korisnik()).grid(row=1, column=0, pady=10)

        Button(
            user_frame,
            text="Otkaži termin",
            width=25,
            command=lambda: otkazi_termin_korisnik(ime_korisnika, prezime_korisnika, broj_korisnika)).grid(row=2, column=0, pady=10)

        # Dodavanje gumba za pregled zakazanih termina
        Button(
            user_frame,
            text="Moji termini",
            width=25,
            command=lambda: prikazi_termine(ime_korisnika, prezime_korisnika, broj_korisnika)).grid(row=3, column=0, pady=10)

        Button(
            user_frame, 
            text="Logout",
            width=25, 
            command=lambda: [user_frame.destroy(), show_buttons()]).grid(row=4, column=0, pady=10)
#-------------------------------------------------------------------------------------------------------


    root.after(2000, show_buttons)
    root.mainloop()   
       
start_app() 













