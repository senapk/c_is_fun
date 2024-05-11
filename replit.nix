{ pkgs }: {
	deps = [
   pkgs.plantuml
    pkgs.neovim
		pkgs.clang_12
		pkgs.ccls
		pkgs.gdb
		pkgs.gnumake
	];
}