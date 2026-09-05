from graphviz import Digraph

# Create a directed graph
dot = Digraph(format='png')

# Global graph styling
dot.attr(rankdir='TB', size='10,15')
dot.attr('node', shape='box', style='filled,rounded', fontname='Helvetica', fontsize='14')

# Define nodes with colors and labels
dot.node('A', 'Data Collection\n\n• Academic Records\n• LMS Data\n• Demographics',
         fillcolor='#A7C7E7')  # light blue

dot.node('B', 'Data Preprocessing\n\n• Cleaning\n• Handling Missing Values\n• Normalization',
         fillcolor='#B5EAD7')  # mint green

dot.node('C', 'Feature Selection\n\n• Important Features\n• Remove Irrelevant Data\n• Dimensionality Reduction',
         fillcolor='#FFF5BA')  # light yellow

dot.node('D', 'ANN Training\n\n• Forward Propagation\n• Backpropagation\n• Weight Updates',
         fillcolor='#FFDAC1')  # peach

dot.node('E', 'Model Evaluation\n\n• Accuracy\n• Precision\n• Recall\n• F1 Score',
         fillcolor='#E2F0CB')  # light green

dot.node('F', 'Performance Prediction\n\n• Final Output\n• Pass/Fail or Grades\n• Insights for Teachers',
         fillcolor='#D5AAFF')  # light purple

# Add edges (arrows)
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('E', 'F')

# Render the diagram
dot.render('student_performance_workflow', view=True)