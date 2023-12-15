import csv
import json

# Define your CSV headers if they are not included in the CSV file, otherwise, this can be omitted
csv_headers = ['id', 'type', 'url', 'x', 'y', 'width', 'height', 'fromNode', 'fromSide', 'toNode', 'toSide']

# Read the CSV file
with open('data.csv', mode='r', encoding='utf-8') as csv_file:
    # If your CSV doesn't have headers, include them using fieldnames parameter
    csv_reader = csv.DictReader(csv_file, fieldnames=csv_headers if not csv.Sniffer().has_header(csv_file.read(1024)) else None)
    # Reset file pointer after Sniffer
    csv_file.seek(0)
    
    # Skip the header if CSV Sniffer detected headers
    if csv.Sniffer().has_header(csv_file.read(1024)):
        next(csv_reader)
    # Reset file pointer again after reading the header
    csv_file.seek(0)

    # Prepare the data structure
    canvas_data = {
        "nodes": [],
        "edges": []
    }

    # Process the CSV rows
    for row in csv_reader:
        # Create a node
        if row['type'] == 'link':
            node = {
                "id": row["id"],
                "type": row["type"],
                "url": row["url"],
                "x": int(row["x"]),
                "y": int(row["y"]),
                "width": int(row["width"]),
                "height": int(row["height"])
            }
            canvas_data["nodes"].append(node)
        # Create an edge
        elif 'fromNode' in row and 'toNode' in row:
            edge = {
                "id": row["id"],
                "fromNode": row["fromNode"],
                "fromSide": row["fromSide"],
                "toNode": row["toNode"],
                "toSide": row["toSide"]
            }
            canvas_data["edges"].append(edge)

# Write the .canvas file
with open('data.canvas', mode='w', encoding='utf-8') as canvas_file:
    json.dump(canvas_data, canvas_file, ensure_ascii=False, indent=4)
