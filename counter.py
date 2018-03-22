#!/usr/bin/env python

import logging
import os
import random

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


NUM_SHARDS = 100

class BasicCounter(ndb.Model):
    count = ndb.IntegerProperty(default=0)

# TODO: Generalize this so that we could have multiple counters.
def get_count():
    total = 0
    for counter in BasicCounter.query():
        total += counter.count
    return total

@ndb.transactional
def increment_count():
    shard_index = random.randrange(NUM_SHARDS)
    shard_name = str(shard_index)
    shard_counter = BasicCounter.get_by_id(shard_name)
    if shard_counter is None:
        shard_counter = BasicCounter(id=shard_name)
    shard_counter.count += 1
    shard_counter.put()


class MainPage(webapp2.RequestHandler):
    def get(self):
        # TODO: Increment after to avoid blocking page?
        increment_count()
        flem_count = get_count()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({
            'flem_count': flem_count,
            }))
        logging.debug("Flems counted: %d", flem_count)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
