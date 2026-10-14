## lab5

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe temporary file creation | Security — High | 40 | `tempfile.mktemp()` generates a temporary filename without securely creating the file, which can introduce a race condition. | Use `tempfile.NamedTemporaryFile()` to create the file safely. |
| Broad exception handler | Reliability — Medium | 18–19 | A bare `except` catches unexpected exceptions and hides the actual cause of a failure. | Catch specific exceptions such as `KeyError` and `ValueError`. |
| Mutable default argument | Code quality — Medium | 10 | `logs=[]` is a mutable default argument that can be shared across calls. | Use `None` as the default and create a new list inside the function. |
| Invalid inspection interval | Logic — Medium | 29–31, 57 | The program accepts negative inspection intervals, producing incorrect inspection results. | Validate that the interval is a positive integer. |
| Empty asset identifier | Logic — Medium | 53 | An asset with an empty identifier can be registered, making the registry unreliable. | Reject empty or whitespace-only identifiers. |
| Duplicate asset registration | Logic — Medium | 54 | Registering `FL-01` again overwrites its existing machine type. | Reject duplicate asset IDs. |
| Unclosed file handling pattern | Code quality — Low | 34–36, 41–43 | Files are opened and closed manually, so exceptions could prevent them from being closed properly. | Use `with open(...)` or a context manager. |
| Incorrect function naming style | Style — Low | 46 | `printAlerts()` uses camelCase instead of the conventional Python snake_case style. | Rename it to `print_alerts()`. |
| Unused import | Code quality — Low | 2 | The `logging` module is imported but never used. | Remove the unused import. |
| Runtime assertion | Reliability — Low | 61 | An assertion is used for a runtime check, although assertions can be disabled. | Use an explicit conditional check. |

## Summary

The original program has security, reliability, style, and logic issues. The revised program validates asset identifiers, prevents duplicate registrations, handles invalid dates, validates inspection intervals, uses safer file handling, and follows Python naming conventions.
