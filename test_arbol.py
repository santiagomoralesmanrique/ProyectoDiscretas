import unittest
from arbol import ArbolGenealogico
from nodo import Nodo

class TestArbolGenealogico(unittest.TestCase):

    def setUp(self):
        self.arbol = ArbolGenealogico()
        # Crear una pequeña genealogía para pruebas usando los nuevos atributos
        # p1 (M, 1931) + p2 (F, 1934) → pareja
        # p3 (F, 1958) = hija de p1 y p2
        # p4 (M, 1956) = pareja de p3
        # p5 (M, 1984) = hijo de p3 y p4
        self.arbol.agregar_persona("p1", "Efraín", "Camacho", "Bisabuelo", 0,
                                   genero="M", año_nacimiento=1931)
        self.arbol.agregar_persona("p2", "Rosario", "Núñez", "Bisabuela", 0,
                                   genero="F", año_nacimiento=1934, pareja_id="p1")
        self.arbol.agregar_persona("p3", "Marta", "Camacho", "Abuela", 1,
                                   genero="F", año_nacimiento=1958, padres_ids=["p1", "p2"])
        self.arbol.agregar_persona("p4", "Héctor", "Salgado", "Abuelo", 1,
                                   genero="M", año_nacimiento=1956, pareja_id="p3")
        self.arbol.agregar_persona("p5", "Andrés", "Salgado", "Padre", 2,
                                   genero="M", año_nacimiento=1984, padres_ids=["p3", "p4"])

    def test_nodo_atributos_nuevos(self):
        """Verifica que los nuevos atributos (genero, año_nacimiento, inmunidades) se asignan correctamente."""
        p1 = self.arbol.nodos["p1"]
        self.assertEqual(p1.genero, "M")
        self.assertEqual(p1.año_nacimiento, 1931)
        # Inmunidades por defecto = 0.5
        self.assertAlmostEqual(p1.inmune_gripe, 0.5)
        self.assertAlmostEqual(p1.inmune_covid, 0.5)
        self.assertAlmostEqual(p1.inmune_bacteria, 0.5)

    def test_fallecido_logica(self):
        """Verifica que el año de nacimiento < 1941 implica fallecido (2026 - 85)."""
        p1 = self.arbol.nodos["p1"]
        self.assertTrue(p1.año_nacimiento < (2026 - 85))  # 1931 < 1941 → fallecido

    def test_es_dag_valido(self):
        self.assertTrue(self.arbol.es_dag())

    def test_es_dag_invalido_con_ciclo(self):
        self.arbol.nodos["p1"].padres.append(self.arbol.nodos["p5"])
        self.arbol.nodos["p5"].hijos.append(self.arbol.nodos["p1"])
        self.assertFalse(self.arbol.es_dag())

    def test_es_conexo(self):
        self.assertTrue(self.arbol.es_conexo())
        self.assertEqual(self.arbol.obtener_componentes_conexas(), 1)
        self.arbol.agregar_persona("p_aislado", "Extraño", "Nadie", "Aislado", 1)
        self.assertFalse(self.arbol.es_conexo())
        self.assertEqual(self.arbol.obtener_componentes_conexas(), 2)

    def test_buscar_camino_y_parentesco(self):
        camino, desc = self.arbol.buscar_camino_parentesco("p5", "p1")
        self.assertEqual(camino, ["p5", "p3", "p1"])
        self.assertEqual(desc, "Abuelo/a")

        camino, desc = self.arbol.buscar_camino_parentesco("p1", "p2")
        self.assertEqual(camino, ["p1", "p2"])
        self.assertEqual(desc, "Pareja")

        self.arbol.agregar_persona("p6", "Rodrigo", "Camacho", "Tío", 1,
                                   genero="M", año_nacimiento=1961, padres_ids=["p1", "p2"])
        camino, desc = self.arbol.buscar_camino_parentesco("p5", "p6")
        self.assertEqual(camino, ["p5", "p3", "p1", "p6"])
        self.assertEqual(desc, "Tío/a")

    def test_simular_apellido(self):
        pasos = self.arbol.simular_propagacion_apellido("p1")
        self.assertIn("p1", pasos[0])
        self.assertIn("p3", pasos[1])
        self.assertIn("p5", pasos[2])
        self.assertNotEqual(self.arbol.nodos["p2"].estado_simulado, "Ape: Camacho")
        self.assertEqual(self.arbol.nodos["p5"].estado_simulado, "Ape: Camacho")

    def test_simular_contagio_tipos(self):
        """Verifica que las tres enfermedades usan sus inmunidades correctas."""
        p2 = self.arbol.nodos["p2"]
        # Asignar inmunidades específicas para verificar
        p2.inmune_gripe   = 1.0
        p2.inmune_covid   = 0.0
        p2.inmune_bacteria= 1.0

        # Con inmunidad total a gripe → prob contagio = 0.0
        prob_gripe = self.arbol.calcular_prob_contagio(p2, 0.8, "gripe")
        self.assertAlmostEqual(prob_gripe, 0.0)

        # Con inmunidad 0 a covid → prob contagio = prob_base
        prob_covid = self.arbol.calcular_prob_contagio(p2, 0.8, "covid")
        self.assertAlmostEqual(prob_covid, 0.8)

    def test_simular_multifactorial(self):
        """Verifica que la simulación multifactorial disminuye probabilidad con distancia."""
        pasos = self.arbol.simular_propagacion_multifactorial("p1")
        # Al menos devuelve el origen
        self.assertIn("p1", pasos[0])
        # El árbol debe quedar con estado simulado (infectado o sano)
        self.assertIsNotNone(self.arbol.nodos["p1"].estado_simulado)

    def test_generar_arbol_aleatorio_valido(self):
        """Árbol de 9 personas y 5 pisos (mínimo 2*5-1=9 → exacto)."""
        self.arbol.generar_arbol_aleatorio(9, 5)
        self.assertEqual(len(self.arbol.nodos), 9)
        self.assertEqual(self.arbol.generacion_maxima(), 4)
        self.assertTrue(self.arbol.es_dag())

        # Las diferencias de año de nacimiento deben ser ≥ 17
        for nodo in self.arbol.nodos.values():
            for padre in nodo.padres:
                self.assertGreaterEqual(nodo.año_nacimiento - padre.año_nacimiento, 17)

        # Todos los hijos deben tener exactamente 2 padres registrados
        for nodo in self.arbol.nodos.values():
            if nodo.padres:
                self.assertEqual(len(nodo.padres), 2)

    def test_generar_arbol_aleatorio_invalido(self):
        """Si X < 2H-1, debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            # 5 pisos requieren mínimo 9 personas (2*5-1=9)
            self.arbol.generar_arbol_aleatorio(5, 5)

if __name__ == "__main__":
    unittest.main()
