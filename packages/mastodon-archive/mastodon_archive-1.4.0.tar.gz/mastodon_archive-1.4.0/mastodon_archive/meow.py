#!/usr/bin/env python3
# Copyright (C) 2018  Alex Schroeder <alex@gnu.org>
# Copyright (C) 2021  cutiful (https://github.com/cutiful)

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import os
import json
import http.server
import socketserver
from progress.bar import Bar
from urllib.parse import urlparse, parse_qs
from . import core

server_port = 13523
meow_origin = "https://purr.neocities.org"
meow_open_path = meow_origin + "/mastodon-archive-import/"

import_complete = False
bar = False

def meow(args):
    """
    Find and serve all archive files for Meow.
    """
    (username, domain) = args.user.split("@")

    status_file = domain + ".user." + username + ".json"
    data = core.load(status_file, required=True, quiet=True, combine=args.combine)

    media_dir = domain + ".user." + username
    media_files = []

    for collection in ["statuses", "favourites"]:
        for status in data[collection]:
            attachments = status["media_attachments"]
            if status["reblog"] is not None:
                attachments = status["reblog"]["media_attachments"]
            for attachment in attachments:
                if attachment["url"]:
                    path = urlparse(attachment["url"]).path
                    if path in media_files:
                        continue

                    # If we have it locally, set it to a relative path so Meow
                    # known to look in its local database. Otherwise, it'll
                    # still try to load the remote image.

                    file_name = media_dir + path
                    if os.path.isfile(file_name):
                        attachment["url"] = path
                        media_files.append(path)

    data["files"] = media_files

    global bar
    if len(media_files) > 0:
        bar = Bar("Exporting files", max = len(media_files) + 1)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            global import_complete
            global bar

            query = parse_qs(urlparse(self.path).query)

            if self.path == "/":
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", meow_origin)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json.dumps(data), "utf-8"))

                if bar:
                    bar.next()
            elif "file" in query and query["file"][0] in media_files:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", meow_origin)
                self.end_headers()

                file_name = media_dir + query["file"][0]
                with open(file_name, "rb") as file:
                    self.wfile.write(file.read())

                if bar:
                    bar.next()
            elif "complete" in query:
                self.send_response(200)
                self.end_headers()

                import_complete = True

                if bar:
                    bar.finish()
            else:
                self.send_error(404)

        def log_message(self, format, *args):
            return

    def not_completed():
        global import_complete
        return not import_complete

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", server_port), Handler) as httpd:
        print("Please, open Meow at", meow_open_path, "to continue!")
        while not_completed():
            httpd.handle_request()

    print("Export finished!")
