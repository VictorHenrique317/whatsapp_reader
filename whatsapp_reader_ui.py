from whatsapp_reader import WhatsappReader
import tkinter
import matplotlib.pyplot as plt
import random


def init_menu():
    def define_users():
        x = []
        for i in range(len(users)):
            if variables[i].get() == 1:
                x.append(users[i])
        return tuple(x)

    def word_count_info():
        def init():
            word = entry.get()
            if word.strip() == "":
                return
            pop_up.destroy()
            selected_users = define_users()
            data = reader.how_many_words(word, users=selected_users)
            print(data)

            pos = range(len(selected_users))
            fig = plt.figure(0)
            fig.canvas.set_window_title("Repetições da palavra {}".format(word))
            plt.bar(pos, data.values())
            plt.xticks(pos, data.keys())
            plt.title("Repetições da palavra {}".format(word))
            plt.show()

        pop_up = tkinter.Toplevel(main_window)
        pop_up.geometry("200x100")

        frame = tkinter.Frame(pop_up)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        entry = tkinter.Entry(frame)
        entry.grid(row=0, column=0)
        tkinter.Button(frame, command=init, text="Pesquisar").grid(row=1, column=0, pady=10)

    def msg_month_info():
        colors = "bgrcmyk"
        temporal_data: dict = reader.extract_temporal_data(define_users(), per_month=True)
        figure, ax = plt.subplots(num="Total de mensagens")
        ax.set(xlabel="Meses", ylabel="Mensagens")

        for user in temporal_data.keys():
            user_data = temporal_data[user]
            x_values = [months[str(int(month_number))] for month_number in list(user_data.keys())]
            y_values = list(user_data.values())
            print(user, x_values,y_values)

            rand = random.randint(0, len(colors) - 1) if len(temporal_data.keys()) <= len(colors) else -1
            color = colors[rand]

            colors = colors.replace(color, "") if len(temporal_data.keys()) <= len(colors) else colors
            line_settings = color + "-"
            ax.plot(x_values, y_values, line_settings, label=user)
        ax.grid()
        plt.title("Mensagens por mês")
        plt.legend()
        plt.show()

    def msg_count_info():
        selected_users = define_users()
        msgs = reader.message_count(selected_users)

        pos = range(len(selected_users))
        fig = plt.figure(0)
        fig.canvas.set_window_title('Total de mensagens')

        plt.bar(pos, msgs.values())
        plt.xticks(pos, msgs.keys())
        plt.title("Total de mensagens")
        plt.show()

    def avr_msg_size_info():
        selected_users = define_users()
        avr_len = reader.average_msg_size(users=selected_users)

        pos = range(len(selected_users))
        plt.figure(0).canvas.set_window_title("Tamanho médio de mensagem (em palavras)")
        plt.bar(pos, avr_len.values())
        plt.xticks(pos, avr_len.keys())
        plt.title("Tamanho médio de mensagem (em palavras)")
        plt.show()

    def most_said_info():
        def init():
            try:
                word_count = int(entry.get())
            except ValueError:
                return
            data = reader.most_said_words(users=selected_users, words=word_count)[
                selected_users[0]]  ## a dict with words and it's frequencies

            pos = range(len(data.keys()))
            fig = plt.figure(0)
            fig.canvas.set_window_title("Palavras mais faladas")
            plt.bar(pos, data.values())
            plt.xticks(pos, data.keys())
            plt.title("Palavras mais faladas")
            pop_up.destroy()
            plt.show()

        selected_users = define_users() if len(define_users()) == 1 else None
        if selected_users is None:
            pop_up = tkinter.Toplevel(main_window)
            pop_up.geometry("180x50")
            # pop_config(pop_up)

            tkinter.Label(pop_up, text="Selecione apenas um usuário").place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            return
        pop_up = tkinter.Toplevel(main_window)
        pop_up.geometry("200x80")

        frame = tkinter.Frame(pop_up)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        tkinter.Label(frame, text="Quantas palavras?").grid(row=0, column=0)
        entry = tkinter.Entry(frame)
        entry.grid(row=1, column=0)
        tkinter.Button(frame, text="Pesquisar", command=init).grid(row=2, pady=10)

    users_frame = tkinter.LabelFrame(main_window, text="Usuários")
    users_frame.grid(column=2, row=1)
    variables = []
    users = reader.get_users()
    for u in users:
        # the index of the user will be equal to the index of his respective variable
        var = tkinter.IntVar()
        variables.append(var)
        tkinter.Checkbutton(users_frame, text=u, variable=var, onvalue=1, offvalue=0, width=20).pack(anchor="w")

    button.destroy()
    button_frame = tkinter.Frame(main_window)
    button_frame.grid(row=1, column=1)

    # ============================== Buttons =======================================#

    tkinter.Button(button_frame, text="Exibir quantidade de mensagens por mês",
                   command=msg_month_info, width=40, height=3).grid(pady=10)
    tkinter.Button(button_frame, text="Exibir total de mensagens", command=msg_count_info,
                   width=40, height=3).grid(row=1, pady=10)
    tkinter.Button(button_frame, text="Exibir tamanho médio de mensagem", command=avr_msg_size_info,
                   width=40, height=3).grid(row=2, pady=10)
    tkinter.Button(button_frame, text="Exibir quantas vezes uma palavra foi repetida",
                   command=word_count_info, width=40, height=3).grid(row=3, pady=10)
    tkinter.Button(button_frame, text="Exibir as palavras mais faladas", command=most_said_info,
                   width=40, height=3).grid(row=4, pady=10)

    tkinter.Button(main_window, text="Selecionar arquivo", command=select_language).grid(row=2, column=1)

    # ============================== Buttons =======================================#


