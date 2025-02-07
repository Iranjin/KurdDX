from .console import Cs, CsCommand
from . import command


def register_commands():
    console = Cs()

    command_say = CsCommand("say")
    command_say.add_argument("channel_id", int)
    command_say.add_argument("message_content", str)
    command_say.set_function(command.say)
    console.add_command(command_say)

    command_export_log = CsCommand("export log")
    command_export_log.set_function(command.export_log)
    console.add_command(command_export_log)

    command_servers = CsCommand("servers")
    command_servers.set_function(command.servers)
    console.add_command(command_servers)

    command_server_list = CsCommand("server list")
    command_server_list.add_argument("fetch_invite", bool, False)
    command_server_list.set_function(command.server_list)
    console.add_command(command_server_list)

    command_server_info = CsCommand("server info")
    command_server_info.add_argument("guild_id", int)
    command_server_info.add_argument("show_members", bool, False)
    command_server_info.set_function(command.server_info)
    console.add_command(command_server_info)

    command_create_invite = CsCommand("create invite")
    command_create_invite.add_argument("guild_id", int)
    command_create_invite.set_function(command.create_invite)
    console.add_command(command_create_invite)

    command_reload = CsCommand("reload")
    command_reload.add_argument("sync_tree", bool, False)
    command_reload.set_function(command.reload)
    console.add_command(command_reload)

    command_sync = CsCommand("sync")
    command_sync.set_function(command.sync)
    console.add_command(command_sync)

    command_clear = CsCommand("clear")
    command_clear.set_function(command.clear)
    console.add_command(command_clear)

    command_leave = CsCommand("leave")
    command_leave.add_argument("guild_id", int)
    command_leave.set_function(command.leave)
    console.add_command(command_leave)

    command_maintenance = CsCommand("maintenance")
    command_maintenance.add_argument("status", bool)
    command_maintenance.set_function(command.maintenance)
    console.add_command(command_maintenance)

    command_stop = CsCommand("stop")
    command_stop.set_function(command.stop)
    console.add_command(command_stop)

    return console
