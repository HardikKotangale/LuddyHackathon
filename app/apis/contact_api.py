from flask import Blueprint, request, jsonify
from app.utils import (
    get_employees_by_product_or_repo,
    add_contact_with_employee_id,
    delete_employee_and_assignments
)

contact_api = Blueprint('contact_api', __name__)

@contact_api.route('/', methods=['GET'])
def get_employees():
    """
    Fetch employees based on product_name, repository_name, or location.
    """
    product_name = request.args.get('product_name')
    repo_name = request.args.get('repository_name')
    location = request.args.get('location')  # Optional location parameter

    if not product_name and not repo_name:
        return jsonify({'error': 'Please provide either product_name or repository_name'}), 400

    try:
        # Call the function with the additional location parameter
        result = get_employees_by_product_or_repo(
            product_name=product_name, repo_name=repo_name, location=location
        )

        # If the function returns an error or status, handle it
        if isinstance(result, tuple):
            error, status = result
            return jsonify(error), status

        if not result:
            return jsonify({'error': 'No employees found for the specified criteria'}), 404

        return jsonify({'employees': result}), 200

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'error': f"An error occurred: {str(e)}", 'trace': error_details}), 500



@contact_api.route('/', methods=['POST'])
def add_product_with_employees_api():
    """
    Add a product with its associated employees.
    """
    data = request.json
    print(data)

    # Validate the presence of the 'product' and 'employees' keys
    if not data:
        return jsonify({'error': 'Request payload is empty'}), 400

    if 'product' not in data:
        return jsonify({'error': 'Missing required key: "product"'}), 400

    if 'employees' not in data:
        return jsonify({'error': 'Missing required key: "employees". Ensure you pass a list of employees'}), 400

    # Validate that 'employees' is a list
    if not isinstance(data['employees'], list):
        return jsonify({'error': 'Employees data should be a list of employee objects'}), 400

    product_required_fields = ['product_name', 'repo_name']  # Add optional fields here
    employee_required_fields = ['first_name', 'last_name', 'email', 'chat_username', 'location', 'title']

    if not any(field in data['product'] for field in product_required_fields):
        return jsonify({'error': f'Missing fields in product data: At least one of {product_required_fields} must be provided'}), 400

    # Additional validation for specific product fields
    if 'product_name' in data['product']:
        product_name = data['product']['product_name']
        if not isinstance(product_name, str) or not product_name.strip():
            return jsonify({'error': 'Invalid value for product_name. It must be a non-empty string'}), 400

    if 'repo_name' in data['product']:
        repo_name = data['product']['repo_name']
        if not isinstance(repo_name, str) or not repo_name.strip():
            return jsonify({'error': 'Invalid value for repo_name. It must be a non-empty string'}), 400

    # Validate employee fields
    invalid_employees = []
    for idx, employee in enumerate(data['employees']):
        missing_fields = [field for field in employee_required_fields if field not in employee]
        if missing_fields:
            invalid_employees.append({'index': idx, 'missing_fields': missing_fields})

    if invalid_employees:
        return jsonify({'error': 'Missing fields in employee data', 'details': invalid_employees}), 400

    try:
        # Call the utility function to add the product and employees
        result = add_contact_with_employee_id(data['product'], data['employees'])

        # Process of adding employee and assignments
        result, status = add_contact_with_employee_id(data['product'], data['employees'])
        if status == 409:
            return jsonify({'error': result['error']}), 409
        return jsonify({'message': 'Data added successfully', 'result': result}), 201
    except KeyError as ke:
        return jsonify({'error': str(ke)}), 400
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Unexpected error: {error_details}")
        return jsonify({'error': 'An internal server error occurred', 'trace': error_details}), 500




@contact_api.route('/email/<email>', methods=['DELETE'])
def delete_employee_by_email(email):
    """
    API Endpoint to delete an employee and their associated assignments by email.
    """
    try:
        response, status_code = delete_employee_and_assignments(email)
        return jsonify(response), status_code

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500

