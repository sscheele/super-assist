""" An assistant to piggyback off Google AVS """
from input_classes import InputHandler
from youtube import YT_TASK
from volume import VOL_TASK

handler = InputHandler()
handler.add_class(YT_TASK)
handler.add_class(VOL_TASK)
handler.scan_input()
