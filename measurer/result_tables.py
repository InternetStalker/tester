from __future__ import annotations
import csv
import pathlib

from rich.table import Table
from rich.console import Console
from abc import ABC, abstractmethod

from . import TestResult
from .args import Arguments


class AbstractResultTable(ABC):
    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def show(self) -> None:
        pass


class BaseResultTable(AbstractResultTable):
    def __init__(self, arguments: Arguments, results: list[TestResult]) -> None:
        self._iters = arguments.iters
        self._results = results
    
    def create_table(self) -> None:
        return super().create_table()
    
    def show(self) -> None:
        return super().show()

    def _get_average(self, results: list[TestResult]) -> TestResult:
        sum_ = 0
        for result in results:
            sum_ += result.result
        return sum_/len(results)


class ConsoleResultTable(BaseResultTable):
    def create_table(self) -> Table:
        self._table = Table()
        self._table.add_column("Tests.")
        self._table.add_column("Functions.")
        for i in range(1, self._iters+1):
            self._table.add_column(f"Iteration {i}.")
        
        if self._iters > 1:
            self._table.add_column("Average.")
        
        raws = set()
        while self.results:
            result = self._results.pop(0)
            raw = [result.test_mode, result.name, result]
            for i, result in enumerate(results):
                if result.test_mode == raw[0] and result.name == raw[1]:
                    raw.append(result.pop(i))

            raw.append(self._get_average(raw[2:])
            raws.add(raw)

    
    def show(self) -> None:
        console = Console()
        console.print(self._table)


class CsvResultTable(BaseResultTable):
    def __init__(
        self,
        arguments: Arguments,
        results:  list[TestResult],
        path_to_csv: pathlib.Path
        ) -> None:
        super().__init__(arguments, results)
        self._path_to_csv = arguments.path_to_csv 

    def create_table(self) -> None:
        self._fieldnames = (
            "Tests.",
            "Functions.",
            *(f"Iteration {i}." for i in range(1, self._iters+1))
        )
        if self._iters > 1:
            self._fieldnames = (
                *self._fieldnames,
                "Average."
            )

        for test, function_names in self._results.items():
            self._rows = []
            for name, values in function_names.items():
                row = {
                    "Tests.": test,
                    "Functions.": name,
                    **{f"Iteration {i}.": str(value) for i, value in enumerate(values, start=1)},
                }

                if self._iters > 1:
                    row["Average."] = str(self._get_average(values))

                self._rows.append(row)


    def show(self) -> None:
        with self._path_to_csv.open("w", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(file, self._fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(self._rows)


def create_result_table(
        results: list[TestResult],
        arguments: Arguments
    ) -> BaseResultTable:
    if arguments.save_to_csv:
        table = CsvResultTable(arguments, results)
        table.create_table()

    else:
        table = ConsoleResultTable(arguments, results)
        table.create_table()
    
    return table

