from service.ConvertBuildingData import format_building_file, upload_building_to_dynamodb
from service.ConvertGraphData import format_graph_file, upload_graph_to_dynamodb
from service.ConvertRegionData import format_region_file, upload_region_to_dynamodb

url1 = "C:/Users/59832/Desktop/data/building_v2.json"
url2 = "C:/Users/59832/Desktop/data/graph_v2.json"
url3 = "C:/Users/59832/Desktop/data/region_v1.json"
tableName = 'users'
building_data = format_building_file(url1)
graph_data = format_graph_file(building_data.get("building_id"), url2)
region_data = format_region_file(building_data.get("building_id"), graph_data.get("floor_num"), url3)
# upload_building_to_dynamodb(building_data, tableName)
upload_region_to_dynamodb(region_data, tableName)


