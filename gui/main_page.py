from pathlib import Path
from dgcs2edi import core
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import re
import os


def main():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("main_assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def go_settings():
        window.destroy()
        import gui.settings as settings
        settings.main()

    window = tk.Tk()
    window.title('Generator faktur w formacie EDI')
    window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file=str(ASSETS_PATH) + '/icon.png'))
    window.geometry("862x519")
    window.configure(bg="#3A7FF6")

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
    canvas.create_rectangle(
        430.9999999999999,
        0.0,
        861.9999999999999,
        519.0,
        fill="#FCFCFC",
        outline="")

    button_image_1 = tk.PhotoImage(
        file=relative_to_assets("button_1.png"))
    generate_button = tk.Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: generate(),
        relief="flat"
    )
    generate_button.place(
        x=556.9999999999999,
        y=401.0,
        width=180.0,
        height=55.0
    )

    button_image_2 = tk.PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = tk.Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: go_settings(),
        relief="flat"
    )
    button_2.place(
        x=122.99999999999989,
        y=401.0,
        width=180.0,
        height=55.0
    )

    canvas.create_text(
        39.999999999999886,
        127.0,
        anchor="nw",
        text="Generator faktur w formacie EDI",
        fill="#FCFCFC",
        font=("Roboto Bold", 23 * -1, "bold"),
        width=360.0
    )

    canvas.create_text(
        481.9999999999999,
        74.0,
        anchor="nw",
        text="Wprowadź dane:",
        fill="#505485",
        font=("Roboto Bold", 23 * -1, "bold"),
        width=190.0
    )

    canvas.create_rectangle(
        39.999999999999886,
        160.0,
        99.99999999999989,
        165.0,
        fill="#FCFCFC",
        outline="")

    entry_image_1 = tk.PhotoImage(
        file=relative_to_assets("entry_1.png")
    )
    canvas.create_image(
        650.4999999999999,
        167.5,
        image=entry_image_1
    )
    email_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        highlightthickness=0,
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16)
    )
    email_entry.place(
        x=489.9999999999999,
        y=137.0 + 24.0,
        width=321.0,
        height=30.0
    )

    entry_image_2 = tk.PhotoImage(
        file=relative_to_assets("entry_2.png")
    )
    canvas.create_image(
        650.4999999999999,
        248.5,
        image=entry_image_2
    )
    country_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        highlightthickness=0,
        insertbackground='black',
        fg='#000000',
        font=("Roboto", 16),
    )
    country_entry.place(
        x=489.9999999999999,
        y=218.0 + 24.0,
        width=321.0,
        height=30.0
    )

    country_entry.insert(tk.END, 'PL')

    canvas.create_text(
        490.9999999999999,
        221.0,
        anchor="nw",
        text="Kraj",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=30.0
    )

    entry_image_3 = tk.PhotoImage(
        file=relative_to_assets("entry_3.png")
    )
    canvas.create_image(
        650.4999999999999,
        329.5,
        image=entry_image_3
    )
    path_entry = tk.Entry(
        bd=0,
        bg="#F1F5FF",
        highlightthickness=0,
        insertbackground='black',
        fg='#000000',
        font=("Roboto Bold", 16)
    )
    path_entry.place(
        x=489.9999999999999,
        y=299.0 + 24.0,
        width=321.0,
        height=30.0
    )

    canvas.create_text(
        490.9999999999999,
        303.0,
        anchor="nw",
        text="Plik",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=30.0
    )

    button_image_3 = tk.PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = tk.Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: select_path(),
    )
    button_3.place(
        x=782.9999999999999,
        y=319.0,
        width=24.0,
        height=22.0
    )

    canvas.create_text(
        490.9999999999999,
        141.0,
        anchor="nw",
        text="Adres e-mail",
        fill="#3A7FF6",
        font=("Roboto Bold", 14 * -1, "bold"),
        width=100.0
    )

    canvas.create_text(
        39.999999999999886,
        204.0,
        anchor="nw",
        text="W polu “Adres e-mail” wprowadź adres, na który ma zostać wysłana wygenerowana faktura. "
             "W polu “Kraj” wprowadź kod kraju kupującego (np. PL). W polu plik wybierz plik faktury wygenerowany w"
             " programie DGCS System za pomocą przycisku “Do pliku”.",
        fill="#FFFFFF",
        font=("Roboto", 16 * -1, "bold"),
        width=346.0
    )

    def select_path():
        output_path = tk.filedialog.askopenfilename(filetypes=[("Plik XML", "*.xml")])
        path_entry.delete(0, tk.END)
        path_entry.insert(0, output_path)

    def generate():
        receiver = email_entry.get()
        filename = path_entry.get()
        country = country_entry.get()

        if not receiver:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź email odbiorcy.")
            return
        if not country:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź symbol kraju odbiorcy.")
            return
        if not filename:
            tk.messagebox.showerror(
                title="Puste pole!", message="Wprowadź ścieżkę pliku.")
            return

        match = re.search(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', receiver.strip())
        if match is None:
            tk.messagebox.showerror(
                "Niepoprawny email!", "Wprowadź poprawny email.")
            return

        iso_match = re.search(
            r'^[A-Z]{2}$', country.strip())
        if iso_match is None:
            tk.messagebox.showerror(
                "Niepoprawny kraj!", "Wprowadź poprawny symbol kraju (np. PL).")
            return

        if os.path.exists(filename) and '.xml' in filename:
            try:
                reader = core.XMLRead(filename)
                attributes, items = reader.read_file()

                writter = core.XMLWrite(attributes, items)
                gen_filename = writter.write_file(country)
                gen_filename = gen_filename.replace('./', '')
                reader.close()

            except Exception as e:
                tk.messagebox.showinfo("Błąd programu!", f'Wystąpił błąd w trakcie generowania pliku: {e}.')
            else:
                send(receiver, gen_filename)

        else:
            tk.messagebox.showerror(
                "Nie ma takiego pliku!",
                f"Wprowadź poprawną ścieżkę pliku.\n")

    def send(receiver, filename):
        try:
            sender = core.XMLSend()
            sender.send_invoice(receiver, filename)
        except Exception as e:
            tk.messagebox.showinfo("Błąd programu!", f'Wystąpił błąd w trakcie wysyłania wiadomości: {e}.')
        else:
            tk.messagebox.showinfo(
                "Sukces!", f"Faktura została wysłana pomyślnie na adres {receiver}.")

    window.resizable(False, False)
    window.mainloop()
