class Building:
    def __init__(self, _id, building_name, num_floor,
                 address, city, state, country, _zip,
                 created_time, update_time, floors):
        self.id = _id
        self.type = 'mobile_building'
        self.client_id = '9537cf58-08ee-435e-946f-200ae0bcb08e'
        self.building_name = building_name
        self.building_id = '623a3401d1ed84fa819e6131'
        self.num_floor = num_floor
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.zip = _zip
        self.create_time = created_time
        self.update_time = update_time
        self.floors = floors
        for floor in self.floors:
            if not 'scale' in floor:
                self.scale = floor['floorplan_scale']
            else:
                self.scale = floor['scale']
            if not 's3_location' in floor:
                self.s3_location = "floorplan.png"
            else:
                self.scale = floor['s3_location']


