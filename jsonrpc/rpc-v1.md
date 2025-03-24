# JSON-RPC 1.0 Specifications ¶

The specifications should provide the developer with the information needed to implement the protocol.

**NOTE:** The  JSON-RPC 2.0 Specification has been published.

## Overview ¶

JSON-RPC is a lightweight remote procedure call protocol. Its designed to be simple!

The general mechanism consists of two peers establishing a data connection. During the lifetime of a connection, peers may invoke methods provided by the other peer. To invoke a remote method, a request is sent. Unless the request is a notification it must be replied to with a response.

## 1.1 Request (method invocation) ¶

A remote method is invoked by sending a request to a remote service. The request is a single object serialized using  JSON.

It has three properties:

*   **method** - A String containing the name of the method to be invoked.
*   **params** - An Array of objects to pass as arguments to the method.
*   **id** - The request id. This can be of any type. It is used to match the response with the request that it is replying to.

## 1.2 Response ¶

When the method invocation completes, the service must reply with a response. The response is a single object serialized using  JSON.

It has three properties:

*   **result** - The Object that was returned by the invoked method. This must be null in case there was an error invoking the method.
*   **error** - An Error object if there was an error invoking the method. It must be null if there was no error.
*   **id** - This must be the same id as the request it is responding to.

## 1.3 Notification ¶

A notification is a special request which does not have a response. The notification is a single object serialized using  JSON.

It has the same properties as the request object with one exception.

*   **id** - Must be null.

## 2.1 JSON-RPC over stream connections ¶

The specifications do not require a certain transport protocol. The use of TCP/IP socket streams is encouraged. The serialized request and response objects are sent to the peers through the byte streams.

Requests and responses may be sent to a peer at any time. The peer must respond to each request unless it is a notification. A response may only be sent in reply to a request.

Closing the connection between peers must raise an exception for all unanswered requests on each peer. Non-valid requests or responses must result in closing the connection.

## 2.2 JSON-RPC over HTTP ¶

With some limitation, HTTP requests can be used as a transport for communicating between peers.

A communication between peers, one being an HTTP client the other an HTTP server, may span multiple HTTP requests. A client side peer may send one or more requests, notifications or responses to its peer by sending an HTTP POST request containing all serialized objects.

The server side peer must reply with responses to all requests sent and may send requests or notifications of its own. The client side peer must reply to requests received by sending another HTTP POST.

To give the serverside peer a chance to send messages to the client side peer, the client side peer may reopen communication by sending an empty HTTP POST.

A non-valid request must result in closing the connection. A non-valid response must raise an exception for all unanswered requests on the client. Closing a connection must raise an exception for all unanswered requests on the client.

FIXME: Describe/define how sessions are handled, as there is no implicit session formed by a TCP-connection.

## 3. JSON Class hinting ¶

There are only simple data types defined in JSON. To overcome this problem in a JSON compatible way a special property for objects is introduced.  
{"__jsonclass__":["constructor", [param1,...]], "prop1": ...}  
The object is then instantiated using the constructor, passing in the parameters. Once constructed the properties (prop1, ...) will be applied.

## 4. Communication Examples ¶

--data sent to service  
<-- data coming from service

*   service.echo("Hello JSON-RPC")

```
--{ "method": "echo", "params": ["Hello JSON-RPC"], "id":
1}
<-- { "result": "Hello JSON-RPC", "error": null, "id": 1}
```

*   multiple request responses

This example shows parts of a communication from an example chat application. The chat service sends notifications for each chat message the client peer should receive. The client peer sends requests to post messages to the chat and expects a positive reply to know the message has been posted.

```
...

--{"method": "postMessage", "params": ["Hello all!"], "id": 99}
<-- {"result": 1, "error": null, "id": 99}
<-- {"method": "handleMessage", "params": ["user1", "we were just talking"], "id":
null}
<-- {"method": "handleMessage", "params": ["user3", "sorry, gotta go now, ttyl"], "id":
null}
--{"method": "postMessage", "params": ["I have a question:"], "id": 101}
<-- {"method": "userLeft", "params": ["user3"], "id": null}
<-- {"result": 1, "error": null, "id": 101}
...
```
