import click
from crafter.commands import *


@click.group()
def cli():
    """CLI tool for the Flask MVC Starter Kit"""


@cli.command()
@click.option("--name", help="Name of controller", required=True, type=str)
def controller(name: str):
    """Create a new controller"""
    create_controller(name)


@cli.command()
@click.option("--name", help="Name of model", required=True, type=str)
def model(name: str):
    """Create a new model"""
    create_model(name)


@cli.command()
@click.option("--name", help="Name of route", required=True, type=str)
def route(name: str):
    """Create a new route"""
    create_route(name)

@cli.command()
# @click.option("--type", help="Type of relationship", required=True, type=str)
@click.option("--type", help="Type of relationship", required=True, type=click.Choice(['one_one', 'one_many', 'many_one', 'many_many']))
@click.option("--models", help="Name of route", nargs = 2, required=True, type=str)

def relationship(type, models):
    """Create a new relationship"""
    model_1, model_2 = models
    
    if type == 'many_many':
        assoc = click.prompt(f"Enter the association table between {model_1} and {model_2}", type=str, default=f"{model_1}_{model_2}")
    else:
        assoc = None

    create_relationship(type, model_1, model_2, assoc)