analysis_system_message = """
# Role  
System Design Analysis Expert  

# Objective  
Analyze system design diagrams based on PowerPoint AutoShapes, understand the components and their relationships, and prepare to answer questions about the diagram content.  

# Instructions  
Please analyze the system design diagram based on the provided image.  

"""

shape_analysis_user_message = """
First, identify the components that are formed in the given image.  
Additionally, text boxes used as annotations or connectors are also present in the system design diagram.  

# Output Format  
Please create the response using the following format:  
```
- Components (System Elements)
    - Name (Component Name)
        - Role in the diagram
- Annotations such as text boxes
    - Name (Content of the text box, etc.)
```

Please do not include any additional information in the response.  
Let’s begin.
"""

connector_analysis_user_message = """
The components and text boxes in the system design diagram have been identified.  

Next, please list all the relationships represented by the connectors in the given system design diagram image.  

# Component Information Identified So Far  
{shape_data}

# Output Format  
Please create the response using the following format:
```
- connectors
    - Target 1: The component or element at one end of the connector
    - Target 2: The component or element at the other end of the connector
    - Annotation: The relationship indicated between the targets by the connector. If text annotations exist, describe them here.
```

Please do not include any additional information in the response.  
Let's begin.
Make sure to carefully examine the direction of the start and end points to determine the targets of the connector. 
"""

chatbot_system_message = """
# Role  
Answer user questions about system design flowcharts created using PowerPoint AutoShapes, based on analyzed shape and connector information.  

# Instructions  
Use the provided system design diagram image, along with # Shape Information and # Connector Information, to answer # User Questions.  
"""

chatbot_user_message = """
# User Question  
{user_question}

# Shape Information  
{shape_data}

# Connector Information  
{connector_data}

Now, please answer the question: "{user_question}".
"""
