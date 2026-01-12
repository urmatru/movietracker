from rich.tree import Tree
from rich.console import Console
from pathlib import Path

def print_project_tree(path: Path, tree: Tree = None, ignore_dirs=None, max_depth=3, current_depth=0):
    if ignore_dirs is None:
        ignore_dirs = ['node_modules', '__pycache__']  # игнорируем всякую ерунду, .venv и подобные обработаем отдельно
    if tree is None:
        tree = Tree(f"📁 {path.name}")
    if current_depth >= max_depth:
        return tree

    # Собираем dirs и files отдельно для сортировки
    dirs = []
    files = []
    for child in path.iterdir():
        if child.name.startswith('.'):  # игнорируем скрытые файлы и папки, включая .venv, .venv310 и т.д.
            continue
        if child.is_dir() and child.name not in ignore_dirs:
            dirs.append(child)
        elif child.is_file():
            files.append(child)

    # Сортируем и добавляем dirs
    for child in sorted(dirs):
        branch = tree.add(f"📁 {child.name}")
        print_project_tree(child, branch, ignore_dirs, max_depth, current_depth + 1)

    # Сортируем и добавляем files
    for child in sorted(files):
        tree.add(f"📄 {child.name}")

    return tree

console = Console()
path = Path(".")  # текущая папка проекта
tree = print_project_tree(path, max_depth=3)  # ограничиваем глубину до 3 уровней, чтобы не углубляться дальше приложений
console.print(tree)