from rest_framework.permissions import IsAuthenticated
from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import BasePermission,SAFE_METHODS


# class UserPermission(BasePermission):

#     '''
#     Django permission usually work on two levels: on the overall endpoint(has_permission) and on an object level(has_object_permission)
#     A great way to write permissions is to always deny by default; that is why we always return False at athe end of each permission method
#     And then you can start adding the conditions. Here, in all the methods, we are checking that anonymous users can only make the SAFE_METHODS requests
#     GET,OPTIONS and HEAD. And othere users we are making sure that they are always authenticated before continuing.
#     '''
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_anonymous:
#             return request.method in SAFE_METHODS
        
#         if view.basename in ['post']:
#             return bool(request.user and request.user.is_authenticated)
#         return False
    
#     def has_permission(self, request, view):
#         if view.basename in ['post']:
#             if request.user.is_anonymous:
#                 return request.method in SAFE_METHODS
#             return bool(request.user and request.user.is_authenticated)
#         return False

class PostViewSet(AbstractViewSet):
    http_method_names = ('post','get','put','delete')
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()
    
    def get_object(self):
        obj= Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request,obj)
        return obj
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.date,status=status.HTTP_201_CREATED)
    
    def update(self,instance,validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance,validated_data)
        return instance
    
    @action(methods=['post'],detail=True)
    def like(self,request,*args,**kwargs):
        post = self.get_object()
        user = self.request.user
        user.like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['post'],detail=True)
    def remove_like(self,request,*args,**kwargs):
        post = self.get_object()
        user = self.request.user
        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    '''
    First we retrieve the concerned post on which we want to call the like or remove the like action,
    The self.get_object() method will automatically return the concerned post
    using the ID passed to the URL request.
    Second we also retrieve the user making the request from the self.request object.This is done so that we can call the remove_like or like method added to the User Model
    Finally we serialized the post using the Serializer class defined on self.serializer_class and return a response
    '''
    