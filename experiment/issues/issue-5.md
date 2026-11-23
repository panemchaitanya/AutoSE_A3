# Issue 5 (vague report) - posted to the fork on GitHub

Title: Searches sometimes return data that doesn't match what's in the db??

Body:

This is driving me nuts. Sometimes a search returns documents with values
that are NOT what's stored. Example: I search for something, tweak the
returned dicts a bit for display purposes (like formatting a field), and
later when I run the SAME search again the old tweaked values show up even
though I never called update or anything. It's like tinydb remembers my
display edits.

If I restart the script the data is fine again, so the file itself is OK. It
only happens within one run and only sometimes (maybe only when I edit the
dicts I got back?). Is this a caching bug? Can you make it so the documents
you get back from search/all are just... normal dicts you can safely edit
without side effects?

Not sure what exactly is going on, happy to provide more info if you tell me
what you need.
