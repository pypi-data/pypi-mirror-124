# tljh-new-user

`tljh-new-user` is a plugin for [The Littlest JupyterHub (TLJH)](https://tljh.jupyter.org) which 
runs after a user is created. 

When run, the plugin copies the folder `new_user_data` (if found) 
in the `state/` folder (typically installed at `/opt/tljh/state)`
into the home directory of the new user. Ownership of the data in 
the home directory is then recursively
set to the user.

Additionally, the plugin looks in `state/` for an executable file 
called `new_user_script` and runs it if it exists. The
script receives the username as its only argument.

# Install

Include `--plugin tljh-new-user` in your TLJH install script.  An 
example install with admin user `administrator` would be:

```
#!/bin/bash
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
  | sudo python3 - \
    --admin administrator --plugin tljh-new-user
```
