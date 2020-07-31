# Error handling with gRPC examples
## Protocols buffers
> Simple language neutral and platform-neutral Interface definition language.
```go
// Hello World
service Greeter { // a Service Method
  rpc sayHello (HelloRequest) returns (HelloReply){}
}

// Who to greet?
message HelloRequest { // a request message type
  string name = 1;
  string locale = 2;
}

// The greeting
message HelloReply { // a response message type
  string greeting = 1;
}
```

- The protocol buffer compiler generates codes that has
  - remote interface stub for Client to call with the methods
  - abstract interface for Server code to implement
- Protocol buffer code will populate, serialize, and retrieve our request and response message types.

- Status Error : yes, no, maybe
  - OK
  - CANCELLED
  - UNKNOWN
  - INVALID_ARGUMENT
  - DEADLINE_EXCEEDED
  - NOT_FOUND
  - ALREADY_EXISTS
  - PERMISSION DENIED
  - UNAUTHENTICATED
  - RESOURCE_EXHAUSTED
  - FAILED_PRECONDITION
  - ABORTED
  - OUT_OF_RANGE
  - UNIMPLEMENTED
  - INTERNAL
  - UNAVAILABLE
  - DATA_LOSS
 
 ## Reference
 - https://www.usenix.org/sites/default/files/conference/protected-files/srecon19apac_slides_sheerin.pdf
