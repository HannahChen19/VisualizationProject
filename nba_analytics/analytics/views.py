# Create your views here.
# analytics/views.py
import pandas as pd
import plotly.express as px
import traceback

from django.shortcuts import render, get_object_or_404

def default_view(request):
    try:
        # Load the NBA player data from the CSV file
        df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')

        # Clean and process the data
        career_lengths = df['target_5yrs']

        # Create an interactive bar chart using Plotly (Vertical)
        vertical_fig = px.bar(
            x=["Career Duration >= 5 years", "Career Duration < 5 years"],
            y=[career_lengths.sum(), len(career_lengths) - career_lengths.sum()],
            title="Player Career Duration Distribution (Vertical)",
            labels={"x": "Career Duration", "y": "Number of Players"}
        )

        # Create a horizontal bar chart
        horizontal_fig = px.bar(
            y=["Career Duration >= 5 years", "Career Duration < 5 years"],
            x=[career_lengths.sum(), len(career_lengths) - career_lengths.sum()],
            title="Player Career Duration Distribution (Horizontal)",
            labels={"x": "Number of Players", "y": "Career Duration"},
        )

        # Ensure labels remain visible when zoomed out
        vertical_fig.update_xaxes(tickmode='auto', automargin=True)
        horizontal_fig.update_xaxes(tickmode='auto', automargin=True)

        # Set the width and height to be equal for both charts
        width = 1000  # Adjust the width as needed
        height = 600  # Adjust the height as needed
        vertical_fig.update_layout(width=width, height=height)
        horizontal_fig.update_layout(width=width, height=height)

        # Add annotations for storytelling
        vertical_fig.add_annotation(
            text="Data shows that majority of players stay for more than 5 years.",
            x=0.5, y=50, showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )
        horizontal_fig.add_annotation(
            text="Data shows that majority of players stay for more than 5 years.",
            x=50, y=0.5, showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )

        plot_div_vertical = vertical_fig.to_html()
        plot_div_horizontal = horizontal_fig.to_html()

        return render(request, 'default.html', {
            'plot_div': plot_div_vertical,
            'plot_div_horizontal': plot_div_horizontal,
        })
    
    except Exception as e:
        traceback.print_exc()  # Print the traceback for debugging
        return render(request, 'error.html', {'error_message': str(e)})

