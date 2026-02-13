from pathlib import Path
from dataclasses import dataclass


@dataclass
class DocFile:
    name: str
    path: Path
    content: str


class DocsReader:
    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = docs_dir.resolve()  

    def _is_safe_path(self, path: Path) -> bool:
        """Проверяет, что путь находится внутри docs_dir"""
        try:
            resolved_path = path.resolve()
            return resolved_path.is_relative_to(self.docs_dir)
        except (ValueError, RuntimeError):
            return False

    def list_libraries(self) -> list[str]:
        """Список доступных библиотек (папок верхнего уровня)"""
        try:
            return [d.name for d in self.docs_dir.iterdir() if d.is_dir()]
        except (OSError, PermissionError):
            return []

    def list_files(self, library: str) -> list[str]:
        """Список всех .md файлов внутри библиотеки"""
        if not library:
            return []
        
        lib_path = self.docs_dir / library
        
        # Защита от path traversal
        if not self._is_safe_path(lib_path):
            return []
        
        if not lib_path.exists() or not lib_path.is_dir():
            return []
        
        try:
            return [
                str(f.relative_to(lib_path))
                for f in lib_path.rglob("*.md")
                if self._is_safe_path(f)  # Дополнительная проверка для каждого файла
            ]
        except (OSError, PermissionError):
            return []

    def get_file(self, library: str, filename: str) -> DocFile | None:
        """Получить конкретный файл"""
        if not library or not filename:
            return None
        
        path = self.docs_dir / library / filename
        
        # Защита от path traversal
        if not self._is_safe_path(path):
            return None
        
        if not path.exists() or not path.is_file():
            return None
        
        try:
            return DocFile(
                name=filename,
                path=path,
                content=path.read_text(encoding="utf-8"),
            )
        except (OSError, PermissionError, UnicodeDecodeError):
            return None

    def search(self, query: str, library: str | None = None) -> list[str]:
        """Поиск по всем документациям или конкретной библиотеке"""
        if not query:
            return []
        
        if library:
            search_root = self.docs_dir / library
            # Защита от path traversal
            if not self._is_safe_path(search_root):
                return []
        else:
            search_root = self.docs_dir
        
        if not search_root.exists() or not search_root.is_dir():
            return []
        
        results: list[str] = []

        try:
            for file in search_root.rglob("*.md"):
                # Защита от path traversal для каждого файла
                if not self._is_safe_path(file):
                    continue
                
                try:
                    content = file.read_text(encoding="utf-8")
                    if query.lower() in content.lower():
                        relative = file.relative_to(self.docs_dir)
                        # находим строки с совпадением
                        for i, line in enumerate(content.splitlines()):
                            if query.lower() in line.lower():
                                results.append(f"[{relative}] line {i + 1}: {line.strip()}")
                                if len(results) >= 30:  # Ограничение результатов
                                    return results
                except (OSError, PermissionError, UnicodeDecodeError):
                    continue
        except (OSError, PermissionError):
            return []

        return results