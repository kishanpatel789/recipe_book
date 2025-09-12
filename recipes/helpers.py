def determine_is_chef(user):
    """Determine if request's user is in Chef group"""
    is_chef = user.groups.filter(name="Chef").exists()
    return is_chef


def update_recipe_modified(recipe, user):
    """Update modified fields of recipe instance"""
    recipe.modified_by = user
    recipe.save(update_fields=["modified_at", "modified_by"])


def get_favorite_recipes(user):
    """Get all favorite recipes for a user"""
    if user.is_authenticated:
        recipes = user.profile.favorites.all()
        return recipes
    else:
        return []
