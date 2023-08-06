from rest_framework.permissions import BasePermission,SAFE_METHODS


class UserPermission(BasePermission):

    '''
    Django permission usually work on two levels: on the overall endpoint(has_permission) and on an object level(has_object_permission)
    A great way to write permissions is to always deny by default; that is why we always return False at athe end of each permission method
    And then you can start adding the conditions. Here, in all the methods, we are checking that anonymous users can only make the SAFE_METHODS requests
    GET,OPTIONS and HEAD. And othere users we are making sure that they are always authenticated before continuing.
    '''
    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_anonymous:
    #         return request.method in SAFE_METHODS
        
    #     if view.basename in ['post']:
    #         return bool(request.user and request.user.is_authenticated)
    #     return False
    
    # def has_permission(self, request, view):
    #     if view.basename in ['post']:
    #         if request.user.is_anonymous:
    #             return request.method in SAFE_METHODS
    #         return bool(request.user and request.user.is_authenticated)
    #     return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)

        if view.basename in ["post-comment"]:
            if request.method in ['DELETE']:
                return bool(request.user.is_superuser or request.user in [obj.author, obj.post.author])

            return bool(request.user and request.user.is_authenticated)

        return False

    def has_permission(self, request, view):
        if view.basename in ["post", "post-comment"]:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)

        return False