def select_language():
    # result = reader.read()
    global lang_window
    lang_window = tkinter.Toplevel(main_window)
    lang_window.geometry("410x300")
    lang_window.rowconfigure(0, weight=10)
    lang_window.rowconfigure(1, weight=1)
    lang_window.rowconfigure(2, weight=1)

    lang_window.columnconfigure(0, weight=10000)
    lang_window.columnconfigure(1, weight=0)
    lang_window.columnconfigure(2, weight=10000)

    tkinter.Label(main_window).grid(row=0)
    tkinter.Label(main_window).grid(row=2)

    label = tkinter.Label(lang_window, text="Selecione a linguagem do seu Whatsapp:", font="TimesNewRoman 15")
    label.grid(row=0)
    en_button = tkinter.Button(lang_window, text="Inglês", width=10, height=2, font="TimesNewRoman 15",
                               command=set_english)
    pt_button = tkinter.Button(lang_window, text="Português", width=10, height=2, font="TimesNewRoman 15",
                               command=set_portuguese)
    en_button.grid(row=1)
    pt_button.grid(row=2)
    print("reading")
    # if result:
    #     init_menu()


def set_english():
    global lang_window
    if reader.set_english():
        init_menu()
    lang_window.destroy()


def set_portuguese():
    # global lang_window
    if reader.set_portuguse():
        init_menu()
    lang_window.destroy()


reader = WhatsappReader()
months = {"1": "Jan",
          "2": "Fev",
          "3": "Mar",
          "4": "Abr",
          "5": "Mai",
          "6": "Jun",
          "7": "Jul",
          "8": "Ago",
          "9": "Set",
          "10": "Out",
          "11": "Nov",
          "12": "Dez"}


lang_window = None
main_window = tkinter.Tk()
main_window.geometry("800x600")
main_window.rowconfigure(0, weight=1000)
main_window.rowconfigure(1, weight=1)
main_window.rowconfigure(2, weight=1000)

main_window.columnconfigure(0, weight=10000)
main_window.columnconfigure(1, weight=0)
main_window.columnconfigure(2, weight=10000)

tkinter.Label(main_window).grid(row=0)
tkinter.Label(main_window).grid(row=2)
button = tkinter.Button(main_window, text="Escolher arquivo de texto", width=40, height=5, font="TimesNewRoman 15",
                        command=select_language)

# pt_button = tkinter.Button(main_window, text="Português", width=40, height=5, font="TimesNewRoman 15",
#                            command=portuguese)
button.grid(row=1, column=1)
tkinter.Label(main_window).grid(column=0, row=0, rowspan=3)
tkinter.Label(main_window).grid(column=2, row=0, rowspan=3)

main_window.mainloop()
