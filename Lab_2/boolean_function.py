from parser import parse_expression
from truth_table import build_truth_table, print_truth_table
from normal_forms import get_dnf, get_cnf, get_numeric_dnf, get_numeric_cnf, get_index_form
from post_classes import get_post_classes
from zhegalkin import get_zhegalkin
from dummy_vars import get_dummy_vars
from boolean_diff import print_derivatives
from minimization.quine_mccluskey import quine_mccluskey_minimize
from minimization.karnaugh import print_karnaugh_map
from utils import print_header


class BooleanFunction:
    def __init__(self, expr: str):
        self.expr = expr.strip()
        self.ast = parse_expression(self.expr)
        self.vars = self._extract_vars()
        self.n = len(self.vars)
        self.truth_table = build_truth_table(self.ast, self.vars)

    def _extract_vars(self):
        vars_set = set()

        def collect(node):
            if isinstance(node, str) and node in "abcde":
                vars_set.add(node)
            elif isinstance(node, list):
                if node[0] == "!":
                    collect(node[1])
                else:
                    collect(node[0])
                    collect(node[2])

        collect(self.ast)
        return sorted(vars_set)

    def print_all(self):
        print_header(f"Функция: {self.expr}   (переменные: {self.vars})")
        print_truth_table(self.truth_table, self.vars)
        print("\nСДНФ:", get_dnf(self.truth_table, self.vars))
        print("СКНФ:", get_cnf(self.truth_table, self.vars))
        print("Числовая СДНФ:", get_numeric_dnf(self.truth_table))
        print("Числовая СКНФ:", get_numeric_cnf(self.truth_table))
        print("Индексная форма:", get_index_form(self.truth_table))
        print("\nКлассы Поста:", ", ".join(get_post_classes(self.truth_table, self.n)) or "—")
        print("Полином Жегалкина:", get_zhegalkin(self.truth_table, self.vars))
        print("Фиктивные переменные:", get_dummy_vars(self.truth_table, self.vars) or "нет")
        print_derivatives(self.truth_table, self.vars)
        print("\n=== Минимизация ===")
        print("--- Расчётный метод (Quine–McCluskey) — ДНФ ---")
        quine_mccluskey_minimize(
            self.truth_table, self.vars, show_stages=True, method="calc", form="dnf"
        )
        print("--- Расчётный метод — КНФ (склеивание по ¬f) ---")
        quine_mccluskey_minimize(
            self.truth_table, self.vars, show_stages=True, method="calc", form="cnf"
        )
        print("--- Расчётно-табличный — ДНФ ---")
        quine_mccluskey_minimize(
            self.truth_table, self.vars, show_stages=True, method="table", form="dnf"
        )
        print("--- Расчётно-табличный — КНФ ---")
        quine_mccluskey_minimize(
            self.truth_table, self.vars, show_stages=True, method="table", form="cnf"
        )
        print("\n--- Карта Карно — ДНФ (в ячейках f) ---")
        print_karnaugh_map(
            self.truth_table, self.vars, caption="Склеивание единиц f → минимальная ДНФ"
        )
        print("\n--- Карта Карно — КНФ (в ячейках ¬f; склеивание единиц = макс. дизъюнкты КНФ) ---")
        print_karnaugh_map(
            [1 - x for x in self.truth_table],
            self.vars,
            caption="1 там, где f = 0",
        )
