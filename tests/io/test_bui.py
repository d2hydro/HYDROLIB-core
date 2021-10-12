from datetime import datetime
from tests.utils import test_input_dir
from hydrolib.core.io.bui.parser import BuiParser
from hydrolib.core.io.bui.serializer import BuiSerializer

class TestModel:
    pass

class TestParser:
    def test_BuiParser_given_valid_file_parses_values(self):
        test_file = test_input_dir / "rr_sample_trimmed" / "rr" / "default.bui"
        assert test_file.is_file(), "Test File not found."
        dict_values = BuiParser.parse(test_file)
        assert dict_values is not None
        assert dict_values["default_dataset"] == "1"
        assert dict_values["number_of_stations"] == "1"
        assert dict_values["name_of_stations"] == ["’Station1’"]
        assert dict_values["number_of_events"] == "1"
        assert dict_values["seconds_per_timestep"] == "10800"
        assert dict_values["first_recorded_event"] == "1996 1 1 0 0 0 1 3 0 0"
        assert dict_values["precipitation_per_timestep"] == ["0.2","0.2","0.2","0.2","0.2","0.2","0.2","0.2","0.2",]


class TestSerializer:
    def test_BuiSerializer_given_dict_serialize_into_text(self):
        
        # 1. Define test data.
        dict_values = dict(
            file_path="my/custom/path",
            default_dataset = "1",
            number_of_stations= "1",
            name_of_stations= ["’Station1’"],
            number_of_events= "1",
            seconds_per_timestep= "10800",
            first_recorded_event= "1996 1 1 0 0 0 1 3 0 0",
            precipitation_per_timestep= [["0.2"],["0.2"],["0.2"],["0.2"],])
        # Define expected datetime (it could fail by a second in a rare occasion)
        expected_datetime = datetime.now().strftime("%d-%m-%y %H:%M:%S")
                
        # 2. Do test.
        serialized_text = BuiSerializer.serialize(dict_values)

        # 3. Verify expectations.
        expected_serialized = f"""*Name of this file: my/custom/path
*Date and time of construction: {expected_datetime}
*Comments are following an * (asterisk) and written above variables
1
*Number of stations
1
*Station Name
’Station1’
*Number_of_events seconds_per_timestamp
1 10800
*Start datetime and number of timestamps in the format: yyyy#m#d:#h#m#s:#d#h#m#s
*Observations per timestamp (row) and per station (column)
1996 1 1 0 0 0 1 3 0 0
0.2
0.2
0.2
0.2
"""
        assert serialized_text == expected_serialized

    def test_BuiSerializer_given_station_ids_serialize_into_text(self):
        stations_ids = ["Hello", "World", "’Station1’"]
        serialized_text = BuiSerializer.serialize_stations_ids(stations_ids)
        assert serialized_text == "Hello World ’Station1’"
    
    def test_BuiSerializer_given_precipitation_serialize_into_text(self):
        precipitation_per_timestep= [["0.2"],["0.2"],["0.2"],["0.2"]]
        serialized_text = BuiSerializer.serialize_precipitation_per_timestep(precipitation_per_timestep)
        assert serialized_text == "0.2\n0.2\n0.2\n0.2"
