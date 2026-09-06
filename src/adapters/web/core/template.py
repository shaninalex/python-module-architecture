import datetime
import os

import jinja2
from starlette.templating import Jinja2Templates


class Templates(Jinja2Templates):
    def __init__(self) -> None:
        template_path = os.environ.get("APP_MARKET_WEB_TEMPLATES_PATH")
        if template_path is None:
            raise Exception("Template path does not set")

        super().__init__(directory=template_path)

        # define custom pipes
        self.env.filters["dateformat"] = _pipe_dateformat

        # Define custom widgets. Example:
        # self.env.globals["brands"] = brands_list(connector)
        # self.env.globals["categories"] = category_list(connector)


    def from_string(self, source: str) -> jinja2.Template:
        return self.env.from_string(source)


def _pipe_dateformat(value: datetime.date | str) -> str:
    """
    Format date time in standard format.
    Usage:
        {{ post.date_published | dateformat }}
    :param value: datetime
    :return: string
    """
    if isinstance(value, str):
        value = datetime.date.fromisoformat(value)
    return value.strftime("%b %d, %Y")
