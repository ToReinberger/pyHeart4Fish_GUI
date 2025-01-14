import sys
import tkinter as tk
from tkinter import ttk, filedialog, Entry, messagebox
import os
import datetime
import time
import json
from threading import Thread
import glob
import pandas as pd


class StartConfigs(tk.Tk):

    def __init__(self):
        super().__init__()  # root is self since root = tk.Tk()
        # create window:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # self.attributes('-fullscreen', True)
        # self.geometry(f'{int(screen_width /2.2)}x
        # {int(screen_height/ 2.8)}+{int(screen_width /9)}+{int(screen_height /8)}')
        self.geometry(f'830x410+{int(screen_width / 9)}+{int(screen_height / 8)}')
        self.resizable(0, 0)
        self.title("pyHeart4Fish")
        self.configure(bg="#3B3E40")
        abspath = os.path.abspath(__file__)
        os.chdir(os.path.dirname(abspath))
        print(os.getcwd())
        if os.path.isfile(os.getcwd() + "/Logo/PyHeart4Fish.ico"):
            self.iconbitmap(os.getcwd() + "/Logo/PyHeart4Fish.ico")
        self.config_dict = dict()
        self.config_dict["timestamp"] = str(timestamp)
        self.config_dict["overwrite_data"] = ""
        self.config_dict["input"] = os.getcwd()
        self.config_dict["output"] = os.getcwd() + f"/Results_{date_str}"
        self.config_dict["every_sec_img"] = 1
        self.config_dict["file_format"] = ".avi"
        self.config_dict["acquisition_mode"] = "Fluorescence (chamber-specific)"

        # create buttons and fields:
        s = ttk.Style()
        s.configure('TFrame', background="#3B3E40")

        browser_frame = ttk.Frame(self, width=int(self.winfo_screenwidth() / 1.8))
        browser_frame.grid(row=0, sticky="ew")
        browser_frame['padding'] = (50, 20, 10, 5)  # (left, top, right, bottom)

        input_label = tk.Label(browser_frame, text="Input folder:",
                               bg="#3B3E40", fg="white", font=("Bahnschrift", 12))
        input_label.grid(row=0, column=0, sticky=tk.E, pady=5, ipady=3)

        input_ = tk.StringVar()

        self.input_entry = tk.Entry(browser_frame, textvariable=input_, width=80, borderwidth=0, )  # show="*"
        self.input_entry.grid(row=0, column=1, columnspan=50, pady=10, ipady=5, padx=10)
        # entry.bind("<Return>", func=StartMenu.welcomeMessage)
        folder_btn = tk.Button(browser_frame, text='Open browser', borderwidth=0, command=self.open_folder)
        folder_btn.configure(width=15)
        folder_btn.grid(row=0, column=56, ipadx=0, ipady=3, padx=10, pady=5)

        # output
        output_label = tk.Label(browser_frame, text="Output folder:",
                                bg="#3B3E40", fg="white", font=("Bahnschrift", 12))
        output_label.grid(row=1, column=0, sticky=tk.E)
        output_ = str(self.input_entry.get()) + "_Results"

        self.output_field = tk.Entry(browser_frame, text=output_, width=80, borderwidth=0, )
        self.output_field.grid(row=1, column=1, columnspan=50, pady=10, ipady=5, padx=10)
        folder_btn2 = tk.Button(browser_frame, text='Change output', borderwidth=0,
                                command=self.change_output_folder)
        folder_btn2.configure(width=15)
        folder_btn2.grid(row=1, column=56, ipadx=0, ipady=3, padx=10, pady=5)

        ######################################################################################
        # define parameter
        ######################################################################################

        param_frame = ttk.Frame(self, width=int(self.winfo_screenwidth() / 1.8), height=20)
        param_frame.grid(row=1, sticky="ew")
        param_frame['padding'] = (50, 5, 10, 20)

        # entry frames per seconds
        param_label = tk.Label(param_frame, text="Please define\nparameter:",
                               bg="#3B3E40", fg="white", font=("Bahnschrift", 12))
        param_label.grid(row=0, column=0, sticky=tk.E, pady=5, ipady=3)

        row = 0
        fbs = tk.Label(param_frame, text="  Frames/seconds:", justify=tk.RIGHT, borderwidth=0,
                       bg="#3B3E40", fg="white", font=("Bahnschrift", 11))  # E = East
        fbs.grid(row=row, column=1, sticky=tk.E, pady=5, ipady=5, padx=10, ipadx=5)

        self.frames = Entry(param_frame, text="10.0", width=10, borderwidth=0,
                            font=("Bahnschrift", 11), justify=tk.CENTER)
        self.frames.grid(row=row, column=2, pady=10, ipady=5, padx=10)
        self.frames.insert(0, "29")
        self.frames.bind('<Return>', self.check_frames_per_sec)
        self.frames.bind('<Leave>', self.check_frames_per_sec)
        self.frames.bind('<Tab>', self.check_frames_per_sec)

        # take only every second image
        sec_img = tk.Label(param_frame, text="Skip images:", justify=tk.RIGHT, borderwidth=0,
                           bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        sec_img.grid(row=row, column=3, sticky=tk.E, pady=5, ipady=5, padx=10, ipadx=5)
        self.skip_images = tk.Entry(param_frame, text="0", width=10, borderwidth=0,
                                    font=("Bahnschrift", 11), justify=tk.CENTER)  # show="*"
        self.skip_images.grid(row=row, column=4, pady=10, ipady=5, padx=10)
        self.skip_images.insert(0, "0")
        self.skip_images.bind('<Return>', self.change_fbs)
        self.skip_images.bind('<Leave>', self.check_skip_images)
        self.skip_images.bind('<Tab>', self.change_fbs)
        self.skip_images.bind('<Double-1>', self.set_true)
        self.calc_skip_images = True

        # entry pixel size
        ps = tk.Label(param_frame, text="Pixel size (µm):", justify=tk.RIGHT, borderwidth=0,
                      bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        ps.grid(row=row + 1, column=1, sticky=tk.E, pady=5, ipady=5, padx=10, ipadx=5)
        self.pixel = tk.Entry(param_frame, text="1.3", width=10, borderwidth=0,
                              font=("Bahnschrift", 11), justify=tk.CENTER)  # show="*"
        self.pixel.grid(row=row + 1, column=2, pady=5, ipady=5, padx=10)
        self.pixel.insert(0, "0.2522")
        self.pixel.bind('<Return>', self.check_pixel_entry)
        self.pixel.bind('<Leave>', self.check_pixel_entry)
        self.pixel.bind('<Tab>', self.check_pixel_entry)

        # cut movie
        cut = tk.Label(param_frame, text="Cut movie (sec):", justify=tk.RIGHT, borderwidth=0,
                       bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        cut.grid(row=row + 1, column=3, sticky=tk.E, pady=5, ipady=5, padx=10, ipadx=5)
        self.cut_entry = tk.Entry(param_frame, text="20", width=10, borderwidth=0,
                                  font=("Bahnschrift", 11), justify=tk.CENTER)  # show="*"
        self.cut_entry.grid(row=row + 1, column=4, pady=5, ipady=5, padx=10)
        self.cut_entry.insert(0, "20.0")
        self.cut_entry.bind('<Return>', self.check_cut_entry)
        self.cut_entry.bind('<Leave>', self.check_cut_entry)
        self.cut_entry.bind('<Tab>', self.check_cut_entry)

        # file format
        format_label = tk.Label(param_frame, text="File format:", justify=tk.RIGHT, borderwidth=0,
                                bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        format_label.grid(row=row + 2, column=1, sticky=tk.E, pady=10, ipady=5, padx=10, ipadx=5)
        file_formats = [".avi", ".czi", ".mp4", ".png", ".tif", ".jpeg"]
        clicked = tk.StringVar(value=".avi")
        s.configure('my.TMenubutton', background="white", font=("Bahnschrift", 11))
        self.file_format = ttk.OptionMenu(param_frame, clicked, file_formats[0], *file_formats,
                                          style='my.TMenubutton', command=lambda x: self.write_file_format(x))
        self.file_format.config(width=5)
        self.file_format.grid(row=row + 2, column=2, sticky=tk.E, pady=10, padx=18, ipadx=5)

        # overwrite raw data: yes/no
        ow = tk.Label(param_frame, text="Overwrite data:", justify=tk.RIGHT, borderwidth=0,
                      bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        ow.grid(row=row + 2, column=3, sticky=tk.E, pady=10, ipady=5, padx=10, ipadx=5)
        self.check_arg = tk.StringVar()
        self.ow_check = ttk.Checkbutton(param_frame, text="", command=self.update_overwrite_state,
                                        variable=self.check_arg, onvalue=" --overwrite", offvalue="",
                                        style='my.TCheckbutton')
        self.ow_check.state(['!alternate'])
        self.ow_check.grid(row=row + 2, column=4, pady=10, ipady=0, padx=10, ipadx=0, sticky="w")

        # acquisition mode
        # Fluorescence (chamber-specific) or bright field (only heartbeat)
        acquisition_mode = tk.Label(param_frame, text="Acquisition mode:", justify=tk.RIGHT, borderwidth=0,
                                    bg="#3B3E40", fg="white", font=("Bahnschrift", 11))
        acquisition_mode.grid(row=row + 3, column=1, sticky=tk.E, pady=8, ipady=5, padx=10, ipadx=5)
        acquisition_modes = ["Fluorescence (chamber-specific)", "Bright field (only heartbeat)"]
        acquisition_clicked = tk.StringVar(value="Fluorescence (chamber-specific)")

        self.acquisition_mode = ttk.OptionMenu(param_frame, acquisition_clicked, acquisition_modes[0],
                                               *acquisition_modes,
                                               style='my.TMenubutton',
                                               command=lambda x: self.write_acquisition_mode(x))
        self.acquisition_mode.config(width=36)
        self.acquisition_mode.grid(row=row + 3, column=2, sticky=tk.E, pady=8, padx=18, ipadx=5, columnspan=4)

        # start | help |  exit bottoms in start_frame
        w = 18
        start_frame = ttk.Frame(self, width=int(self.winfo_screenwidth() / 1.8), height=20)
        start_frame.grid(row=3, sticky="ew")
        start_frame['padding'] = (150, 5, 10, 10)

        # start
        start_button = tk.Button(start_frame, text='Start',
                                 command=self.start_program,
                                 borderwidth=0, )
        start_button.configure(width=w, height=2)
        start_button.grid(row=1, column=2, padx=20, ipadx=4, ipady=2)

        # help
        help_button = tk.Button(start_frame, text='Help',
                                command=self.show_help,
                                borderwidth=0, )
        help_button.configure(width=w, height=2)
        help_button.grid(row=1, column=3, padx=20, ipadx=4, ipady=2)

        # exit
        exit_button = tk.Button(start_frame, text='Exit', command=self.exit_all, borderwidth=0, )
        exit_button.configure(width=w, height=2)
        exit_button.grid(row=1, column=4, padx=20, ipadx=4, ipady=2)

    def open_folder(self):
        messagebox.showinfo(title="Choose folder",
                            message="Please, choose one folder where all videos of fish hearts are stored!")
        folder = filedialog.askdirectory()
        print(folder)
        self.config_dict["input"] = folder
        folder_temp = folder.split("/")
        self.input_entry.delete(0, tk.END)
        self.output_field.delete(0, tk.END)
        if len(folder_temp) > 5:
            self.input_entry.insert(0, ".../" + "/".join(folder_temp[-5:]))
        else:
            self.input_entry.insert(0, folder)
        # if len(start_window.output_field.get()) == 0:

        self.output_field.insert(0, str(self.input_entry.get()) + "_Results")
        self.config_dict["output"] = folder + "_Results"

    def change_output_folder(self):
        messagebox.showinfo(title="Define output folder",
                            message="Please, create output folder manually and select output folder.")
        output_folder = filedialog.askdirectory()
        self.config_dict["output"] = output_folder
        folder_temp = output_folder.split("/")
        self.output_field.delete(0, tk.END)
        self.output_field.insert(0, ".../" + "/".join(folder_temp[-5:]))

    def write_file_format(self, format_):
        self.config_dict["file_format"] = format_

    def write_acquisition_mode(self, mode_):
        self.config_dict["acquisition_mode"] = mode_

    def update_overwrite_state(self):
        check = self.check_arg.get()
        self.config_dict["overwrite_data"] = str(check)
        # print(check)

    def check_frames_per_sec(self, event):
        try:
            float(self.frames.get())
            # self.calc_skip_images = True
            self.config_dict["frames_per_sec"] = self.frames.get()
        except ValueError:
            self.frames.delete(0, tk.END)
            self.frames.insert(0, "29")
            tk.messagebox.showinfo("Wrong entry type", "Please type only integer or float!")

    def change_fbs(self, event):
        try:
            num = int(self.skip_images.get())
            if num < 0 or num > 10:
                tk.messagebox.showinfo("Out of scope", "Values between 0 and 10 are allowed!")
                self.skip_images.delete(0, tk.END)
                self.skip_images.insert(0, "0")
            else:
                if self.calc_skip_images:
                    fps_temp = float(self.frames.get())
                    new_fps = fps_temp / (num + 1)
                    self.frames.delete(0, tk.END)
                    self.frames.insert(0, str(new_fps))
                    # self.config_dict["frames_per_sec"] = self.frames.get()
                    self.calc_skip_images = False
                self.config_dict["skip_images"] = int(self.skip_images.get())
        except ValueError:
            self.skip_images.delete(0, tk.END)
            self.skip_images.insert(0, "0")
            tk.messagebox.showinfo("Wrong entry type", "Please type only integer!")

    def set_true(self, event):
        self.calc_skip_images = True

    def check_skip_images(self, event):
        try:
            num = int(self.skip_images.get())
            if num < 0 or num > 10:
                tk.messagebox.showinfo("Out of scope", "Values between 0 and 10 are allowed!")
                self.skip_images.delete(0, tk.END)
                self.skip_images.insert(0, "0")
            else:
                self.config_dict["skip_images"] = int(self.skip_images.get())
        except ValueError:
            self.skip_images.delete(0, tk.END)
            self.skip_images.insert(0, "0")
            tk.messagebox.showinfo("Wrong entry type", "Please type only integer!")

    def check_pixel_entry(self, event):
        try:
            float(self.pixel.get())
            self.config_dict["pixel_size"] = self.pixel.get()
        except ValueError:
            self.pixel.delete(0, tk.END)
            self.pixel.insert(0, "0.2522")
            tk.messagebox.showinfo("Wrong entry type", "Please type only float!")

    def check_cut_entry(self, event):
        try:
            float(self.pixel.get())
            self.config_dict["cut_movie"] = self.cut_entry.get()
        except ValueError:
            self.cut_entry.delete(0, tk.END)
            self.cut_entry.insert(0, "20.0")
            tk.messagebox.showinfo("Wrong entry type", "Please type only float!")

    def start_program(self):

        # check whether format is correct
        format_correct = True
        if len(glob.glob(self.config_dict["input"] + "/*" + self.config_dict["file_format"])) == 0:
            file_example = glob.glob(self.config_dict["input"] + "/*.*")
            if len(file_example) == 0:
                format_correct = False
                if len(glob.glob(self.config_dict["input"] + "/*/*" + self.config_dict["file_format"])) == 0:
                    if len(glob.glob(self.config_dict["input"] + "/*/*.*")) == 0:
                        messagebox.showwarning("Folder Error",
                                               f"""In the case of images series, please move all images/
                                                   frames per fish into one subfolder and restart!""")
                    file_example = glob.glob(self.config_dict["input"] + "/*/*.*")[0]
                    messagebox.showwarning("File Format Error",
                                           f"""Please choose another file format! For example: {file_example}""")
            else:
                if ".avi" in file_example or ".czi" in file_example or ".mp4" in file_example:
                    format_correct = False
                    messagebox.showwarning("File Format Error",
                                           f"""Please choose another file format! For example: {file_example}""")
                elif ".png" in file_example or ".tif" in file_example or ".jpeg" in file_example:
                    format_correct = False
                    messagebox.showwarning("File Format Error",
                                           f"""Please move images into a subfolder (e.g., fish_01) and restart!
                                       """)

        if len(glob.glob(self.config_dict["input"] + "/*/*" + self.config_dict["file_format"])) > 0:
            format_correct = True

        if not format_correct:
            return

        print("\nStart processing\n")
        if not os.path.isdir(self.config_dict["output"]):
            os.mkdir(self.config_dict["output"])
        with open(self.config_dict["output"] + "/status.txt", "w") as file:
            file.write("run")
        self.config_dict["frames_per_sec"] = self.frames.get()
        self.config_dict["pixel_size"] = self.pixel.get()
        self.config_dict["cut_movie"] = self.cut_entry.get()
        self.config_dict["skip_images"] = int(self.skip_images.get())
        if not os.path.isdir(self.config_dict["output"]):
            os.mkdir(self.config_dict["output"])
        with open(self.config_dict["output"] + "/config_file.json", "w") as config_file:
            json.dump(self.config_dict, config_file)
        time.sleep(0.2)
        # start_window.destroy()
        # start_window.quit()
        # prepare threads
        t1 = Thread(target=self.run_program)
        t1.daemon = True
        # This turns the thread into a daemon, which automatically
        # shuts down the secondary thread when the main thread exits.
        t1.start()

    def exit_all(self):
        if os.path.isfile(self.config_dict["output"] + "/status.txt"):
            with open(self.config_dict["output"] + "/status.txt", "w") as file:
                file.write("stop all")
                if os.path.isfile(self.config_dict["output"] + "/config_file.json"):
                    os.remove(self.config_dict["output"] + "/config_file.json")
        sys.exit()

    def run_program(self):
        with open(self.config_dict["output"] + "/config_file.json") as config_file:
            configs = json.load(config_file)

        print(configs)
        frames_per_sec = configs["frames_per_sec"]
        pixel_size = configs["pixel_size"]  # Keyence 10x objective, 3x zoom: 0.2522 µm per pixel
        cut_movie_at = configs["cut_movie"]  # default 20 sec

        project_folder = configs["input"]
        project_name = project_folder.split("/")[-1]
        output_folder = configs["output"]
        file_format = configs["file_format"]
        acq_mode = configs["acquisition_mode"]  # default IF

        print("File_format", file_format)

        file_format_ = ""
        # videos
        if file_format == ".avi":
            file_format_ = ".avi"
            movies = sorted(glob.glob(fr"{project_folder}\*{file_format_}"))  # key=os.path.getmtime
        elif file_format == ".czi":
            file_format_ = ".czi"
            movies = sorted(glob.glob(fr"{project_folder}\*{file_format_}"))
        elif file_format == ".mp4":
            file_format_ = ".mp4"
            movies = sorted(glob.glob(fr"{project_folder}\*{file_format_}"))
        else:
            movies = sorted(glob.glob(fr"{project_folder}\*.*"))

        if file_format == ".png" or file_format == ".tif" or file_format == ".jpeg":
            movies = []
            for folder in os.listdir(project_folder):
                if "~" not in folder and "log" not in folder and os.path.isdir(project_folder + r"\\" + folder):
                    movies.append(project_folder + r"\\" + folder)

        num_movies = len(movies)
        print("Number of conditions to analyze: ", num_movies)

        # analyze every single fish by executing heart_beat_GUI_only_one_fish_multiprocessing.py
        for idx, movie_file in enumerate(movies):
            if os.path.isfile(output_folder + "/status.txt"):
                with open(output_folder + "/status.txt", "r") as file:
                    status = file.readline()
                    if "stop all" in status:
                        sys.exit()

            print(f"{idx + 1}/{num_movies}")
            image_counter = f"{idx + 1}/{num_movies}"
            condition_folder_name = movie_file.split("\\")[-1]
            condition_folder_name = condition_folder_name.replace(f"{file_format_}", "")
            if (os.path.isfile(output_folder + "\\" + condition_folder_name + fr"\{condition_folder_name}.csv")
                    and "overwrite" not in configs["overwrite_data"]):
                print(movie_file, "already analyzed")
                continue

            script = "fluorescence_heart_chambers.py"
            if acq_mode == "Fluorescence (chamber-specific)":
                # run fluorescent script
                script = "fluorescence_heart_chambers.py"
            elif acq_mode == "Bright field (only heartbeat)":
                # run bright field script
                script = "bright_field_whole_fish.py"
            else:
                print("An unexpected error occurred!")

            query = f'{script} "{movie_file}" ' \
                    f'--output "{output_folder}" ' \
                    f'--name "{project_name}" ' \
                    f'--pixel_size {pixel_size} ' \
                    f'--cut_movie_at {cut_movie_at} ' \
                    f'--frames_per_sec {frames_per_sec} ' \
                    f'--image_counter {image_counter} ' \
                    f'{configs["overwrite_data"]} ' \
                    f'--skip_images {configs["skip_images"]} ' \
                    f'--file_format {file_format}'

            abspath = os.path.abspath(__file__)
            os.chdir(os.path.dirname(abspath))
            print(os.getcwd())
            if not os.path.isfile(os.getcwd() + fr"\{script}"):
                python_path = r"C:\Users\*\AppData\Local\Programs\Python\Python*\Lib\site-packages"
                alt = python_path + rf"\pyHeart4Fish_python\{script}"
                query = glob.glob(alt)[0] + query.replace(f"{script}", "")
            os.system(f"python {query}")  # send query to command console
            print(query)

        if os.path.isfile("config_file.json"):
            os.remove("config_file.json")

        if os.path.isfile(output_folder + "/status.txt"):
            os.remove(output_folder + "/status.txt")
        # combine excel sheets
        # also executable using combine_excel_sheets.py
        combine_excel = True
        if combine_excel:
            print("\nWrite excel")
            out2 = pd.concat([pd.read_csv(file) for file in glob.glob(output_folder + rf"\*\*.csv")])
            out2.sort_values("Condition", inplace=True)
            out2.to_excel(output_folder + rf"\{project_name}_Final_results.xlsx", index=False)

            root2 = tk.Tk()
            root2.lift()
            root2.attributes('-topmost', True)
            root2.after_idle(root2.attributes, '-topmost', False)
            root2.withdraw()
            answer = messagebox.askyesno("Analysis finished", "Do you want to open the excel sheet?")
            if answer:
                os.startfile(output_folder + rf"\{project_name}_Final_results.xlsx")
            root2.destroy()
            root2.mainloop()
        print("\nProgram finished")

    @staticmethod
    def show_help():
        # open help window
        tk.messagebox.showinfo("Help desk",
                               "Please ask Tobias Reinberger (tobias.reinberger@uni-luebeck.de "
                               "for help! Documentation is under construction!")
        return


if __name__ == '__main__':
    """

    * define input folder, output folder and other configs in this GUI main window
    * by clicking >Start< the script heart_beat_GUI_MAIN.py is executed

    * PIXEL SIZE INFO
    * 65 pixel = 100 µm --> 10x magnification = 65 pixel = 10 µm
      for 8x ist die Pixelgröße: 1.703 µm
      168px = 525µm für 6.3x  = 3.125 µm pro pixel

    """

    print(datetime.datetime.now())
    timestamp = datetime.datetime.now()
    date_str = str(timestamp).split(" ")[0].replace("-", "_")

    start_window = StartConfigs()
    start_window.mainloop()
    # print(config_dict)
