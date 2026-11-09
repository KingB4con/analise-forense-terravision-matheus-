"""Testes básicos do projeto. Execute com: python -m unittest discover -s tests"""
import unittest
import numpy as np


class TestFormula(unittest.TestCase):
    def test_diferenca_posterior_menos_anterior(self):
        anterior = np.array([100.0, 120.0, 80.0])
        posterior = np.array([95.0, 125.0, 80.0])
        diferenca = posterior - anterior
        self.assertTrue(np.allclose(diferenca, [-5.0, 5.0, 0.0]))


if __name__ == "__main__":
    unittest.main()
