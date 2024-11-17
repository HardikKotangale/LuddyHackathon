import traceback
import uuid
from flask import request, jsonify
from firebase_admin import db


def add_contact_with_employee_id(product, employees):
    """
    Adds contacts with employee IDs (UUID) and updates assignments.
    """
    try:
        # Firebase references
        employee_ref = db.reference('employees')
        assignment_ref = db.reference('emp_assignment')
        product_ref = db.reference('products')

        added_employees = []
        assignments = []

        for employee in employees:
            # Check if the employee already exists based on email
            existing_employee_query = employee_ref.order_by_child('email').equal_to(employee['email']).get()
            existing_assignment = False 
            if existing_employee_query:
                # Employee exists, fetch the existing record
                existing_employee = next(iter(existing_employee_query.values()))
                employee_id = existing_employee.get('employee_id')
                print(f"Existing employee found: {existing_employee}")
            else:
                # Add a new employee with a UUID
                employee['employee_id'] = str(uuid.uuid4())
                employee_ref.push(employee)
                employee_id = employee['employee_id']
                added_employees.append({
                    'employee_id': employee_id,
                    'email': employee['email']
                })
                print(f"New employee added: {employee}")

            # Fetch product details based on product_name or repo_name
            product_query = None
            if 'product_name' in product and product['product_name']:
                product_query = product_ref.order_by_child('product_name').equal_to(product['product_name']).get()
            elif 'repo_name' in product and product['repo_name']:
                product_query = product_ref.order_by_child('repository_name').equal_to(product['repo_name']).get()

            if not product_query:
                return {'error': 'Invalid or missing product/repo data'}, 400

            product_data = next(iter(product_query.values()), None)
            if not product_data:
                return {'error': 'Invalid or missing product/repo data'}, 400
            product_id = product_data['product_id']

            # Check if the assignment already exists
            existing_assignment_query = assignment_ref.order_by_child('product_id').equal_to(product_id).get()

            assignment_exists = any(
                assignment['employee_id'] == employee_id
                for assignment in existing_assignment_query.values()
            )
            print(assignment_exists)
            if assignment_exists:
                return {
                    'error': f"Assignment for product_id '{product_id}' and employee_id '{employee_id}' already exists"
                
                }, 400
            # Create the new assignment
            assignment_data = {'product_id': product_id, 'employee_id': employee_id}
            assignment_ref.push(assignment_data)
            assignments.append(assignment_data)
            print(f"Assignment created: {assignment_data}")

        return {
            'added_employees': added_employees,
            'assignments': assignments
        }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in add_contact_with_employee_id: {error_details}")
        raise RuntimeError(f"Failed to add contacts and assignments: {e}")


def get_employees_by_product_or_repo(product_name=None, repo_name=None, location=None):
    """
    Fetch employees associated with a product based on product_name or repository_name, 
    optionally filtering by location.
    """
    if not product_name and not repo_name:
        return {'error': 'Please provide either product_name or repository_name'}, 400

    try:
        # Fetch product by product_name or repository_name
        product_ref = db.reference('products')
        query_result = None

        if product_name:
            query_result = product_ref.order_by_child('product_name').equal_to(product_name).get()
        elif repo_name:
            query_result = product_ref.order_by_child('repository_name').equal_to(repo_name).get()

        if not query_result:
            return {'error': 'No product or repository found'}, 404

        # Get the product_id
        product_data = next(iter(query_result.values()))
        product_id = product_data.get('product_id')

        if not product_id:
            return {'error': 'Product data is invalid or missing "product_id"'}, 404

        # Fetch employee assignments linked to the product_id
        assignment_ref = db.reference('emp_assignment')
        assignments = assignment_ref.order_by_child('product_id').equal_to(product_id).get()

        if not assignments:
            return {'error': 'No employees assigned to this product or repository'}, 404

        # Fetch employee details for valid assignments
        employee_ref = db.reference('employees')
        employees = []

        for assignment in assignments.values():
            employee_id = assignment.get('employee_id')
            if not employee_id:
                print("Skipping assignment due to missing or invalid employee_id:", assignment)
                continue

            # Query using indexed `employee_id`
            employee_query = employee_ref.order_by_child('employee_id').equal_to(employee_id).get()
            if employee_query:
                employee_data = next(iter(employee_query.values()))
                
                # Filter by location if provided
                if location and employee_data.get('location') != location:
                    print(f"Skipping employee due to location mismatch: {employee_data}")
                    continue

                employees.append(employee_data)

        if not employees:
            return {'error': 'No employees match the specified criteria'}, 404

        print("Final list of employees:", employees)
        return employees

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {'error': f"An error occurred: {str(e)}", 'trace': error_details}, 500
    
import traceback
from firebase_admin import db


def delete_employee_and_assignments(email):
    """
    Delete an employee and all their associated assignments based on the email.
    :param email: The email of the employee to be deleted
    :return: A dictionary with a success message or an error message
    """
    try:
        # Firebase references
        employee_ref = db.reference('employees')
        assignment_ref = db.reference('emp_assignment')

        # Query for the employee using email
        employee_query = employee_ref.order_by_child('email').equal_to(email).get()

        if not employee_query:
            return {'error': 'Employee with the provided email not found'}, 404

        # Get the employee_id from the employee record
        employee_data = next(iter(employee_query.items()))  # Get the first result
        employee_id = employee_data[1]['employee_id']  # Firebase key for the employee record
        print(employee_id)

        # Delete all assignments linked to this employee_id
        assignment_query = assignment_ref.order_by_child('employee_id').equal_to(employee_id).get()
        if assignment_query:
            for assignment_id in assignment_query.keys():
                assignment_ref.child(assignment_id).delete()
                print(f"Deleted assignment: {assignment_id}")

        # Delete the employee record
        employee_ref.child(employee_id).delete()
        print(f"Deleted employee: {employee_id}")

        return {
            'message': f"Employee with email '{email}' and associated assignments deleted successfully"
        }, 200

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error in delete_employee_and_assignments: {error_details}")
        return {
            'error': f"An error occurred: {str(e)}",
            'trace': error_details
        }, 500
