from pathlib import Path
import tkinter as tk
import tkinter.messagebox
import re
import configparser
import os

def main():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("settings_assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def go_main_page():
        window.destroy()
        import gui.main_page as main_page
        main_page.main()

    def load():
        login_entry.insert(0, config['email']['login'])
        passwd_entry.insert(0, config['email']['passwd'])
        server_entry.insert(0, config['email']['server'])
        port_entry.insert(0, config['email']['port'])
        
        iln_entry.insert(0, config['edi']['iln'])
        bank_entry.insert(0, config['edi']['bank_number'])
        country_entry.insert(0, config['edi']['country'])
        bdo_entry.insert(0, config['edi']['bdo'])
        krs_entry.insert(0, config['edi']['krs'])

    def save():
        login = login_entry.get()
        passwd = passwd_entry.get()
        server = server_entry.get()
        port = port_entry.get()

        iln = iln_entry.get()
        bank_number = bank_entry.get()
        country = country_entry.get()
        bdo = bdo_entry.get()
        krs = krs_entry.get()

        if not login:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź adres e-mail.")
            return
        if not passwd:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź hasło.")
            return
        if not server:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź adres serwera.")
            return
        if not port:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź numer portu serwera.")
            return
        if not bank_number:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź numer konta bankowego.")
            return

        match = re.search(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', login.strip())
        if match is None:
            tk.messagebox.showerror(
                "Niepoprawny email!", "Wprowadź poprawny email.")
            return

        port_match = re.search(
            r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', port.strip())
        if port_match is None:
            tk.messagebox.showerror(
                "Niepoprawny port!", "Wprowadź poprawny port serwera.")
            return

        iln_match = re.search(
            r'^$|^(\d{13})$', iln.strip())
        if iln_match is None:
            tk.messagebox.showerror(
                "Niepoprawny numer ILN!", "Wprowadź poprawny numer ILN.")
            return

        bank_match = re.search(
            r'^\d{26}$', bank_number.strip())
        if bank_match is None:
            tk.messagebox.showerror(
                "Niepoprawny numer konta bankowego!", "Wprowadź poprawny numer konta bankowego.")
            return

        iso_match = re.search(
            r'^[A-Z]{2}$', country.strip())
        if iso_match is None:
            tk.messagebox.showerror(
                "Niepoprawny kraj!", "Wprowadź poprawny symbol kraju (np. PL).")
            return

        config['email']['login'] = login
        config['email']['passwd'] = passwd
        config['email']['server'] = server
        config['email']['port'] = port

        config['edi']['iln'] = iln
        config['edi']['bank_number'] = bank_number
        config['edi']['country'] = country
        config['edi']['bdo'] = bdo
        config['edi']['krs'] = krs

        with open('./dgcs2edi/db.ini', 'w') as configfile:
            config.write(configfile)

        tk.messagebox.showerror("Ustawienia zapisane!", "Ustawienia zostały pomyślnie zapisane.")

    window = tk.Tk()
    window.title('Generator faktur w formacie EDI')
    window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file=str(ASSETS_PATH) + '/icon.png'))
    window.geometry("862x519")
    window.configure(bg="#3A7FF6")

    config = configparser.ConfigParser()

    if os.path.isfile('./dgcs2edi/db.ini'):
        config.read('./dgcs2edi/db.ini')
    else:
        config.add_section("email")
        config.set("email", "login", "")
        config.set("email", "passwd", "")
        config.set("email", "server", "")
        config.set("email", "port", "")
        config.set("email", "subject", "Nowa faktura w formacie EDI")
        config.set("email", "content", "Otrzymali Państwo nową fakturę w formacie EDI")

        config.add_section("edi")
        config.set("edi", "iln", "")
        config.set("edi", "bank_number", "")
        config.set("edi", "country", "")
        config.set("edi", "bdo", "")
        config.set("edi", "krs", "")

        with open('./dgcs2edi/db.ini', 'w') as configfile:
            config.write(configfile)


    canvas = tk.Canvas(
        window,
        bg="#3A7FF6",
        height=519,
        width=862,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        557.9999999999999,
        31.000000000000007,
        anchor="nw",
        text="Ustawienia EDI:",
        fill="#FCFCFC",
        font=("Roboto Bold", 23 * -1, "bold"),
        width=168.0
    )

    canvas.create_rectangle(
        1.1368683772161603e-13,
        7.105427357601002e-15,
        431.0000000000001,
        519.0,
        fill="#FCFCFC",
        outline="")

    button_image_1 = tk.PhotoImage(
        file=relative_to_assets("button_1.png"))
    save_button = tk.Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: save(),
        relief="flat"
    )
    save_button.place(
        x=125.99999999999989,
        y=445.0,
        width=180.0,
        height=55.0
    )

    canvas.create_text(
        58.999999999999886,
        50.00000000000001,
        anchor="nw",
        text="Ustawienia serwera e-mail:",
        fill="#505485",
        font=("Roboto Bold", 23 * -1, "bold"),
        width=293.0
    )

    entry_image_1 = tk.PhotoImage(
        file=relative_to_assets("entry_1.png")
    )
    canvas.create_image(
        219.4999999999999,
        135.5,
        image=entry_image_1
    )
    login_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    login_entry.place(
        x=58.999999999999886,
        y=105.0 + 24,
        width=321.0,
        height=30.0
    )

    entry_image_2 = tk.PhotoImage(
        file=relative_to_assets("entry_2.png")
    )
    canvas.create_image(
        219.4999999999999,
        221.5,
        image=entry_image_2
    )
    passwd_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0,
        show='•'
    )
    passwd_entry.place(
        x=58.999999999999886,
        y=191.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        59.999999999999886,
        193.0,
        anchor="nw",
        text="Hasło",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=45
    )

    entry_image_3 = tk.PhotoImage(
        file=relative_to_assets("entry_3.png")
    )
    canvas.create_image(
        219.4999999999999,
        307.5,
        image=entry_image_3
    )
    server_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    server_entry.place(
        x=58.999999999999886,
        y=277.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        59.999999999999886,
        282.0,
        anchor="nw",
        text="Serwer",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=50.0
    )

    entry_image_4 = tk.PhotoImage(
        file=relative_to_assets("entry_4.png")
    )
    canvas.create_image(
        219.4999999999999,
        393.5,
        image=entry_image_4
    )
    port_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    port_entry.place(
        x=58.999999999999886,
        y=363.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        59.999999999999886,
        367.0,
        anchor="nw",
        text="Port",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=35.0
    )

    canvas.create_text(
        59.999999999999886,
        109.0,
        anchor="nw",
        text="Adres e-mail",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=100.0
    )

    entry_image_5 = tk.PhotoImage(
        file=relative_to_assets("entry_5.png")
    )
    canvas.create_image(
        641.4999999999999,
        115.5,
        image=entry_image_5
    )
    iln_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    iln_entry.place(
        x=480.9999999999999,
        y=85.0 + 24,
        width=321.0,
        height=30.0
    )

    entry_image_6 = tk.PhotoImage(
        file=relative_to_assets("entry_6.png")
    )
    canvas.create_image(
        641.4999999999999,
        201.5,
        image=entry_image_6
    )
    bank_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    bank_entry.place(
        x=480.9999999999999,
        y=171.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        481.9999999999999,
        174.0,
        anchor="nw",
        text="Numer konta sprzedającego",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=200.0
    )

    entry_image_7 = tk.PhotoImage(
        file=relative_to_assets("entry_7.png")
    )
    canvas.create_image(
        641.4999999999999,
        287.5,
        image=entry_image_7
    )
    country_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    country_entry.place(
        x=480.9999999999999,
        y=257.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        481.9999999999999,
        262.0,
        anchor="nw",
        text="Kraj sprzedającego",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=150.0
    )

    entry_image_8 = tk.PhotoImage(
        file=relative_to_assets("entry_8.png")
    )
    canvas.create_image(
        641.4999999999999,
        373.5,
        image=entry_image_8
    )
    bdo_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    bdo_entry.place(
        x=480.9999999999999,
        y=343.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        481.9999999999999,
        348.0,
        anchor="nw",
        text="Numer BDO sprzedającego (opcjonalne)",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=300
    )

    entry_image_9 = tk.PhotoImage(
        file=relative_to_assets("entry_9.png")
    )
    canvas.create_image(
        641.4999999999999,
        454.5,
        image=entry_image_9
    )
    krs_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
        highlightthickness=0
    )
    krs_entry.place(
        x=480.9999999999999,
        y=424.0 + 24,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        481.9999999999999,
        429.0,
        anchor="nw",
        text="Numer KRS sprzedającego (opcjonalne)",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=300
    )

    canvas.create_text(
        481.9999999999999,
        89.0,
        anchor="nw",
        text="ILN sprzedającego (opcjonalne)",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=250.0
    )

    button_image_2 = tk.PhotoImage(
        file=relative_to_assets("button_2.png"))
    back_button = tk.Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: go_main_page(),
        relief="flat"
    )
    back_button.place(
        x=12.999999999999886,
        y=13.000000000000007,
        width=35.0,
        height=35.0
    )

    load()

    window.resizable(False, False)
    window.mainloop()
