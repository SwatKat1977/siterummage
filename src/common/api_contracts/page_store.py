'''
Copyright (C) 2021 Siterummage
All Rights Reserved.

NOTICE:  All information contained herein is, and remains the property of
Siterummage.  The intellectual and technical concepts contained herein are
proprietary to Siterummage and may be covered by U.K. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from Siterummage.
'''

class WebpageAdd:
    ''' Definition of the webpage/add JSON schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the JSON elements'''
        #pylint: disable=too-few-public-methods

        # -- Top-level json elements --
        toplevel_general = 'general settings'
        toplevel_metadata = 'metadata'

        # -- General Settings sub-elements --
        # -----------------------------------
        general_domain = 'domain'
        general_url_path = 'url path'
        general_read_successful = 'successfully read'
        general_hash = 'hash'

        # -- Metadata sub-elements --
        # ---------------------------
        metadata_title = 'title'
        metadata_abstract = 'abstract'

    Schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'general settings':
            {
                "additionalProperties" : False,
                "properties":
                {
                    'domain':
                    {
                        "type" : "string"
                    },
                    'url path':
                    {
                        "type" : "string"
                    },
                    'hash':
                    {
                        "type" : "string"
                    },
                    'successfully read':
                    {
                        "type" : "boolean"
                    }
                },
                "required" : ['domain', 'url path', 'hash',
                              'successfully read']
            },
            'metadata':
            {
                "additionalProperties" : False,
                "properties":
                {
                    'title':
                    {
                        "type" : "string"
                    },
                    'abstract':
                    {
                        "type" : "string"
                    },
                },
                "required" : ['title', 'abstract']
            }
        },
        "required" : ['general settings', 'metadata']
    }

class WebpageDetails:
    ''' Definition of the webpage/details JSON schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the JSON elements'''
        #pylint: disable=too-few-public-methods

        # -- General Settings sub-elements --
        # -----------------------------------
        domain = 'domain'
        url_path = 'url path'

    Schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'domain':
            {
                "type" : "string"
            },
            'url path':
            {
                "type" : "string"
            }
        },
        "required" : ['domain', 'url path']
    }

class WebpageDetailsResponse:
    ''' Definition of the webpage/details response JSON schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the JSON elements'''
        #pylint: disable=too-few-public-methods

        read_successful = 'read successful'
        title = 'title'
        abstract = 'abstract'
        last_scanned = 'last scanned'
        page_hash = 'hash'

    Schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'title':
            {
                "type" : "string"
            },
            'abstract':
            {
                "type" : "string"
            },
            'read successful':
            {
                "type" : "boolean"
            },
            'last scanned':
            {
                "type" : "boolean"
            },
            'hash':
            {
                "type" : "string"
            }
        },
        "required" : ['title', 'abstract', 'read successful', 'last scanned']
    }
