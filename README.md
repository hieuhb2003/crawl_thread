# crawl_thread
## Env
```bash
$ conda create -n crawler python=3.10.14
```
## Activate
```bash
$ conda activate crawler python=3.10.14
```
## Select Interpreter in VS Code

Open VS Code.

Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) to open the Command Palette.

Type Python: Select Interpreter and select it.

From the list, select the interpreter for the crawler environment (Python 3.10.14 ('crawler': conda)).

## Installation
```bash
$ pip install -r requirements.txt
```
## Run
```bash
make USERNAME=<your_thread_username> PASSWORD=<your_thread_password> NUMBER=<number_reload_thread> 
```
