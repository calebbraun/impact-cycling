#!/usr/bin/env python
# -*- coding: utf-8 -*-
# impact-cycling (c) Caleb Braun

from impact_cycling.wsgi import app
app.run(port=app.config['PORT'])
