from gpxpy import parse
from random import random
from datetime import datetime, timedelta


class PreProcesser:
    def preprocess(self, input_path):
        gpx_file = open(input_path, 'r')
        gpx = parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                points = segment.points[::3]
                for point in points:
                    point.extensions.clear()
                    point.remove_elevation()
                    point.latitude += (random() - 0.5) * 1e-5
                    point.longitude += (random() - 0.5) * 1e-5
                segment.points = points

        length = gpx.length_2d()
        least_time = length * 0.24
        num_points = gpx.get_points_no()
        second_interval = int(least_time / num_points) + 1

        self.length = length

        start_time = datetime.now().replace(microsecond=0)
        time_delta = timedelta(seconds=second_interval)

        gpx.fill_time_data_with_regular_intervals(start_time=start_time,
                                                  time_delta=time_delta,
                                                  force=True)

        with open("./preprocessed/tempgpx.gpx", "w") as f:
            f.write(gpx.to_xml())

        gpx_file.close()
        self.gpx = gpx

    def show_info(self):
        tb = self.gpx.get_time_bounds()
        durtime = tb.end_time - tb.start_time

        # 以秒记录的总时长
        total_time_sec = durtime.total_seconds()
        # 以分秒记录的总时长
        total_min, total_sec = divmod(total_time_sec, 60)

        avg_speed = (total_time_sec / 60) / (self.length / 1000)
        avg_speed_min = int(avg_speed)
        avg_speed_sec = int((avg_speed - avg_speed_min) * 60)

        currtime = datetime.now()
        end_time = durtime + currtime

        print(f"""
跑步开始：
  总里程：\t{int(self.length)}米
  平均配速：\t{avg_speed_min}分{avg_speed_sec}秒每公里
  总时长：\t{int(total_min)}分{int(total_sec)}秒
  开始时间：\t{currtime}
  结束时间：\t{end_time}（预计）
""")

    def __init__(self, input_path) -> None:
        self.length = 0
        self.preprocess(input_path)


if __name__ == "__main__":
    input = r"./samples/54_3.5km.gpx"
    a = PreProcesser(input)
    a.show_info()
