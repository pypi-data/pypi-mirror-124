import click
from string import Template
from os.path import isfile
import inflect
import pkg_resources
from crafter.commands.create_controller import create_controller
from crafter.commands.create_model import create_model


p = inflect.engine()


def create_route(name: str):

    if  isfile(f"app/routes/{name}_route.py"):
        click.echo(f"{name.capitalize()} Route already exists")
        return
    

    d = {
        'model_name': name,
        'model_name_uc': name.capitalize(),
        'model_name_plural': p.plural(name)
    }

    with open(pkg_resources.resource_filename("crafter", "templates/route.tpl"), "r") as f:
        src = Template(f.read())

    result_route = src.substitute(d)

    with open(f"app/routes/{name}_route.py", "a") as f:
        f.write(result_route)
   
    click.echo(f"{name.capitalize()} Route created successfully ✅")

    if  not isfile(f"app/models/{name}.py"):
        click.echo(f"No {name.capitalize()} Model detected. Creating model...")
        create_model(name)


    if  not isfile(f"app/controllers/{name}_controller.py"):
        click.echo(f"No {name.capitalize()} Controller detected. Creating controller...")
        create_controller(name)