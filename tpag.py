import numpy
import pygad
import pygad.nn
import pygad.gann
from csv_logger import CsvLogger
import logging
from time import sleep

filename = 'log5.csv'
delimiter = ','
level = logging.INFO
custom_additional_levels = ['logs']
fmt = f'%(asctime)s{delimiter}%(levelname)s{delimiter}%(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
max_size = 1024
max_files = 4
header = ['date', 'level', 'value_1', 'value_2']

#Crear logger
csvlogger = CsvLogger(filename=filename,
                      delimiter=delimiter,
                      level=level,
                      add_level_names=custom_additional_levels,
                      add_level_nums=None,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)


class Materia:
    def __init__(self, c, t, m, d, n):
        self.codigo = c
        self.turno = t
        self.modalidad = m 
        self.dia = d
        self.nombre = n
        self.cupo = 3

inteligenciaArtificial1 = Materia(1, "N", "P", "Lunes", "Inteligencia Artificial")
inteligenciaArtificial2 = Materia(2, "N", "V", "Martes", "Inteligencia Artificial")
inteligenciaArtificial3 = Materia(3, "T", "M", "Martes", "Inteligencia Artificial")
inteligenciaArtificial4 = Materia(4, "M", "M", "Lunes", "Inteligencia Artificial")
sistemasDeGestion1 = Materia(5, "M", "M", "Martes", "Sistemas de Gestion")
sistemasDeGestion2 = Materia(6, "N", "P", "Miercoles", "Sistemas de Gestion")
sistemasDeGestion3 = Materia(7, "T", "V", "Martes", "Sistemas de Gestion")
sistemasDeGestion4 = Materia(8, "T", "M", "Viernes", "Sistemas de Gestion")
admGerencial1 = Materia(9, "T", "M", "Miercoles", "Administracion Gerencial")
admGerencial2 = Materia(10, "N", "V", "Jueves", "Administracion Gerencial")
admGerencial3 = Materia(11, "N", "P", "Jueves", "Administracion Gerencial")
admGerencial4 = Materia(12, "M", "V", "Jueves", "Administracion Gerencial")
proyecto1 = Materia(13, "N", "P", "Jueves", "Proyecto")
proyecto2 = Materia(14, "T", "M", "Viernes", "Proyecto")
proyecto3 = Materia(15, "T", "V", "Jueves", "Proyecto")
proyecto4 = Materia(16, "M", "M", "Viernes", "Proyecto")
none = Materia(17, None, None, None, "No seleccionada")

materias = [inteligenciaArtificial1, inteligenciaArtificial2, inteligenciaArtificial3, inteligenciaArtificial4, sistemasDeGestion1, sistemasDeGestion2, sistemasDeGestion3, sistemasDeGestion4, admGerencial1, admGerencial2, admGerencial3, admGerencial4, proyecto1, proyecto2, proyecto3, proyecto4, none]

class Restriccion:
    def __init__(self, mat, t=None, m=None, d=None):
        self.materia = mat
        self.turno = t
        self.modalidad = m 
        self.dia = d

restriccion1 = Restriccion("Inteligencia Artificial", "N", "P", "Lunes")
restriccion2 = Restriccion("Sistemas de Gestion", "T", "V", "Martes")
restriccion3 = Restriccion("Administracion Gerencial", "T", "M", "Miercoles")
restriccion4 = Restriccion("Proyecto", "T", "V", "Jueves")
alumno1 = [restriccion1, restriccion2, restriccion3, restriccion4]

restriccion5 = Restriccion("Inteligencia Artificial", "T", "M", "Martes")
restriccion6 = Restriccion("Sistemas de Gestion", "M", "M", "Martes")
restriccion7 = Restriccion("Administracion Gerencial", "M", "V", "Jueves")
restriccion8 = Restriccion("Proyecto", None, None, "Viernes")
alumno2 = [restriccion5, restriccion6, restriccion7, restriccion8]

restriccion9 = Restriccion("Inteligencia Artificial", "N", None, None)
restriccion10 = Restriccion("Sistemas de Gestion", None, None, "Miercoles")
restriccion11 = Restriccion("Administracion Gerencial", "N", None, "Jueves")
restriccion12 = Restriccion("Proyecto", None, None, "Viernes")
alumno3 = [restriccion9, restriccion10, restriccion11, restriccion12]

restriccion13 = Restriccion("Inteligencia Artificial", "M", "M", "Lunes")
restriccion14 = Restriccion("Sistemas de Gestion", "T", "M", "Viernes")
restriccion15 = Restriccion("No seleccionada", None, None, None)
restriccion16 = Restriccion("Proyecto", "T", "M", "Viernes")
alumno4 = [restriccion13, restriccion14, restriccion15, restriccion16]

restriccion17 = Restriccion("Inteligencia Artificial", "N", "V", "Martes")
restriccion18 = Restriccion("Sistemas de Gestion", "N", "P", "Miercoles")
restriccion19 = Restriccion("Administracion Gerencial", "N", "P", "Jueves")
restriccion20 = Restriccion("No seleccionada", None, None, None)
alumno5 = [restriccion17, restriccion18, restriccion19, restriccion20]

#Funciones
def buscar_materia(codigo_materia_a_buscar):
    for mat in materias:
        if (mat.codigo == codigo_materia_a_buscar):
            return mat


