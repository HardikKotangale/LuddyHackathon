from flask import Blueprint, request, jsonify
from app.utils import get_contact, add_contact, update_contact, delete_contact

contact_api = Blueprint('contact_api', __name__)

@contact_api.route('/', methods=['GET'])
def get_point_of_contact():
    product_name = request.args.get('product_name')
    repo_name = request.args.get('repo_name')

    if not product_name and not repo_name:
        return jsonify({'error': 'Please provide either product_name or repo_name'}), 400

    try:
        contact = get_contact(product_name=product_name, repo_name=repo_name)
        if not contact:
            return jsonify({'error': 'No point of contact found'}), 404

        return jsonify(contact), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contact_api.route('/', methods=['POST'])
def add_point_of_contact():
    data = request.json
    required_fields = ['product_name', 'repo_name', 'chat_user_name', 'email', 'first_name', 'last_name', 'location', 'title']

    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing fields: {", ".join(required_fields)}'}), 400

    try:
        contact_id = add_contact(data)
        return jsonify({'message': 'Contact added successfully', 'id': contact_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contact_api.route('/<chat_user_name>', methods=['PUT'])
def update_point_of_contact(chat_user_name):
    data = request.json

    try:
        success = update_contact(chat_user_name, data)
        if not success:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify({'message': 'Contact updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contact_api.route('/<chat_user_name>', methods=['DELETE'])
def delete_point_of_contact(chat_user_name):
    try:
        success = delete_contact(chat_user_name)
        if not success:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify({'message': 'Contact deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
