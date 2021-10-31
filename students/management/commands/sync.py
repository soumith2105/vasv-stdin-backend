import asyncio

from django.core.management.base import BaseCommand

from students.management.commands._sequences import admin_sync, sequence_starter


class Command(BaseCommand):
    help = "Syncing sequence to syncing details of the students."

    def add_arguments(self, parser):

        # For super user account creation
        parser.add_argument("--suroll", "-sr", nargs="?", help="Admin Student Roll Number", type=str)
        parser.add_argument("--semlist", "-sl", nargs="?", help="Sem Sync list", type=str)

    def handle(self, *args, **options):
        # For super user account creation
        if options["suroll"] and options["semlist"]:
            roll_number = options["suroll"]
            semester_list = options["semlist"]
            asyncio.run(admin_sync(roll_number, semester_list, self.print_console))

        else:
            asyncio.run(sequence_starter(message=self.print_console))

    def print_console(self, message: str, style: str = None) -> None:
        """
        Different types of stdout messages

        PARAMETERS
        ----------
        message   : str
            message that need to be printed in stdout
        style     : str
            style of the output printed in stdout (optional)
            Options: error, success, warning, notice
        """
        if style == "success":
            self.stdout.write(self.style.SUCCESS(message))
        elif style == "error":
            self.stdout.write(self.style.ERROR(message))
        elif style == "warning":
            self.stdout.write(self.style.WARNING(message))
        elif style == "notice":
            self.stdout.write(self.style.NOTICE(message))
        else:
            self.stdout.write(message)
