import os


class AdbShellCmdsManager:
    """
    The AdbShellCmdsManager manages various custom adb shell commands related to interfacing with an android device
    via the ConnectionClient.

    Commands are stored in different bash files located in the device/adb_shell_cmds directory. The filenames without
    the .sh extensions serve as names for the commands that a client can invoke through this manager.
    """

    BASE_PATH = "device/adb_shell_cmds"

    # All possible commands
    CLOSE_APPLICATIONS = "close_applications"
    SHUTDOWN_MONKEY_ON_DEVICE = "shutdown_monkey_on_device"

    ALL_COMMANDS = [CLOSE_APPLICATIONS, SHUTDOWN_MONKEY_ON_DEVICE]

    def __init__(self, device):
        """
        Initialize an AdbShellsCmdsManager by parsing the bash files related to possible commands
        :param device: MonkeyDevice instance that is used to carry out shell commands
        """

        self.device = device

        # Iterate through the possible commands and retrieve parsed arguments
        self.parsed_commands = dict()
        for command in self.ALL_COMMANDS:
            self.parsed_commands[command] = self.retrieve_command(command)

    def take_command(self, command):
        """
        Invoke the passed in command on the device.
        :param command: if part of self.parsed_commands, carry out the command on the device;
                        otherwise, raise an Exception.
        """

        if command in self.parsed_commands:
            self.device.shell(self.parsed_commands[command])
        else:
            raise Exception(str(command) + " is not a supported command")

    def close_applications(self):
        """
        Close all applications on the device.
        """

        self.take_command(self.CLOSE_APPLICATIONS)

    def shutdown_monkey_on_device(self):
        """
        Manually shutdown any processes relating to monkeyrunner on the device.
        """

        self.take_command(self.SHUTDOWN_MONKEY_ON_DEVICE)

    @classmethod
    def retrieve_command(cls, command):
        """
        Helper function that runs during initialization. It parses the appropriate bash file associated with command
        to retrieve its contents as a string.
        :param command: if part of ALL_COMMANDS, parse the associated bash file to retrieve the string contents;
                        otherwise, raise an Exception.
        :return string contents located in the bash file associated with command.
        """

        script_path = os.path.join(cls.BASE_PATH, str(command) + ".sh")

        if os.path.exists(script_path):
            fp = open(script_path, 'r')
            contents = '\n'.join(fp.readlines())
            fp.close()
            return contents
        else:
            raise Exception(str(command) + " is not a supported command")