def player_performance_view(request):
    try:
        # Load the NBA player data from the CSV file
        df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')

        # Create an interactive bar chart using Plotly (Vertical)
        vertical_fig = px.bar(
            x=['Average Games Played', 'Average Minutes Per Game', 'Average Points Per Game'],
            y=[df['gp'].mean(), df['min'].mean(), df['pts'].mean()],
            title='Player Performance Analysis (Vertical)',
            labels={'x': 'Performance Metric', 'y': 'Average Value'}
        )

        # Create a horizontal bar chart
        horizontal_fig = px.bar(
            y=['Average Games Played', 'Average Minutes Per Game', 'Average Points Per Game'],
            x=[df['gp'].mean(), df['min'].mean(), df['pts'].mean()],
            title='Player Performance Analysis (Horizontal)',
            labels={'x': 'Average Value', 'y': 'Performance Metric'},
        )

        # Ensure labels remain visible when zoomed out
        vertical_fig.update_xaxes(tickmode='auto', automargin=True)
        horizontal_fig.update_xaxes(tickmode='auto', automargin=True)

        # Set the width and height to be equal for both charts
        width = 1000  # Adjust the width as needed
        height = 600  # Adjust the height as needed
        vertical_fig.update_layout(width=width, height=height)
        horizontal_fig.update_layout(width=width, height=height)

        # Add annotations for storytelling (vertical)
        vertical_fig.add_annotation(
            text="Average Number of Games Played: " + str(round(df['gp'].mean(), 2)) + "<br>" + "Average Number of Minutes Played (Min): " + str(round(df['min'].mean(), 2)) + "<br>" + "Average Number of Points Scored (Pts): " + str(round(df['pts'].mean(), 2)),
            x=2, y=40, showarrow=False,
            font=dict(size=14, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )

        # Add annotations for storytelling (horizontal)
        horizontal_fig.add_annotation(
            text="Average Number of Games Played: " + str(round(df['gp'].mean(), 2)) + "<br>" + "Average Number of Minutes Played (Min): " + str(round(df['min'].mean(), 2)) + "<br>" + "Average Number of Points Scored (Pts): " + str(round(df['pts'].mean(), 2)),
            x=40, y=2, showarrow=False,
            font=dict(size=14, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )

        plot_div_vertical = vertical_fig.to_html()
        plot_div_horizontal = horizontal_fig.to_html()

        return render(request, 'player_performance.html', {
            'plot_div': plot_div_vertical,
            'plot_div_horizontal': plot_div_horizontal,
        })
    
    except Exception as e:
        traceback.print_exc()  # Print the traceback for debugging
        return render(request, 'error.html', {'error_message': str(e)})
    
def shooting_performance_view(request):
    try:
        # Load the NBA player data from the CSV file
        df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')

        # Create a grouped bar chart for shooting performance metrics
        shooting_metrics = ['Average Field Goals Made (FGM)', 'Average Field Goal Attempts (FGA)', 'Average Field Goal Percentage (FG%)']
        vertical_fig = px.bar(
            x=shooting_metrics,
            y=[df['fgm'].mean(), df['fga'].mean(), df['fg'].mean()],  # Multiply by 100 to get a percentage
            title='Shooting Performance Analysis (Vertical)',
            labels={'x': 'Performance Metric', 'y': 'Average Value'},
            text=[round(df['fgm'].mean(), 2), round(df['fga'].mean(), 2), str(round(df['fg'].mean(), 2)) + '%'],
            height=600,  # Adjust the height as needed
        )

        horizontal_fig = px.bar(
            y=shooting_metrics,
            x=[df['fgm'].mean(), df['fga'].mean(), df['fg'].mean()],  # Multiply by 100 to get a percentage
            title='Shooting Performance Analysis (Horizontal)',
            labels={'x': 'Average Value', 'y': 'Performance Metric'},
            text=[round(df['fgm'].mean(), 2), round(df['fga'].mean(), 2), str(round(df['fg'].mean(), 2)) + '%'],
            height=600,  # Adjust the height as needed
        )

        # Ensure labels remain visible when zoomed out
        vertical_fig.update_xaxes(tickmode='auto', automargin=True)
        horizontal_fig.update_xaxes(tickmode='auto', automargin=True)

        # Set the width and height to be equal for both charts
        width = 1000  # Adjust the width as needed
        height = 600  # Adjust the height as needed
        vertical_fig.update_layout(width=width, height=height)
        horizontal_fig.update_layout(width=width, height=height)

        # Add annotations for storytelling (vertical)
        vertical_fig.add_annotation(
            text="Shooting Performance Analysis:<br>" +
                 "Average Field Goals Made (FGM): " + str(round(df['fgm'].mean(), 2)) + "<br>" +
                 "Average Field Goal Attempts (FGA): " + str(round(df['fga'].mean(), 2)) + "<br>" +
                 "Average Field Goal Percentage (FG%): " + str(round(df['fg'].mean(), 2)) + "%",
            x=1, y=25, showarrow=False,
            font=dict(size=14, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )

        # Add annotations for storytelling (horizontal)
        horizontal_fig.add_annotation(
            text="Shooting Performance Analysis:<br>" +
                 "Average Field Goals Made (FGM): " + str(round(df['fgm'].mean(), 2)) + "<br>" +
                 "Average Field Goal Attempts (FGA): " + str(round(df['fga'].mean(), 2)) + "<br>" +
                 "Average Field Goal Percentage (FG%): " + str(round(df['fg'].mean(), 2)) + "%",
            x=25, y=1, showarrow=False,
            font=dict(size=14, color='black'),
            bgcolor='rgba(255, 255, 255, 0.6)',
            bordercolor='black',
            borderwidth=1,
        )

        plot_div_vertical = vertical_fig.to_html()
        plot_div_horizontal = horizontal_fig.to_html()

        return render(request, 'shooting_performance.html', {
            'plot_div': plot_div_vertical,
            'plot_div_horizontal': plot_div_horizontal,
        })
    
    except Exception as e:
        traceback.print_exc()  # Print the traceback for debugging
        return render(request, 'error.html', {'error_message': str(e)})




