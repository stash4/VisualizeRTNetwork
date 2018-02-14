class RTData:
    def __init__(self, user_id, status_id, user_name, distance=-1, group=-2, connection_list=[]):
        self.user_id = user_id
        self.status_id = status_id
        self.user_name = user_name
        self.distance = distance
        self.group = group
        self.connection_list = connection_list
