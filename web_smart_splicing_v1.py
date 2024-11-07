import re
import plotly.graph_objects as go
import streamlit as st
from shapely.geometry import Polygon, Point
from io import StringIO

# Function to parse all sections from the .CUT file
def parse_all_sections(raw_lines):
    
    lines = raw_lines

    shapes_by_section = {}
    current_shape = []
    current_section = None

    for line in lines:
        line = line.strip()

        # Check if the line corresponds to an N command
        n_match = re.match(r'N(\d+)\*', line)
        if n_match:
            if current_section is not None and current_shape:
                shapes_by_section.setdefault(current_section, []).append(current_shape)
                current_shape = []
            current_section = int(n_match.group(1))
            continue  # Skip the N line itself

        # Look for X and Y coordinates in lines
        match = re.match(r'X(-?\d+)Y(-?\d+)', line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            current_shape.append((x, y))

        # Handle other end of section conditions
        elif line.startswith('N') and '*' in line and current_section is not None:
            if current_shape:
                shapes_by_section.setdefault(current_section, []).append(current_shape)
                current_shape = []

    # Append the last shape if any
    if current_section is not None and current_shape:
        shapes_by_section.setdefault(current_section, []).append(current_shape)

    return shapes_by_section

# Function to create Plotly figure from parsed shapes


def plot_all_sections_original(raw_lines):
    # Parse the shapes from the .CUT file
    shapes_by_section = parse_all_sections(raw_lines)

    # Initialize plotly figure
    fig = go.Figure()
    points_to_consider = []
    # Define global bounds for axis
    global_min_x, global_max_x, global_min_y, global_max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
    # Loop through all sections and plot the shapes
    for section, shapes in shapes_by_section.items():
        for shape in shapes:
            if shape:
                x_data, y_data = zip(*shape)

                # Create a polygon from the shape points
                polygon = Polygon(shape)

                

                # Define fill color based on intersection
                fill_color = 'orange'

                # Plot the shape with the determined fill color
                fig.add_trace(go.Scatter(
                    x=x_data, y=y_data, mode='lines+markers', 
                    fill='toself',
                    marker=dict(color=fill_color, size=3),
                    line=dict(color=fill_color, width=2),
                    name=f'Section {section}'
                ))



                # Update global coordinates for bounding box
                global_min_x = min(global_min_x, *x_data)
                global_max_x = max(global_max_x, *x_data)
                global_min_y = min(global_min_y, *y_data)
                global_max_y = max(global_max_y, *y_data)


    # Set axis limits
    fig.update_layout(
        xaxis=dict(range=[global_min_x - 10, global_max_x + 10],
                   showticklabels=False,   # Hide X-axis tick labels
                   zeroline=False,         # Hide X-axis zero line
                   showgrid=False),
        yaxis=dict(range=[global_min_y - 10, global_max_y + 10], 
                   showticklabels=False,   # Hide Y-axis tick labels
                   zeroline=False,         # Hide Y-axis zero line
                   showgrid=False),        # Optionally, hide grid lines as well
        title="Cut File Visalization",
        xaxis_title=f"{global_max_x/100} cm",
        yaxis_title=f"{global_max_y/100} cm",
        autosize=True,
        template="plotly_white",
        dragmode='zoom',  # Enable zooming by dragging
        showlegend=False,
        hovermode='closest',
    )

    return fig

def plot_all_sections_smart_splicing(raw_lines, defect):
    # Parse the shapes from the .CUT file
    shapes_by_section = parse_all_sections(raw_lines)

    # Initialize plotly figure
    fig = go.Figure()
    points_to_consider = []
    # Define global bounds for axis
    global_min_x, global_max_x, global_min_y, global_max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
    vertical_line_x = int(defect)
    # Loop through all sections and plot the shapes
    for section, shapes in shapes_by_section.items():
        for shape in shapes:
            if shape:
                x_data, y_data = zip(*shape)

                # Create a polygon from the shape points
                polygon = Polygon(shape)

                # Check for intersection by testing multiple points along x = 5000 within the shape's bounding box
                intersects = False
                min_y, max_y = min(y_data), max(y_data)
                for y in range(min_y, max_y + 1, 10):  # Step by 10 for faster processing
                    point = Point(vertical_line_x, y)
                    if polygon.contains(point):
                        intersects = True
                        points_to_consider.append(x_data)
                        break

                # Define fill color based on intersection
                fill_color = 'red' if intersects else 'orange'

                # Plot the shape with the determined fill color
                fig.add_trace(go.Scatter(
                    x=x_data, y=y_data, mode='lines+markers', 
                    fill='toself',
                    marker=dict(color=fill_color, size=3),
                    line=dict(color=fill_color, width=2),
                    name=f'Section {section}'
                ))

                fig.add_shape(
                    type="line",
                    x0=vertical_line_x, y0=global_min_y,  # Start at the bottom of the plot (global_min_y)
                    x1=vertical_line_x, y1=global_max_y,  # End at the top of the plot (global_max_y)
                    line=dict(color="red", width=2, dash="dash"),  # Line style (blue, dashed)
                    name="Vertical Line at x=5000"
)

                # Update global coordinates for bounding box
                global_min_x = min(global_min_x, *x_data)
                global_max_x = max(global_max_x, *x_data)
                global_min_y = min(global_min_y, *y_data)
                global_max_y = max(global_max_y, *y_data)

    min_value = min([min(t) for t in points_to_consider])
    max_value = max([max(t) for t in points_to_consider])

    fig.add_shape(type="line",
                x0=min_value, y0=global_min_y,  # Start at the bottom of the plot (global_min_y)
                x1=min_value, y1=global_max_y,  # End at the top of the plot (global_max_y)
                line=dict(color="green", width=2, dash="solid"),  # Line style (blue, dashed)
                name="Vertical Line at x=5000")



    fig.add_shape(type="line",
                x0=max_value, y0=global_min_y,  # Start at the bottom of the plot (global_min_y)
                x1=max_value, y1=global_max_y,  # End at the top of the plot (global_max_y)
                line=dict(color="green", width=2, dash="solid"),  # Line style (blue, dashed)
                name="Vertical Line at x=5000")

    # Set axis limits
    fig.update_layout(
        xaxis=dict(range=[global_min_x - 10, global_max_x + 10],
                   showticklabels=False,   # Hide X-axis tick labels
                   zeroline=False,         # Hide X-axis zero line
                   showgrid=False),
        yaxis=dict(range=[global_min_y - 10, global_max_y + 10], 
                   showticklabels=False,   # Hide Y-axis tick labels
                   zeroline=False,         # Hide Y-axis zero line
                   showgrid=False),        # Optionally, hide grid lines as well
        title="Smart Splicing",
        xaxis_title=f"{global_max_x/100} cm",
        yaxis_title=f"{global_max_y/100} cm",
        autosize=True,
        template="plotly_white",
        dragmode='zoom',  # Enable zooming by dragging
        showlegend=False,
        hovermode='closest',
    )
    

    

    return fig, min_value, max_value

def process_string(data):
    # Replace asterisks and spaces with newlines
    processed_data = data.replace("*", "*\n").replace(" ", "\n")
    
    # Split into lines and remove empty lines and lines with only one symbol like "*"
    lines = processed_data.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != "" and line.strip() != "*"]
    
    # Join the non-empty lines back together
    processed_data = "\n".join(non_empty_lines)
    return processed_data





# Streamlit app interface
def main():
    st.title('**Cutting Room Management**')
    st.title('MR sistemas')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()
        
        processed_string = process_string(string_data)
        global lines1
        raw_lines = processed_string.split("\n")


        

    # Let the user specify the file path manually
    #file_path = st.text_input("Enter the file path for the .CUT file:", "test.cut")
    
    
    if raw_lines:
        try:
            # Plot and display the combined shapes in Plotly
            fig = plot_all_sections_original(raw_lines)
            st.plotly_chart(fig, use_container_width=True, key="plot")

            Smart_Splicing = st.checkbox("Smart Splicing")

            if Smart_Splicing:
                defect = int(st.text_input("Defect location (cm)", 100))*100
                fig2, min_value, max_value = plot_all_sections_smart_splicing(raw_lines, defect)
                
                # Display the plot with a unique key
                
                st.plotly_chart(fig2, use_container_width=True, key="plot2")
                st.markdown(f"Overlapping #1: **{min_value/100} cm**")
                st.markdown(f"Overlapping #2: **{max_value/100} cm**")

        except Exception as e:
            st.error(f"Error loading or plotting the file: {e}")


if __name__ == "__main__":
    main()
