def determine_is_chef(request):
    """Determine if request's user is in Chef group"""
    is_chef = request.user.groups.filter(name="Chef").exists()
    return is_chef
