import uuid


class Session:
    _instance = None
    _session_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._session_id = uuid.uuid4()

        return cls._instance
    
    @property
    def session_id(self) -> str:
        return str(self._session_id)
