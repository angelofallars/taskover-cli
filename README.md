# 📕 Taskover <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>

<img src="https://i.imgur.com/PBA0LaH.png" alt="taskover command line interface" align="right" height="240px">

**Taskover** is a simple and fast todo list with Vim-like keybindings made in `Python`.

- Add tasks swiftly, mark them as done and delete them when you're finished.
- If you use Vim, this program's commands will be familiar.

This program is minimal and only requires Python 3. If you know some Python, it's easy to hack and change this program to suit your needs.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) 

## Dependencies

`python3`

`xdg`

## How to run

Unix-based (Linux)

`git clone https://github.com/angelofallars/taskover`

`cd taskover`

`chmod +x ./taskover`

`./taskover`

~~Windows~~ (Not supported in this version again)

`git clone https://github.com/angelofallars/taskover`

`cd taskover`

`python3 .\main.py`

## Usage

`taskover` - Run the program

```
usage: taskover [options]

Options:
  help        Display this help message.
  list        Print the tasks ordered numerically and exit.

Program keywords:
  j - move downwards
  k - move upwards
  i - Insert a new task
  u - Update the description of a task
  m - Mark a task as done (or unmark a completed task)
  d - Delete a task
  q - Quit the program
```

## Contributing

This project is still in progress. Feel free to make a fork and contribute
changes you think will be good!
