from data.halo_ce_location_data import CE_LOCATION_DATA

def get_location_name_to_id():
    location_map = {
        **{f"{data.level} - {name}": data.id for name, data in CE_LOCATION_DATA.items()},
    }