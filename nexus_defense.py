import random

class NexusDefenseIA:
    def __init__(self):
        self.nodos_activos = ["Norte", "Sur", "Oriente", "Occidente"]

    def analizar_sensores(self):
        # Procesa 8 cámaras (2 por punto cardinal)
        detecciones = []
        for punto in self.nodos_activos:
            # Simulación de detección por IA
            hallazgo = random.choice(["Lince", "Jaguar", "Persona", "Ninguno"])
            confianza = random.uniform(0.7, 0.99)
            if hallazgo != "Ninguno":
                detecciones.append({
                    "zona": punto,
                    "objeto": hallazgo,
                    "confianza": confianza
                })
        return detecciones

    def triangulacion_acustica(self):
        # Lógica para los 4 micrófonos direccionales
        puntos_sonido = random.choice(self.nodos_activos)
        return f"Sonido detectado en cuadrante: {puntos_sonido}"