class QueueException(Exception):
    pass

class QueueEmpty(QueueException):
    pass


class QueueFull(QueueException):
    pass
    
    
class QueueLocked(QueueException):
    pass
    
    
class QueueInputLocked(QueueLocked):
    pass
    
    
class QueueOutputLocked(QueueLocked):
    pass
    

class AlreadyQueued(QueueException):
    pass


class AlreadyLocked(QueueLocked):
    pass

    
class AlreadyUnlocked(QueueLocked):
    pass
    
