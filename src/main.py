"""
This is the research project to DVM for Hoover, William
The purpose and goal of this project is to scrape the data from
arXiv api for all research papers related to the field of AI: Artificial Intelligence
over the course of a 10-year period, to track the growth of the field and to see
if research has been speeding up or slowing down
"""


# imports
import pandas as pd
from src.arXiv_Api_Access import scrape_arxiv
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib import widgets
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Toplevel, Button, filedialog


def update_data():
   #update ai_research_data.xlsx with updated data
   scrape_arxiv()



# Variables and options usable throughout the program
df = pd.read_csv('data/ai_research_data.csv')
pivot_data = df.groupby(['Year', 'Query']).size().reset_index(name='Count')
pivot_data = pivot_data.pivot(index='Year', columns='Query', values='Count').fillna(0)
total_sum = pivot_data.sum()
sns.set_palette('pastel')


def create_menu(window, figure):
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Pass both window and figure to the save function
    file_menu.add_command(label="Save", command=lambda: save(window, figure))


def save(parent_window, figure):
    # Create a new Toplevel window
    save_window = tk.Toplevel(parent_window)

    # Make it modal by setting it as transient to the parent window
    save_window.transient(parent_window)

    # Set the title for the dialog window
    save_window.title("Save As")

    # Create a label to prompt the user
    tk.Label(save_window, text="Choose a location to save the file:").pack()

    # Create a button to open the "Save As" file dialog
    tk.Button(save_window, text="Save", command=lambda: save_file(figure, save_window)).pack()

    # Run the main loop for the dialog window
    save_window.mainloop()


def save_file(figure, save_window):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        figure.savefig(file_path)
    save_window.destroy()


def main_window():
    root = tk.Tk()
    root.title("AI Research Analysis")

    tk.Button(root, text="Update Data", command=update_data).pack()
    tk.Button(root, text="Show Bar Graph", command=show_bar_graph).pack()
    tk.Button(root, text="Show Stacked Area Plot", command=show_stacked_area_plot).pack()
    tk.Button(root, text="Show Heat Map", command=show_heat_graph).pack()
    tk.Button(root, text="Exit", command=root.quit).pack()

    root.mainloop()

def show_bar_graph():
    fig = Figure(figsize=[15, 10])
    ax = fig.add_subplot(111)
    bar_data = pivot_data.reset_index().melt(id_vars='Year')
    sns.barplot(data=bar_data, x='Year', y='value', hue='Query', ax=ax)
    ax.set_title('Number of Papers Published per Year for Different AI Fields')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Papers')
    ax.legend(title='Subject', loc='upper left')

    new_window = Toplevel()
    new_window.title("Bar Graph")

    # create save menu
    create_menu(new_window, fig)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    new_window.mainloop()
    pass

def show_stacked_area_plot():
    fig = Figure(figsize=[15, 10])
    ax = fig.add_subplot(111)

    # Plot the stacked area chart
    ax.stackplot(pivot_data.index, pivot_data.T, labels=pivot_data.columns, alpha=0.6)
    ax.set_title('Number of Papers Published per Year for Different AI Fields')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Papers')
    ax.legend(title='Subject', loc='upper left')

    new_window = Toplevel()
    new_window.title("Stacked Area Plot")

    #create save menu
    create_menu(new_window, fig)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    new_window.mainloop()

    pass

def show_heat_graph():
    fig = Figure(figsize=[20, 10])
    ax = fig.add_subplot(111)

    sorted_columns = pivot_data.sum().sort_values(ascending=False).index
    pivot_data_sorted = pivot_data[sorted_columns]
    pivot_data_sorted_transposed = pivot_data_sorted.T
    sns.heatmap(pivot_data_sorted_transposed, cmap='RdBu_r', annot=True, linewidths=.5, ax=ax)

    ax.set_title('Heatmap of Papers Published per Year for Different AI Fields')
    ax.set_xlabel('Year')
    ax.set_ylabel('Subject')

    new_window = Toplevel()
    new_window.title("Heat Map")
    # create save menu
    create_menu(new_window, fig)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    new_window.mainloop()


    pass

if __name__ == "__main__":
    main_window()