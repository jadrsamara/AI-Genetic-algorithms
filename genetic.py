import threading
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import csv
import random
from typing import List
from multiprocessing import Pool

num_of_groups = 36
num_of_projects = 38 + 1
fitness_type = 0
population_size = 10
generation_type = 0

file_name_1 = ''  # 'Students+selections.csv'
file_name_2 = ''  # 'Graduation+projects.csv'

un_wanted_list = []
new_wanted_list = []

ideal_list_1 = []
ideal_list_2 = []
ideal_list_3 = []

projects_list_1 = []
projects_list_2 = []

Genome = List[int]
Population = List[Genome]

exit_event = threading.Event()

then = time.time()


def update_generation(choice: str):
    switcher = {
        "Random": 0,
        "Random -Diff.": 1,
        "GPA": 2
    }
    global generation_type, new_wanted_list
    generation_type = switcher.get(choice)
    if generation_type == 0:
        new_wanted_list = sorted(random.sample(list(range(1, num_of_projects)), k=num_of_groups))


def random_genome(values: int, length: int) -> Genome:
    global new_wanted_list
    switcher = {
        0: random.sample(list(range(1, values)), length),
        1: random.sample(new_wanted_list, length),
    }
    return switcher.get(generation_type)


def random_population(size: int, values: int, length: int) -> Population:
    return [random_genome(values, length) for _ in range(size)]


def fitness(genome_under_testing: Genome) -> [int, int, list]:
    switcher = {
        0: fitness_0(genome_under_testing),
        1: fitness_1(genome_under_testing),
        2: fitness_2(genome_under_testing)
    }
    return switcher.get(fitness_type)


def update_fitness(choice: str):
    switcher = {
        "Satisfied groups favorable": 0,
        "First choice favorable": 1,
        "Not Ranked": 2
    }
    global fitness_type
    fitness_type = switcher.get(choice)


def fitness_0(genome_under_testing: Genome) -> [int, int, list]:
    score = 0
    score2 = 0
    counter = 0
    s_1 = 0
    s_2 = 0
    s_3 = 0
    for gene in genome_under_testing:
        if int(gene) == int(ideal_list_1[counter]):
            score += 100
            s_1 += 1
        elif int(gene) == int(ideal_list_2[counter]):
            score += 10
            s_2 += 1
        elif int(gene) == int(ideal_list_3[counter]):
            score += 1
            s_3 += 1
        else:
            # number of unmatched choices
            score2 += 1
        # number of groups
        counter += 1

    result = (counter - score2) * 1000 + score

    return result, counter - score2, [s_1, s_2, s_3]


def fitness_1(genome_under_testing: Genome) -> [int, int, list]:
    score = 0
    score2 = 0
    counter = 0
    s_1 = 0
    s_2 = 0
    s_3 = 0
    for gene in genome_under_testing:
        if int(gene) == int(ideal_list_1[counter]):
            score += 1000
            s_1 += 1
        elif int(gene) == int(ideal_list_2[counter]):
            score += 10
            s_2 += 1
        elif int(gene) == int(ideal_list_3[counter]):
            score += 1
            s_3 += 1
        else:
            # number of unmatched choices
            score2 += 1
        # number of groups
        counter += 1

    result = (counter - score2) * 100 + score

    return result, counter - score2, [s_1, s_2, s_3]


def fitness_2(genome_under_testing: Genome) -> [int, int, list]:
    score2 = 0
    counter = 0
    s_1 = 0
    s_2 = 0
    s_3 = 0
    for gene in genome_under_testing:
        if int(gene) == int(ideal_list_1[counter]):
            s_1 += 1
        elif int(gene) == int(ideal_list_2[counter]):
            s_2 += 1
        elif int(gene) == int(ideal_list_3[counter]):
            s_3 += 1
        else:
            # number of unmatched choices
            score2 += 1
        # number of groups
        counter += 1

    result = (counter - score2)

    return result, counter - score2, [s_1, s_2, s_3]


