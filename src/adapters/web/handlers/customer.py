from dataclasses import asdict

from starlette.requests import Request

from adapters.web.core.template import Templates
from core.application import Application
from modules.customer.application.commands import CustomerCreateCommand
from modules.customer.domain.customer import CustomerCreate


class CustomerPages:
    def __init__(self, app: Application, templates: Templates):
        self.templates = templates
        self.app = app

    async def register_get(self, request: Request):
        return self.templates.TemplateResponse(request, "views/registration.html", {})

    async def register_submit(self, request: Request):
        # TODO: parse form
        # TODO: validation
        form = await request.form()
        customer = await self.app.execute(
            CustomerCreateCommand(
                payload=CustomerCreate(
                    full_name=f"{str(form['first_name'])} {str(form['last_name'])}",
                    email=str(form["email"]),
                    active=True,
                    password=str(form["password"]),
                ),
            )
        )

        return self.templates.TemplateResponse(request, "views/registration.html", {
            "customer": customer,
        })
