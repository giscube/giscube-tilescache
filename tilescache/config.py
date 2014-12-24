from TileCache.Config import Config


class DjangoConfig(Config):

    def __init__(self, *args, **kwargs):
        super(DjangoConfig, self).__init__('django', *args, **kwargs)

        self.metadata = {}
        self.layers = {}

    def read_config(self, service):
        for layer in service.layers.all():
            print layer.name
            l = {}
            for attr in ('name', 'debug', 'type', 'url', 'extension',
                         'layers', 'levels'):
                if getattr(layer, attr):
                    l[attr] = getattr(layer, attr)
            l['srs'] = 'EPSG:%s' % layer.projection
            l['tms_type'] = 'google'
            if layer.bbox:
                l['bbox'] = map(float, layer.bbox.split(','))
            if layer.resolutions:
                l['resolutions'] = map(float, layer.resolutions.split(','))
            print l
            self.layers[layer.name] = self._load_layer(**l)
