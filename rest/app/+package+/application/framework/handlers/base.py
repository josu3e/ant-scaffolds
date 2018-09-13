# -*- coding: utf-8 -*-
import falcon
from {{ package }}.application.framework.decorators.service import service_validator


class BaseCollectionHandler:
    service = None

    @service_validator
    def on_get(self, req, resp):
        try:
            resp.media = self.service.find_all()
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = e.__str__()
            resp.status = falcon.HTTP_500


class BaseHandler:
    service = None

    @service_validator
    def on_get(self, req, resp, id):
        try:
            resp.media = self.service.find_by_id(id)
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = e.__str__()
            resp.status = falcon.HTTP_500

    @service_validator
    def on_put(self, req: falcon.Request, resp, id):
        try:
            kwargs = req.media['metadata']
            resp.media = self.service.update(id, **kwargs)
            resp.status = falcon.HTTP_200
        except (Exception, AttributeError) as e:
            resp.media = e.__str__()
            resp.status = falcon.HTTP_500

    @service_validator
    def on_delete(self, req, resp, id):
        try:
            resp.media = self.service.delete(id)
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = e.__str__()
            resp.status = falcon.HTTP_500

    @service_validator
    def on_post(self, req: falcon.Request, resp, id):
        try:
            kwargs = req.media['metadata']
            resp.media = self.response.success(self.service.create(id, **kwargs))
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = e.__str__()
            resp.status = falcon.HTTP_500
