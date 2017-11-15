# Performing operations on hot observables with back-pressure results in better memory handling.

from rx import Observable

from rxbackpressure.subjects.controlledsubject import ControlledSubject

# create some buffered subjects
s1 = ControlledSubject()
s2 = ControlledSubject()
s3 = ControlledSubject()

# flat map operation
s2.flat_map(lambda v1, idx: s1.map(lambda v2: v2*v1)) \
    .to_observable() \
    .filter(lambda v: 800 < v) \
    .subscribe(print, on_completed=lambda: print('completed'))

# zip operation
s1.zip(s3, lambda v1, v2: (v1, v2)) \
    .to_observable() \
    .filter(lambda v: 90 < v[0]) \
    .subscribe(print, on_completed=lambda: print('completed'))

# trigger hot observables
Observable.range(0, 100).subscribe(s1)
Observable.range(0, 10).subscribe(s2)
Observable.range(0, 100).subscribe(s3)