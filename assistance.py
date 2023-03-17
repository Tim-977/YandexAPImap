def getSpn(min_lon, min_lat, max_lon, max_lat):

    def calc_size_in_degrees(min_lon, min_lat, max_lon, max_lat):

        horizontal_distance = abs(max_lon - min_lon)
        vertical_distance = abs(max_lat - min_lat)

        size_in_degrees_of_longitude = horizontal_distance
        size_in_degrees_of_latitude = vertical_distance

        return size_in_degrees_of_latitude, size_in_degrees_of_longitude

    size_in_degrees_of_latitude, size_in_degrees_of_longitude = calc_size_in_degrees(
        min_lon, min_lat, max_lon, max_lat)
    spn = f"{size_in_degrees_of_longitude:.6f},{size_in_degrees_of_latitude:.6f}"
    print('spn: ', spn)
    return spn