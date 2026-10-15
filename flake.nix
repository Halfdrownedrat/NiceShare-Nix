# To run: nix develop 
# To reinitialize the: nix flake update
# Manuall uv sync: uv sync --dev 
# To run the project: uv run niceshare

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
            gcc-unwrapped
          ];

          # Potential issue with loading from env, replace later with better reading or secret managment

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.gcc-unwrapped.lib}/lib:$LD_LIBRARY_PATH
            export UV_PYTHON_PREFERENCE=only-system
            export UV_PYTHON=python314

            export NEXTCLOUD_TOKEN=my-super-secret-nextcloud-app-token
            export NEXTCLOUD_USER=exampleuser
            export NEXTCLOUD_DOMAIN=cloud.example.org

            export UI_STORAGE_SECRET=somerandomstringlongenoughtobesafe
            export UI_ADMIN_PASSWORD="some password you will use to log in to admin panel"
            export UI_AUTH_SECRET=somerandomstringlongerthan32characters

            export MAIL_USER=user@example.org
            export MAIL_PORT=465
            export MAIL_PASSWORD="my super secret mail password"
            export MAIL_DOMAIN=mailserver.example.org

            echo "Python: $(python --version)"
            echo "Syncing dependencies..."
            uv sync --dev
            echo "Start with \"uv run niceshare\""
          '';
        };
      }
    );
}