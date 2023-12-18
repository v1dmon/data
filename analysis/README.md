```bash
$ nix develop
$ cd ../benchmark
$ poetry --directory ../analysis run jupyter notebook
```

```bash
$ poetry install
$ poetry shell
$ export LD_LIBRARY_PATH=(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:$LD_LIBRARY_PATH
```
