from rx.core import Disposable

from rxbackpressure.observable import Observable
from rxbackpressure.observer import Observer
from rxbackpressure.scheduler import Scheduler


class TestObservable(Observable):
    def __init__(self):
        self.observer = None

    def on_next(self, val):
        return self.observer.on_next(val)

    def on_error(self, exc):
        return self.observer.on_error(exc)

    def on_completed(self):
        return self.observer.on_completed()

    def unsafe_subscribe(self, observer: Observer, scheduler: Scheduler, subscribe_scheduler: Scheduler):
        self.observer = observer
        return Disposable.empty()