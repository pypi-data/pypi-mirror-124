class NotFoundError(Exception):
    """
    Class of custom Exception

    Args:
        data (all types): input data
    """
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return f"Not Found {self.data}, please check the name again"


class CollisionError(Exception):
    """
    Class of custom Exception

    Args:
        data (all types): input data
    """
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return f"Check the collision.. {self.data}, please check the obastacle setting again"