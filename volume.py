import subprocess
from input_classes import Task, Expression
from re import compile


def set_volume(vol, chan):
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", vol + "%"])


VOL_TASK = Task("vol",
                [Expression(compile(r"set volume to (\d+)"), ("vol",)),
                 Expression(compile(r"volume (\d+)"), ("vol",)),
                 Expression(compile(r"set volume (\d+)"), ("vol",))
                 ], [], set_volume)
