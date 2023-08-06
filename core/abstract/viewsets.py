from rest_framework import viewsets
from rest_framework import filters

class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    # filter_backends: this sets the default filter backends
    ordering_fields = ['updated','created']
    # ordering_fields : This list contains fields that can be user as ordering Parameters when making a request
    ordering = ['-updated']
    # ordering : this tell Django rest in which order to send many objects as a response.In this case, all responses will be ordered
    # the most recently updated