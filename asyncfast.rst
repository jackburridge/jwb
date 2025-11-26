###########
 AsyncFast
###########

AsyncFast_ is a modern, event framework for building event APIs with Python, based on standard Python type hints. This
is my current project to help develop well-documented asynchronous APIs.

I've taken ideas from ASGI_ (creating my own specification AMGI_), and FastAPI_, and used them to allow for the
development of asynchronous APIs to be fast, and portable.

Core aims:

-  **Portable**: Following AMGI_ should allow for implementations of any protocol, applications should be able run
   anywhere regardless of compute. Running in Lambda_ should be no more difficult than running on EC2_
-  **Standards-based**: Based on AsyncAPI_, and `JSON Schema`_. The framework should allow for easy documentation
   generation
-  **Clean Implementation**: Each protocol should be implemented well, this means easy to use, and as optimal as
   possible

***********
 Protocols
***********

At the moment there are base implementations for the following protocols, these are all working AMGI_ servers:

:Kafka:
   amgi-aiokafka_ is a basic Kafka_ sever implementation

:MQTT:
   amgi-paho-mqtt_ is a basic MQTT_ sever implementation

:Redis:
   amgi-redis_ is a basic Redis_ server implementation, soon with support for `Redis Streams`_

:SQS:
   amgi-aiobotocore_ contains a basic SQS_ sever implementation. amgi-sqs-event-source-mapping_ allows you to run an
   application in Lambda_, with it translating the SQS Lambda event to the necessary AMGI_ calls. This was my target for
   proof of viability (and I must say it worked quite well)

*********
 Example
*********

Building an application should be as simple as any micro framework, if you've used Flask_, or FastAPI_ this shouldn't look too dissimilar:

.. literalinclude:: examples/lifespan.py

***************
 Documentation
***************

Documentation should be easy, this is why the framework has it built in:


.. code::

    $ asyncfast asyncapi lifespan:app
    {
      "asyncapi": "3.0.0",
      "info": {
        "title": "AsyncFast",
        "version": "0.1.0"
      },
      "channels": {
        "HandleOrder": {
          "address": "order",
          "messages": {
            "HandleOrderMessage": {
              "$ref": "#/components/messages/HandleOrderMessage"
            }
          }
        }
      },
      "operations": {
        "receiveHandleOrder": {
          "action": "receive",
          "channel": {
            "$ref": "#/channels/HandleOrder"
          }
        }
      },
      "components": {
        "messages": {
          "HandleOrderMessage": {
            "payload": {
              "$ref": "#/components/schemas/Order"
            },
            "bindings": {
              "kafka": {
                "key": {
                  "type": "string"
                }
              }
            }
          }
        },
        "schemas": {
          "Item": {
            "properties": {
              "sku_id": {
                "title": "Sku Id",
                "type": "string"
              },
              "amount": {
                "title": "Amount",
                "type": "integer"
              }
            },
            "required": [
              "sku_id",
              "amount"
            ],
            "title": "Item",
            "type": "object"
          },
          "Order": {
            "properties": {
              "items": {
                "items": {
                  "$ref": "#/components/schemas/Item"
                },
                "title": "Items",
                "type": "array"
              },
              "status": {
                "title": "Status",
                "type": "string"
              }
            },
            "required": [
              "items",
              "status"
            ],
            "title": "Order",
            "type": "object"
          }
        }
      }
    }


It will generate documentation following the AsyncAPI_ spec.

.. _amgi: https://amgi.readthedocs.io/en/latest/

.. _amgi-aiobotocore: https://pypi.org/project/amgi-aiobotocore/

.. _amgi-aiokafka: https://pypi.org/project/amgi-aiokafka/

.. _amgi-paho-mqtt: https://pypi.org/project/amgi-paho-mqtt/

.. _amgi-redis: https://pypi.org/project/amgi-redis/

.. _amgi-sqs-event-source-mapping: https://pypi.org/project/amgi-sqs-event-source-mapping/

.. _asgi: https://asgi.readthedocs.io/en/latest/

.. _asyncapi: https://www.asyncapi.com/

.. _asyncfast: https://asyncfast.readthedocs.io/en/latest/

.. _ec2: https://aws.amazon.com/ec2/

.. _fastapi: https://fastapi.tiangolo.com/

.. _json schema: https://json-schema.org/

.. _kafka: https://kafka.apache.org/

.. _lambda: https://aws.amazon.com/lambda/

.. _mqtt: https://mqtt.org/

.. _pydantic: https://docs.pydantic.dev/

.. _redis: https://redis.io/

.. _redis streams: https://redis.io/docs/latest/develop/data-types/streams/

.. _sqs: https://aws.amazon.com/sqs/

.. _flask: https://flask.palletsprojects.com/en/stable/
