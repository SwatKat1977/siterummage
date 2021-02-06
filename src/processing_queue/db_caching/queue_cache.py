'''
Copyright 2021 Siterummage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import threading
from .cached_queue_entry import CachedQueueEntry, LinkType
from common.logger import LogType

class QueueCache:
    __slots__ = ['_config', '_db_interface', '_logger', '_lock',
                 '_processing_queue', '_queue_cache']

    @property
    def size_all_queue(self):
        return len(self.queue_size)

    def __init__(self, db_interface, configuration, logger, processing_queue):
        self._config = configuration
        self._db_interface = db_interface
        self._logger = logger
        self._queue_cache = []
        self._processing_queue = processing_queue
        self._lock = threading.Lock()

        self._logger.log(LogType.Info, 'Caching processing queue...')

        cache_size = self._config.db_settings.cache_size

        entry_count, cached_count = self._load_queue(cache_size,
                                                     get_cached=True)

        self._logger.log(LogType.Info, f"-> Read {entry_count} of which" + \
            f" {cached_count} were previously cached")

        if cached_count:
            recache_size = cache_size - (entry_count - cached_count)

            self._logger.log(LogType.Info, "-> Attempting to cache" + \
                f" {recache_size} more record")

            entry_count, _ = self._load_queue(recache_size)
            self._logger.log(LogType.Info, f"-> Read {entry_count} more" + \
                " entries have been cached")

    def _load_queue(self, cache_size, get_cached=False):

        entry_count = 0
        cached_count = 0
        id_list = []

        entries = self._db_interface.get_queue_cache(cache_size, get_cached)

        for entry in entries:
            try:
                link_type = LinkType(entry['link_type'])

            except ValueError:
                err = f"Cannot cache database entry '{entry['id']}' due" + \
                    f" to link type ({entry['link_type']}) being invalid"
                self._logger.log(LogType.Error, err)
                continue

            cache_entry = CachedQueueEntry(entry['id'], entry['url'],
                                           entry['insertion_date'], link_type)
            self._queue_cache.append(cache_entry)

            id_list.append(entry['id'])

            entry_count += 1

            if entry['cached']:
                cached_count += 1

        self._db_interface.set_ids_to_cached(id_list)

        return entry_count, cached_count

    def pop_to_processing(self):

        with self._lock:
            try:
                cached_entry = self._queue_cache.pop(0)
            except IndexError:
                return None

            self._processing_queue.add_url(cached_entry)
            return cached_entry
