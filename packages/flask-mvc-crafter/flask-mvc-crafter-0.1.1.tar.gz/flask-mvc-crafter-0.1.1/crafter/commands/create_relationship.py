import click
from string import Template
import ast
from os.path import isfile
import inflect
import pkg_resources

from crafter.commands import create_model

p = inflect.engine()

def create_relationship(relationship_type, model_1, model_2, assoc = None):
    assoc_name = ''
    if (relationship_type == 'many_many'):
        assoc_name = assoc

    statements = {
        "one_one" : [
            f"{model_2} = db.relationship('{model_2.capitalize()}', backref='{model_1.lower()}', lazy=True, uselist=False)",
            f"{model_1}_id = db.Column(db.Integer, db.ForeignKey('{model_1}.id'), nullable=False)",
        ],
        "one_many": [
            f"{p.plural(model_2)} = db.relationship('{model_2.capitalize()}', backref='{model_1.lower()}', lazy=True)",
            f"{model_1}_id = db.Column(db.Integer, db.ForeignKey('{model_1}.id'), nullable=False)",
        ],
        "many_one": [
            f"{model_2}_id = db.Column(db.Integer, db.ForeignKey('{model_2}.id'), nullable=False)",
            f"{p.plural(model_1)} = db.relationship('{model_1.capitalize()}', backref='{model_2.lower()}', lazy=True)",
        ],
        "many_many": [
            f"{p.plural(assoc_name)} = db.relationship('{model_2.capitalize()}', secondary={assoc_name}, backref=db.backref('{assoc_name}', lazy=True))",
            None,
        ],

    }

    insert_statement(statements[relationship_type][0], model_1)
    insert_statement(statements[relationship_type][1], model_2)

    if (relationship_type == "many_many"):
        create_assoc_table(assoc_name, model_1, model_2)
        add_import(assoc_name, model_1)

    
    click.echo(f"{model_1} and {model_2} Relationship created successfully ✅")

def add_import(assoc_name, model):
    with open(f"app/models/{model}.py", "r") as f:
        root = ast.parse(f.read())
    import_node = ast.parse(f"import {assoc_name}")
    root.body.insert(1, import_node)
    ast.fix_missing_locations(root)

    unparsed = ast.unparse(root)

    with open(f"app/models/{model}.py", "w") as f:
        f.write(unparsed)


def create_assoc_table(assoc_name, model_1, model_2):

    d = {
        'assoc_name': assoc_name,
        'model_1': model_1,
        'model_2': model_2,
        
    }

    with open(pkg_resources.resource_filename("crafter", "templates/assoc_table.tpl"), "r") as f:
        src = Template(f.read())
    result_table = src.substitute(d)

    with open(f"app/models/{assoc_name}.py", "w") as f:
        f.write(result_table)
   
    click.echo(f"{assoc_name} Table created successfully ✅")


def insert_statement(statement, model):
    if statement is None:
        if not isfile(f"app/models/{model}.py"):
            create_model(model)
        return 
    if not isfile(f"app/models/{model}.py"):
        create_model(model)

    with open(f"app/models/{model}.py", "r") as f:
        root = ast.parse(f.read())

    classdef = root.body[-1]
    assign_node = ast.parse(statement)
    classdef.body.insert(2, assign_node)
    ast.fix_missing_locations(root)

    unparsed = ast.unparse(root)

    with open(f"app/models/{model}.py", "w") as f:
        f.write(unparsed)
    
