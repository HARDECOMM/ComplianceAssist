from typing import Dict
from google.adk.runners import InMemoryRunner
from google.adk.events import Event
import asyncio
import logging

from config import settings
from agents.qa import qa_agent
from agents.qc import qc_agent
from agents.regulatory import reg_agent
from agents.pv import pv_agent
from agents.market_access import ma_agent
from agents.search import search_agent
from agents.report import report_agent

log = logging.getLogger("runner")

def make_user_event(text: str) -> Event:
    ev = Event(author="user", invocationId=text)
    object.__setattr__(ev, "role", ev.author)
    object.__setattr__(ev, "parts", [{"text": text}])
    return ev


class RunnerManager:
    def __init__(self):
        self.runners: Dict[str, InMemoryRunner] = {}

    async def init(self):
        self.runners = {
            "QA": InMemoryRunner(agent=qa_agent, app_name=settings.app_name),
            "QC": InMemoryRunner(agent=qc_agent, app_name=settings.app_name),
            "Regulatory": InMemoryRunner(agent=reg_agent, app_name=settings.app_name),
            "PV": InMemoryRunner(agent=pv_agent, app_name=settings.app_name),
            "MarketAccess": InMemoryRunner(agent=ma_agent, app_name=settings.app_name),
            "Search": InMemoryRunner(agent=search_agent, app_name=settings.app_name),
            "Report": InMemoryRunner(agent=report_agent, app_name=settings.app_name),
        }

        await asyncio.gather(*[
            r.session_service.create_session(
                user_id=settings.user_id,
                session_id=settings.session_id,
                app_name=settings.app_name
            )
            for r in self.runners.values()
        ])
        log.info("All sessions initialized.")

    def runner(self, key: str) -> InMemoryRunner:
        return self.runners[key]

    def consume_output(self, result):
        if isinstance(result, str):
            return result
        elif hasattr(result, "__iter__") and not isinstance(result, dict):
            return "".join(str(chunk) for chunk in result)
        return str(result)

manager = RunnerManager()
