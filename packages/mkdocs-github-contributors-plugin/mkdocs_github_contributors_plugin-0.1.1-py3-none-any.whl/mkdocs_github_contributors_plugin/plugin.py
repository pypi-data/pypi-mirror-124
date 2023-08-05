#!/usr/bin/python3

import requests
import re

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

item_formatting = """\
<div class=contributors-github>
    <div class="contributor-github-item">
        <a href="https://github.com/{username}"> title="{username}">
            <img src="{avatar_url}">
        </a>
    </div>
</div>\n"""

class GitHubContributorsPlugin(BasePlugin):

    config_scheme = (
        ('repository', config_options.Type(str, default='')),
        ('token', config_options.Type(str, default='')),
    )
    matcher = re.compile("{{ github.contributors }}")

    def __init__(self):
        self._data = requests.get("https://api.github.com/repos/{}/contributors".format(self.config['repository'])).json()
        self.formatted_contributors = ""
        for contributor in self._data:
            self.formatted_contributors += item_formatting.format(username=contributor['login'], avatar_url=contributor['avatar_url']


    def on_page_markdown(self, markdown, page=None, config=None, **kwargs):
        return markdown.replace("{{ github.contributors }}", self.formatted_contributors)
