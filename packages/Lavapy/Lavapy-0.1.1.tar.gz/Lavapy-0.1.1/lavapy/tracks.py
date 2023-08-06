"""
MIT License

Copyright (c) 2021-present Aspect1103

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
from typing import Dict, Any, List


class Track:
    def __init__(self, id: str, info: Dict[str, Any]) -> None:
        self.id = id
        self.info: Dict[str, Any] = info
        self.identifier: str = info.get("identifier")
        self.isSeekable: bool = info.get("isSeekable")
        self.author: str = info.get("author")
        self.length: int = info.get("length")
        self.type: str = info.get("sourceName")
        self.title: str = info.get("title")
        self.uri: str = info.get("uri")

    def __repr__(self) -> str:
        return f"<Lavapy Track (Identifier={self.identifier}) (Type={self.type})>"


class Playlist:
    def __init__(self, name: str, tracks: List[Dict[str, Any]]):
        self.name = name
        self.tracks = [Track(track["track"], track["info"]) for track in tracks]

    def __repr__(self):
        return f"<Lavapy Playlist (Name={self.name}) (Track count={len(self.tracks)})>"
