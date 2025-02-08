from flask import Flask, jsonify
from src.aws_collector import list_ec2_instances

app = Flask(__name__)

@app.route('/api/ec2', methods=['GET'])
def get_ec2_instances():
    instances = list_ec2_instances()
    return jsonify(instances)

if __name__ == '__main__':
    app.run(debug=True)