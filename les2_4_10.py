from typing import Generator


def my_awesome_gen() -> Generator[str, str, None]:
    output: str = yield 'Hello!'
    while True:
        output = yield (
            output.capitalize() if output.isalpha() else output.lower()
        )


g = my_awesome_gen()

print(g.send(None))  # type: ignore # выводит Hello!
print(g.send("COOL!"))  # выводит cool!
print(g.send("Das Auto"))  # выводит das auto
print(g.send("nIcE"))  # выводит Nice
