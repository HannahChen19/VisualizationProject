# views.py
import pandas as pd
import plotly.express as px
import traceback
from django.shortcuts import render, get_object_or_404

def generate_chart(request, query=None):
    try:
        title = ""  # Default title
        x_label = ""  # Default x_label
        y_label = ""  # Default y_label

        if not query:
            # Handle the case where the query is missing
            plot_div_vertical = ''
            plot_div_horizontal = ''
            title = "No Query Provided"
        else:
            # Load the NBA player data from the CSV file
            df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')

            # Split the query to identify the chart type and selected columns
            query_parts = query.split()
            chart_type = query_parts[0]  # The first word in the query determines the chart type

            # Check if SELECT is in the query and get the selected columns
            selected_columns = None
            if "SELECT" in query_parts:
                select_index = query_parts.index("SELECT")
                selected_columns = query_parts[select_index + 1:]
                # If there are commas in the selected columns, split them
                selected_columns = [col.strip(',') for col in selected_columns]

            # Initialize vertical_fig and horizontal_fig to None
            vertical_fig = None
            horizontal_fig = None

            if chart_type == 'career_duration':
                # Customize the chart for career duration
                if selected_columns:
                    # Create an interactive bar chart based on selected columns
                    vertical_fig = px.bar(
                        data_frame=df,
                        x=selected_columns,
                        title="Career Duration Distribution (Vertical)",
                    )

                    horizontal_fig = px.bar(
                        data_frame=df,
                        y=selected_columns,
                        title="Career Duration Distribution (Horizontal)",
                    )
                    title = f"Career Duration Distribution for {', '.join(selected_columns)}"
                    x_label = "Career Duration"
                    y_label = "Number of Players"

            # Add other chart types and customizations for 'player_performance' and 'shooting_performance' as per your needs

            if vertical_fig and horizontal_fig:
                # Customize the charts further as needed
                # ...

                # Ensure labels remain visible when zoomed out
                vertical_fig.update_xaxes(tickmode='auto', automargin=True)
                horizontal_fig.update_xaxes(tickmode='auto', automargin=True)

                # Set the width and height to be equal for both charts
                width = 1000  # Adjust the width as needed
                height = 600  # Adjust the height as needed
                vertical_fig.update_layout(width=width, height=height)
                horizontal_fig.update_layout(width=width, height=height)

                # Add annotations for storytelling
                # ...

                plot_div_vertical = vertical_fig.to_html()
                plot_div_horizontal = horizontal_fig.to_html()
            else:
                # Handle the case where the chart type is not assigned
                plot_div_vertical = ''
                plot_div_horizontal = ''

        return render(request, 'default.html', {
            'plot_div': plot_div_vertical,
            'plot_div_horizontal': plot_div_horizontal,
            'chart_title': title,
            'x_label': x_label,
            'y_label': y_label,
        })

    except Exception as e:
        traceback.print_exc()  # Print the traceback for debugging
        return render(request, 'error.html', {'error_message': str(e)})
