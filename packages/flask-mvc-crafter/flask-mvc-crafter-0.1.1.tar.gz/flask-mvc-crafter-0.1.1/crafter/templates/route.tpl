from flask import Blueprint
from app.controllers import ${model_name}_controller
prefix = '${model_name_plural}'
route = Blueprint(prefix, __name__)

route.get('/${model_name_plural}')(${model_name}_controller.index)
route.get('/${model_name_plural}/create')(${model_name}_controller.create)
route.post('/${model_name_plural}')(${model_name}_controller.store)
route.get('/${model_name_plural}/<int:${model_name}_id>')(${model_name}_controller.show)
route.get('/${model_name_plural}/<int:${model_name}_id>/edit')(${model_name}_controller.edit)
route.post('/${model_name_plural}/<int:${model_name}_id>')(${model_name}_controller.update)
route.delete('/${model_name_plural}/<int:${model_name}_id>')(${model_name}_controller.delete)