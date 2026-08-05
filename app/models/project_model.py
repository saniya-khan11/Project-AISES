from dataclasses import dataclass, field
from typing import List


@dataclass
class Function:

    name: str

    parameters: List[str] = field(default_factory=list)

    start_line: int = 0

    end_line: int = 0


@dataclass
class Method:

    class_name: str

    name: str

    parameters: List[str] = field(default_factory=list)

    start_line: int = 0

    end_line: int = 0


@dataclass
class Class:

    name: str

    methods: List[Method] = field(default_factory=list)

    start_line: int = 0

    end_line: int = 0


@dataclass
class SourceFile:

    file_id: str

    path: str

    language: str

    imports: List[str] = field(default_factory=list)

    classes: List[Class] = field(default_factory=list)

    functions: List[Function] = field(default_factory=list)