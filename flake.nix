# nix develop 
{
  description = "Python development setup with Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    {
      devShells.x86_64-linux =
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
        python = pkgs.python3.withPackages (ps: with ps; [
          matplotlib
          pyinstaller
        ]);
      in
      {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python
            tk 
          ];
        };
      };
    };
}