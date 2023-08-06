"""
MIT License

Copyright (c) 2021 Hype3808

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class BotInfo():
    def __init__(self, json: dict):
        self.id = json['id']
        self.username = json['username']
        self.discriminator = json['discriminator']
        self.discrim = self.discriminator
        self.prefix = json['prefix']
        self.website = json['webSite']
        self.support_server = json['supportServer']
        self.server = self.support_server
        self.tags = json['tags']
        self.owner = json['owner']
        self.owners = json['owners']
        self.added_on = json['adedDate']
        self.votes = json['votes']
        self.invites = json['invites']
        self.servers = json['servers']
        self.members = json['members']
