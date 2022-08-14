from rest_framework import mixins
from rest_framework.generics import (
    ListCreateAPIView as BaseListCreateAPIView,
    ListAPIView as BaseListAPIView,
    GenericAPIView
)

from utils.mixins import ResponseMixin, ResponseQueryFilterMixin


class ListAPIView(ResponseQueryFilterMixin, BaseListAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return self.get_response(data=serializer.data)


class ListCreateAPIView(ResponseQueryFilterMixin, BaseListCreateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.get_response(status_code=201)
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return self.get_response(data=serializer.data)


class UpdateDeleteAPIView(ResponseMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericAPIView):
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        return self.get_response(status_code=200)
    
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return self.get_response(status_code=200)
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return self.get_response(status_code=200)


class DetailAPIView(ResponseMixin, GenericAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer([instance], many=True)
        return self.get_response(data=serializer.data)
