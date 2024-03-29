import plotly.express as px
import palmerpenguins
import pandas as pd
import seaborn as sns  # Add this line
from shiny import reactive, render
from shiny.express import input, ui
from shinywidgets import render_plotly

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Set page options
ui.page_opts(title="Jose Guzman's Penguin Data", fillable=True)

# Define reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list()) &
                       penguins_df["island"].isin(input.penguin_islands())]

# Sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Menu")
    ui.a("GitHub", href="https://github.com/jg2012/cintel-03-reactive/tree/main", target="_blank")
    ui.input_selectize("selected_attribute", "Select Attribute", 
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", 20)
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 100, 20)
    ui.hr()
    ui.input_checkbox_group("selected_species_list", "Select Species", 
                            ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie"], inline=False)
    ui.input_checkbox_group("penguin_islands", "Islands", ["Torgersen", "Biscoe", "Dream"],
                            selected=["Dream"], inline=False)

# Data Tables
with ui.nav_panel("Tables"):
    with ui.layout_columns():
        with ui.card(width=6):  # Adjust the width of the cards as needed
            ui.card_header("Palmer Penguins Data Table")
            @render.data_frame
            def render_penguins_table():
                return filtered_data()
        with ui.card(width=6):  # Adjust the width of the cards as needed
            ui.card_header("Palmer Penguins Data Grid")
            @render.data_frame
            def penguins_data():
                return render.DataGrid(penguins_df, row_selection_mode="multiple") 

# Plots
with ui.nav_panel("Scatterplot"):
    with ui.layout_columns():
        with ui.card():
            ui.card_header("Plotly Scatterplot: Species")
            @render_plotly
            def plotly_scatterplot():
                return px.scatter(filtered_data(),
                                   x="bill_length_mm",
                                   y="body_mass_g",
                                   color="species",
                                   title="Penguins Plot",
                                   labels={"bill_length_mm": "Bill Length (mm)",
                                           "body_mass_g": "Body Mass (g)"})

# Histograms
with ui.nav_panel("Histograms"):
    with ui.layout_columns():
        with ui.card():
            ui.card_header("Plotly Histogram")
            @render_plotly
            def plotly_histogram():
                return px.histogram(filtered_data(), x=input.selected_attribute(), nbins=input.plotly_bin_count())
        with ui.card(full_screen=True):
            ui.card_header("Seaborn Histogram")
            @render.plot(alt="Seaborn Histogram")
            def seaborn_histogram():
                histplot = sns.histplot(filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count())
                histplot.set_title("Palmer Penguins")
                histplot.set_xlabel("Mass")
                histplot.set_ylabel("Count")
                return histplot
