from rest_framework import serializers 
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer

class PostSerializer(AbstractSerializer):
    '''
    Defing the type of relationship field we want to use can also be crucial to tell Django exactly what to do
    that why SlugRelatedField comes in. It is used to represent the target of relationship
    using a field on the target
    '''
    author = serializers.SlugRelatedField(queryset = User.objects.all(),slug_field='public_id')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_liked(self,instance):
        request = self.context.get('request',None)
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)
    
    def get_likes_count(self,instance):
        return instance.liked_by.count()

    def validate_author(self,value):
        if self.context['request'].user != value:
            raise ValidationError("you can't create a post for another user")
        
        return value
    
    '''
    validate_author method checks validation for the author field.Here we want to make sure that the user creating the post is the same user as in the author field
    context dictionary is available in every serializer. It is usually contains the request object that we can use to mark some checks 
    '''

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data
        return rep
    
    '''
    Actually the author field accepts public_id and returns public_id.While it does the work, it can be a  little bit difficult to identify the user.This cause it to make a request again with public_id of the user to get the pieces of information about the user 
    to_representation method takes the object instance that requires serialization and 
    return the primitive representation.This usually means returning a structure of built-in-Python data types.
    '''
    
    class Meta:
        model = Post
        fields = ['id','author','body','edited','created','updated']
        read_only_fields = ['edited']



