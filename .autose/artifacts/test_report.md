# Test report

Tests written: tests_autose/test_limit_search.py

Verdict: FAIL

```
full suite failed:
s in bytes, and therefore any "input" should
        be bytes, and the stdout and stderr will be bytes. If in text mode, any
        "input" should be a string, and stdout and stderr will be strings decoded
        according to locale encoding, or by "encoding" if set. Text mode is
        triggered by setting any of text, encoding, errors or universal_newlines.
    
        The other arguments are the same as for the Popen constructor.
        """
        if input is not None:
            if kwargs.get('stdin') is not None:
                raise ValueError('stdin and input arguments may not both be used.')
            kwargs['stdin'] = PIPE
    
        if capture_output:
            if kwargs.get('stdout') is not None or kwargs.get('stderr') is not None:
                raise ValueError('stdout and stderr arguments may not be used '
                                 'with capture_output.')
            kwargs['stdout'] = PIPE
            kwargs['stderr'] = PIPE
    
        with Popen(*popenargs, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(input, timeout=timeout)
            except TimeoutExpired as exc:
                process.kill()
                if _mswindows:
                    # Windows accumulates the output in a single blocking
                    # read() call run on child threads, with the timeout
                    # being done in a join() on those threads.  communicate()
                    # _after_ kill() is required to collect that and add it
                    # to the exception.
                    exc.stdout, exc.stderr = process.communicate()
                else:
                    # POSIX _communicate already populated the output so
                    # far into the TimeoutExpired exception.
                    process.wait()
                raise
            except:  # Including KeyboardInterrupt, communicate handled that.
                process.kill()
                # We don't call process.wait() as .__exit__ does that for us.
                raise
            retcode = process.poll()
            if check and retcode:
>               raise CalledProcessError(retcode, process.args,
                                         output=stdout, stderr=stderr)
E               subprocess.CalledProcessError: Command '['git', 'diff', 'origin/main', '--', 'tinydb']' returned non-zero exit status 1.

/opt/hostedtoolcache/Python/3.12.16/x64/lib/python3.12/subprocess.py:571: CalledProcessError
----------------------------- Captured stdout call -----------------------------
[implementation] already passed, skipping
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.16-final-0 _______________

Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
tinydb/__init__.py          5      0      0      0   100%
tinydb/database.py         57      0     10      0   100%
tinydb/middlewares.py      44      3     14      3    90%
tinydb/mypy_plugin.py      26     26      2      0     0%
tinydb/operations.py       26      0      0      0   100%
tinydb/queries.py         130      2     30      4    96%
tinydb/storages.py         57      0      8      0   100%
tinydb/table.py           248      1    114      8    98%
tinydb/utils.py            78      1     18      1    98%
tinydb/version.py           1      0      0      0   100%
---------------------------------------------------------
TOTAL                     672     33    196     16    94%
=========================== short test summary info ============================
FAILED workflow/tests/test_testing_coverage.py::TestingCoverage::test_explicit_untested_criterion_blocks_testing_gate - subprocess.CalledProcessError: Command '['git', 'diff', 'origin/main', '--', 'tinydb']' returned non-zero exit status 1.
=================== 1 failed, 287 passed, 1 skipped in 1.41s ===================

```
