### Nix

```bash
# Nix only!
# Skip if they are already enabled. 
# Enable nix experimental features:
$ export NIX_CONFIG="experimental-features = nix-command flakes"

# Nix only!
$ nix develop
# Wait until you are led to a poetry shell.
(venv) $ jupyter notebook # ...
```

### Manual

```bash
# Nix only!
# Skip if you already have these dependencies.
# Install poetry and python version 3.11.
$ nix shell nixpkgs#poetry nixpkgs#python311

$ poetry install
$ poetry shell
(venv) $ hx . # ...

# NixOS only!
# jupyter notebook command fix:
# ImportError: libstdc++.so.6 cannot open shared object file: No such file or directory
(venv) $ export LD_LIBRARY_PATH=(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:$LD_LIBRARY_PATH
(venv) $ jupyter notebook
```
