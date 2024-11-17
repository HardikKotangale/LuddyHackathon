from firebase_admin import db

def get_contact(product_name=None, repo_name=None):
    ref = db.reference('contacts')
    result = None

    if product_name:
        result = ref.order_by_child('product_name').equal_to(product_name).get()
    elif repo_name:
        result = ref.order_by_child('repo_name').equal_to(repo_name).get()

    if not result:
        return None

    return next(iter(result.values()))


def add_contact(data):
    ref = db.reference('contacts')
    new_contact_ref = ref.push(data)
    return new_contact_ref.key


def update_contact(chat_user_name, data):
    ref = db.reference('contacts')
    contacts = ref.order_by_child('chat_user_name').equal_to(chat_user_name).get()

    if not contacts:
        return False

    contact_id = next(iter(contacts.keys()))
    ref.child(contact_id).update(data)
    return True


def delete_contact(chat_user_name):
    ref = db.reference('contacts')
    contacts = ref.order_by_child('chat_user_name').equal_to(chat_user_name).get()

    if not contacts:
        return False

    contact_id = next(iter(contacts.keys()))
    ref.child(contact_id).delete()
    return True
