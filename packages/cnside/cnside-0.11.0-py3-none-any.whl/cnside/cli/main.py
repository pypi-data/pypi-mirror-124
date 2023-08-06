#!/usr/bin/env python
import argparse
import random
import sys
import time
from typing import Text

from pydantic import BaseModel

from cnside import metadata, errors
from cnside.authenticator import Authenticator, AuthenticatorConfig, OAUTHToken
from cnside.cli import APIClient, APIClientConfig
from cnside.cli.core import PrintColors, ParsedWrappedCommand, generate_request_document, \
    execute_command
from cnside.cli.documents import CNSIDERequestDocument
from cnside.errors import FailedToLoadToken, FailedToRefreshToken
from cnside.storage import StorageHandlerConfig, StorageHandler


class Joker:
    def __init__(self):
        self.colors = PrintColors()

    def ill_let_myself_out(self):
        if not random.randint(0, 1000):
            time.sleep(1)
            self.colors.point_warning("ENCRYPTING ALL YOUR COMPUTER FILES!")
            time.sleep(3)
            self.colors.point_fail("SYKE!!! THE FILE ENCRYPTION MODE IS DISABLED. 😑")
            time.sleep(1)
            self.colors.point("TIP: To enable file encryption mode run 'cnside --enable-encrypt-my-file'")


class Messages:
    LOGGED_IN = ""
    LOGGED_OUT = ""
    TOKEN_LOAD_FAILED = "Failed to load token."
    AUTH_REQUIRED = "Authentication required. Please run: 'cnside illustria auth'."
    UNHANDLED_AUTH_ERROR = "Unhandled authentication error."
    UNHANDLED_REQUEST_ERROR = "Unhandled package request error."
    LIBRARY_REJECTED = "LIBRARY REJECTED"
    LIBRARY_APPROVED = "LIBRARY APPROVED"
    FAILED_REFRESH_TOKEN = "Failed to refresh authentication token."


class CLIConfig(BaseModel):
    cnside_base_url: Text = "https://cnside.illustria.io"
    cnside_npm_repo: Text = "https://repo.illustria.io/repository/cnside_npm_hosted/"
    cnside_pypi_repo: Text = "https://repo.illustria.io/repository/cnside_pypi_hosted/simple"
    auth_url: Text = "https://illustria.frontegg.com/oauth/authorize"
    token_url: Text = "https://illustria.frontegg.com/oauth/token"
    client_id: Text = "cf890130-015c-41b0-bd3d-ea03fa393b41"


class CLIInterface:
    def __init__(self, config: CLIConfig):
        self.colors = PrintColors()
        self.config = config

        self.storage_handler = StorageHandler(StorageHandlerConfig())
        self.authenticator = Authenticator(
            config=AuthenticatorConfig(auth_url=config.auth_url, token_url=config.token_url,
                                       storage_handler=self.storage_handler, client_id=self.config.client_id)
        )

    @staticmethod
    def interface() -> ParsedWrappedCommand:
        """
        Provides script interface for end user.

        """
        # todo: build a hierarchical parser for all commands
        parser = argparse.ArgumentParser(usage="cnside [PACKAGE MANAGER COMMAND]\n"
                                               "Command Line Interface Tool for interacting with CNSIDE Service\n"
                                               "Usage example: cnside pip install flask".format(__file__))
        parser.add_argument("manager", help="Package Manager (Supported: pip, npm, nuget, maven, illustria)")
        parser.add_argument("action", help="Action (install, auth)")
        parser.add_argument('arguments', nargs=argparse.REMAINDER)
        args = parser.parse_args()
        cli_command = ParsedWrappedCommand(package_manager=args.manager, action=args.action, arguments=args.arguments)
        return cli_command

    def execute(self, command):
        if command.package_manager == "illustria":
            index = {
                "auth": self.authenticator.authenticate
            }
            index[command.action]()
        else:
            self.request_packages(command=command)

    @staticmethod
    def req_from_cnside(api_client: APIClient, request_document: CNSIDERequestDocument) -> bool:
        approved = api_client.request_packages_from_cnside_system(request_document=request_document)
        return approved

    def gen_api_client(self):
        token = self.load_token()
        config = APIClientConfig(
            base_url=self.config.cnside_base_url,
            headers={"Authorization": f"{token.token_type} {token.access_token}"}
        )
        api_client = APIClient(config=config)
        return api_client

    def request_packages(self, command: ParsedWrappedCommand, skip_install: bool = False):
        try:
            api_client = self.gen_api_client()

            # generating request document
            request_document = generate_request_document(command)
            self.colors.header("Requesting packages from CNSIDE System.")
            if request_document.packages:
                self.colors.point(f"Packages: {request_document.packages}")
            else:
                self.colors.point(f"Manifest: {request_document.manifest}")

            # requesting package
            try:
                approved = self.req_from_cnside(api_client=api_client, request_document=request_document)
            except errors.api.TokenExpired:
                api_client.close()

                try:
                    token = self.authenticator.load_token()
                    token = self.authenticator.refresh_token(token=token)
                    self.storage_handler.token.save(token)
                except FailedToRefreshToken:
                    self.colors.point_fail(Messages.FAILED_REFRESH_TOKEN)
                    self.colors.point_fail(Messages.AUTH_REQUIRED)
                    sys.exit()

                api_client = self.gen_api_client()
                approved = self.req_from_cnside(api_client=api_client, request_document=request_document)
            except errors.api.RemoteServerError as e:
                self.colors.point_fail(f"Error: Remote Server Error:\n\tStatus Code: {e.data.status_code}")
                sys.exit()
            except Exception as e:
                raise e
            finally:
                api_client.close()

            if approved:
                self.colors.point_ok(Messages.LIBRARY_APPROVED)
                if command.package_manager == metadata.packages.PackageManagers.NPM:
                    command.arguments.extend(["--registry", self.config.cnside_npm_repo])
                elif command.package_manager == metadata.packages.PackageManagers.PIP:
                    command.arguments.extend(["--index-url", self.config.cnside_pypi_repo])
                else:
                    raise errors.UnsupportedPackageManager()
                if not skip_install:
                    execute_command(command=command)
                else:
                    self.colors.point_warning("Skipping Installation (skip_install=True)")
            else:
                self.colors.point_fail(Messages.LIBRARY_REJECTED)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            self.colors.point_fail(Messages.UNHANDLED_REQUEST_ERROR)
            self.colors.point_fail(e)
            sys.exit()

    def load_token(self) -> OAUTHToken:
        try:
            token = self.authenticator.load_token()
        except FailedToLoadToken:
            self.colors.point_fail(Messages.TOKEN_LOAD_FAILED)
            self.colors.point_fail(Messages.AUTH_REQUIRED)
            sys.exit()
        except Exception as e:
            self.colors.point_fail(Messages.UNHANDLED_AUTH_ERROR)
            self.colors.point_fail(e)
            sys.exit()

        return token


def main():
    cli_interface = CLIInterface(config=CLIConfig())
    command = cli_interface.interface()
    cli_interface.execute(command=command)


# todo: add report error functionality - when error happens
# todo: save to config file


if __name__ == '__main__':
    main()