def buscar_materias(materias_alumno):
    found_mats = []
    for materia_alu in materias_alumno:
        for mat in materias:
            if (mat.codigo == materia_alu):
                found_mats.append(mat)
                break
    return found_mats

def restar_por_materias_repetidas(solutions_alumno):
    puntaje = 0
    materias_alu_solution = buscar_materias(solutions_alumno)
    mapped_sol_lenght = len(set(map(lambda x : x.nombre, materias_alu_solution)))
    if (mapped_sol_lenght < 4):
        puntaje = -1000
    return puntaje

def puntuar_por_cumplimiento_restriccion(solutions_alumno, restricciones_alumno):
    puntaje = 0
    materias_alu_solution = buscar_materias(solutions_alumno)
    for mat in materias_alu_solution:
        res_materias_alu = list(filter(lambda x : x.materia == mat.nombre, restricciones_alumno))
        if (len(res_materias_alu) > 0):
            res_turno_alu = list(filter(lambda x : x.materia == mat.nombre and (x.turno == mat.turno or x.turno == None), restricciones_alumno))
            if (len(res_turno_alu) > 0):
                res_modalidad_alu = list(filter(lambda x : x.materia == mat.nombre and (x.modalidad == mat.modalidad or x.modalidad == None), restricciones_alumno))
                if (len(res_modalidad_alu) > 0):
                    res_dia_alu = list(filter(lambda x : x.materia == mat.nombre and (x.dia == mat.dia or x.dia == None), restricciones_alumno))
                    if (len(res_dia_alu) > 0):
                        puntaje = puntaje + 400
                    else:
                        puntaje = puntaje - 1000    
                else:
                    puntaje = puntaje - 1000               
            else:
                puntaje = puntaje - 1000
        else:
            puntaje = puntaje - 1000
    return puntaje

def fitness_func(solutions, solution_index):
    fit = 0
    solutions_alumno1 = []
    solutions_alumno2 = []
    solutions_alumno3 = []
    solutions_alumno4 = []
    solutions_alumno5 = []

    for index, solution in enumerate(solutions):
        if (index in range(0, 4)):
            solutions_alumno1.append(solution)
        if (index in range(4, 8)):
            solutions_alumno2.append(solution)
        if (index in range(8, 12)):
            solutions_alumno3.append(solution)
        if (index in range(12, 16)):
            solutions_alumno4.append(solution)
        if (index in range(16, 20)):
            solutions_alumno5.append(solution)

    fit += restar_por_materias_repetidas(solutions_alumno1)
    fit += restar_por_materias_repetidas(solutions_alumno2)
    fit += restar_por_materias_repetidas(solutions_alumno3)
    fit += restar_por_materias_repetidas(solutions_alumno4)
    fit += restar_por_materias_repetidas(solutions_alumno5)

    fit += puntuar_por_cumplimiento_restriccion(solutions_alumno1, alumno1)
    fit += puntuar_por_cumplimiento_restriccion(solutions_alumno2, alumno2)
    fit += puntuar_por_cumplimiento_restriccion(solutions_alumno3, alumno3)
    fit += puntuar_por_cumplimiento_restriccion(solutions_alumno4, alumno4)
    fit += puntuar_por_cumplimiento_restriccion(solutions_alumno5, alumno5)
    return fit

def on_generation(instance):
    print("Iteracion terminada")

#Configuraciones
sol_per_pop = 20 #Numero de cromosomas
num_generations=500 #Numero de generaciones
num_genes = 20  #Cantidad de materias a las cuales se anota el alumno * cantidad de alumnos
gene_space = range(1, 18) #Valores posibles cada gen
gene_type = int #Tipo de gen
parent_selection_type = "rank" #Metodo de seleccion: Ranking
keep_parents = 0 #Al cruzarse se eliminan los padres.
mutation_probability = 0.1 #Probabilidad simple
mutation_by_replacement = True #Reemplaza el gen

#Instancia
ga_instance = pygad.GA(sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       num_generations=num_generations,
                       num_parents_mating=2,
                       gene_type=gene_type,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       mutation_probability=mutation_probability,
                       mutation_by_replacement=mutation_by_replacement,
                       gene_space=gene_space,
                       fitness_func=fitness_func,
                       on_generation=on_generation)

ga_instance.run()

ga_instance.plot_fitness()

#Informacion final
solution, solution_fitness, solution_idx = ga_instance.best_solution()
csvlogger.logs([" Mejor solucion: {solution}".format(solution=solution)])
sleep(0.1)
csvlogger.logs([" Parametros: \n - Numero de cromosomas: {numeroCromosomas}\n - Numero de generaciones: {numeroGeneraciones}\n - Cantidad de materias: {cantidadMaterias}\n - Valores de cada gen: {valoresCadaGen}\n - Tipo de gen: {tipoGen}\n - Metodo de seleccion: {metodoSeleccion}\n - Se eliminan los padres: {eliminarPadres}\n - Probabilidad de mutacion: {probabilidadMutacion}".format(numeroCromosomas=sol_per_pop, numeroGeneraciones=num_generations, cantidadMaterias=num_genes, valoresCadaGen=gene_space, tipoGen="int", metodoSeleccion=parent_selection_type, eliminarPadres="Si", probabilidadMutacion=mutation_probability)])
sleep(0.1)
if ga_instance.best_solution_generation != -1:
    csvlogger.logs([" La mejor solución fue alcanzada después de {best_solution_generation} generaciones.".format(best_solution_generation=ga_instance.best_solution_generation)])