from dataclasses import dataclass


@dataclass
class DataCollection:
    frame_path: str
    steering_position: float
