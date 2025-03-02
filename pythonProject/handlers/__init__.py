from .instruction import instruction_router
from .commands import start_router
from .support import support_router
from .step_back import step_back_router
from .generate_recipe import generate_recipe_router
from .add_recipe import add_recipe_router
from .show_saved_recipes import show_saved_recipes_router
from .waste_messages import waste_messages_router

routes = [
    instruction_router,
    start_router,
    support_router,
    step_back_router,
    generate_recipe_router,
    add_recipe_router,
    show_saved_recipes_router,
    waste_messages_router
]