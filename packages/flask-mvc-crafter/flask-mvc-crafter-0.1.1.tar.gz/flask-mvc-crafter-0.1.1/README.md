# Crafter

A CLI tool for rapidly building applications with [FlaskMVC Starter Kit](https://github.com/rdp-jr/flask-mvc-starter-kit)

## Getting Started
1. Create a project using [FlaskMVC Starter Kit](https://github.com/rdp-jr/flask-mvc-starter-kit) and install the dependencies (this installs Crafter as well)


## Usage
- the format of running commands with crafter is as follows:
```
crafter <command> <args>
```

## Commands

### **model**
Create a model with a name of post
```
crafter model --name post
```
- generates `post.py` in `app/models`

### **controller**
Create a controller with a name of post
```
crafter controller --name post
```
- generates `post_controller.py` in `app/controllers`
- generates a model if no model with given name is found

### **route**
Create a route with a name of post
```
crafter route --name post
```
- generates `post_route.py` in `app/routes`
- generates a controller if no controller with given name is found
- generates a model if no model with given name is found

### **relationship**
Create a relationship between two models
- type: [`one_one`, `one_many`, `many_one`, `many_many`]
- models: `model_1`, `model_2`



```
crafter relationship --type one_one --models student contact
```
- generates either models if no model with given names are found
- creates a one-to-one relationship between `student` and `contact`

```
crafter relationship --type one_many --models knight sword
```
- creates a one-to-many relationship between `knight` and `sword` (one `knight` has many `swords`)
- if we swap the positions (`--models sword knight`) the relationship would be one `sword` has many `knights`, which may or may not be intended

`many_one` works the same way as `one_many`, just take note of the positions of the arguments

To create a many-to-many relationship, an additional argument is needed, the `association`

```
crafter relationship --type many_many --models wizard spell
Enter the association table between wizard and spell: spellbook
```
- A bridging table named `spellbook` is created
- if no input is given, default table name is `{model_1}_{model_2}` (in this case, `wizard_spell`)