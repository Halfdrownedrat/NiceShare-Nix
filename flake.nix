# To run the flake:
# nix develop 

# BROKEN: 
# To create/update the requirements.nix 
# nix run github:nix-community/pip2nix -- generate -r requirements.txt
{
  description = "NiceShare development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python314
            uv
            tk
          ];

          shellHook = ''
            export UV_PYTHON_PREFERENCE=only-system
            export UV_PYTHON=python314
            
            echo "Python: $(python --version)"
            echo "Syncing dependencies..."
            uv sync --dev
            echo "Start with \"niceshare\""
          '';
        };
      }
    );
}