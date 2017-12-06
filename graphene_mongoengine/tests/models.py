
from mongoengine import (
    Document, EmbeddedDocument, DynamicEmbeddedDocument, DynamicDocument,
    StringField, IntField, BooleanField, DateTimeField,
    ListField, DictField,
    EmbeddedDocumentField
)

class Crontab(EmbeddedDocument):

    minute = StringField(default='*', required=True, description='CRON minute expression')
    hour = StringField(default='*', required=True, description='CRON hour expression')
    day_of_week = StringField(default='*', required=True, description='CRON da of week expression')
    day_of_month = StringField(default='*', required=True, description='CRON day of month expression')
    month_of_year = StringField(default='*', required=True, description='CRON month expression')


class Interval(EmbeddedDocument):
    
    PERIODS = ('days', 'hours', 'minutes', 'seconds', 'microseconds')

    every = IntField(min_value=0, default=0, required=True, description='Interval value')
    period = StringField(choices=PERIODS, description='Interval period')


class PeriodicTask(Document):
    """mongo database model that represents a periodic task"""


    name = StringField(unique=True, required=True, description='Periodic Task name')
    task = StringField(required=True, description='Task to execute with provided arguments')
    description = StringField(description='Task description')

    enabled = BooleanField(default=False, description='Whether the scheduled task should run when the conditions are met')

    interval = EmbeddedDocumentField(Interval, description='Interval based schedule')
    crontab = EmbeddedDocumentField(Crontab, description='Cron expression schedule')

    args = ListField(description='List of task arguments (*args)')
    kwargs = DictField(description='Dict with task keyword arguments (**kwargs)')

    queue = StringField(description='Queue to execute the task on?')
    exchange = StringField(description='')
    routing_key = StringField(description='Task routing key')
    soft_time_limit = IntField(description='')

    expires = DateTimeField(description='Date when the task expires (no longer ticks)')
    start_after = DateTimeField(description='Date to start processing ticks after')
    last_run_at = DateTimeField(description='Last time the task was run')

    total_run_count = IntField(min_value=0, default=0, description='Number of times the task was executed')
    max_run_count = IntField(min_value=0, default=0, description='Max number of times the task can run before expiring')

    date_changed = DateTimeField(description='Last modification date')
    run_immediately = BooleanField(description='Whether the task should run as soon as created?')

