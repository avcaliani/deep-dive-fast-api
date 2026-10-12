# Web Sockets

The Dunder Mifflin PA System: an intercom chat and a Schrute Bucks ticker, both over FastAPI WebSockets.

## How to run

```bash
cd snippets/web-sockets
uv run uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`. The page has two panels, each with a connection lamp and auto-reconnect:

- `WS /ws/intercom`: send a line, a random employee answers with a catchphrase and the receipt time. Send `close` to hang up.
- `WS /ws/ticker`: every 1, 3 or 5 seconds a `check-in` or `redeem` event arrives. The page sums `schrute_bucks` and calls a fire drill every 7th event.

## Example

Terminal client (nothing installed globally):

```bash
uv run --with websockets python -m websockets ws://127.0.0.1:8000/ws/intercom
```

```text
Connected to ws://127.0.0.1:8000/ws/intercom.
< Stanley: "Did I stutter?" (heard "Is it Pretzel Day?" at 21:46:27 UTC)
Connection closed: 1000 (OK).
```

Ticker (same client, `/ws/ticker`), one JSON per message:

```text
< {"socket_id":"783840d4-5426-4583-a0f6-1f1e6d8238b4","count":1,"type":"check-in","employee":"Michael","detail":"😡 angry","schrute_bucks":5,"at":"21:46:31"}
```

`schrute_bucks` is a delta: `+5` per check-in, minus the item cost per redeem.

## References

- [FastAPI: WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Starlette: WebSockets](https://www.starlette.dev/websockets/)
