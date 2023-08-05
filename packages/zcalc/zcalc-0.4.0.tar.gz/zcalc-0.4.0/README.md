# zcalc

[![Build Status](https://app.travis-ci.com/blackchip-org/zcalc.svg?branch=main)](https://app.travis-ci.com/blackchip-org/zcalc)

A fun RPN calculator. If you find it fun too, let me know. This is a constant work in progress.

To install and run from PyPI:

```bash
python3 -m pip install --upgrade pip
pip3 install zcalc
zcalc
```

## Goals

- Have fun!
- Easy to type. Avoid the shift key in the common case. Prefer the name of `a` for addition over `+`
- Use fixed point arithmetic when possible. Prefer `3.3` for `1.1 + 2.2` over `3.3000000000000003`
- Auto-completion
  - Operations should have descriptive names and easily found by auto complete.
  - Commonly used operations should have easy-to-type aliases. Example: `scientific-notation` and `sn`.
- Documentation should also be test cases.

## Usage

When running `zcalc` a prompt is presented. When a line is entered at the
prompt, it first checked to see if it is the name of an operation. If so, that
operation is performed. Otherwise, the line is placed on the stack.

An example of adding two numbers:

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `2`              | `1 ; 2`
| `a`              | `3`

The first line, `1`, does not match an operation so its value is
placed on the stack. The next line is a `2` and is also placed on the stack.
When `a` is entered, that matches the addition operation. The first two
items are popped from the stack, the result is added, and the result is
placed back on the stack.

When examples are presented in this input/stack table format, each row
shows the state of the *stack* after *input* is entered at the prompt.
Stack items are separated by semicolons and the top element on the stack
is at the right.

Operations may have name aliases. The addition operation has a standard long form (`add`), a traditional operator form (`+`) and a short form that is easy
to type without the use of the shift key (`a`).

The basic math operations are as follows:

| Operation        | Description
|------------------|-----------------|
| `add`, `+`, `a`  | addition
| `sub`, `-`, `s`  | subtraction
| `mul`, `*`, `m`  | multiplication
| `div`, `/`, `d`  | division

More basic math operations can be found in the [math](doc/stdlib/math.md) module documentation.

### Quoting, Multi-lines, and Whitespace

Any type of value can be pushed to the stack as long as it isn't the name of an
operation. To push the name of an operation to the stack instead of evaluating
it, start the line with a single quote (`'`). In the following example, the
`len` operation is used to return the length of text:

| Input                | Stack
|----------------------|-------------|
| `apples and bananas` | `apples and bananas`
| `len`                | `18`
| `'len`               | `18 ; len`
| `len`                | `18 ; 3`

Multiple lines can be submitted on the same line by separating each line with a semicolon (`;`):

| Input                | Stack
|----------------------|-------------|
| `'len; len`          | `3`

Whitespace is significant. Placing a space between the string and semicolon
changes the result:

| Input                | Stack
|----------------------|-------------|
| `'len ; len`         | `4`

### Prefix notation

While RPN works great for calculations, sometimes it is more natural to use
prefix notation. Using postfix notation, the following can be rounded with:

| Input            | Stack
|------------------|-------------|
| `2`              | `2`
| `3`              | `2 ; 3`
| `d`              | `0.6666666666666667`
| `2`              | `0.6666666666666667 ; 2`
| `round`          | `0.67`

With prefix notation, this can instead be as follows:

| Input            | Stack
|------------------|-------------|
| `2`              | `2`
| `3`              | `2 ; 3`
| `d`              | `0.6666666666666667`
| `[round 2`       | `0.67`

To use prefix notation the line must start with a `[` and be directly followed
by the operation name. Any additional text is treated as arguments to the
operation and each argument is separated by whitespace.

| Input            | Stack
|------------------|-------------|
| `[a 1 2`         | `3`

Arguments in prefix notation are always treated as values and never
evaluate as operations:

| Input            | Stack
|------------------|-------------|
| `[len len`       | `3`

If the operation needs more arguments than provided, the additional arguments
are consumed from the stack.

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `[a 2`           | `3`

If more arguments are provided than needed by the operation, the extra
arguments are pushed to the stack.

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `[a 2 3 4`       | `1 ; 2 ; 7`

Leading and trailing whitespace are not significant with arguments. Surround
arguments with single quotes if necessary:

| Input            | Stack
|------------------|-------------|
| `[len ' len`     | `4`
| `[len ' len '`   | `4 ; 5`

### Macros

Define a macro by starting a line with a back quote (`` ` ``) followed by the
macro name. All items on the stack are added to the macro. Recall the macro
with an equals sign (`=`) followed by the macro name. Example:

| Input            | Stack
|------------------|-------------|
| `2`              | `2`
| `'m`             | `2 ; m`
| `` `double``     |
| `6`              | `6`
| `=double`        | `12`

If the macro definition has arguments, those are used instead of the stack.
Arguments in this context follow the same rules as arguments in prefix
notation:

| Input            | Stack
|------------------|-------------|
| `` `double 2 m`` |
| `6`              | `6`
| `=double`        | `12`

As a shortcut for a common operation, a macro that is defined with the name
of `=` can simply be recalled with `=`.

| Input            | Stack
|------------------|-------------|
| `` `= 2 m``      |
| `6`              | `6`
| `=`              | `12`

### Stack Operations

Pop the top item from the stack by entering a blank line:

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `2`              | `1 ; 2`
|                  | `1`

Clear the entire stack with `clear` or `c`:

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `2`              | `1 ; 2`
| `c`              |

Undo the previous action with `undo` or `u`:

| Input            | Stack
|------------------|-------------|
| `1`              | `1`
| `2`              | `1 ; 2`
| `a`              | `3`
| `u`              | `1 ; 2`

Apply a macro to each item in the stack with `each`:

| Input            | Stack
|------------------|-------------|
| `` `double 2 m`` |
| `1`              | `1`
| `2`              | `1 ; 2`
| `3`              | `1 ; 2 ; 3`
| `[each double`   | `2 ; 4 ; 6`

More stack operations can be found in the [builtin](doc/stdlib/builtin.md) module documentation.

### Modules

Operations provided by the calculator are grouped into modules. The `builtin`
module always has its operations available. Modules that belong to the
prelude have their operations available by default when starting the
application. Other modules must be explicitly imported with the `use` operation.
Example:

| Input            | Stack
|------------------|-------------|
| `[use unit`      |
| `0`              | `0`
| `C->F`           | `32`

The `unit` module contains submodules. With `[use unit`, all operations in
the submodules are included. To include only a submodule, use the following:

| Input            | Stack
|------------------|-------------|
| `[use unit.temp` |
| `0`              | `0`
| `C->F`           | `32`

The list of modules available are as follows:

| Name                                 | Auto?     | Description
|--------------------------------------|-----------|----------------|
| [bit](doc/stdlib/bit.md)             | prelude   | Bitwise operations
| [builtin](doc/stdlib/builtin.md)     | always    | Builtin operations
| [math](doc/stdlib/math.md)           | prelude   | Basic math operations
| [sci](doc/stdlib/sci.md)             | prelude   | Scientific math operations
| [str](doc/stdlib/str.md)             | prelude   | String operations
| [unit.temp](doc/stdlib/unit/temp.md) |           | Temperature conversions

## Development Setup

In general:

```bash
pip3 install -e .
zcalc
```

Setup python 3.7 environment on macOS:

```bash
brew install python@3.7
/usr/local/opt/python@3.7/bin/python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Setup environment on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Running tests:

```bash
pip install pytest
python -m unittest
```

## License

MIT
