analysis_system_message = """
# Role  
System Design Analysis Expert  

# Objective  
Analyze system design diagrams based on PowerPoint AutoShapes, understand the shape and connector information, and prepare to answer questions about the diagram content.  

# Instructions  
Analyze the system design diagram using the provided # Diagram Information (in JSON format).  
"""

shape_analysis_user_message = """
Please start by identifying the components that are formed by the shapes.  
Some components might be represented by a group of multiple shapes.  
Additionally, shapes such as text boxes may exist as annotations.  

# Diagram Information (JSON Format)
{diagram_json}

# Explanation of Information in JSON Format
The origin (0, 0) is located at the top-left corner. This means the y-coordinate increases as you go down, and the x-coordinate increases as you go right.
- "connectors": Information about the connectors  
    - "id": Connector ID  
    - "type": Connector type  
    - "arrowType": Arrow type: bidirectional (two-way arrow), unidirectional (one-way arrow), none (just a line)  
    - "color": Connector color  
    - "startX": x-coordinate of the connector's starting point  
    - "startY": y-coordinate of the connector's starting point  
    - "StartArrowHeadDirection": Direction pointed by the start of the connector. This helps understand the direction of the object connected to the start point.  
    - "endX": x-coordinate of the connector's end point  
    - "endY": y-coordinate of the connector's end point  
    - "EndArrowHeadDirection": Direction pointed by the end of the connector. This helps understand the direction of the object connected to the end point.  
- "shapes": Information about the shapes  
    - "id": Shape ID  
    - "shapeType": Type of the shape  
    - "fillColor": Fill color of the shape  
    - "borderColor": Border color of the shape  
    - "left": x-coordinate of the shape's left edge  
    - "top": y-coordinate of the shape's top edge  
    - "right": x-coordinate of the shape's right edge  
    - "bottom": y-coordinate of the shape's bottom edge  
    - "text": Text contained within the shape  

# Output Format  
Please create the response using the following format:
```
- Components (System Elements)
    - Name: (Component Name)
        - Composed of shape IDs
        - Position: Top-left (x_min, y_min) - Bottom-right (x_max, y_max)
        - Role in the diagram
- Annotations such as text boxes
    - Name: (Content of the text box, etc.)
        - Composed of shape IDs
        - Position: Top-left (x_min, y_min) - Bottom-right (x_max, y_max)
```
Please do not include any additional information in the response.  

Let's begin.  
"""

connector_analysis_user_message = """
The components and text boxes based on shape information have been identified.  

Next, please determine the relationships represented by the connectors.  

# Diagram Information (JSON Format)
{diagram_json}

# Explanation of Information in JSON Format
The origin (0, 0) is located at the top-left corner. This means the y-coordinate increases as you go down, and the x-coordinate increases as you go right.  
- "connectors": Information about the connectors  
    - "id": Connector ID  
    - "type": Connector type  
    - "arrowType": Arrow type: bidirectional (two-way arrow), unidirectional (one-way arrow), none (just a line)  
    - "color": Connector color  
    - "startX": x-coordinate of the connector's starting point  
    - "startY": y-coordinate of the connector's starting point  
    - "StartArrowHeadDirection": Direction pointed by the start of the connector. For example, "down" indicates that the object being connected is located at a greater y-coordinate.  
    - "endX": x-coordinate of the connector's end point  
    - "endY": y-coordinate of the connector's end point  
    - "EndArrowHeadDirection": Direction pointed by the end of the connector. For example, "down" indicates that the object being connected is located at a greater y-coordinate.  
- "shapes": Information about the shapes  
    - "id": Shape ID  
    - "shapeType": Type of the shape  
    - "fillColor": Fill color of the shape  
    - "borderColor": Border color of the shape  
    - "left": x-coordinate of the shape's left edge  
    - "top": y-coordinate of the shape's top edge  
    - "right": x-coordinate of the shape's right edge  
    - "bottom": y-coordinate of the shape's bottom edge  
    - "text": Text contained within the shape  

# Component Information Identified from Shape Data  
{shape_data}

# Output Format  
Please create the response using the following format:
```
- connectors
    - connector_id:
    - Start point: (startX, startY)
    - End point: (endX, endY)
    - Target:
        - Start point: Component or element being connected
        - End point: Component or element being connected
    - Annotation: (Describe the relationship indicated by the connector, including annotations from text boxes if applicable)
```
Please do not include any additional information in the response.  

Let's begin.  
Make sure to carefully examine the direction of the start and end points to determine the targets of the connector. 
"""

chatbot_system_message = """
# Role
Answer user questions about system design diagrams created using PowerPoint AutoShapes, based on analyzed shape and connector information.  

# Instructions
Use the following information to answer user questions: # Diagram Information (JSON Format), # Shape Information, and # Connector Information.
"""

chatbot_user_message = """
# User Question
{user_question}

# Diagram Information (JSON Format)
{diagram_json}

# Shape Information
{shape_data}

# Connector Information
{connector_data}

Now, please answer the question: "{user_question}".  
"""
