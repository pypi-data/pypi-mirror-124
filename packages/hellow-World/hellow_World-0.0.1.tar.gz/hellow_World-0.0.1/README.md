# hellow_world
A package to difficult task of printing "Hello World".

There are 3 data types.

- `Character`
- `Message`
- `Hello`

## `Character`
`Character` is used to create a character.

For example, one can create a character `h` as such:

```python
from hello_world import Character

c = Character("h")
```

## `Message`
`Message` is a data type to combine characters.

For example, one can create a message `ab` as such:

```python
from hello_world import Character, Message

a = Character("a")
b = Character("b")

m = Message([a, b])
```

or for an easy usage one can directly embed a `Character` to the list:

```python
from hello_world import Character, Message

m = Message([Character("a"), Character("b")])
```

## `Hello`
`Hello` is a data type to display a message.

For example, one can print a message as such:

```python
from hello_world import Character, Message, Hello

m = Message([Character("a"), Character("b")])

h = Hello(m)
h.print()
```

## Example for `Hello World`

```python
from hello_world import Character, Message, Hello

if __name__ == '__main__':
    m = Message(
        [
            Character("H"), Character("e"), Character("l"),
            Character("l"), Character("o"), Character(" "),
            Character("W"), Character("o"), Character("r"),
            Character("l"), Character("d"), Character("!")
        ]
    )
    h = Hello(m)
    h.print()
```
Voilà. Here you have "Hello World!" printed.

See jupyter example: https://github.com/mshemuni/hellow_world/blob/main/example.ipynb
