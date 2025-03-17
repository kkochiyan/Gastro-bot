from .processing_commands_handler import start_router
from .send_message_to_support_handler import support_router
from .step_back_handler import step_back_router
from .generate_recipe_handler import generate_recipe_router
from .add_recipe_handler import add_recipe_router
from .show_saved_recipes_handler import show_saved_recipes_router
from .processing_waste_messages_handler import waste_messages_router
from .edit_recipe_handler import edit_recipe_router

routes = [
    start_router,
    support_router,
    step_back_router,
    generate_recipe_router,
    add_recipe_router,
    show_saved_recipes_router,
    waste_messages_router,
    edit_recipe_router
]