import os
import atexit
from typing import Tuple
from flask import Flask
from dotenv import load_dotenv
from slack.web.client import WebClient
from slackeventsapi import SlackEventAdapter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

load_dotenv()


def create_app() -> Flask:
    return Flask(__name__)


def create_slack_client() -> WebClient:
    return WebClient(token=os.environ.get('SLACK_TOKEN'))


def create_slack_event_adapter(app: Flask) -> SlackEventAdapter:
    return SlackEventAdapter(os.environ.get('SLACK_SIGNING_SECRET'), "/slack/events", app)


def create_background_scheduler() -> BackgroundScheduler:
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    scheduler = BackgroundScheduler(jobstores=jobstores)

    return scheduler


def init_services() -> Tuple[Flask, WebClient, SlackEventAdapter, BackgroundScheduler]:
    app = create_app()
    client = create_slack_client()
    slack_events_adapter = create_slack_event_adapter(app)
    scheduler = create_background_scheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    return (app, client, slack_events_adapter, scheduler)


app, client, slack_events_adapter, scheduler = init_services()
