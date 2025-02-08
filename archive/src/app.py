# app.py

from flask import Flask, jsonify
from aws_collector import collect_ec2_instances, collect_s3_buckets

app = Flask(__name__)

@app.route('/api/ec2', methods=['GET'])
def get_ec2_instances():
    """
    Endpoint to retrieve EC2 instance data.
    """
    instances = collect_ec2_instances()
    return jsonify(instances)


@app.route('/api/s3', methods=['GET'])
def get_s3_buckets():
    """
    Endpoint to retrieve S3 bucket data.
    """
    buckets = collect_s3_buckets()
    return jsonify(buckets)


@app.route('/api/scan', methods=['POST'])
def scan_resources():
    """
    Endpoint to trigger a full scan of AWS resources.
    """
    collect_ec2_instances()
    collect_s3_buckets()
    return jsonify({"message": "Scan completed successfully."})


if __name__ == '__main__':
    app.run(debug=True)