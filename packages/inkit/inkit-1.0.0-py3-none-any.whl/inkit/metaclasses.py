import re
import json

from inkit.exceptions import InkitException


class ProductMetaclass(type):

    def __init__(cls, classname, superclasses, attr_dict):
        super().__init__(classname, superclasses, attr_dict)
        for handler in cls._main_resource.handlers:  # noqa
            setattr(cls, handler, getattr(cls._main_resource, handler))  # noqa

    def __call__(cls, *args, **kwargs):
        raise InkitException(f'Class {cls.__name__} is not instantiable')


class ResourceBuilderMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        mcs.set_validator(attr_dict)
        mcs.set_handlers(attr_dict)
        return super().__new__(mcs, classname, superclasses, attr_dict)

    @staticmethod
    def set_validator(attr_dict):
        def check_request_data(path, http_method, data):
            request_data = {
                'path': path,
                'http_method': http_method
            }
            if http_method.upper() in ('GET', 'DELETE') and data:
                request_data.update(params={
                    key.replace('_', '-', 1) if key.startswith('data_') else key: val
                    for key, val in data.items()
                })

            if http_method.upper() in ('POST', 'PATCH'):
                request_data.update(data=json.dumps(data))

            return request_data

        attr_dict[check_request_data.__name__] = staticmethod(check_request_data)

    @classmethod
    def set_handlers(mcs, attr_dict):
        handlers = []
        for route in attr_dict['routes']:
            attr_dict[route.sdk_method_name] = mcs.handlers_factory(
                resource_path=route.path,
                http_method=route.http_method,
                doc=route.doc
            )
            handlers.append(route.sdk_method_name)
        attr_dict['handlers'] = handlers

    @staticmethod
    def handlers_factory(resource_path, http_method, doc):
        if re.search(r'/{id}', resource_path):
            def handler(self, entity_id, **kwargs):
                request_data = self.check_request_data(
                    path=resource_path.format(id=entity_id),
                    http_method=http_method,
                    data=kwargs
                )
                return self.client.send(**request_data)
            handler.__doc__ = doc
            return handler

        else:
            def handler(self, **kwargs):
                request_data = self.check_request_data(
                    path=resource_path,
                    http_method=http_method,
                    data=kwargs
                )
                return self.client.send(**request_data)

            handler.__doc__ = doc
        return handler
