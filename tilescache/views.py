import os
import time
import subprocess

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

import requests
from requests.exceptions import ConnectionError
from tilescache.models import Service
from tilescache.config import DjangoConfig

from TileCache.Service import Service as TCService

from django.core.cache import cache


SERVICE_CACHE = {}


class TilescacheView(View):
    def get(self, request):
        path_info = request.path_info.split('/')
        service_name = path_info[2]
        path_info = '/%s' % '/'.join(path_info[3:])

        cache_key = 'tilescache-%s' % service_name
        #theService = cache.get(cache_key)
        theService = SERVICE_CACHE.get(cache_key, None)

        if not theService:
            print 'rebuild service %s' % service_name
            service = get_object_or_404(Service, name=service_name)
            cfg = DjangoConfig()
            cfg.read_config(service)
            configs = [cfg]
            layers = TCService.LayerConfig()
            for conf in configs:
                layers.update(conf)
    
            theService = TCService(configs, layers)
            from TileCache.Caches.Disk import Disk
            theService.cache = Disk(base='/tmp/tilescache')

            #cache.set(cache_key, theService, 10)
            SERVICE_CACHE[cache_key] = theService

        fields = request.GET
        req_method = request.method
        host = request.META.get('HTTP_HOST', 'localhost')
        format, image = theService.dispatchRequest(fields, path_info,
                                                   req_method, host)

        response = HttpResponse(image, content_type=format)
        return response