def pair_selector(population: Population) -> Population:
    p = random.sample(range(0, len(population) // 2), 2)
    return [population[p[0]], population[p[1]]]


def crossover(parent_1: Genome, parent_2: Genome) -> [Genome, Genome]:
    cross_point_list = random.choices(list(range(1, len(parent_1))))
    cross_point = cross_point_list[0]

    res_1 = parent_1[0:cross_point]
    res_2 = parent_2[0:cross_point]

    # print(new_wanted_list)

    for i in parent_2[cross_point:]:
        if i not in res_1:
            res_1.append(i)
        else:
            for e in new_wanted_list:
                if e not in res_1:
                    res_1.append(e)
                    break

    for i in parent_1[cross_point:]:
        if i not in res_2:
            res_2.append(i)
        else:
            for e in new_wanted_list:
                if e not in res_2:
                    res_2.append(e)
                    break

    return res_1, res_2


def mutation(genome_to_be_mutated: Genome) -> Genome:
    mute_points = random.choices(list(range(1, len(genome_to_be_mutated))), k=2)
    temp = genome_to_be_mutated[mute_points[0]]
    genome_to_be_mutated[mute_points[0]] = genome_to_be_mutated[mute_points[1]]
    genome_to_be_mutated[mute_points[1]] = temp
    return genome_to_be_mutated


def open_data_file():
    global file_name_1
    file_name_1 = filedialog.askopenfilename(initialdir='/',
                                             title='Select .CSV Data File',
                                             filetypes=(('Data', '*.csv'), ("all files", '*.*')))
    file_label_text['text'] = file_name_1
    frame.update_idletasks()

    open_files()


def open_data_file_2():
    global file_name_2
    file_name_2 = filedialog.askopenfilename(initialdir='/',
                                             title='Select .CSV Data File',
                                             filetypes=(('Data', '*.csv'), ("all files", '*.*')))
    file_2_label_text['text'] = file_name_2
    frame.update_idletasks()

    try:
        file_ = open(file_name_2)
        csv_reader = csv.reader(file_)

        global projects_list_1, projects_list_2
        projects_list_1 = []
        projects_list_2 = []

        for row in csv_reader:
            projects_list_1.append(row[1])
            projects_list_2.append(row[2])

    except OSError:
        print("Could not open/read file:", file_name_2)


def open_files():
    try:
        file_ = open(file_name_1)
        csv_reader = csv.reader(file_)

        header = next(csv_reader)

        global ideal_list_1, ideal_list_2, ideal_list_3, un_wanted_list
        ideal_list_1 = []
        ideal_list_2 = []
        ideal_list_3 = []
        un_wanted_list = []

        for row in csv_reader:
            ideal_list_1.append(int(row[1]))
            ideal_list_2.append(int(row[2]))
            ideal_list_3.append(int(row[3]))

    except OSError:
        print("Could not open/read file:", file_name_1)

    counter = 0
    for i in range(1, num_of_groups):
        if counter >= num_of_projects - (num_of_groups + 1):
            break
        if i in ideal_list_1:
            continue
        if i in ideal_list_2:
            continue
        if i in ideal_list_3:
            continue
        un_wanted_list.append(i)
        counter += 1

    global new_wanted_list
    new_wanted_list = list(range(1, num_of_projects))
    for i in un_wanted_list:
        new_wanted_list.pop(new_wanted_list.index(i))


def start_evolution(
        population_generation_limit: int,
        fitness_limit: int,
        name
) -> [Population, int]:
    global file_name_1
    file_name_1 = name
    open_files()
    population = random_population(population_size, num_of_projects, num_of_groups)
    counter = 0
    i = 0
    for i in range(population_generation_limit):

        counter += 1

        population = sorted(
            population,
            key=lambda genome: fitness(genome),
            reverse=True
        )

        best_pair_fitness = fitness(population[0])

        if best_pair_fitness[1] >= fitness_limit:
            break

        next_generation = [population[0], population[1]]

        for j in range(int(len(population) / 2) - 1):
            # population is already sorted based on fitness
            parent_1, parent_2 = pair_selector(population)
            child_1, child_2 = crossover(parent_1, parent_2)
            child_1 = mutation(child_1)
            child_2 = mutation(child_2)
            next_generation += [child_1, child_2]

        population = next_generation

    # sort based on fitness before return
    population = sorted(
        population,
        key=lambda genome: fitness(genome),
        reverse=True
    )

    return population, i


def check():
    if CheckVar.get() == 1:
        scale["state"] = "disabled"
        scale["fg"] = "gray"
        scale["bg"] = "light gray"
        frame.update_idletasks()
    else:
        scale["state"] = "normal"
        scale["fg"] = "black"
        scale["bg"] = "#f2f2f2"
        frame.update_idletasks()


def stop():
    exit_event.set()


def start():
    if CheckVar.get() == 1:
        iterations = 1000000
    else:
        iterations = scale.get()

    # clear thread exit event
    exit_event.clear()

    # creating thread
    t1 = threading.Thread(target=threaded_start, args=(iterations, scale_2.get(), scale_3.get()))
    t1.daemon = True

    # starting thread 1
    t1.start()


def threaded_start(iterations: int, generations: int, threshold: int):
    if file_name_1 == '':
        open_data_file()

    if file_name_1 == '':
        return 0

    global then
    then = time.time()  # Time before the operations start

    global population_size
    population_size = scale_5.get()

    start["state"] = "disabled"
    start["bg"] = "gray"
    frame.update_idletasks()

    # populations list
    populations = []

    progress_bar['value'] = 0
    progress_bar_label_2['text'] = 0, '%'
    frame.update_idletasks()

    Solution_text_area.delete('1.0', END)
    Process_text_area.delete('1.0', END)

    temp_ = []
    b_fitness = [0, 0]
    for i in range(iterations):

        if exit_event.is_set():
            break

        # temp = start_evolution(generations, threshold)
        # populations += temp[0]

        ar = []
        for k in range(scale_6.get()):
            ar += [[generations, threshold, file_name_1]]

        with Pool() as pool:
            L = pool.starmap(start_evolution, ar)

        for j in range(scale_6.get()):
            temp = L[j]

            populations += temp[0]

            progress_bar['value'] = ((i + 1) / iterations * 100)
            progress_bar_label_2['text'] = int((i + 1) / iterations * 100), '%'

            c_fitness = fitness(temp[0][0])

            if c_fitness[1] >= scale_4.get():
                Process_text_area.insert(tk.END, str(temp[0][0]) + ' -> ' + str(c_fitness[0])
                                         + ':' + str(fitness(temp[0][0])[1:]) + '\n')
                Process_text_area.see(tk.END)

            if c_fitness[0] > b_fitness[0]:
                b_fitness = c_fitness
                temp_ = temp[0][0]

            now = time.time()  # Time after it finished

            Solution_text_area.delete('1.0', END)
            Solution_text_area.insert(tk.END, str(temp_) + ' -> ' + str(b_fitness[0])
                                      + ':' + str(fitness(temp_)[1:]) + '\n'
                                      + 'Number of iterations: ' + str(i + 1) + '*' + str(scale_6.get()) + ', time: '
                                      + str(round(now - then, 2)) + ' seconds.')

            frame.update_idletasks()

        if b_fitness[1] >= threshold:
            break

    populations = sorted(
        populations,
        key=lambda genome: fitness(genome),
        reverse=True
    )

    # if file 2 is entered
    if len(file_name_2) > 0:
        res_on_process(populations[0])

    start["state"] = "normal"
    start["bg"] = "green"
    frame.update_idletasks()


def res_on_process(solution: Population):
    Process_text_area.delete('1.0', END)

    fit = fitness(solution)
    Process_text_area.insert(tk.END, 'Number of satisfied groups: ' + str(fit[1]) + '\nwith ' + str(fit[2][0])
                             + ' groups getting their first selection, ' + str(
        fit[2][1]) + ' getting their second selection, and ' + str(fit[2][2]) + ' getting their last selection.\n')

    j = 0
    for element in solution:
        j += 1
        Process_text_area.insert(tk.END, 'Group ' + str("{:02d}".format(j)) + ': ' + projects_list_1[int(element) - 1] +
                                 '; ' + projects_list_2[int(element) - 1] + '\n')


if __name__ == '__main__':

    # Root
    root = tk.Tk()
    root.title("Graduation Projects Distribution")

    # Canvas
    canvas = tk.Canvas(root, height=700, width=1200, bg='#222222')
    canvas.pack()

    # Frame
    frame = tk.Frame(root, bg='#f2f2f2')
    frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

    # Files input
    file_label = Label(frame, text="File name:").place(x=160, y=23)
    file_label_text = Label(frame, text="Not yet imported.")
    file_label_text.place(x=220, y=23)
    file = Button(frame, relief='flat', text='import data', fg='white', bg='#e60000', command=open_data_file
                  ).place(x=42, y=20)

    file_2_label = Label(frame, text="File name:").place(x=160, y=53)
    file_2_label_text = Label(frame, text="Not yet imported.")
    file_2_label_text.place(x=220, y=53)
    file_2 = Button(frame, relief='flat', text='import projects', fg='white', bg='#ffa31a', command=open_data_file_2
                    ).place(x=42, y=50)

    # Stop
    stop = Button(frame, relief='flat', text='Stop', fg='white', bg='#e60000', command=stop).place(x=1005, y=20)

    # Settings
    scale_label = Label(frame, text="Iterations:").place(x=42, y=110)
    scale = Scale(frame, relief='flat', orient='horizontal', from_=10, to=1000, length=240, resolution=10, width=10)
    scale.set(50)
    scale.place(x=102, y=93)

    # infinite iterations
    CheckVar = IntVar()
    C1 = Checkbutton(frame, text="Infinite", variable=CheckVar, onvalue=1, offvalue=0, height=2, width=5, command=check)
    C1.place(x=350, y=101)

    # num of generations per iteration
    scale_label_2 = Label(frame, text="Generations:").place(x=470, y=110)
    scale_2 = Scale(frame, relief='flat', orient='horizontal', from_=100, to=10000, length=200, resolution=100, width=10)
    scale_2.set(2000)
    scale_2.place(x=550, y=93)

    # fitness stop value
    scale_label_3 = Label(frame, text="Fitness Stop value:").place(x=820, y=110)
    scale_3 = Scale(frame, orient='horizontal', from_=0, to=num_of_groups, length=100, resolution=1, width=10)
    scale_3.set(29)
    scale_3.place(x=935, y=93)

    # show what solutions based on fitness score
    scale_label_4 = Label(frame, text="Show by fitness:").place(x=840, y=155)
    scale_4 = Scale(frame, orient='horizontal', from_=1, to=num_of_groups, length=100, resolution=1, width=10)
    scale_4.set(1)
    scale_4.place(x=934, y=140)

    # fitness function selection
    variable = StringVar(root)
    # variable.set("Satisfied groups favourable")  # default value
    drop_down = ttk.OptionMenu(root, variable, "Satisfied groups favorable", "Satisfied groups favorable",
                               "First choice favorable", "Not Ranked",
                               command=update_fitness)
    drop_down.configure(width=25)
    drop_down.place(x=630, y=190)

    # population size
    scale_label_5 = Label(frame, text="Population Size:").place(x=210, y=155)
    scale_5 = Scale(frame, relief='flat', orient='horizontal', from_=10, to=1000, length=100, resolution=10, width=10)
    scale_5.set(10)
    scale_5.place(x=310, y=140)

    # num of processes
    scale_label_6 = Label(frame, text="Num of\nProcesses:").place(x=850, y=25)
    scale_6 = Scale(frame, relief='flat', orient='vertical', from_=1, to=16, length=50, resolution=1, width=10)
    scale_6.set(10)
    scale_6.place(x=800, y=20)

    # start generation type
    variable_2 = StringVar(root)
    # variable.set("Satisfied groups favourable")  # default value
    drop_down_2 = ttk.OptionMenu(root, variable_2, "Random", "Random",
                                 "Random -Diff.",  # "GPA",
                                 command=update_generation)
    drop_down_2.configure(width=10)
    drop_down_2.place(x=525, y=190)

    # Process
    Process = Label(frame, text="Progress:").place(x=40, y=160)
    Process_text_area = Text(frame, font=('Consolas', 8), relief='flat', height=21, width=165)
    Process_text_area.place(x=42, y=185)

    # Solution
    Solution = Label(frame, text="Solution:").place(x=40, y=485)
    Solution_text_area = Text(frame, font=('Consolas', 8), relief='flat', height=2, width=165)
    Solution_text_area.place(x=42, y=510)

    # Progress Bar
    progress_bar = ttk.Progressbar(frame, orient='horizontal', length=930, mode='determinate', maximum=100, value=0)
    progress_bar.place(x=70, y=570)
    progress_bar_label_1 = Label(frame, text="Progress:").place(x=10, y=570)
    progress_bar_label_2 = Label(frame, text="0%")
    progress_bar_label_2.place(x=1010, y=570)

    # Start
    start = tk.Button(frame, relief='flat', text='Start', fg='white', bg='green', command=start)
    start.pack(side=tk.BOTTOM, fill='x')

    root.mainloop()
