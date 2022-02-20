def decor_unknown_command(function):
    def wrap(self, offset_to_jump_command, has_offset=False):
        try:
            return function(self, offset_to_jump_command, has_offset)
        except KeyError or AttributeError:
            return "unknown_command", offset_to_jump_command, has_offset

    return wrap
