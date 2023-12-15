import json
import csv
from datetime import datetime

NODE_SIZE = (50, 50)  # Adjust as needed

def parse_canvas(canvas_file):
    with open(canvas_file, 'r') as file:
        return json.load(file)

def find_free_space(existing_nodes, new_node_size):
    # Implementation of finding free space on the canvas
    rightmost_x = max((node['x'] + node['width'] for node in existing_nodes), default=0)
    return (rightmost_x + 10, 0)

def create_new_canvas():
    return {"nodes": [], "connections": []}

def add_node(canvas_data, node):
    canvas_data['nodes'].append(node)

def create_connection(canvas_data, tweet_node, tag_node):
    connection = {'from': tweet_node['id'], 'to': tag_node['id']}
    canvas_data['connections'].append(connection)

def read_csv(csv_file):
    tweets = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            tweets.append(row)
    return tweets

def process_tweets(existing_canvas_data, csv_tweets):
    new_canvas = create_new_canvas()
    existing_tweets = {node['id']: node for node in existing_canvas_data['nodes'] if node['type'] == 'tweet'}
    
    for tweet in csv_tweets:
        tweet_id = tweet['tweet_url']
        tweet_tags = tweet.get('tags', '').split(',')
        tweet_node = existing_tweets.get(tweet_id, None)

        if not tweet_node:
            position = find_free_space(new_canvas['nodes'], NODE_SIZE)
            tweet_node = {'id': tweet_id, 'type': 'tweet', 'x': position[0], 'y': position[1],
                          'width': NODE_SIZE[0], 'height': NODE_SIZE[1]}
        add_node(new_canvas, tweet_node)

        for tag in tweet_tags:
            tag_node = next((node for node in new_canvas['nodes'] if node['id'] == tag and node['type'] == 'tag'), None)
            if not tag_node:
                tag_position = find_free_space(new_canvas['nodes'], NODE_SIZE)
                tag_node = {'id': tag, 'type': 'tag', 'x': tag_position[0], 'y': tag_position[1],
                            'width': NODE_SIZE[0], 'height': NODE_SIZE[1]}
                add_node(new_canvas, tag_node)
            create_connection(new_canvas, tweet_node, tag_node)

    return new_canvas

# File paths
canvas_file_path = r"C:\Users\tomdimsdale\OneDrive - M7 Real Estate\Documents\VSC\updated_tweets_canvas_v21.canvas"
csv_file_path = r"C:\Users\tomdimsdale\OneDrive - M7 Real Estate\Documents\VSC\Dewey_export_final_tags new.csv"

existing_canvas_data = parse_canvas(canvas_file_path)
csv_tweets = read_csv(csv_file_path)
new_canvas_data = process_tweets(existing_canvas_data, csv_tweets)

new_canvas_filename = f"new_canvas_{datetime.now().strftime('%Y%m%d-%H%M%S')}.canvas"
with open(new_canvas_filename, 'w') as file:
    json.dump(new_canvas_data, file, indent=4)