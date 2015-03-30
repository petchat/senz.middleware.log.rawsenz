__author__ = 'woodie'

def SenzCollector(filter=2, **time_lines):
    '''
    SENZ COLLECTOR

    It used to collect senz tuple from discrete timestamp seqs which include motion, sound, location and so on.
        eg. senz tuple look like:
            {
                "motion":   2015-03-18 05:49:04,
                "location": 2015-03-18 05:49:10,
                "sound":    2015-03-18 05:49:05
            }
    You should input timestamp lists into SenzCollector, and select a key as primary key.
    The algo will output a list of timestamp group which other key's timestamp is closet to the primary key's timestamp.
    So the timestamp of every item's primary key in the output list is consequent.


    :param time_lines:
        *time_lines* is a dict, and it can contain more than one timestamp sequences.
        Every sequence also is a dict, key is the name of time line, and value is a list which contains timestamp seqs.
        Key can be any word. The selected key will be *primary key* which clustering algo based on.
        eg. {
                "key 0": [key0_timestamp0, key0_timestamp1, ...],
                "key 1": [key1_timestamp0, key1_timestamp1, ...],
                "key 2": [key2_timestamp0, key2_timestamp1, ...],
                ...
                "primaryKey": "key 0"
            }
    :return:
        Return value is a list, the item of return list is a dict which contains N sub-dict( key: key_timestamp ).
        eg. [
                {
                    "senzTimestamp": key0_timestamp0,
                    "key0": key0_timestamp0,
                    "key1": key1_timestamp1,
                    "key2": key2_timestamp0,
                    ...
                },
                ...
            ]
    '''
    # If there is primary key,
    # then get the primary key, and remove the primary key from input.
    if time_lines.has_key("primaryKey"):
        primary_key = time_lines.pop("primaryKey")
        return SenzFilter(ClusteringBaseOnPrimaryKey(primary_key, time_lines), filter)
    # If there is no primary key,
    # then it will clutering decentralized.
    return SenzFilter(ClusteringDecentralized(time_lines), filter)



def ClusteringBaseOnPrimaryKey(primary_key, time_lines):
    result_list = []
    # Scan the primary key list's timestamp one by one.
    for primary_timestamp in time_lines.pop(primary_key):
        senz_tuple = {primary_key: primary_timestamp}
        # Select the closest timestamp to primary key timestamp in different time line
        for (key, time_line) in time_lines.items():
            min_delta        = 99999999999
            closet_timestamp = 0
            # Compare every timestamp with primary key timestamp in time line.
            for normal_timestamp in time_line:
                if abs(primary_timestamp - normal_timestamp) < min_delta:
                    min_delta        = abs(primary_timestamp - normal_timestamp)
                    closet_timestamp = normal_timestamp
                else:
                    break
            senz_tuple[key] = closet_timestamp
        result_list.append(senz_tuple)
    return result_list



def ClusteringDecentralized(time_lines):
    return []



def SenzFilter(tuple_list, filter):
    for tuple in tuple_list:
        # Expectation of timestamps in a tuple
        expectation = 0
        for timestamp in tuple.values():
            expectation += timestamp
        expectation /= len(tuple)
        # Variance Square of timestamps in a tuple
        variance_square = 0
        for timestamp in tuple.values():
            variance_square += pow(timestamp - expectation, 2)
        # Filtering
        if variance_square >= pow(filter, 2):
            tuple_list.remove(tuple)
    return tuple_list





if __name__ == "__main__":
    print SenzCollector(filter=1, key0=[2,4,6,9], key1=[3,4,7,9], key2=[1,3,6], primaryKey="key0")
    # print SenzFilter([{'key2': 1, 'key1': 3, 'key0': 2}, {'key2': 3, 'key1': 4, 'key0': 4}, {'key2': 6, 'key1': 7, 'key0': 6}, {'key2': 6, 'key1': 9, 'key0': 9}], 1)