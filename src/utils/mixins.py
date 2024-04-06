from jsonschema import validate


class MapFieldsFromJsonValidationSchemaMixin:
    """
    The purpose of this is to map the fields of the database table
    with the fields of the json validation schema.
    """
    @classmethod
    def map_fields(cls, json_schema: dict, data: dict):
        validate(data, json_schema)
        extracted_data = {}
        for key, value in data.items():
            if key in json_schema["properties"]:
                database_table_related_field = str(json_schema["properties"][key]["database_table_related_field"])
                _, field_name = database_table_related_field.split(".")
                extracted_data[field_name] = value
        return cls(**extracted_data)
