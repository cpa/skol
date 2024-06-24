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

class RawFormat(Format):
    name = "Raw"

    @staticmethod
    def load(data):
        return data.splitlines()

    @staticmethod
    def to_string(obj):
        '\n'.join([o for o in obj])

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
        if isinstance(python_data, list):
            return python_data
        raise CannotLoadDataError

    @staticmethod
    def to_string(obj):
        return str(obj)


class PostgresFormat(Format):
    name = "Postgres"

    @staticmethod
    def load(data):
        raise CannotLoadDataError

    @staticmethod
    def to_string(obj):
        # TODO: check if the input is a list of string/float/ints and warn otherwise
        if not isinstance(obj, list):
            logging.warning("Data is not a list. Will try to output something, but check the result carefully.")
        elif not all([isinstance(e, int) or isinstance(e, float) or isinstance(e, str) for e in obj]):
            logging.warning(
                "Some elements of the data are not recognized as either int, float or string. Will try to output something, but check the result carefully."
            )

        escaped_obj = ["'" + e.replace("[", "\[").replace("]", "\]").replace(",", "\,").replace("'", "'") + "'" for e in obj]
        output = "ARRAY[ " + ",".join(escaped_obj) + "]"
        return output


FORMATS = [JSONFormat, PythonFormat, PostgresFormat, RawFormat]
