from flask import Flask, render_template, request, jsonify, redirect
import os
from test import get_search_list, get_episodes, get_episodes_video

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'public'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400

    data = get_search_list(query)
    return jsonify(data)

@app.route('/api/episodes/<drama_id>', methods=['GET'])
def episodes(drama_id):
    data = get_episodes(drama_id)
    return jsonify(data)

@app.route('/api/episodes/<drama_id>/<episodeSid>', methods=['GET'])
def episodes_video(drama_id, episodeSid):
    data = get_episodes_video(drama_id, episodeSid)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)