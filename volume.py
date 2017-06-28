import subprocess
from input_classes import Task, Expression
from re import compile


def set_volume(args, chan):
    to_call = ["amixer", "sset", "PCM", args['vol'] + "%"]
    print(to_call)
    subprocess.call(to_call)

VOL_TASK = Task("vol",
                [Expression(compile(r"set volume to (\d+)%?"), ("vol",)),
                 Expression(compile(r"volume (\d+)%?"), ("vol",)),
                 Expression(compile(r"set volume (\d+)%?"), ("vol",))
                 ], [], set_volume)
