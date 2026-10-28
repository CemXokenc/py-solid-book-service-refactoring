import json
from typing import TypeVar
from xml.etree.ElementTree import Element, SubElement, tostring
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class DisplayContent(ABC):
    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplayContent(DisplayContent):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplayContent(DisplayContent):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class PrintBook(ABC):
    def __init__(self, method: DisplayContent) -> None:
        self.method = method

    @abstractmethod
    def print(self, book: Book) -> None:
        pass


class ConsolePrintBook(PrintBook):
    def print(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        self.method.display(book)


class ReversePrintBook(PrintBook):
    def print(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        self.method.display(book)


class SerializeBook(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JSONSerializeBook(SerializeBook):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XMLSerializeBook(SerializeBook):
    def serialize(self, book: Book) -> str:
        root = Element("book")
        title = SubElement(root, "title")
        title.text = book.title
        content = SubElement(root, "content")
        content.text = book.content
        return tostring(root, encoding="unicode")


DISPLAYS: dict[str, DisplayContent] = {
    "console": ConsoleDisplayContent(),
    "reverse": ReverseDisplayContent(),
}

PRINTERS: dict[str, PrintBook] = {
    "console": ConsolePrintBook(ConsoleDisplayContent()),
    "reverse": ReversePrintBook(ReverseDisplayContent()),
}

SERIALIZERS: dict[str, SerializeBook] = {
    "json": JSONSerializeBook(),
    "xml": XMLSerializeBook(),
}

T = TypeVar("T")


def get_handler(registry: dict[str, T], key: str, kind: str) -> T:
    try:
        return registry[key]
    except KeyError:
        raise ValueError(f"Unknown {kind} type: {key}") from None


def main(book: Book, commands: list) -> None | str:
    for cmd, method_type in commands:
        match cmd:
            case "display":
                get_handler(DISPLAYS, method_type, cmd).display(book)
            case "print":
                get_handler(PRINTERS, method_type, cmd).print(book)
            case "serialize":
                return get_handler(SERIALIZERS, method_type, cmd).serialize(
                    book,
                )
    return None


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
