from pathlib import Path
from typing import List, Optional
import random
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel



BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

class Contact(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str] = None


contacts_db: List[Contact] = []


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"title": "Home"}
    )


@app.get("/contacts")
async def get_contacts(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"contacts": contacts_db, "title": "Contacts"},
    )


@app.get("/add_contact")
async def add_contact_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="add_edit.html", context={"title": "Add Contact"}
    )


@app.post("/add_contact")
async def create_contact(
        request: Request,
        name: str = Form(...),
        phone: str = Form(...),
        email: Optional[str] = Form(None)
):
    new_id = max([c.id for c in contacts_db], default=0) + 1
    new_contact = Contact(id=new_id, name=name, phone=phone, email=email)
    contacts_db.append(new_contact)

    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"contacts": contacts_db, "title": "Contacts"},
    )


@app.get("/edit_contact/{contact_id}")
async def edit_contact_form(request: Request, contact_id: int):
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    return templates.TemplateResponse(
        request=request,
        name="add_edit.html",
        context={"contact": contact, "title": "Edit Contact"},
    )


@app.post("/edit_contact/{contact_id}")
async def update_contact(
        request: Request,
        contact_id: int,
        name: str = Form(...),
        phone: str = Form(...),
        email: Optional[str] = Form(None),
):
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if contact:
        contact.name = name
        contact.phone = phone
        contact.email = email

    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"contacts": contacts_db, "title": "Contacts"},
    )


@app.get("/delete_contact/{contact_id}")
async def delete_contact(request: Request, contact_id: int):
    global contacts_db
    contacts_db = [c for c in contacts_db if c.id != contact_id]
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"contacts": contacts_db, "title": "Contacts"},
    )