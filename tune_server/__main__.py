from __future__ import annotations

import asyncio
import signal
import sys


def main() -> None:
    from tune_server.app import run_server

    async def _run() -> None:
        shutdown_event = asyncio.Event()
        if sys.platform != "win32":
            loop = asyncio.get_running_loop()
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(sig, shutdown_event.set)
        await run_server(shutdown_event)

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass  # Ctrl+C — clean shutdown


if __name__ == "__main__":
    main()
