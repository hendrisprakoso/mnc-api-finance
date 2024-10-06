import uuid


def generate_uuid():
	return str(uuid.uuid4())


def masking_phone_number(value) -> str:
    if value in ('', 'NULL', 'null', None, "nan"):
        return None
    else:
        value = value.replace("'", "")
        value = value.replace(" ", "")
        value = str(value.split(".")[0])
        if '/' in value:
            value = value.split('/')[0]

        if len(value) < 6 or len(value) > 15:
            return None

        if value[0:3] == '000':
            return None
        
        if value[0:3] == '021':
            return None

        if value[0:1] == '8':
            return f"08{value[1:]}"

        if value[0:2] == '08':
            return f"08{value[2:]}"

        if value[0:3] == '628':
            return f"08{value[3:]}"

        if value[0:4] == '+628':
            return f"08{value[4:]}"
        
        return value
