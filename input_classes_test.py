import input_classes
from pandora import PANDORA_TASK
from time import sleep
from re import compile

def not_youtube(args, chan):
    print("Hi, I'm not YouTube")

YT_TASK = input_classes.Task("youtube",
               [input_classes.Expression(compile(r"search for (.+) on youtube"), ('query',)),
                input_classes.Expression(compile(r"search youtube for (.+)"), ('query',)),
                input_classes.Expression(compile(r"play (.+) on youtube"), ('query',)),
                ],
               [input_classes.Expression(compile("pause"), ("command",)),
                input_classes.Expression(compile("play"), ("command",))
                ],
               not_youtube)

h = input_classes.InputHandler()
h.add_class(YT_TASK)
h.add_class(PANDORA_TASK)
h.handle_input("play billy joel on pandora")
sleep(10) # give Pandora time to start
h.handle_input("pause")
