from flask import Flask, request, jsonify # type: ignore
from transformers import LlamaTokenizer, LlamaForCausalLM # type: ignore
import torch # type: ignore
import requests # type: ignore
import base64
import safetensors # type: ignore

app = Flask(__name__)

# Load the tokenizer and model
model_path = 'openlm-research/open_llama_13b'
tokenizer = LlamaTokenizer.from_pretrained(model_path, legacy=False)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map='auto', low_cpu_mem_usage=True, offload_folder=r'C:\Users\Ragavendra\Desktop\Files\DOCKER_FILE\WEIGHT_OUTPUT'
)

SPOTIFY_CLIENT_ID = '6ce8f52663d24acc8693600eb5ee75fe'
SPOTIFY_CLIENT_SECRET = '94451a49b8be431cbedd8e2ae05d5ff9'

def get_spotify_access_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token")

@app.route('/query', methods=['POST'])
def query_model():
    data = request.json
    question = data['question']

    # Tokenize the input question
    prompt = f"Q: {question}\nA:"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    # Generate a response using the LLaMA model
    generation_output = model.generate(input_ids=input_ids, max_new_tokens=32)

    # Decode the response
    response = tokenizer.decode(generation_output[0], skip_special_tokens=True)

    return jsonify({'answer': response})

@app.route('/spotify/track', methods=['POST'])
def get_track_info():
    data = request.json
    track_name = data['track']

    access_token = get_spotify_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 1
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code == 200:
        track_data = response.json()
        return jsonify(track_data)
    else:
        return jsonify({'error': 'Unable to fetch track info'}), 404

@app.route('/agent', methods=['POST'])
def agent():
    data = request.json
    query = data['query']

    if 'track' in query.lower():
        track_name = query.split('track ')[1]
        response = get_track_info_response(track_name)
        return jsonify({'response': response})
    else:
        response = get_model_response(query)
        return jsonify({'response': response})

def get_track_info_response(track_name):
    access_token = get_spotify_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 1
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code == 200:
        track_data = response.json()
        return track_data
    else:
        return 'Unable to fetch track info'

def get_model_response(query):
    # Tokenize the input question
    prompt = f"Q: {query}\nA:"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    # Generate a response using the LLaMA model
    generation_output = model.generate(input_ids=input_ids, max_new_tokens=32)

    # Decode the response
    response = tokenizer.decode(generation_output[0], skip_special_tokens=True)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
