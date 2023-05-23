import re


def is_db_exists(client, table_name):
    try:
        client.describe_table(TableName=table_name)
    except client.exceptions.ResourceNotFoundException:
        return False
    return True


def password_validation(password):
    pwd_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pwd_pattern = re.compile(pwd_regex)
    password_regex_match = re.search(pwd_pattern, password)
    return password_regex_match


def email_validation(email):
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_pattern = re.compile(email_regex)
    email_regex_match = re.search(email_pattern, email)
    return email_regex_match
