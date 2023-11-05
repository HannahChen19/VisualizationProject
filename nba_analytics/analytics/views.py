# views.py
import re
import numpy as np
import pandas as pd
import spacy
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from fuzzywuzzy import fuzz
from autoviz import AutoViz_Class
#from autoviz.AutoViz_Class import AutoViz_Class

def generate_chart(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        print("QUERY: ", query)

        plt.style.use('default')
        
        #df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')

        try:
            df = pd.read_csv('https://drive.google.com/uc?export=download&id=1UaF5oTjgTcB4C1m4ehQqHkmWHYTGKeN0')
        except Exception as e:
            print(f"Error loading CSV: {e}")
            # Handle the error gracefully, e.g., return an error message to the user

        # Basic NLP processing with spaCy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(query)

        # Define a mapping between common names and actual column names
        column_mapping = {
            'name': 'name',
            'games_played': 'gp',
            'minutes_per_game': 'min',
            'average_points_per_game': 'pts',
            'field_goals_made_per_game': 'fgm',
            'field_goal_attempts_per_game': 'fga',
            'field_goal_percentage': 'fg',
            '3-point_field_goals_made_per_game': '3p_made',
            '3-point_attempts_per_game': '3pa',
            '3-point_percentage': '3p',
            'free_throws_made per game': 'ftm',
            'free_throw_attempts per game': 'fta',
            'free_throw_percentage': 'ft',
            'offensive_rebounds_per game': 'oreb',
            'defensive_rebounds_per game': 'dreb',
            'total_rebounds_per_game': 'reb',
            'assists_per_game': 'ast',
            'steals_per_game': 'stl',
            'blocks_per_game': 'blk',
            'turnovers_per_game': 'tov',
            'career_duration': 'target_5yrs'
        }

        # Initialize lists for selected columns and filter conditions
        selected_columns = []
        filter_conditions = []

        # Initialize variables for sorting and chart type
        sort_column = None
        sum_column = None
        avg_column = None

        sum_result = 0
        avg_result = 0.0

        chart_type = 'bar'  # Default chart type

        # Convert the doc to a list of tokens for iteration
        tokens = list(doc)

        group_by_column = None  # Initialize group_by_column to None

        # Iterate through the tokens in the user's query
        for i, token in enumerate(tokens):
            token_text = token.text.lower()
            best_match = None
            best_score = 0

            # Check for the best fuzzy match between the token and keywords
            for keyword, column_name in column_mapping.items():
                score = fuzz.token_set_ratio(token_text, keyword)  # Use token_set_ratio for improved matching
                if score > best_score:
                    best_score = score
                    best_match = keyword

            # Check for specific commands in the user's query
            #commands = ['sort by', 'sum of', 'average of', 'group by', 'greater than', 'less than']
            commands = [
                'sort by', 'sum of',  
                'ascending order', 'descending order', 
                'average of', 'compare', 'greater_than', 
                'less_than', 'equals', 'not_equals', 
                'and', 'or', 'between', 'using bar chart', 
                'using pie chart', 'using line chart'
            ]

            if "sort by" in query:
                for i, token in enumerate(tokens):
                    token_text = token.text.lower()
                    if token_text == 'by' and i > 0 and tokens[i - 1].text == 'sort':
                        if i + 1 < len(tokens):
                            next_token = tokens[i + 1]
                            #column_name = column_mapping.get(next_token.text.lower(), None)
                            column_name = column_mapping.get(best_match, None)
                            if column_name:
                                sort_column = column_name  
                                break 
                            else:
                                i += 1 
                            
                if sort_column:
                    if "descending order" in query:
                        df = df.sort_values(by=sort_column, ascending=False)
                    else:
                        df = df.sort_values(by=sort_column, ascending=True)
                else:
                    print("No valid 'sort by' found in the query.")


            if "sum of" in query:
                for i, token in enumerate(tokens):
                    token_text = token.text.lower()
                    if token_text == 'of' and i > 0 and tokens[i - 1].text == 'sum':
                        if i + 1 < len(tokens):
                            next_token = tokens[i + 1]
                            #column_name = column_mapping.get(next_token.text.lower(), None)
                            column_name = column_mapping.get(best_match, None)
                            if column_name:
                                sum_column = column_name 
                                break  
                            else:
                                i += 1  
                if sum_column:
                    sum_result = df[column_name].sum()

            if "average of" in query:
                for i, token in enumerate(tokens):
                    token_text = token.text.lower()
                    if token_text == 'of' and i > 0 and tokens[i - 1].text == 'average':
                        if i + 1 < len(tokens):
                            next_token = tokens[i + 1]
                            #column_name = column_mapping.get(next_token.text.lower(), None)
                            column_name = column_mapping.get(best_match, None)
                            if column_name:
                                avg_column = column_name 
                                break  
                            else:
                                i += 1  
                if avg_column:
                    avg_result = df[column_name].mean()

            if "compare" in query:
                if "where" not in query:
                    tokens = query.split()  # Assuming query is a string
                    compare_index = tokens.index("compare")
                    compared_columns = None

                    if compare_index > 0 and compare_index < len(tokens) - 1:
                        column_before_compare = tokens[compare_index - 1]
                        column_after_compare = tokens[compare_index + 1]

                        column_before_compare = column_mapping.get(column_before_compare, None)
                        column_after_compare = column_mapping.get(column_after_compare, None)   

                        # Check if the compared columns are valid
                        compared_columns = [column_before_compare, column_after_compare]
                        df_filtered_columns = df[[column_before_compare, column_after_compare]]
                        print("BEFORE: ", column_before_compare)
                        print("AFTER: ", column_after_compare)
                        
                if "where" in query:
                    tokens = query.split()  # Assuming query is a string
                    compare_index = tokens.index("compare")
                    compared_columns = None

                    if compare_index > 0 and compare_index < len(tokens) - 1:
                        column_before_compare = tokens[compare_index - 1]
                        column_after_compare = tokens[compare_index + 1]

                        column_before_compare = column_mapping.get(column_before_compare, None)
                        column_after_compare = column_mapping.get(column_after_compare, None)   

                        # Check if the compared columns are valid
                        compared_columns = [column_before_compare, column_after_compare]
                        df_filtered_columns = df[[column_before_compare, column_after_compare]]
                        print("BEFORE: ", column_before_compare)
                        print("AFTER: ", column_after_compare)

                        # loop through all tokens starting after 'where' keyword
                        where_index = tokens.index("where")

                        #if "and" not in query:
                            #if "or" not in query:
                        if "greater_than" in query:
                            greater_than = tokens.index("greater_than")
                            if greater_than > 0 and greater_than < len(tokens) - 1:
                                greater_than_column = tokens[greater_than - 1]
                                greater_than_value = tokens[greater_than + 1]

                                greater_than_column = column_mapping.get(greater_than_column, None)
                                # Convert to int64
                                greater_than_value = np.int64(greater_than_value)
                                #greater_than_value = column_mapping.get(greater_than_value, None)

                                #df_filtered_columns = df_filtered_columns[df_filtered_columns[greater_than_column] > greater_than_value]
                                print("HEREEEE COLUMN: ", greater_than_column)
                                print("HEREEEE VALUE: ", greater_than_value)
                                df_filtered_columns = df_filtered_columns[df_filtered_columns[greater_than_column] > greater_than_value]
                                print("HEREEE: ", df_filtered_columns)
                        elif "less_than" in query:
                            less_than = tokens.index("less_than")
                            if less_than > 0 and less_than < len(tokens) - 1:
                                less_than_column = tokens[less_than - 1]
                                less_than_value = tokens[less_than + 1]

                                less_than_column = column_mapping.get(less_than_column, None)
                                #less_than_value = column_mapping.get(less_than_value, None)
                                less_than_value = np.int64(less_than_value)

                                df_filtered_columns = df_filtered_columns[df_filtered_columns[less_than_column] < less_than_value]
                        elif "equals" in query:
                            equals = tokens.index("equals")
                            if equals > 0 and equals < len(tokens) - 1:
                                equals_column = tokens[equals - 1]
                                equals_value = tokens[equals + 1]

                                equals_column = column_mapping.get(equals_column, None)
                                #equals_value = column_mapping.get(equals_value, None)
                                equals_value = np.int64(equals_value)

                                df_filtered_columns = df_filtered_columns[df_filtered_columns[equals_column] == equals_value]
                        elif "not_equals" in query:
                            not_equals = tokens.index("not_equals")
                            if not_equals > 0 and not_equals < len(tokens) - 1:
                                not_equals_column = tokens[not_equals - 1]
                                not_equals_value = tokens[not_equals + 1]

                                not_equals_column = column_mapping.get(not_equals_column, None)
                                #not_equals_value = column_mapping.get(not_equals_value, None)
                                not_equals_value = np.int64(not_equals_value)

                                df_filtered_columns = df_filtered_columns[df_filtered_columns[not_equals_column] != not_equals_value]
                        elif "between" in query:
                            between = tokens.index("between")
                            if between > 0 and between < len(tokens) - 1:
                                between_column = tokens[between - 1]
                                between_value1 = tokens[between + 1]
                                between_value2 = tokens[between + 3]

                                between_column = column_mapping.get(between_column, None)
                                #between_value1 = column_mapping.get(between_value1, None)
                                #between_value2 = column_mapping.get(between_value2, None)
                                between_value1 = np.int64(between_value1)
                                between_value2 = np.int64(between_value2)

                                df_filtered_columns = df_filtered_columns[df_filtered_columns[between_column] > between_value1]
                                df_filtered_columns = df_filtered_columns[df_filtered_columns[between_column] < between_value2]
                            
                            #for k in range(where_index + 1, len(tokens)):
                            
                            

                
                print("COMPARED COLUMNS: ", compared_columns)
                print("DF Filtered Columns: ", df_filtered_columns)

                # Create a bar chart if compared_columns is not None
                if compared_columns:
                    # AutoViz can handle creating visualizations automatically
                    
                    x_axis_label = df_filtered_columns.columns[0]  # Assuming the first column is the x-axis
                    y_axis_label = df_filtered_columns.columns[1]  # Assuming the second column is the y-axis

                    AV = AutoViz_Class()

                    df_viz = AV.AutoViz(
                        filename="",
                        sep=",",
                        depVar="",
                        dfte=df_filtered_columns,   #df,
                        header=0,
                        verbose=0,
                        lowess=False,
                        chart_format="svg",
                    )

                    # Adjust the figure size using matplotlib functions
                    fig = plt.gcf()
                    fig.set_size_inches(18, 6)  # Set the figure size to 8x6 inches
                    title = query
                    plt.title(title)
                    plt.xlabel(x_axis_label)
                    plt.ylabel(y_axis_label)
                    # You can also save the generated visualization
                    #plt.savefig('visualization.png', format='png')

                    # Save the chart as BytesIO and encode it to base64
                    buffer = BytesIO()
                    #df_viz.savefig(buffer, format='png')
                    chart_data = base64.b64encode(buffer.getvalue()).decode()
                    print("ÄUTOVIZ CHART: ", chart_data)
                else:
                    # If no compared columns are specified, generate an HTML table
                    table_html = df.to_html(classes="table table-striped", index=False)

                #print("DF VIZ: ", df_viz)
                

        # Check for specific chart type specifications
        if 'using pie chart' in query:
            chart_type = 'pie'
        elif 'using line chart' in query:
            chart_type = 'line'

        # Create a bar chart if a valid group_by_column is specified or no group_by_column
        if(selected_columns):
            plt.figure()
            if chart_type == 'bar':
                if group_by_column is not None:
                    if selected_columns:
                        plt.bar(df[group_by_column], df[selected_columns[0]])
                        plt.xlabel(group_by_column)
                        plt.ylabel(selected_columns[0])
                    plt.title('Generated Chart')
                else:
                    # Handle the case when there is no valid group_by_column
                    print("INFO: No valid group_by_column specified.")

            elif chart_type == 'pie':
                # Generate a pie chart here
                pass
            elif chart_type == 'line':
                # Generate a line chart here
                pass
        else:
            # If no columns are selected for the chart, generate an HTML table
            table_html = df.to_html(classes='table table-striped', index=False)


        # Filter data based on specified conditions
        for condition in filter_conditions:
            df = df.query(condition)

        # Save the chart to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        chart_data = base64.b64encode(buffer.getvalue()).decode()
        #print("CHART DATA: ", chart_data)
        #print("TABLE HTML: ", table_html)
        print("SORT COLUMN: ", best_match)
        print("TOKEN TEXT: ", token_text)
        
        '''
        if(selected_columns):
            return render(request, 'combined.html', {'chart_data': chart_data})
        else:
            return render(request, 'combined.html', {'table_html': table_html})'
        '''

        print("SUM RESULT: ", sum_result)
        if "sort by" in query:
            return render(request, 'combined.html', {'table_html': table_html})
        elif "sum of" in query:
            return render(request, 'combined.html', {'sum_result': sum_result})
        elif "average of" in query:
            return render(request, 'combined.html', {'avg_result': avg_result})
        else:
            return render(request, 'combined.html', {'chart_data': chart_data})

    return render(request, 'combined.html')
