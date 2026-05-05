"""
data_engine.py
Motor de carga y transformación de datos para el módulo de analítica.

Gestiona la conexión a MySQL y expone DataFrames enriquecidos con métricas
calculadas. Si la base de datos no está disponible activa automáticamente
el modo demo con datos sintéticos representativos (40 empleados, 18 proyectos).
"""

import os
import warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

warnings.filterwarnings("ignore")


class DataEngine:
    """
    Fuente única de datos para el análisis de RRHH y proyectos.

    Parámetros de entorno:
        DATABASE_URL: cadena de conexión SQLAlchemy completa.
                      Por defecto: mysql+mysqlconnector://root:@localhost:3306/practica

    Ejemplo:
        engine = DataEngine()
        df_emp = engine.get_employees()
        df_prj = engine.get_projects()
        df_asg = engine.get_assignments()
    """

    _DB_DEFAULT = "mysql+mysqlconnector://root:@localhost:3306/practica"

    def __init__(self):
        db_url = os.getenv("DATABASE_URL", self._DB_DEFAULT)
        try:
            self._engine = create_engine(db_url, pool_pre_ping=True)
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.is_mock = False
            print("[DataEngine] Conexión establecida con la base de datos.")
        except Exception:
            self.is_mock = True
            print("[DataEngine] MODO DEMO activo — base de datos no disponible.")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def get_employees(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame de empleados con métricas calculadas.

        Columnas originales esperadas:
            ID_EMPLEADO, TX_NOMBRE, F_ALTA, F_NACIMIENTO, F_BAJA, CX_EDOCIVIL

        Columnas añadidas:
            ANTIGUEDAD_ANOS (float): años desde la fecha de alta.
            EDAD            (float): edad actual en años.
            ESTADO          (str):   'Activo' | 'Inactivo'.

        Returns:
            pd.DataFrame: un registro por empleado.
        """
        df = self._mock_employees() if self.is_mock else pd.read_sql(
            "SELECT * FROM EM_EMPLEADOS", self._engine
        )
        return self._enrich_employees(df)

    def get_projects(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame de proyectos con métricas calculadas.

        Columnas originales esperadas:
            ID_PROYECTO, TX_DESCRIPCION, F_INICIO, F_FIN, F_BAJA, TX_LUGAR

        Columnas añadidas:
            DURACION_DIAS (int): días entre inicio y fin (o hoy si sigue activo).
            ESTADO        (str): 'Activo' | 'Cesado'.

        Returns:
            pd.DataFrame: un registro por proyecto.
        """
        df = self._mock_projects() if self.is_mock else pd.read_sql(
            "SELECT * FROM PR_PROYECTOS", self._engine
        )
        return self._enrich_projects(df)

    def get_assignments(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame de asignaciones empleado-proyecto.

        Columnas: PROYECTO, TX_NOMBRE, ID_EMPLEADO, ID_PROYECTO

        Returns:
            pd.DataFrame: un registro por vínculo empleado-proyecto.
        """
        if self.is_mock:
            return self._mock_assignments()

        query = """
            SELECT
                p.TX_DESCRIPCION        AS PROYECTO,
                e.TX_NOMBRE             AS TX_NOMBRE,
                ep.ID_EMPLEADO,
                ep.ID_PROYECTO
            FROM PR_EMPLEADOS_PROYECTO ep
            JOIN PR_PROYECTOS   p ON ep.ID_PROYECTO = p.ID_PROYECTO
            JOIN EM_EMPLEADOS   e ON ep.ID_EMPLEADO = e.ID_EMPLEADO
        """
        return pd.read_sql(query, self._engine)

    # ------------------------------------------------------------------
    # Enriquecimiento de datos
    # ------------------------------------------------------------------

    @staticmethod
    def _enrich_employees(df: pd.DataFrame) -> pd.DataFrame:
        today = datetime.now()
        df["F_ALTA"]       = pd.to_datetime(df["F_ALTA"],       errors="coerce")
        df["F_NACIMIENTO"] = pd.to_datetime(df["F_NACIMIENTO"], errors="coerce")
        df["F_BAJA"]       = pd.to_datetime(df["F_BAJA"],       errors="coerce")
        df["ANTIGUEDAD_ANOS"] = (today - df["F_ALTA"]).dt.days / 365.25
        df["EDAD"]         = (today - df["F_NACIMIENTO"]).dt.days / 365.25
        df["ESTADO"]       = df["F_BAJA"].apply(
            lambda x: "Inactivo" if pd.notnull(x) else "Activo"
        )
        return df

    @staticmethod
    def _enrich_projects(df: pd.DataFrame) -> pd.DataFrame:
        today = datetime.now()
        df["F_INICIO"] = pd.to_datetime(df["F_INICIO"], errors="coerce")
        df["F_FIN"]    = pd.to_datetime(df["F_FIN"],    errors="coerce")
        df["F_BAJA"]   = pd.to_datetime(df["F_BAJA"],   errors="coerce")
        df["DURACION_DIAS"] = (
            df["F_FIN"].fillna(today) - df["F_INICIO"]
        ).dt.days.clip(lower=0)
        df["ESTADO"] = df["F_BAJA"].apply(
            lambda x: "Cesado" if pd.notnull(x) else "Activo"
        )
        return df

    # ------------------------------------------------------------------
    # Datos de demostración
    # ------------------------------------------------------------------

    @staticmethod
    def _mock_employees() -> pd.DataFrame:
        """
        Genera 40 empleados sintéticos con distribuciones realistas.
        La semilla fija garantiza reproducibilidad entre ejecuciones.
        """
        np.random.seed(42)
        n = 40
        nombres = [
            "Ana García", "Carlos López", "María Martínez", "Luis Rodríguez",
            "Sara Fernández", "Jorge Sánchez", "Elena González", "Pablo Torres",
            "Sofía Ramírez", "Miguel Díaz", "Laura Moreno", "David Jiménez",
            "Carmen Ruiz", "Javier Hernández", "Isabel Flores", "Raúl Vargas",
            "Natalia Castro", "Sergio Ortega", "Beatriz Romero", "Alejandro Vidal",
            "Rosa Navarro", "Antonio Molina", "Pilar Ramos", "Fernando Gil",
            "Mónica Serrano", "Ricardo Blanco", "Cristina Domínguez", "Juan Morales",
            "Patricia Guerrero", "Alberto Muñoz", "Teresa Alonso", "Víctor Iglesias",
            "Marta Cabrera", "Óscar Medina", "Lucía Delgado", "Rubén Peña",
            "Gloria Vázquez", "Enrique León", "Silvia Prieto", "Andrés Cano",
        ]

        # Altas distribuidas desde 2015, con mayor densidad en 2019-2022
        altas = sorted(pd.date_range("2015-01-01", periods=n, freq="3ME"))

        nacimientos = [
            datetime(1975 + (i % 22), (i % 12) + 1, min((i % 28) + 1, 28))
            for i in range(n)
        ]

        # ~20 % de empleados con baja registrada
        bajas = [
            altas[i] + timedelta(days=365 * (1 + i % 3)) if i % 5 == 0 else None
            for i in range(n)
        ]

        return pd.DataFrame({
            "ID_EMPLEADO":  range(1, n + 1),
            "TX_NOMBRE":    nombres,
            "F_ALTA":       altas,
            "F_NACIMIENTO": nacimientos,
            "F_BAJA":       bajas,
            "CX_EDOCIVIL":  np.random.choice(["S", "C"], n, p=[0.45, 0.55]),
        })

    @staticmethod
    def _mock_projects() -> pd.DataFrame:
        """Genera 18 proyectos sintéticos distribuidos entre 2019 y 2024."""
        np.random.seed(42)
        descripciones = [
            "Portal Corporativo", "App Móvil B2C", "Migración Cloud AWS",
            "Auditoría ISO 27001", "IA Predictiva", "ERP Integración",
            "Data Warehouse", "Plataforma E-learning", "Ciberseguridad 360",
            "Transformación Digital", "API Gateway", "CRM Renovación",
            "Infraestructura DevOps", "Gestión Documental", "Smart Analytics",
            "Red Interna 5G", "Automatización RPA", "Plataforma IoT",
        ]
        sedes = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga"]
        n = len(descripciones)

        inicios = list(pd.date_range("2019-01-01", periods=n, freq="4ME"))
        fins    = [i + timedelta(days=int(np.random.uniform(180, 900))) for i in inicios]
        bajas   = [
            fins[i] + timedelta(days=30) if i % 4 == 0 else None
            for i in range(n)
        ]

        return pd.DataFrame({
            "ID_PROYECTO":    range(1, n + 1),
            "TX_DESCRIPCION": descripciones,
            "F_INICIO":       inicios,
            "F_FIN":          fins,
            "F_BAJA":         bajas,
            "TX_LUGAR":       np.random.choice(sedes, n),
        })

    @staticmethod
    def _mock_assignments() -> pd.DataFrame:
        """
        Genera asignaciones coherentes con los datos de demo.
        Deja 2 proyectos sin asignaciones para probar la detección de anomalías.
        """
        np.random.seed(42)
        records = []
        sin_cobertura = {17, 18}  # proyectos intencionalmente vacíos

        for proj_id in range(1, 19):
            if proj_id in sin_cobertura:
                continue
            n_asignados = int(np.random.uniform(2, 9))
            empleados   = np.random.choice(range(1, 41), size=n_asignados, replace=False)
            for emp_id in empleados:
                records.append({
                    "PROYECTO":    f"Proyecto {proj_id}",
                    "TX_NOMBRE":   f"Empleado {emp_id}",
                    "ID_EMPLEADO": int(emp_id),
                    "ID_PROYECTO": proj_id,
                })

        return pd.DataFrame(records)
