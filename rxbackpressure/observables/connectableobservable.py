from rx.core import Disposable
from rx.disposables import CompositeDisposable

from rxbackpressure.observable import Observable
from rxbackpressure.subjects.publishsubject import PublishSubject


class ConnectableObservable:

    def __init__(self, source, subject=None):
        super().__init__()
        self.source = source
        self.subject = subject or PublishSubject()
        self.has_subscription = False
        self.subscription = None

    def connect(self, scheduler, subscribe_scheduler):
        """Connects the observable."""

        if not self.has_subscription:
            self.has_subscription = True

            def dispose():
                self.has_subscription = False

            disposable = self.source.unsafe_subscribe(self.subject, scheduler, subscribe_scheduler)
            self.subscription = CompositeDisposable(disposable, Disposable.create(dispose))

        return self.subscription

    def ref_count(self):

        class RefCountObservable(Observable):
            def __init__(self, source):
                self.source = source
                self.count = 0
                self.connectable_subscription = None

            def unsafe_subscribe(self, observer, scheduler, subscribe_scheduler):
                self.count += 1
                should_connect = self.count == 1
                subscription = self.source.subject.unsafe_subscribe(observer, scheduler, subscribe_scheduler)
                if should_connect:
                    self.connectable_subscription = self.source.connect(scheduler, subscribe_scheduler)

                def dispose():
                    subscription.signal_stop()
                    self.count -= 1
                    if not self.count:
                        self.connectable_subscription.signal_stop()

                return Disposable.create(dispose)

        return RefCountObservable(self)
