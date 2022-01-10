# Documentation on the different commands, to be displayed when the "help" command is used
COMMAND_INFO = {
    "choose": {
        "args": [
            {
                "name": "after",
                "des": "Only include suggestions from after a certain date. Format YYYY-mm-dd.",
                "required": False
            }
        ],
        "des": "Select a random suggestion from this channel. Suggestions are messages that begin with the word 'idea'."
    },
    "help": {
        "args": [
            {
                "name": "command_name",
                "des": "When provided, only displays help text for the given command.",
                "required": False
            }
        ],
        "des": "Display the description of all commands (no arguments), or the description of a specific command."
    }
}

def build_command_help_msg(command: str, metadata: dict) -> str:
    help_msg = f"\n\n!{command}"

    # Build the information about the command arguments
    args = metadata.get("args", [])

    arg_msg = "\n\n\tArguments:" if args else ""
    for arg in args:
        arg_msg += f"\n\t\t{arg['name']}: {'' if arg['required'] else '(OPTIONAL) '}{arg['des']}"
        help_msg += f" {arg['name']}" if arg["required"] else f" [{arg['name']}]"

    help_msg += f"\n\t{metadata['des']}"
    help_msg += arg_msg

    return help_msg
