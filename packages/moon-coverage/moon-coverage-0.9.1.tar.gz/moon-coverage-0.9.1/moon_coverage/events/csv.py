"""Events csv file module."""

from collections import UserDict
from pathlib import Path

from .event import AbstractEvent, EventsList, date
from ..misc import logger


warn, _ = logger('EventsFileParser')


class EventsFile(UserDict):
    """Event File object.

    Parameters
    ----------
    fname: str or pathlib.Path
        Input CSV event filename.
    primary_key: str, optional
        Header primary key (default: `name`)
    header: str, optional
        Optional header definition (to be appended at the beging of the file).

    """
    fields, rows = [], []

    def __init__(self, fname, primary_key='name', header=None):
        super().__init__({})

        self.primary_key = primary_key.lower()
        self.header = header
        self.fname = fname

    def __str__(self):
        return self.fname.name

    def __repr__(self):
        n_events = len(self)
        events = f'{n_events} event' + ('s' if n_events > 1 else '')

        if n_events > 0:
            events = f'({date(self.start)} -> {date(self.stop)} | {events})'

            events += '\n - '.join([':', *[
                str(event) for event in self.values()
            ]])

        return f'<{self.__class__.__name__}> {self} {events}'

    def __getitem__(self, key):
        if isinstance(key, slice):
            return list(self.values())[key]

        if key in self:
            return self.data[key]

        if key.lower() in self.fields:
            i = self.fields.index(key.lower())
            return [row[i] for row in self.rows]

        raise KeyError(key)

    @property
    def fname(self):
        """Events filename."""
        return self.__fname

    @fname.setter
    def fname(self, fname):
        """Parse events file."""
        self.__fname = Path(fname)

        if not self.fname.exists():
            raise FileNotFoundError(fname)

        csv_text = (self.header + '\n') if self.header else ''
        csv_text += self.fname.read_text()

        self._parse_csv(csv_text)

    def _parse_csv(self, csv_text):
        """Parse rows content as Events objects."""
        self.fields, self.rows = self._read_csv(csv_text)

        # Extract primary key values
        if self.primary_key not in self.fields:
            raise KeyError(f'Primary key `{self.primary_key}` not found')

        i = self.fields.index(self.primary_key)

        for row in self.rows:
            kwargs = dict(zip(self.fields, row))
            key = row[i]
            k = key.upper()

            if k.endswith('_START') or k.endswith('_DESC'):
                key, _ = key.rsplit('_', 1)  # pop `_START` and `_DESC`

                start = kwargs.pop('event time [utc]')

                kwargs.update({
                    self.primary_key: key,
                    't_start': start,
                    't_end': 'NaT',
                })

            elif k.endswith('_END') or k.endswith('_ASCE'):
                key, _ = key.rsplit('_', 1)  # pop `_END` and `_ASCE`
                stop = kwargs['event time [utc]']

                if key not in self:
                    missing = row[i].replace('_END', '_START').replace('_ASCE', '_DESC')
                    warn.warning(
                        'Found `%s` (at %s) without `%s`.',
                        row[i], stop, missing
                    )
                    continue

                if isinstance(self[key], EventsList):
                    self[key][-1]['t_end'] = stop
                else:
                    self[key]['t_end'] = stop

                continue  # Go to the next row

            if key in self:
                if not isinstance(self[key], EventsList):
                    self[key] = EventsList([self[key]])

                self[key].append(AbstractEvent(key, **kwargs))
            else:
                self[key] = AbstractEvent(key, **kwargs)

    @staticmethod
    def _read_csv(csv_text):
        """Read CSV file."""
        header, *lines = csv_text.splitlines()

        # Parse header columns
        fields = [
            field.lower().replace('#', '').strip() if field else f'column_{i}'
            for i, field in enumerate(header.split(','))
        ]

        # Strip rows content
        rows = [
            tuple(value.strip() for value in line.split(','))
            for line in lines
        ]

        return fields, rows

    @property
    def start(self):
        """Global events start time."""
        return min([event.start for event in self.values()])

    @property
    def stop(self):
        """Global events stop time."""
        return max([event.stop for event in self.values()])
