from threading import Lock

lock = Lock()


class SessionStore:
    sessionID = 1  # should not be used directly
    file = 'sessionID.txt'

    @staticmethod
    def __init__():
        SessionStore.get()
        print("SessionStore init with value {0}".format(SessionStore.sessionID))

    @staticmethod
    def fetch_add():
        index = SessionStore.get()
        SessionStore.set(index + 1)
        print("SessionStore fetch_add, writing {0} and returning {1}".format(index + 1, index))
        return index

    @staticmethod
    def set(value):  # should not be used directly
        print("SessionStore set value {0}".format(value))
        with lock:
            with open(SessionStore.file, 'w') as file:
                file.write(str(value))
                file.flush()

    @staticmethod
    def get():  # should not be used directly
        with lock:
            try:
                with open(SessionStore.file, 'r') as file:
                    data = file.read().split()[0]
                    SessionStore.sessionID = int(data)
                    print("SessionStore get value {0} from data {1}".format(SessionStore.sessionID, data))
                    file.close()
            except Exception as e:
                print(e)
                return 1
        return SessionStore.sessionID
