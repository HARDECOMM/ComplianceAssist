import asyncio
import logging
import re
from runner import manager
from orchestrator import orchestrator

log = logging.getLogger("main")

async def app():
    await manager.init()
    log.info("Runner manager initialized.")
    while True:
        q = input("\nEnter your query (or 'quit'): ").strip()
        if q.lower() == "quit":
            break
        try:
            result = await orchestrator(q)
            print("\nCompliance Report\n")
            print(result)
        except Exception as e:
            msg = str(e)
            # Handle quota exceeded (429) with retry
            if "RESOURCE_EXHAUSTED" in msg or "Too Many Requests" in msg:
                print("⚠️ Gemini API quota exceeded.")
                # Try to extract retry delay from error message
                delay_match = re.search(r"retry in (\d+)", msg)
                delay = int(delay_match.group(1)) if delay_match else 40
                print(f"⏳ Waiting {delay} seconds before retry...")
                await asyncio.sleep(delay)
                try:
                    result = await orchestrator(q)
                    print("\nCompliance Report\n")
                    print(result)
                except Exception as e2:
                    print(f"Retry failed: {e2}")
            elif "UNAVAILABLE" in msg:
                print("⚠️ Gemini service is temporarily overloaded. Try again later.")
            else:
                print(f"Unexpected error: {e}")
                log.exception("Unhandled error during orchestrator run")

if __name__ == "__main__":
    try:
        asyncio.run(app())
    except KeyboardInterrupt:
        log.info("Shutting down gracefully.")
