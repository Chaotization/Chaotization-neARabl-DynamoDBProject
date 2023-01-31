class Graph:
    def __init__(self, _id, created_time, landmarks):
        self.infor = []
        self.id = _id
        self.type = 'mobile_region'
        self.created_time = created_time
        self.landmarks = landmarks
        for landmark in self.landmarks:
            self.landmark_id = landmarks.get(landmark)['id']
            self.floor_num = str(landmarks.get(landmark)['id'][0])
            if 'transformed_w_location' in landmarks.get(landmark):
                self.transform_world_location = landmarks.get(landmark)['transformed_w_location']
            elif 'transform_world_location' in landmarks.get(landmark):
                self.transform_world_location = landmarks.get(landmark)['transform_world_location']
            else:
                self.transform_world_location = None
            self.regions = self.landmark_id
            self.access_level = 1
            if 'destination_type' in landmarks.get(landmark):
                self.destination_type = landmarks.get(landmark)['destination_type']
            else:
                self.destination_type = 2
            if 'connection' in landmarks.get(landmark):
                self.connection = landmarks.get(landmark)['connection']['to']
            else:
                self.connection = None
            self.infor += {'landmark_id':self.landmark_id, 'transform_world_location':self.transform_world_location,
                           'regions': self.regions,'access_level': self.access_level, 'destination_type': self.destination_type,
                           'connection': self.connection}
