import asyncio
import aiohttp
from typing import List, Dict, Any

async def fetch_data(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Dict[str, Any]:
    """
    Fetches data from a single URL, bounded by a concurrency semaphore.
    Includes built-in timeout and error handling for production resilience.
    """
    async with semaphore:
        try:
            # Enforce a strict timeout to prevent hanging connections
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            # In a real pipeline, this would route to a Dead Letter Queue (DLQ)
            return {"url": url, "error": str(e)}

async def fetch_all_endpoints(urls: List[str], max_concurrent: int = 10) -> List[Dict[str, Any]]:
    """
    Asynchronously fetches data from multiple APIs while strictly adhering to rate limits.
    Demonstrates Connection Pooling and Semaphore usage.
    """
    if not urls or max_concurrent <= 0:
        return []

    # The semaphore acts as a bouncer, only letting 'max_concurrent' requests execute at once.
    semaphore = asyncio.Semaphore(max_concurrent)
    
    # Utilizing a single ClientSession enables connection pooling (massive performance boost)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, semaphore) for url in urls]
        
        # gather schedules and executes all tasks concurrently, maintaining order
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return list(results)
