{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python311
        poetry
      ];
      env = {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc
        ];
        POETRY_VIRTUALENVS_IN_PROJECT = "true";
        POETRY_VIRTUALENVS_PATH = "./.venv";
        POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON = "true";
      };
      shellHook = ''
        poetry install
        poetry shell
      '';
    };
  };
}
