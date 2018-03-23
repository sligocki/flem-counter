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


class BasicCounter(ndb.Model):
    count = ndb.IntegerProperty(default=0)

# NUM_SHARDS = 100

# # TODO: Generalize this so that we could have multiple counters.
# def get_count():
#     total = 0
#     for counter in BasicCounter.query():
#         total += counter.count
#     return total

# def increment_count():
#     shard_index = random.randrange(NUM_SHARDS)
#     shard_name = str(shard_index)
#     get_and_increment(shard_name)

def get_count(id):
    counter = BasicCounter.get_or_insert(id)
    return counter.count

@ndb.transactional
def get_and_increment(id):
    counter = BasicCounter.get_or_insert(id)
    counter.count += 1
    counter.put()
    return counter.count

FLEM_COUNTER_ID = "flem-counter"

class MainPage(webapp2.RequestHandler):
    def get(self):
        # TODO: Increment after to avoid blocking page?
        flem_count = get_and_increment(FLEM_COUNTER_ID)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({
            'flem_count': flem_count,
            }))
        logging.debug("Flems counted: %d", flem_count)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
