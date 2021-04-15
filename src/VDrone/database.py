# **********************************************************************************************************************
#   FileName:
#       database.py
#
#   Description:
#       Utilities for managing the global system database
#
#   4/13/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import collections
from threading import RLock
from typing import Callable, Any, DefaultDict, List
from enum import Enum
from VDrone.parameters import ParameterID, IParameter
# Database is a collection of IParameters organized by key
# Database will have a callback registry for acting on events
# Database will have a core type, with each type containing a parameter and accessory functions
# Database will have ability to register new parameters from an IParameter


class Events(Enum):
    UPDATE = 'update'
    TIMEOUT = 'timeout'
    INVALID = 'invalid'
    REMOVED = 'removed'
    ERROR = 'error'


class Entry:

    def __init__(self, param_id: ParameterID, param_data: IParameter, dependencies: List[ParameterID] = None):
        """
        Initialize a database entry object
        Args:
            param_id: Which ID is associated with this entry
            param_data: Core data container for the parameter
            dependencies: Parameters upon which this entry depends for validity
        """
        self._param_id = param_id
        self._param_data = param_data
        self._dependencies = dependencies
        self._lock = RLock()

        # ---------------------------------------------------------
        # Listener registry for each supported event type. Uses a
        # set() type to prevent duplicate callback entries.
        # ---------------------------------------------------------
        self._callbacks = {key.value: set([]) for key in Events}

    @property
    def param_id(self):
        return self._param_id

    @property
    def validity(self) -> bool:
        # TODO: Walk the dependency tree to determine validity
        return self._param_data.is_valid()

    @property
    def depends(self) -> List[ParameterID]:
        return self._dependencies

    def register_listener(self, event_id: Events, callback: Callable[[ParameterID], None]) -> None:
        """
        Register a listener callback to execute
        Args:
            event_id: Which event to attach the listener to
            callback: Callback to attach

        Returns:
            None
        """
        # Due to this being a set(), callbacks won't be duplicated
        with self._lock:
            self._callbacks[event_id].add(callback)

    def remove_listener(self, event_id: Events,  callback: Callable[[ParameterID], None]) -> None:
        """
        Removes a listener callback
        Args:
            event_id: Which event to remove the listener from
            callback: Callback to remove

        Returns:
            None
        """
        with self._lock:
            self._callbacks[event_id].remove(callback)

    def update(self, new_value: Any) -> bool:
        updated = self._param_data.update(new_value=new_value)
        if updated:
            self._notify_listeners(Events.UPDATE)
        else:
            self._notify_listeners(Events.ERROR)
        return updated

    def value(self) -> Any:
        with self._lock:
            return self._param_data.value()

    def _notify_listeners(self, event_id: Events):
        with self._lock:
            [callback(self._param_id) for callback in self._callbacks[event_id.value] if callable(callback)]


class ParameterDatabase:

    def __init__(self):
        self._lock = RLock()
        self._database = collections.defaultdict()  # type: DefaultDict[ParameterID, Entry]

    def exists(self, param_id: ParameterID) -> bool:
        pass

    def invalidate(self, param_id: ParameterID) -> None:
        pass

    def create(self, entry: Entry) -> None:
        with self._lock:
            if entry.param_id not in self._database.keys():
                self._database[entry.param_id] = entry

    def set(self, param_id: ParameterID, new_value: Any) -> bool:
        with self._lock:
            return self._database[param_id].update(new_value=new_value)

    def get(self, param_id: ParameterID) -> Any:
        with self._lock:
            return self._database[param_id].value()

    def is_valid(self, param_id: ParameterID) -> bool:
        with self._lock:
            return self._database[param_id].validity

    def dependency_list(self, param_id: ParameterID) -> List[ParameterID]:
        with self._lock:
            return self._database[param_id].depends
