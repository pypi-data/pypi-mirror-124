# flake8-escaping-style

A [flake8](https://flake8.pycqa.org) plugin to help maintain a consistent style
of escape sequences in string and bytes literals throughout your project.

## Installation

This plugin requires at least version 3.7 of Python.

Like most flake8 plugins, start by installing the package:
```
pip install flake8-escaping-style
```

Then in your flake8 configuration, use a combination of `select` and `ignore`
that matches your preferences.

For example, here's how it would look like if you wanted to prevent all escapes
except for `\N{name of character}`:
```
select=ESC1
ignore=ESC105
```


## List of error codes

### For string literals (`str`)

| Error code | Escape sequence style  | Example string (`"café"`)                  |
| ---------- | ---------------------- | ------------------------------------------ |
| `ESC101`   | Octal (3 digits)       | `"caf\351"`                                |
| `ESC102`   | Hexadecimal (2 digits) | `"caf\xe9"`                                |
| `ESC103`   | Hexadecimal (4 digits) | `"caf\u00e9"`                              |
| `ESC104`   | Hexadecimal (8 digits) | `"caf\U000000e9"`                          |
| `ESC105`   | Named character        | `"caf\N{latin small letter e with acute}"` |


### For byte string literals (`bytes`)

For completeness's sake, this plugin can also detect escape styles in bytestring
literals:

| Error code | Escape sequence style  | Example bytestring |
| ---------- | ---------------------- | ------------------ |
| `ESC201`   | Octal (3 digits)       | `b"caf\351"`       |
| `ESC202`   | Hexadecimal (2 digits) | `b"caf\xE9"`       |


## Motivation

Python has several different ways to write
[escape sequences](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals).

In the old days of Python 2, any file was assumed to be ascii encoded unless
you added a special comment on the first line. That meant that if you wanted
to write the string `"café"` in your source code, you had to either add that
comment on the first line of your file, or use an escape sequence like
`"caf\xe9"` or `"caf\u00E9"`.

Nowadays, Python has lifted those limitations and uses a more practical default
encoding (utf-8, see [PEP3120](https://www.python.org/dev/peps/pep-3120/)).
So for most string literals you can use the character you want without having
to use escape sequences at all.

I'd still recommend using an escape sequence when using "weird" [^1] characters
and especially invisible ones. But in that case I like to use the "named character"
escaping style `\N{name}`.

[^1]: By "weird" I mean any character that requires more than two fingers to
type on my keyboard.

Consider for example the case of a [non-breaking space](https://en.wikipedia.org/wiki/Non-breaking_space).
It's a nifty little character and it can be very useful sometimes but it can
also lead to some tough debugging:

Can you spot the difference?
```
>>> "hello world" == "hello world"
False
```

Using an escape sequence here (rather than the character itself) makes it more
obvious as to what is going on:
```
>>> "hello world" == "hello\xa0world"
False
```

That's better in my opinion, but it still requires knowing which character has
the number `A0` in hexadecimal. The best option is to use a named escape sequence:
```
>>> "hello world" == "hello\N{no-break space}world"
False
```

For that reason, I prefer my projects to only use the "named" style of escape
sequences (`ESC105`).
