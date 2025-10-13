:blogpost:
   true

:date:
   2025-10-13

:tags:
   ASGI, Kafka, Event-Driven

:category:
   python

###########################################
 Best Header You Probably Haven't Heard Of
###########################################

I'm now going to discuss something I have referred to as the **"create problem"**.

What is the create problem?

Well this is how I would describe it:

-  You have a command in an event-driven system that creates some kind of resource (An order, for example)
-  You have used the `Return Address`_ pattern, when you get a reply you know that reply is for a request you asked
-  You need to be able to tell which specific request gave you a specific reply

In HTTP this would be easy, you already know because you are making the request. In an event-driven architecture you
don't. So what can you do:

#. You add something to the payload to keep track (Nope!)
#. You add a header to the request, and return a header in the response

We are going to go with 2!

*************************
 What To Use What To Use
*************************

We need to have some kind of id to keep of our request. The header you may reach for is ``X-Request-Id``.

In your request message you simply add the ``X-Request-Id`` header:

.. literalinclude:: header/createOrder.json

.. note::

   These examples are in the form of a kcat_ JSON envelope

Then in your reply you add the the ``X-Request-Id``:

.. literalinclude:: header/createOrder.reply.json
   :name: createOrder.reply

Now when your system receives the reply it know which request to create was replied to. Good that works!

*******************
 X-Echo-Set-Header
*******************

Now time for another header, the ``X-Echo-Set-Header``. This is the header you probably have never heard of, if you
search public code in Sourcegraph you will find less then ten repositories where it occurs: `context:global
"X-Echo-Set-Header" <https://sourcegraph.com/search?q=context:global+%22X-Echo-Set-Header%22>`_.

In essence ``X-Echo-Set-Header`` is a header with a header as its value. Meaning if you had the header
``X-Echo-Set-Header: X-Foo: value1`` your response would have the header ``X-Foo: value1``. As defined in
:RFC:`2616#section-4.2` you can have multiple of the same headers, so you could set multiple response headers.

If you had a HTTP server that supported the ``X-Echo-Set-Header`` the following request:

.. code::

   curl --location 'http://0.0.0.0:8000/orders' \
   --header 'x-echo-set-header: x-request-id: 74cb6636-c6a1-4f0e-827a-e6415969dfa2' \
   --header 'content-type: application/json' \
   --include \
   --data '{"skus":["id-17236"]}'

Would give you the following response:

.. code::

   HTTP/1.1 200 OK
   date: Mon, 13 Oct 2025 08:12:03 GMT
   server: uvicorn
   content-length: 65
   content-type: application/json
   x-request-id: 74cb6636-c6a1-4f0e-827a-e6415969dfa2

   {"id":"40e3078c-1139-486c-be8c-b277fd434d3e","skus":["id-17236"]}

This maps very nicely to the Request-Reply_ pattern, you can simply add the ``X-Echo-Set-Header`` to the request
message:

.. literalinclude:: header/createOrder.echoSetHeader.json

This example would give you the same createOrder.reply_ as before.

*********
 But Why
*********

In a word, Flexibility!

Now you have a way to send more data in the reply, without relying on the replier having to understand how to. This
means multiple applications can make a requests with different response data.

This extensibility in an event-driven workflow is incredibly useful!

Time for a contrived example:

-  You have a Factory that produces some toys they use screws to makes the toys
-  When the amount of screws in the inventory changes an event is published
-  When the amount of screws they have in the Factory goes below a certain amount they want to order new ones from a
   wholesaler
-  When the order has been made they want to update the Factory inventory to mark the screws as pending delivery

In order the process would be something like this:

#. The amount of screws in the inventory changes, an event is published to notify this change, and the amount of screws
   has dropped below the order threshold
#. Your system makes a request to the wholesaler, looking up the SKU (Stock keeping unit), mapping it to the SKU of the
   wholesaler
#. The order response is received, it contains the wholesalers SKU so you look up the mapping to your SKU
#. You make a request to update your inventory with the pending order using the inventories SKU

You'll notice in step 3 that we are looking up the SKU again. We have a mechanism now so we don't need to do that. If we
use ``X-Echo-Set-Header`` we can put the mapping in a response header: ``x-echo-set-header: sku-mapping:
{"wholesaler_id":"WHLS-67387","inventory_id":"INV-1312"}``, now we will receive the mapping in the response message.

You have now reduced the number of calls your system need to make. The systems can be independent, or have outages, and
you would still be able to make the request to update the inventory at the end. In the best case you would send the SKU
mapping along with the notification event where the screws changes, and you would never have to do a lookup!

*******************
 An Implementation
*******************

.. _kcat: https://github.com/edenhill/kcat

.. _request-reply: https://www.enterpriseintegrationpatterns.com/patterns/messaging/RequestReply.html

.. _return address: https://www.enterpriseintegrationpatterns.com/patterns/messaging/ReturnAddress.html
