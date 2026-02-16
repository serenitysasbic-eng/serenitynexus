# -*- coding: utf-8 -*-
import psycopg2
from datetime import datetime
import os

class SerenityDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST")
        )
        self.cursor = self.conn.cursor()
        self._crear_tablas()

    def _crear_tablas(self):
        # Tabla para telemetría de cámaras y micrófonos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS avistamientos (
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP,
                faro_id TEXT,
                tipo_deteccion TEXT,
                probabilidad FLOAT,
                coordenadas TEXT
            )
        """)
        self.conn.commit()

    def registrar_evento(self, faro, tipo, prob, coords):
        query = "INSERT INTO avistamientos (fecha, faro_id, tipo_deteccion, probabilidad, coordenadas) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (datetime.now(), faro, tipo, prob, coords))
        self.conn.commit()