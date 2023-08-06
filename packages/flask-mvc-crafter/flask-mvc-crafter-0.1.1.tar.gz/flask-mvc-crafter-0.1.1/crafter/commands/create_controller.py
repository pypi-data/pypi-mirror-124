import click
from string import Template
from os.path import isfile
import pkg_resources
from crafter.commands.create_model import create_model


def create_controller(name: str):

    if isfile(f"app/controllers/{name}_controller.py"):
        click.echo(f"{name.capitalize()} Controller already exists")
        return

    d = {"model_name": name, "model_name_uc": name.capitalize()}

    with open(
        pkg_resources.resource_filename("crafter", "templates/controller.tpl"), "r"
    ) as f:
        src = Template(f.read())

    result_controller = src.substitute(d)

    with open(f"app/controllers/{name}_controller.py", "a") as f:
        f.write(result_controller)

    click.echo(f"{name.capitalize()} Controller created successfully ✅")

    if not isfile(f"app/models/{name}.py"):
        click.echo(f"No {name.capitalize()} Model detected. Creating model...")
        create_model(name)
