from starlette.requests import Request

from adapters.web.core.template import Templates


class StaticPages:
    def __init__(self, templates: Templates):
        self.templates = templates

    async def contact(self, request: Request):
        return self.templates.TemplateResponse(request, "views/contact.html", {})

    async def about(self, request: Request):
        return self.templates.TemplateResponse(request, "views/about.html", {})

    async def terms_conditions(self, request: Request):
        return self.templates.TemplateResponse(request, "views/terms.html", {})
