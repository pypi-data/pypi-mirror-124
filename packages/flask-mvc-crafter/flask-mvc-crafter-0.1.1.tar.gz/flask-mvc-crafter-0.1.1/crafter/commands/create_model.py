import click
from string import Template
import pkg_resources
import inflect

p = inflect.engine()


def create_model(name: str):

    d = {
        "model_name": name.lower(),
        "table_name": p.plural(name.lower()),
        "model_name_uc": name.capitalize(),
    }

    with open(
        pkg_resources.resource_filename("crafter", "templates/model.tpl"), "r"
    ) as f:
        src = Template(f.read())

    result_model = src.substitute(d)

    with open(f"app/models/{name}.py", "w") as f:
        f.write(result_model)

    click.echo(f"{name.capitalize()} Model created successfully ✅")
