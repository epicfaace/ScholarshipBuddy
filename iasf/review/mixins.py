from django.contrib.auth.mixins import AccessMixin

class UserIsStaffMixin(AccessMixin):
    """Verify that the current user is authenticated and is staff."""
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)