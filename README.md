# pydirl
simple static webserver and directory listing built with Flask and Bootstrap


Did you ever used `python3 -m http.server` to quickly share files or serve static content?
This is an improoved version with the following features:
 - concurrent requests support (gevent)
 - responsive interface built with bootstrap
 - download folder as archive (allanlei/python-zipstream)
 - intuitive command line interface
 - exclude files and folder through regular expression
 - request and debug logging
 - single file mode

## Usage

 - Share the current working directory:
   ```pydirl```

 - Share the current working directory on custom port:
   ```pydirl -p 1235```

 - Share a specific subtree:
   ```pydirl /path/to/the/root/```

 - Do not show hidden file:
   ```pydirl --exclude="^\."```

 - Single file mode: share a single file
   ```pydirl ./my_file.ext```

Once the server is up and running you can use a browser to navigate the shared subtree, download files and entire folders.
