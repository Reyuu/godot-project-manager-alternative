import pathlib
import shutil
import subprocess

root_path = pathlib.Path(".")
shutil.rmtree(root_path / "main.out")

out_path = root_path / "main.out"
out_icons = out_path / "icons"

res = subprocess.run(
    "venv\\Scripts\\python -m nuitka --follow-imports --enable-plugin=pyside6 --disable-console --onefile .\main.py"
)
res.check_returncode()

shutil.copytree(root_path / "icons", out_path / "icons")
shutil.copy2(root_path / "config_template.json", out_path / "config_template.json")
shutil.copy2(root_path / "README.md", out_path / "README.md")
shutil.copy2(root_path / "main.exe", out_path / "main.exe")
shutil.move(out_path / "main.exe", out_path / "GBPM.exe")
