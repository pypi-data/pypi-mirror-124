"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

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

import datetime
from typing import Dict, Any, Optional, List
from dateutil import parser
from .abc import Messageable
from .http import HTTPClient
from .metrics import UserPublicMetrics



class User(Messageable):
    """
    Represent a user in Twitter.
    This user is an account that has created by other person, not from an apps.

    Parameters:
    ===================
    data: Dict[str, Any]
        The complete data of the user through a dictionary!

    Attributes:
    ===================
    original_payload
        Represent the main data of a tweet.

    http_client
        Represent a :class: HTTPClient that make the request.
    
    user_metrics
	    Represent the public metrics of the user.
    """

    def __init__(self, data: Dict[str, Any], **kwargs):
        super().__init__(data, **kwargs)
        self.original_payload = data
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None
        self.user_metrics = UserPublicMetrics(self.original_payload)

    def __str__(self) -> str:
        return "<User: name={0.name} username={0.username} bio={0.bio} id={0.id} created_at={0.created_at} verified={0.verified} protected={0.protected} avatar_url={0.avatar_url} location={0.location} followers_count={0.followers_count} following_count={0.following_count} tweet_count={0.tweet_count}>".format(
            self
        )

    def __repr__(self) -> str:
        return "<User Object: {0.username}>".format(self)

    @property
    def name(self) -> str:
        """str: Return the user's name."""
        return self.original_payload.get("name")

    @property
    def username(self) -> str:
        """str: Return the user's username, this usually start with '@' follow by their username."""
        return "@" + self.original_payload.get("username")

    @property
    def id(self) -> int:
        """id: Return the user's id."""
        return int(self.original_payload.get("id"))

    @property
    def bio(self) -> str:
        """str: Return the user's bio."""
        return self.original_payload.get("description")

    @property
    def description(self) -> str:
        """str: Return the user's bio, an alias to :class:User.bio"""
        return self.original_payload.get("description")

    @property
    def profile_link(self) -> str:
        """str: Return the user's profile link"""
        return f"https://twitter.com/{self.username.replace('@', '', 1)}"

    @property
    def link(self) -> str:
        """str: Return url where the user put links, return an empty string if there isnt a url"""
        return self.original_payload.get("url")

    @property
    def verified(self) -> bool:
        """bool: Return True if the user is verified account, else False."""
        return self.original_payload.get("verified")

    @property
    def protected(self) -> bool:
        """bool: Return True if the user is protected, else False."""
        return self.original_payload.get("protected")

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[str]: Return the user profile image."""
        return self.original_payload.get("profile_image_url")

    @property
    def location(self) -> Optional[str]:
        """str: Return the user's location"""
        return self.original_payload.get("location")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:datetime.datetime: Return datetime.datetime object with the user's account date."""
        date = str(parser.parse(self.original_payload.get("created_at")))
        y, mo, d = date.split("-")
        h, mi, s = date.split(" ")[1].split("+")[0].split(":")

        return datetime.datetime(
            year=int(y),
            month=int(mo),
            day=int(d.split(" ")[0]),
            hour=int(h),
            minute=int(mi),
            second=int(s),
        )

    @property
    def followers(self) -> List[object]:
        """List[:class:object]: Returns a list of users (object) who are followers of the specified user ID."""
        return self.original_payload.get("followers")

    @property
    def following(self) -> List[object]:
        """List[:class:object]: Returns a list of users thats followed by the specified user ID."""
        return self.original_payload.get("following")

    @property
    def followers_count(self) -> int:
        """int: Return total of followers that a user has."""
        return int(self.user_metrics.followers_count)

    @property
    def following_count(self) -> int:
        """int: Return total of following that a user has."""
        return int(self.user_metrics.following_count)

    @property
    def tweet_count(self) -> int:
        """int: Return total of tweet that a user has."""
        return int(self.user_metrics.tweet_count)

    @property
    def listed_count(self) -> int:
        """int: Return total of listed that a user has."""
        return int(self._metrics.listed_count)