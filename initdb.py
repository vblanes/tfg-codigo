import operacionesbd as bd
import analizador_texto as an


#introduco todas las castas en la bd
bd.introducir_coleccion_en_bd()
#introducir las aristas
cartas = bd.listar_cartas("INS")
rel = an.crear_relaciones(cartas)
bd.insertar_relaciones_en_bd(rel)
