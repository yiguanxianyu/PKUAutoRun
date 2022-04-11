from gpxpy import parse
from random import random
from datetime import datetime, timedelta


class PreProcessor:

    def __init__(self, input_path, speed) -> None:
        self.time_bounds = None
        self.points = None
        self.length = 0
        self.speed = speed
        self.path = input_path
        self.preprocess(input_path)

    def preprocess(self, input_path):
        with open(input_path, 'r') as gpx_file:
            gpx = parse(gpx_file)

        points = gpx.tracks[0].segments[0].points[::2]

        for point in points:
            point.extensions.clear()
            point.remove_elevation()
            point.latitude += (random() - 0.5) * 5e-6
            point.longitude += (random() - 0.5) * 5e-6

        gpx.tracks[0].segments[0].points = points
        self.points = points
        self.length = gpx.length_2d()

        start_time = datetime.now().replace(microsecond=0)

        dur_time = timedelta(seconds=self.length * self.speed / 1000)

        gpx.fill_time_data_with_regular_intervals(
            start_time=start_time, end_time=start_time + dur_time, force=True
        )

        # from pathlib import Path
        # Path("./preprocessed").mkdir(exist_ok=True)
        # with open("./preprocessed/temp-gpx.gpx", "w") as f:
        #     f.write(gpx.to_xml())

        self.time_bounds = gpx.get_time_bounds()

    def show_info(self):
        dur_time = self.time_bounds.end_time - self.time_bounds.start_time

        # 以秒记录的总时长
        total_time_sec = dur_time.total_seconds()
        # 以分秒记录的总时长
        total_min, total_sec = divmod(total_time_sec, 60)

        avg_speed = (total_time_sec / 60) / (self.length / 1000)
        avg_speed_min = int(avg_speed)
        avg_speed_sec = int((avg_speed - avg_speed_min) * 60)

        curr_time = datetime.now()
        end_time = dur_time + curr_time

        print(f"""
跑步开始：
  总里程：\t{int(self.length)}米
  平均配速：\t{avg_speed_min}分{avg_speed_sec}秒每公里
  总时长：\t{int(total_min)}分{int(total_sec)}秒
  开始时间：\t{curr_time}
  结束时间：\t{end_time}（预计）
""")


if __name__ == "__main__":
    _input = r"./samples/54_3.5km.gpx"
    a = PreProcessor(_input)
    a.show_info()
