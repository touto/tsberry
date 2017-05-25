import os

# bit resolution of DAC
DAC_RESOLUTION = 8

# upper threshold for temperature color control
TEMP_UPPER_THRESHOLD = 30

# lower threshold for temperature color control
TEMP_LOWER_THRESHOLD = 20

# default brightness in percent for temperature control mode
TEMP_DEFAULT_BRIGHTNESS = 100

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

IF_MATCH = False

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
people = {
    # 'title' tag used in item links.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'lastname'
    },

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'schema': {
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            # talk about hard constraints! For the purpose of the demo
            # 'lastname' is an API entry-point, so we need it to be unique.
            'unique': True,
        },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["author", "contributor", "copy"],
        },
        # An embedded 'strongly-typed' dictionary.
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },
        'born': {
            'type': 'datetime',
        },
    }
}

works = {
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name, and use it as the item_title.
    #'item_title': 'work',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'people',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
    }
}

bulbs = {
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name, and use it as the item_title.
    #'item_title': 'work',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'area': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'areas',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
        'description': {
            'type': 'string',
        },
        'colors': {
            'type': 'dict',
            'schema': {
                'red': {'type': 'integer'},
                'green': {'type': 'integer'},
                'blue': {'type': 'integer'},
                'white': {'type': 'integer'},
            },
        },
        'remote': {
            'type': 'boolean',
            'default' : False,
            'required' : True,
        },
        'address': {
            'type': 'string',
            'required' : True,
        },
    }
}

areas = {
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name, and use it as the item_title.
    #'item_title': 'work',
    
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    
    'schema': {
        'title': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'description': {
            'type': 'string',
        },
        'mode': {
             'type': 'string',
        },
        'member': {
            'type': 'objectid',
            #'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'bulbs',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
        'colors': {
            'type': 'dict',
            'schema': {
                'red': {'type': 'integer'},
                'green': {'type': 'integer'},
                'blue': {'type': 'integer'},
                'white': {'type': 'integer'},
            },
        },
    }
}


# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'people': people,
    'works': works,
    'areas': areas,
    'bulbs': bulbs,
}

# validate variables

# brightness must be between 0 and 100
#if not 0 <= TEMP_DEFAULT_BRIGHTNESS <= 100:
#    print "TEMP_DEFAULT_BRIGHTNESS error"
try:
    if not 0 <= TEMP_DEFAULT_BRIGHTNESS <= 100:
        raise ValueError('invalid value for TEMP_DEFAULT_BRIGHTNESS in %s\nvalue must be between 0 and 100' % __file__)
    if TEMP_LOWER_THRESHOLD > TEMP_UPPER_THRESHOLD:
                raise ValueError('invalid value for temperature thresholds in %s\nTEMP_LOWER_THRESHOLD must be lower than TEMP_UPPER_THRESHOLD:' % __file__)
except ValueError as err:
    print err
    raise SystemExit

