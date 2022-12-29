# Loosely following along with this solution
# https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2022/
# d15_beacon_exclusion_zone/more_sensors_and_beacons.py

import re

def distance(x1, y1, x2, y2):
    # Manhattan distance from (x1, y1) to (x2, y2)
    return abs(x1-x2) + abs(y1-y2)

class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        self.radius = distance(sx, sy, bx, by)

sensors = []
beacons = set()
for line in open("2022/d15_input.txt").readlines():
    sx, sy, bx, by = tuple(map(int, re.findall("-*\\d+", line.strip())))
    sensors.append(Sensor(sx, sy, bx, by))
    # More than one sensor can point to the same beacon
    beacons.add((bx, by))

print("# sensors: ", len(sensors))

# Part 1
yoi = 2000000

# Identify sensors that are close to the y of interest, compute x-interval
# they cover on that y
def coverage_for_row(y, sensors):
    intervals = []
    for s in sensors:
        dist_to_row = abs(s.sy - yoi)
        range_on_yoi = s.radius - dist_to_row
        if range_on_yoi < 0:
            # can't reach the row
            continue
        # print("({}, {})".format(s.sx, s.sy), end="")
        interval = [s.sx - range_on_yoi, s.sx + range_on_yoi]
        # print(interval)
        intervals.append(interval)

    # Collapse the intervals together
    intervals.sort()
    intervals_merged = [intervals[0]]
    for interval in intervals[1:]:
        # Check for overlapping interval
        if intervals_merged[-1][0] <= interval[0] <= intervals_merged[-1][-1]:
            intervals_merged[-1][-1] = max(intervals_merged[-1][-1], interval[-1])
        # If not overlapping, just add it to the list
        else:
            intervals_merged.append(interval)
    
    return intervals_merged

yoi_intervals = coverage_for_row(yoi, sensors)
total_interval_coverage = sum(i[1] - i[0] + 1 for i in yoi_intervals)
beacons_to_exclude = sum(1 for b in beacons if b[1] == yoi)

print("Part 1: ", total_interval_coverage - beacons_to_exclude)

# Part 2
def find_distress_beacon(sensors, distress_lims = [0, 0, 4000000, 4000000]):
    # Iterate over all points that are radius+1 units away from their sensors,
    # looking for a gap in the excluded intervals in that row.
    distress_min_x, distress_min_y, distress_max_x, distress_max_y = distress_lims
    for s in sensors:
        for dx in range(s.radius+2): # max dx is radius+1
            dy = s.radius+1 - dx
            assert(dx+dy == s.radius+1)

            # Apply the points in all four quadrants
            for sign_x, sign_y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                test_x = s.sx + (sign_x * dx)
                test_y = s.sy + (sign_y * dy)

                # Check inbounds
                if not (
                    distress_min_x <= test_x <= distress_max_x and 
                    distress_min_y <= test_y <= distress_max_y
                ): continue

                # Get the intervals that do not contain a beacon in this row
                row_intervals = coverage_for_row(test_y, sensors)

                # look for a gap between any intervals
                if len(row_intervals) > 1:
                    for i in range(1, len(row_intervals)+1):
                        if row_intervals[i][0] > row_intervals[0][1] + 1:
                            x = row_intervals[i][0] - 1
                            return x, test_y

tuning_multiplier = 4000000
distress_x, distress_y = find_distress_beacon(sensors)

print("Part 2: ", distress_x*tuning_multiplier + distress_y)
