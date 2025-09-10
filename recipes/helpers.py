def determine_is_chef(request):
    """Determine if request's user is in Chef group"""
    is_chef = request.user.groups.filter(name="Chef").exists()
    return is_chef


def update_recipe_modified(recipe, user):
    """Update modified fields of recipe instance"""
    recipe.modified_by = user
    recipe.save(update_fields=["modified_at", "modified_by"])
