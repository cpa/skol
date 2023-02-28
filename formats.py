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
            logging.debug(f"Data is not a {cls.name} expression")
            return False
        logging.debug(f"Data is a {cls.name} expression")
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
            raise CannotLoadDataError
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
            raise CannotLoadDataError
        # if isinstance(python_data, list):
        return python_data
        # raise CannotLoadDataError

    @staticmethod
    def to_string(obj):
        return str(obj)


FORMATS = [JSONFormat, PythonFormat]
