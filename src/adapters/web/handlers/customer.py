from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import RedirectResponse

from adapters.web.core.forms import Form
from adapters.web.core.template import Templates
from core.application import Application
from modules.customer.application.commands import CustomerCreateCommand, CustomerGetByEmailCommand
from modules.customer.domain.customer import CustomerCreate
from modules.customer.domain.exceptions import CustomerAlreadyExistsException

PASSWORD_MIN_LENGTH = 8


@dataclass
class CustomerRegistrationForm(Form):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    terms: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def validate(self) -> None:
        self.required("first_name", "last_name", "email", "password")
        self.valid_email("email")
        self.min_length("password", PASSWORD_MIN_LENGTH)
        self.same_as("confirm_password", "password")
        self.checked("terms")


@dataclass
class CustomerLoginForm(Form):
    email: str = ""
    password: str = ""

    def validate(self) -> None:
        self.required("email", "password")
        self.valid_email("email")


class CustomerPages:
    def __init__(self, app: Application, templates: Templates):
        self.templates = templates
        self.app = app

    async def register_get(self, request: Request):
        return self.templates.TemplateResponse(request, "views/registration.html", {
            "form": CustomerRegistrationForm(),
        })

    async def register_submit(self, request: Request):
        form = await CustomerRegistrationForm.from_request(request)
        if not form.valid:
            return self.templates.TemplateResponse(request, "views/registration.html", {
                "form": form,
            }, status_code=400)

        try:
            customer = await self.app.execute(
                CustomerCreateCommand(
                    payload=CustomerCreate(
                        full_name=form.full_name,
                        email=form.email,
                        active=True,
                        password=form.password,
                    ),
                )
            )

            request.session["user_id"] = str(customer.id)

            return self.templates.TemplateResponse(request, "views/registration.html", {
                "form": CustomerRegistrationForm(),
                "customer": customer,
            })

        except CustomerAlreadyExistsException:
            return self.templates.TemplateResponse(request, "views/registration.html", {
                "form": CustomerRegistrationForm(),
                "submit_error": "Customer already exists",
            })

    async def login_get(self, request: Request):
        return self.templates.TemplateResponse(request, "views/login.html", {
            "form": CustomerLoginForm(),
        })

    async def login_post(self, request: Request):
        form = await CustomerLoginForm.from_request(request)
        if not form.valid:
            return self.templates.TemplateResponse(request, "views/login.html", {
                "form": form,
            }, status_code=400)

        customer = await self.app.execute(
            CustomerGetByEmailCommand(email=form.email)
        )
        if customer is None:
            return self.templates.TemplateResponse(request, "views/login.html", {
                "form": CustomerLoginForm(),
                "submit_error": "Customer does not exists",
            })
        request.session["user_id"] = str(customer.id)
        return RedirectResponse(url="/", status_code=303)

    async def logout(self, request: Request):
        request.session["user_id"] = None
        return RedirectResponse(url="/", status_code=303)
