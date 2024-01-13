===nodes===
d0 Manager .
  d0s0 Manager .
    d0s0c0 REST API .
    d0s0c1 NATS Client .

d1 Broker .
  d1s0 Broker .
    d1s0 NATS .

d2 Outer DB .
  d2s0 Outer DB .
    d2s0c0 PostgreSQL .

d3 Frontend!nc .
  d3s3 Frontend .
    d3s3c3 ReactJS .

d4 Analytics .
  d4s1 Clusterization .
    d4s1c0 Computational Module .
    d4s1c1 NATS Client .
  d4s2 Storage .
    d4s1c2 SQLite .


| {
|     name: str
|     message: str
|     protocol: Literal["HTTP", "NATS", "SQL", "gRPC"] = "HTTP"
|     method: Optional[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT"]] = None
|     url: str = None
|     status: Literal["200", "201", "202", "204", "400", "401", "403", "404", "500", "502", "503", "504"] | None = None
|     subject: str = None
|     comment: str = None
| }
===edges===
d3s3c3 -> d0s0c0 {m0, }

