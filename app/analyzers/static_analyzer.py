from app.analyzers.complexity_analyzer import ComplexityAnalyzer
from app.analyzers.documentation_analyzer import DocumentationAnalyzer
from app.analyzers.import_analyzer import ImportAnalyzer
from app.analyzers.maintainability_analyzer import MaintainabilityAnalyzer
from app.analyzers.naming_analyzer import NamingAnalyzer
from app.analyzers.security_analyzer import SecurityAnalyzer


class StaticAnalyzer:
    """
    Purpose:
        Coordinates all static analysis modules and aggregates their
        findings into a unified analysis report.

    Responsibilities:
        - Execute each static analyzer.
        - Collect findings from all analyzers.
        - Return a consolidated static analysis report.

    Current Analyzers:
        - Import Analyzer
        - Naming Analyzer
        - Documentation Analyzer

    Future Analyzers:
        - Complexity Analyzer
        - Dead Code Analyzer
        - Metrics Analyzer
        - Security Analyzer
        - Performance Analyzer
        - Best Practices Analyzer
    """

    def __init__(self):

        self.import_analyzer = ImportAnalyzer()
        self.naming_analyzer = NamingAnalyzer()
        self.documentation_analyzer = DocumentationAnalyzer()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.maintainability_analyzer = MaintainabilityAnalyzer()

    def analyze(self, graph):

        report = {

        "imports": self.import_analyzer.analyze(graph),

        "naming": self.naming_analyzer.analyze(graph),

        "documentation": self.documentation_analyzer.analyze(graph),

        "complexity": self.complexity_analyzer.analyze(graph),

        "security": self.security_analyzer.analyze(graph),

        "maintainability": self.maintainability_analyzer.analyze(graph)

        }

        return report