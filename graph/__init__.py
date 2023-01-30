class Graph:
    def __init__(self, created_time, floor_num, transform_world_location, landmarks):
        self.id = '630cec62cb4fde05f5d4020c'
        self.type = 'mobile_region'
        self.created_time = created_time
        self.floor_num = floor_num
        self.landmarks = landmarks
        for landmark in self.landmarks:
            self.landmark_id = '9C1DD204-635B-4C8B-982E-BE98CC83B84F'
            self.transform_world_location = transform_world_location
            if 'id' in landmark:
                self.regions = landmark['id']
            else:
                self.regions = ""
            self.access_level = 1
            self.destination_type = 2
            if 'connection' in landmark:
                self.connection = landmark['connection']
            else:
                self.connection = []

