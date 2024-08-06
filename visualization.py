# src/visualization.py

from bokeh.plotting import figure, show
from bokeh.io import output_notebook

class Visualizer:
    def plot_data(self, training_data, test_data, ideal_functions, mapped_data):
        output_notebook()
        p = figure(title="Data Visualization", x_axis_label='X', y_axis_label='Y')

        # Plot training data
        p.line(training_data['X'], training_data['Y1'], legend_label="Training Data Y1", line_width=2, color='blue')
        p.line(training_data['X'], training_data['Y2'], legend_label="Training Data Y2", line_width=2, color='green')
        p.line(training_data['X'], training_data['Y3'], legend_label="Training Data Y3", line_width=2, color='red')
        p.line(training_data['X'], training_data['Y4'], legend_label="Training Data Y4", line_width=2, color='orange')

        # Plot test data
        p.scatter(test_data['X'], test_data['Y'], legend_label="Test Data", size=8, color='black')

        # Plot ideal functions
        for col in ideal_functions.columns[1:]:
            p.line(ideal_functions['X'], ideal_functions[col], legend_label=f"Ideal {col}", line_width=1, line_dash='dashed', alpha=0.3)

        # Plot mapped data
        for col in mapped_data['Ideal_Function'].unique():
            mapped_subset = mapped_data[mapped_data['Ideal_Function'] == col]
            p.scatter(mapped_subset['X'], mapped_subset['Y'], legend_label=f"Mapped {col}", size=6, alpha=0.6)

        show(p)
