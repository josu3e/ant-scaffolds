# -*- coding: utf-8 -*-
from {{ package }}.application.framework import FalconApi
from dotenv import load_dotenv


class App:
    def __init__(self):
        load_dotenv('config/config.env')
        self.api = FalconApi().api
