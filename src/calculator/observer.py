from abc import ABCMeta, abstractmethod


class IEventManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe(self, event_type, listener):
        pass

    @abstractmethod
    def unsubscribe(self, event_type, listener):
        pass

    @abstractmethod
    def notify(self, event_type, data):
        pass


class IListener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_it(self, data):
        pass


class EventManager(IEventManager):
    __event_listeners = {}

    def _get_listeners(self, event_type):
        return self.__event_listeners.get(event_type) or []

    def _set_listeners(self, event_type, listeners):
        self.__event_listeners[event_type] = listeners

    def subscribe(self, event_type, listener):
        listeners = self._get_listeners(event_type)
        listeners.append(listener)
        self._set_listeners(event_type, listeners)

    def unsubscribe(self, event_type, listener):
        listeners = self._get_listeners(event_type)
        if listener in listeners:
            listeners.remove(listener)
            self._set_listeners(event_type, listeners)

    def notify(self, event_type, data):
        for listener in self._get_listeners(event_type):
            listener.update_it(data)
