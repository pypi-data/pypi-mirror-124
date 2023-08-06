import subprocess
from typing import List, Text

from cnside import errors
from cnside import metadata
from cnside.cli.documents import CNSIDERequestDocument
from cnside.cli.parsers import PIPInstallParser, PackageParam, NPMInstallParser, PackageParamType
import colorama


class PrintColors(object):
    def __init__(self):
        colorama.init()
        self._header = colorama.Fore.LIGHTMAGENTA_EX
        self._blue = colorama.Fore.BLUE
        self._success = colorama.Fore.GREEN
        self._yellow = colorama.Fore.LIGHTYELLOW_EX
        self._warning = colorama.Fore.LIGHTYELLOW_EX
        self._fail = colorama.Fore.RED
        self._end = colorama.Style.RESET_ALL
        self._bold = colorama.Style.BRIGHT

    def header(self, text):
        print(u"\n{}{}{}{}".format(self._bold, self._header, text, self._end))

    def header_point(self, text):
        print(u"{}[*]{} {}".format(self._header, self._end, text))

    def footer(self, text):
        print(u"\n{}{}{}{}\n".format(self._bold, self._header, text, self._end))

    def point(self, text):
        print(u"{}[*]{} {}".format(self._yellow, self._end, text))

    def point_ok(self, text):
        print(u"{}[V] {}{}".format(self._success, text, self._end))

    def point_warning(self, text):
        print(u"{}[X] {}{}".format(self._warning, text, self._end))

    def point_fail(self, text):
        print(u"{}[X] {}{}".format(self._fail, text, self._end))

    def custom(self, text):
        print(text)

    def empty_line(self):
        print("")


# todo: turn into an object that can "digest" commands and return all needed info about it
class ParsedWrappedCommand:
    def __init__(self, package_manager: Text, action: Text, arguments: List):
        self.package_manager = package_manager
        self.action = action
        self.arguments = arguments

    def to_list(self) -> List[Text]:
        rv = [self.package_manager, self.action]
        rv.extend(self.arguments)
        return rv


def execute_command(command: ParsedWrappedCommand):
    process = subprocess.Popen(command.to_list(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
        print(line.decode("utf-8"), end="")

    for line in iter(process.stderr.readline, b''):
        print(line.decode("utf-8"), end="")

    process.stdout.close()
    process.stderr.close()
    process.wait()


def extract_pip_packages(arguments: List[Text]) -> List[PackageParam]:
    parser = PIPInstallParser(arguments)
    return parser.packages


def extract_npm_packages(arguments: List[Text]) -> List[PackageParam]:
    parser = NPMInstallParser(arguments)
    return parser.packages


def generate_request_document(command: ParsedWrappedCommand) -> CNSIDERequestDocument:
    supported_package_managers = metadata.packages.PackageManagers.to_list()
    supported_actions = ["install", "i"]

    if command.package_manager not in supported_package_managers:
        raise errors.UnsupportedPackageManager(command.package_manager)

    if command.action not in supported_actions:
        raise errors.UnsupportedAction(command.action)

    extractors = {
        metadata.packages.PackageManagers.PIP: extract_pip_packages,
        metadata.packages.PackageManagers.NPM: extract_npm_packages,
        # metadata.packages.PackageManagers.MAVEN: extract_maven_packages,
        # metadata.packages.PackageManagers.NUGET: extract_nuget_packages,
    }

    package_params_list: List[PackageParam] = extractors[command.package_manager](command.arguments)

    upid_list = []
    manifest = ""
    for package in package_params_list:
        if package.typ == PackageParamType.UPID:
            upid_list.append(package.data)
        elif package.typ == PackageParamType.MANIFEST:
            with open(package.data, "r+") as fp:
                manifest = fp.read()

    return CNSIDERequestDocument(package_manager=command.package_manager, packages=upid_list, manifest=manifest)
