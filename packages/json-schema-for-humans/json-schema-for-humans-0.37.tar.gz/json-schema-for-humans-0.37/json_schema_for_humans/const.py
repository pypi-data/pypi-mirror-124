from enum import Enum
from io import TextIOWrapper, FileIO
from typing import Union, TextIO

TYPE_ARRAY = "array"
TYPE_BOOLEAN = "boolean"
TYPE_CONST = "const"
TYPE_ENUM = "enum"
TYPE_INTEGER = "integer"
TYPE_NULL = "null"
TYPE_NUMBER = "number"
TYPE_OBJECT = "object"
TYPE_STRING = "string"

DESCRIPTION = "description"
DEFAULT = "default"
EXAMPLES = "examples"
ITEMS = "items"
TYPE = "type"
REF = "$ref"

MULTIPLE_OF = "multipleOf"
MAXIMUM = "maximum"
EXCLUSIVE_MAXIMUM = "exclusiveMaximum"
MINIMUM = "minimum"
EXCLUSIVE_MINIMUM = "exclusiveMinimum"

LINE_WIDTH = 80


FileLikeType = Union[TextIO, TextIOWrapper, FileIO]


class ResultExtension(Enum):
    HTML = "html"
    MD = "md"


class TemplateName(Enum):
    FLAT = "flat"
    JS = "js"
    MD = "md"
    MD_NESTED = "md_nested"

    @property
    def result_extension(self) -> ResultExtension:
        if self in [self.FLAT, self.JS]:
            return ResultExtension.HTML
        if self in [self.MD, self.MD_NESTED]:
            return ResultExtension.MD


class DefaultFile(Enum):
    CSS_FILE_NAME = "schema_doc.css"
    JS_FILE_NAME = "schema_doc.min.js"
    TEMPLATE_FILE_NAME = "base.html"
