# Taskover

A simple and fast todo list with Vim-like keybindings made in `Python`.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

![image](https://i.imgur.com/PBA0LaH.png)

Stay on top of your tasks with this terminal-based tool!

Add tasks with ease, mark them as done and delete them when you're finished.
And if you use Vim, this program's commands will be familiar.

This program is minimal and only requires Python 3. If you know some Python, it's easy to hack and change this program to suit your needs.

## Dependencies

`python3`

## Installation

`git clone https://github.com/angelofallars/taskover`

`cd taskover`

Linux:

`chmod +x ./taskover`

`ln -s </path/to/taskover/executable> ~/.local/bin`

~~Run on Windows:~~

~~`python3 .\taskover`~~ (Windows support is not yet implemented for this
        version.)

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
