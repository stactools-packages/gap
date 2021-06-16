import stactools.core

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.gap import commands
    registry.register_subcommand(commands.create_gap_command)


__version__ = "0.1.0"
