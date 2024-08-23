[PhysLatexSync](https://pythonlatexsync.achilleme.com/) hosted on my server.

# PythonLatexSync
A seamless service that provides automatic, real-time synchronization from your Python scripts to Overleaf documents. Enhance your workflow by keeping your code and LaTeX documents perfectly in sync, without any manual copy-pasting.

# Python usage
Installation is from this Github repo using pip VCS support
```
pip install -e "git+https://github.com/prenone/PythonLatexSync#egg=PythonLatexSync&subdirectory=pls"
```

Please see `pls/example.py` for usage of the library

# Overleaf usage
From the **Upload dialog** select **From external URL** and add the URL that is returned by `pls.push` (or the URL from the API docs).

When the assets is pushed from Python it can be pulled from Overleaf by just pressing the **Refresh** button for that asset.

## Tampermonkey
This Tampermonkey script `Overleaf.js` adds the "Refresh All Linked items" feature to the file tree toolbar
![Screenshot](https://achilleme.com/static/pls/overleaf_screenshot.png)
This features programmaticallys opens each linked assets and emulates clicking the Refresh button.

# API Docs
[https://pythonlatexsync.achilleme.com/docs](https://pythonlatexsync.achilleme.com/docs)
