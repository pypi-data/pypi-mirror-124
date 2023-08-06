# Simple Shell

Run a shell command, and receive `stdout`, `stderr`, and `returncode`.  It's dead simple.

```python
$ python3
[...]
>>> from simpleshell import ss
>>> output = ss('head -3 LICEN*')
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout=['MIT License', '', 'Permission is hereby granted, free of charge, to any person obtaining a copy'],
    stderr=['']
)
>>>
```
All calls are synchronous, therefore it's not possible to see the output until the command exits. This makes Simple Shell unsuitable for `tail`ing a log.
## Return values
### On success
`CompletedProcess` object with member variables `args`, `returncode`, `stdout`, `stderr`.

`stdout` and `stderr` may be a `str` or a `list[str]` based on optional parameter `convert_stdout_stderr_to_list`.
### On error
```python
if optional parameter 'exit_on_error':
    nothing
else:
    subprocess.CalledProcessError exception object
```

## Optional parameters
* ### `print_output_on_success=True`
When `False`, nothing gets printed when the command exits with `0`.
```python
>>> output = ss('head -3 LICEN*', print_output_on_success=False)
>>>
```

* ### `print_output_on_error=True`
When `False`, nothing gets printed when the command exists with a non-`0`.  
In the below example, the command exited with return code `127` and caused the `python3` process to exit.
```python
>>> output = ss('invalid command', print_output_on_error=False)
$ echo $?
127
$
```

* ### `convert_stdout_stderr_to_list=True`
When `False`, `output.stdout` and `output.stderr` are strings with `\n` embedded in them.
```python
>>> output = ss('head -3 LICEN*', convert_stdout_stderr_to_list=False)
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout='MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\n',
    stderr=''
)
>>>
```

* ### `keep_empty_lines=True`
When `False` and `convert_stdout_stderr_to_list` is `True`, empty lines form `output.stdout` and `output.stderr` lists are removed.

In the below example, there is an empty line after the first line `MIT License`, but `output.stdout` list doesn't contain the empty line.

⚠️ This parameter does not change the way output is printed.
```python
>>> output = ss('head -3 LICEN*', keep_empty_lines=False)
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>> print(output)
CompletedProcess(
    args='head LICEN*',
    returncode=0,
    stdout=['MIT License', 'Permission is hereby granted, free of charge, to any person obtaining a copy'],
    stderr=[]
)
>>>
```

* ### `exit_on_error=True`
When `False`, a command exiting with a non-`0` return code doesn't cause the `python3` process to exit. Afterward, `subprocess.CalledProcessError` exception object is returned so that the caller can further examine the error.
```python
>>> output = ss('invalid command', exit_on_error=False)
/bin/sh: invalid: command not found

>>> print(type(output))
<class 'subprocess.CalledProcessError'>
>>> print(output)
Command 'invalid command' returned non-zero exit status 127.
>>>
```

* ### `echo=False`
When `True`, the command is printed before the output is printed. This is useful for creating a screen capture which shows the command that was run.

⚠️ The leading `$` does not change to `#` even if you're `root`. PR welcome.
```python
>>> output = ss('head -3 LICEN*', echo=True)
$ head -3 LICEN*
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy

>>>
```

* ### `timeout=60`
Number of seconds to wait for the process to finish before exiting with an error. Since all calls are synchronous, it's not possible to see the output until the command exits.

In the below example, the exception detail was printed because `print_output_on_error` defaults to `True`, and the `python3` process exited because `exit_on_error` also defaults to `True`.
```python
>>> ss('sleep 10', timeout=3)
Command 'sleep 10' timed out after 3 seconds
$
```
