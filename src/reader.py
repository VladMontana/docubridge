from pathlib import Path
from dataclasses import dataclass


@dataclass
class DocFile:
    name: str
    path: Path
    content: str


class DocsReader:
    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = docs_dir

    def list_libraries(self) -> list[str]:
        """Список доступных библиотек (папок верхнего уровня)"""
        return [d.name for d in self.docs_dir.iterdir() if d.is_dir()]

    def list_files(self, library: str) -> list[str]:
        """Список всех .md файлов внутри библиотеки"""
        lib_path = self.docs_dir / library
        if not lib_path.exists():
            return []
        return [
            str(f.relative_to(lib_path))
            for f in lib_path.rglob("*.md")
        ]

    def get_file(self, library: str, filename: str) -> DocFile | None:
        """Получить конкретный файл"""
        path = self.docs_dir / library / filename
        if not path.exists():
            return None
        return DocFile(
            name=filename,
            path=path,
            content=path.read_text(encoding="utf-8"),
        )

    def search(self, query: str, library: str | None = None) -> list[str]:
        """Поиск по всем документациям или конкретной библиотеке"""
        search_root = self.docs_dir / library if library else self.docs_dir
        results: list[str] = []

        for file in search_root.rglob("*.md"):
            content = file.read_text(encoding="utf-8")
            if query.lower() in content.lower():
                relative = file.relative_to(self.docs_dir)
                # находим строки с совпадением
                for i, line in enumerate(content.splitlines()):
                    if query.lower() in line.lower():
                        results.append(f"[{relative}] line {i + 1}: {line.strip()}")

        return results[:30]