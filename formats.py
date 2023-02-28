import logging


class CannotLoadDataError(Exception):
    pass


class Format:
    name: str

    @staticmethod
    def load(data):
        raise NotImplementedError

    @classmethod
    def is_valid(cls, data):
        try:
            cls.load(data)
        except CannotLoadDataError:
            return False
        return True

    @staticmethod
    def to_string(obj):
        raise NotImplementedError


class JSONFormat(Format):
    name = "JSON"

    @staticmethod
    def load(data):
        import json

        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as e:
            logging.info("Data is not a JSON object")
            raise CannotLoadDataError
        logging.info("Data is a JSON object")
        return json_data

    @staticmethod
    def to_string(obj):
        import json

        return json.dumps(obj)


class PythonFormat(Format):
    name = "Python"

    @staticmethod
    def load(data):
        import ast

        try:
            python_data = ast.literal_eval(data)
        except Exception:
            logging.info("Data is not a Python object")
            raise CannotLoadDataError
        if isinstance(python_data, list):
            logging.info("Data is a Python list")
            return python_data
        logging.info("Data is a Python object, but not a list")
        raise CannotLoadDataError

    @staticmethod
    def to_string(obj):
        return str(obj)


FORMATS = [JSONFormat, PythonFormat]
