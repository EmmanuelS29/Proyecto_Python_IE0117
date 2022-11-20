#!/usr/bin/python3
'''
********************************************************************************
                          Universidad de Costa Rica
                       Escuela de Ingeniería Eléctrica
                                  IE-0117
                    Programación Bajo Plataformas Abiertas

                                proyecto.py

Autores:
         Sebastián Ávila Badilla / B90817 / sebastian.avilabadilla@ucr.ac.cr
         Emmanuel Solano Monge   / B97580 / emmanuel.solanomonge@ucr.ac.cr
         Gabriel Torres Garbanzo / B97828 / gabriel.torresgarbanzo@ucr.ac.cr


Fecha: 21/11/2022

Descripción:
Este script contiene el cuerpo principal del juego "Astra-BOOM", creado por los
tres estudiantes anteriormente mencionados. El juego consiste en eliminar
enemigos a través de una nave llamada "Yei-yi" que dispara balas. En el juego
se tiene la posibilidad de un menú, que a su vez despliega cuatro opciones:
"Jugar", "Instrucciones", "Highscore", "Salir". Dentro de cada opción hay un
botón para retroceder. Además, si sobrepasa el highscore guardado, el juego le
da la posibilidad de agregar un nombre con 3 dígitos (letras o números).
Finalmente, cuenta con una vida que resiste ocho golpes de enemigos, conforme
la nave es golpeada la vida se reduce
********************************************************************************
'''

# Se importan las librerías a utilizar
import pygame
import os
import random

# Variables y objetos que se necesitan en varias funciones
ancho = 960  # Ancho de la interfaz
alto = 540  # Altura de la interfaz
negro = (0, 0, 0)  # Color negro
blanco = (255, 255, 255)  # Color blanco
verde = (0, 255, 0)  # Color verde

# Configuraciones generales
pygame.init()  # Inicialización de pygame
pygame.mixer.init()  # Para agregar sonidos con pygame
pantalla = pygame.display.set_mode((ancho, alto))  # Configuración de pantalla
pygame.display.set_caption("Astra-BOOM!")  # Título de la interfaz
clock = pygame.time.Clock()  # Configuración del reloj de pygame

# Cargar imagen de fondo
fondo = pygame.image.load("assets/Fondo.png").convert()

# Cargar imágenes de enemigos
enemigos_img = []
lista_enemigos = ["assets/enemigo1.png", "assets/enemigo2.png",
                  "assets/enemigo3.png", "assets/enemigo4.png",
                  "assets/enemigo5.png", "assets/enemigo6.png"]

for img in lista_enemigos:
    enemigos_img.append(pygame.image.load(img).convert())

# Carga imágenes de explosión
explosion_anim = []
for i in range(9):
    file = "assets/Explosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(negro)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Sonido del láser
laser_sound = pygame.mixer.Sound("assets/Laser.ogg")

# Carga la imagen del botón
boton_img = pygame.image.load("assets/Boton.png").convert()
# Escala la imagen del botón
boton = pygame.transform.scale(boton_img, (370, 50))

# Definición de clases --------------------------------------------------------


# Clase para los proyectiles
class Proyectil(pygame.sprite.Sprite):

    def __init__(self, x, y):
        '''
        Este constructor configura los argumentos del proyectil.
        '''
        super().__init__()
        #  Se asigna gráficamente la skin del proyectil
        self.image = pygame.image.load("assets/Proyectil.png")
        self.image.set_colorkey(negro)  # Hace transparente el color negro
        self.rect = self.image.get_rect()  # rect para la imagen del proyectil
        self.rect.y = y  # Ubica al proyectil en la coordenada y del jugador
        self.rect.centerx = x  # Ubica al proyectil en la coordenada x del
        # jugador
        self.speedy = -10  # Fija la velocidad en y del proyectil en -10

    def update(self):
        '''
        Este método permite que se actualice el movimiento en las dirección
        y del proyectil.
        '''
        self.rect.y += self.speedy  # Actualiza la velocidad en y del proyectil
        if self.rect.bottom < 0:  # Si el límite superior es menor a cero
            self.kill()  # Elimina el proyectil


# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #  Se asigna gráficamente la skin del jugador
        self.image = pygame.image.load("assets/jugador.png").convert()
        self.image.set_colorkey(negro)  # Hace transparente el color negro
        self.rect = self.image.get_rect()  # rect para la imagen de jugador
        self.rect.centerx = ancho // 2  # Posición en el eje x de la interfaz
        self.rect.bottom = alto - 10  # Posición en el eje y de la interfaz
        self.velocidad_x = 0  # Velocidad en x inicializada en 0
        self.velocidad_y = 0  # Velocidad en y inicializada en 0
        self.vida = 200  # Se inicializa la vida del jugador en 200

    def update(self):
        '''
        Este método permite que se actualice el movimiento en las direcciones
        x & y del objeto jugador.
        '''
        self.velocidad_x = 0  # Velocidad inicial del eje x en 0
        keystate = pygame.key.get_pressed()  # Si se presionan teclas
        if keystate[pygame.K_LEFT]:  # Si se presiona la flecha "izquierda"
            self.velocidad_x = -5  # La velocidad en x cambia a -5 (- de direc)
        if keystate[pygame.K_RIGHT]:  # Si se presiona la flecha "derecha"
            self.velocidad_x = 5  # La velocidad en x cambia a 5 (+ de direc)
        self.rect.x += self.velocidad_x  # Actualiza la velocidad en x
        if self.rect.right > ancho:  # Si se supera el límite derecho de ancho
            self.rect.right = ancho  # Se impide salirse del límite derecho
        if self.rect.left < 0:  # Si se supera el límite izquierdo de ancho
            self.rect.left = 0  # Se impide salirse del límite izquierdo
        self.velocidad_y = 0  # Velocidad inicial del eje y en 0
        keystate = pygame.key.get_pressed()  # Si se presionan teclas
        if keystate[pygame.K_UP]:  # Si se presiona la flecha "superior"
            self.velocidad_y = -5  # La velocidad en y cambia a -5 (- de direc)
        if keystate[pygame.K_DOWN]:  # Si se presiona la flecha "inferior"
            self.velocidad_y = 5  # La velocidad en y cambia a 5 (+ de direc)
        self.rect.y += self.velocidad_y  # Actualiza la velocidad en y
        if self.rect.bottom > alto:   # Si se supera el límite inferior de alto
            self.rect.bottom = alto  # Se impide salirse del límite inferior
        if self.rect.top < 0:  # Si se supera el límite superior de alto
            self.rect.top = 0  # Se impide salirse del límite superior

    def disparo(self):
        '''
        Este método configura el disparo del objeto jugador.
        '''
        proyectil = Proyectil(self.rect.centerx, self.rect.top)
        all_sprites.add(proyectil)
        bullets.add(proyectil)
        laser_sound.play()


# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):

    def __init__(self):
        '''
        Este constructor configura los argumentos de los enemigos.
        '''
        super().__init__()
        self.image = random.choice(enemigos_img)  # Elige enemigo aleatorio
        self.image.set_colorkey(negro)  # Hace transparente el color negro
        self.rect = self.image.get_rect()  # rect para la imagen del enemigo
        self.rect.x = random.randrange(ancho - self.rect.width)  # Ubica al
        # enemigo aleatoriamente en el eje x
        self.rect.y = random.randrange(-140, -100)  # Ubica al enemigo
        # aleatoriamente en el eje y
        self.speedy = random.randrange(1, 10)  # Fija velocidad aleatoria en
        # eje y
        self.speedx = random.randrange(-5, 5)  # Fija velocidad aleatoria en
        # eje x

    def update(self):
        '''
        Este método permite que se actualice el movimiento en las direcciones
        x & y de los enemigos.
        '''
        self.rect.y += self.speedy  # Actualiza la velocidad en y del enemigo
        self.rect.x += self.speedx  # Actualiza la velocidad en x del enemigo
        #  En caso de que el enemigo se salga de la pantalla de juego
        sge_1 = self.rect.top > alto + 10
        sge_2 = self.rect.left < -40
        sge_3 = self.rect.right > ancho + 40
        if sge_1 or sge_2 or sge_3:
            self.rect.x = random.randrange(ancho - self.rect.width)  # Toma la
            # posición en x del enemigo como un valor aleatorio en un rango
            self.rect.y = random.randrange(-140, - 100)  # Toma la posición en
            # y del enemigo como un valor aleatorio en un rango
            self.speedy = random.randrange(1, 10)  # Toma la velocidad en y del
            # enemigo como un valor aleatorio


# Clase para la explosión
class Explosion(pygame.sprite.Sprite):

    def __init__(self, centro):
        '''
        Este constructor configura los argumentos de las explosiones.
        '''
        super().__init__()
        self.image = explosion_anim[0]  # Toma la primera imagen de explosión
        self.rect = self.image.get_rect()  # rect para la imagen de explosión
        self.rect.center = centro  # Centra la explosión
        self.frame = 0  # Pone frame inicial
        self.last_update = pygame.time.get_ticks()  # Toma la última
        # actualización en milisegundos desde que inició el juego
        self.frame_rate = 50  # Fija la velocidad de la explosión

    def update(self):
        '''
        Este método permite que se actualice el estado de la explosión.
        '''
        ahora = pygame.time.get_ticks()  # Toma el tiempo actual como los
        # milisegundos desde que inició el juego
        if ahora - self.last_update > self.frame_rate:  # Si el tiempo actual
            # menos el de la última actualización es mayor a la velocidad de
            # explosión
            self.last_update = ahora  # Fija la última actualización al tiempo
            # actual
            self.frame += 1  # Suma en 1 la velocidad de explosión
            if self.frame == len(explosion_anim):  # Si la velocidad de
                # explosión es igual a la cantidad de imágenes de explosión
                self.kill()  # Elimina la explosión
            else:  # Si la velocidad de explosión es diferente a la cantidad de
                # imágenes de explosión
                centro = self.rect.center  # Toma centro como la explosión
                # centrada inicialmente
                self.image = explosion_anim[self.frame]  # Toma la imagen de
                # explosión como la animación de la imagen en la posición de la
                # velocidad de explosión
                self.rect = self.image.get_rect()  # rect para la imagen de
                # explosión
                self.rect.center = centro  # Toma la explosión centrada
                # inicialmente como centro


class Boton:

    def __init__(self, imagen, posicion, texto_dentro, font, color_base):
        '''
        Este constructor configura los argumentos de los botones para accesar a
        diferentes opciones en el juego.
        '''
        self.image = imagen  # Se asigna la imagen del botón
        self.x = posicion[0]  # Se asigna posición en x
        self.y = posicion[1]  # Se asigna posición en y
        self.font = font  # Se asigna la fuente del texto
        self.base_color = color_base  # Color base del texto del botón
        self.text_in = texto_dentro  # Para introducir texto en el botón
        self.text = self.font.render(self.text_in, True, self.base_color)

        if self.image is None:  # En caso de no introducir imagen para el botón
            self.image = self.text  # se toma self.text

        # Posicionar el botón
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    # Función para actualizar la pantalla principal
    def update(self, pantalla):
        '''
        Este método permite que se actualice el estado de los botones.
        '''
        if self.image is not None:
            pantalla.blit(self.image, self.rect)
        pantalla.blit(self.text, self.text_rect)

    #  Función para revisar si el usuario dio alguna entrada
    def esperando_estados(self, posicion):
        '''
        Este método revisa que el ratón esté posicionado sobre alguna de las
        opciones.
        '''
        if posicion[0] in range(self.rect.left, self.rect.right):
            if posicion[1] in range(self.rect.top, self.rect.bottom):
                return True
        return False

# Fin de definición de clases -------------------------------------------------

# Declaración de las funciones ------------------------------------------------


def formato_texto(surface, texto, tamaño, x, y):
    '''
    Esta función se utiliza para configurar la escritura del texto en el
    juego. Se configura el tipo de texto, el tamaño y su ubicación en dos di-
    mensiones (x, y).
    '''
    fuente = pygame.font.SysFont("publicpixel", tamaño)  # Fuente y tamaño text
    texto_surface = fuente.render(texto, True, blanco)  # Superficie del texto
    texto_rect = texto_surface.get_rect()  # Crea un rect con x & y en (0, 0)
    texto_rect.midtop = (x, y)  # Posicionar el texto
    surface.blit(texto_surface, texto_rect)  # Se dibuja el texto en el rect


def formato_vida(surface, x, y, cantidad):
    '''
    Esta función se utiliza para configurar la vida del jugador, su aspecto,
    posición en la interfaz, tamaño gráfico y cantidad.
    '''
    ancho_barra = 200
    altura_barra = 10
    vida = (cantidad / 200) * ancho_barra  # Formato de la vida en la barra
    encuadre_barra = pygame.Rect(x, y, ancho_barra, altura_barra)  # Rectángulo
    vida = pygame.Rect(x, y, vida, altura_barra)  # Área rectangular de vida
    pygame.draw.rect(surface, verde, vida)  # Color de la vida
    pygame.draw.rect(surface, blanco, encuadre_barra, 2)  # Color del encuadre


def letra(tamaño):
    '''
    Esta función se utiliza para ajustar la fuente y el tamaño de las letras
    del texto utilizado en el juego.
    '''
    return pygame.font.Font(os.path.join(
                                        'assets/PublicPixel-z84yD.ttf'
                                        ),
                            tamaño
                            )


def menu_instrucciones():
    '''
    Esta función muestra las instrucciones del juego.
    '''
    # Se sitúa la pantalla sobre la imagen de fondo
    pantalla.blit(fondo, [0, 0])
    # Escribe el título del juego en la pantalla inicial
    formato_texto(pantalla, "Bienvenidos a Astra-BOOM!", 30, ancho // 2,
                  (alto / 2) - 200)
    # Escribe el título "Instrucciones" en la pantalla inicial
    formato_texto(pantalla, "Instrucciones", 25, ancho // 2, (alto / 2) - 110)
    # Leer archivo instrucciones para mostrar en pantalla
    directorio_actual = os.getcwd()  # Obtiene directorio actual
    direccion_inst = str(directorio_actual) + "/Instrucciones.txt"  # Agrega
    # Nombre de archivo al directorio actual
    inst = open(direccion_inst, 'r')  # Abre archivo con las instrucciones

    # Determinar cantidad de líneas  que hay en el archivo "Instrucciones.txt"
    with open(direccion_inst) as arch_inst:
        num_lineas = sum(1 for line in arch_inst)

    # Lee el archivo para mostrarlo en pantalla
    pos_ins = -50  # Fija primera posición
    for i in range(num_lineas):
        inst_v = inst.readline()  # Lee líneas del archivo
        inst_v = inst_v.rstrip('\n')  # Quitar salto de línea
        formato_texto(pantalla, inst_v, 15, ancho // 2, (alto / 2) + pos_ins)
        pos_ins += 25

    # Crea el botón para volver al menú principal
    volver = Boton(
                boton,
                ((ancho / 2) + 285, (alto - 510)),
                "Volver",
                letra(27),
                blanco
                )

    # Actualiza el botón en la pantalla
    volver.update(pantalla)
    pygame.display.flip()  # Actualiza toda la pantalla
    espera = True
    # Asignación de tareas a realizar con el botón volver
    while espera:
        # Asignación de tareas a realizar con el botón volver
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                cursor_menu = pygame.mouse.get_pos()
                if volver.esperando_estados(cursor_menu):
                    espera = False
                    pantalla_inicial()
        pygame.display.flip()  # Actualiza toda la pantalla


def menu_highscore():
    '''
    Esta función muestra el highscore junto al nombre de tres dígitos del
    jugador que logró ese valor.
    '''
    # Pone la pantalla sobre la imagen de fondo
    pantalla.blit(fondo, [0, 0])
    # Escribe el título del juego en la pantalla inicial
    formato_texto(pantalla, "Astra-BOOM!", 65, ancho // 2, (alto / 2) - 250)
    # Escribe el título "Highscore" en la pantalla inicial
    formato_texto(pantalla, "Highscore", 50, ancho // 2, (alto / 2) - 50)

    # Leer highscore para mostrar en pantalla
    val_highs = open(highscore, 'r')  # Abre archivo con highscore
    hscore_s = val_highs.readlines()  # Lee líneas del archivo
    hscor_s = hscore_s[0].rstrip('\n')  # Quitar salto de línea

    # Leer nombre highscore para mostrar en pantalla
    directorio_actual = os.getcwd()  # Obtiene directorio actual
    direccion_nombre = str(directorio_actual) + "/Nombre.txt"  # Agrega
    # nombre de archivo al directorio actual
    nombre_highs = open(direccion_nombre, 'r')  # Abre archivo con nombre de
    # jugador que tiene el récord
    hscore_n = nombre_highs.readlines()  # Lee líneas del archivo
    hscor_n = hscore_n[0].rstrip('\n')  # Quitar salto de línea

    # Escribe nombre y highscore en la pantalla inicial
    nh_total = hscor_n + " *----* " + hscor_s + " pts"
    formato_texto(pantalla, nh_total, 35, ancho // 2, (alto / 2) + 40)
    pygame.display.flip()  # Actualiza toda la pantalla

    # Crea el botón para volver al menú principal
    volver = Boton(
                boton,
                ((ancho / 2) + 285, (alto - 40)),
                "Volver",
                letra(27),
                blanco
                )

    # Actualiza el botón en la pantalla
    volver.update(pantalla)
    pygame.display.flip()  # Actualiza toda la pantalla
    espera = True
    while espera:
        # Asignación de tareas a realizar con el botón volver
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                cursor_menu = pygame.mouse.get_pos()
                if volver.esperando_estados(cursor_menu):
                    espera = False
                    pantalla_inicial()
        pygame.display.flip()  # Actualiza toda la pantalla


def pantalla_inicial():
    '''
    Esta función muestra la pantalla inicial del juego, en dicha pantalla se
    puede seleccionar entre: Jugar, Instrucciones, ver Highscores y Salir.
    '''
    # Se sitúa la pantalla sobre la imagen de fondo
    pantalla.blit(fondo, [0, 0])
    # Escribe el título del juego en la pantalla inicial
    formato_texto(pantalla, "Astra-BOOM!", 65, ancho // 2, (alto / 2) - 250)

    # Escribe la opción Jugar en la pantalla inicial
    jugar = Boton(
                boton,
                (ancho / 2, (alto / 2) - 60),
                "Jugar",
                letra(27),
                blanco
                )

    # Escribe la opción Instrucciones en la pantalla inicial
    instrucciones = Boton(
                        boton,
                        (ancho / 2, (alto / 2)),
                        "Instrucciones",
                        letra(27),
                        blanco
                        )

    # Escribe la opción Highscore en la pantalla inicial
    highscore = Boton(
                    boton,
                    (ancho / 2, (alto / 2) + 60),
                    "Highscore",
                    letra(27),
                    blanco
                    )

    # Escribe la opción Salir en la pantalla inicial
    salir = Boton(
                boton,
                (ancho / 2, (alto / 2) + 120),
                "Salir",
                letra(27),
                blanco
                )

    # Actualiza los botones en la pantalla
    jugar.update(pantalla)
    instrucciones.update(pantalla)
    highscore.update(pantalla)
    salir.update(pantalla)

    pygame.display.flip()  # Actualiza toda la pantalla
    espera = True  # Declara espera como True
    while espera:  # Se ejecuta mientas espera sea True
        clock.tick(60)  # Actualiza el reloj
        # Asignación de las tareas a realizar con cada botón
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                cursor_menu = pygame.mouse.get_pos()
                if jugar.esperando_estados(cursor_menu):
                    espera = False
                if instrucciones.esperando_estados(cursor_menu):
                    menu_instrucciones()
                if highscore.esperando_estados(cursor_menu):
                    menu_highscore()
                if salir.esperando_estados(cursor_menu):
                    pygame.quit()
                    exit()
        pygame.display.flip()  # Actualiza toda la pantalla


def nombre_highscore(caracter, contador):
    '''
    Esta función muestra en pantalla el nombre del jugador que obtuvo un nuevo
    récord conforme ingresa cada letra.
    '''
    if contador == 1:  # En caso de que sea la primera letra ingresada
        # Se muestra la letra en pantalla ubicada en la primera posición
        formato_texto(
                pantalla, caracter,
                27, (ancho // 2) - 27,
                alto // 1.7
                )
    if contador == 2:  # En caso de que sea la segunda letra ingresada
        # Se muestra la letra en pantalla ubicada en la segunda posición
        formato_texto(
                pantalla, caracter,
                27, ancho // 2,
                alto // 1.7
                )
    if contador == 3:  # En caso de que sea la tercera letra ingresada
        # Se muestra la letra en pantalla ubicada en la tercera posición
        formato_texto(
                pantalla, caracter,
                27, (ancho // 2) + 27,
                alto // 1.7
                )
    pygame.display.flip()  # Actualiza toda la pantalla


def pantalla_highscore(score):
    '''
    Esta función muestra la pantalla de nuevo highscore cuando el jugador
    completa un nuevo récord.
    '''
    # Pone la pantalla sobre la imagen de fondo
    pantalla.blit(fondo, [0, 0])
    # Escribe NUEVO RÉCORD en la pantalla inicial
    formato_texto(pantalla, "NUEVO RECORD", 65, ancho // 2, alto // 11)
    # Escribe el récord numérico en la pantalla inicial
    formato_texto(pantalla, str(score), 40, ancho // 2, alto // 4)
    # Muestra texto para indicar la escritura nombre de tres letras y guardar
    # el récord
    formato_texto(
                pantalla, "Escriba su nombre compuesto por tres",
                20, ancho // 2,
                alto // 2.5
                )
    # Muestra texto para indicar la escritura nombre de tres letras y guardar
    # el récord
    formato_texto(
                pantalla, "caracteres (cuando finalice",
                20, ancho // 2,
                alto // 2.2
                )
    # Muestra texto para indicar la escritura nombre de tres letras y guardar
    # el récord
    formato_texto(
                pantalla, "presione la tecla espacio)",
                20, ancho // 2,
                alto // 1.9
                )
    # Muestra espacio para escribir nombre de tres letras y guardar el récord
    formato_texto(
                pantalla, "___",
                27, ancho // 2,
                alto // 1.6
                )
    pygame.display.flip()  # Actualiza toda la pantalla
    espera = True  # Declara espera como True
    nombre = ""  # Declara nombre como string vacío, luego se sobreescribe
    contador = 0  # Declara contador inicialmente como cero

    while espera:  # Se ejecuta mientas espera sea True

        # Crea lista para insertar teclas en "evento.type == pygame.KEYDOWN"
        lista_K = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
                   pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
                   pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
                   pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                   pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y,
                   pygame.K_z, pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                   pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                   pygame.K_9]

        # Crea lista con letras del abecedario
        lista_tecla = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                       "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                       "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6",
                       "7", "8", "9"]

        clock.tick(60)  # Actualiza el reloj
        for evento in pygame.event.get():  # Verifica entrada por usuario
            if evento.type == pygame.QUIT:  # Si se cierra la pantalla
                pygame.quit()  # Se cierra el juego
            if evento.type == pygame.KEYDOWN:  # Si se presiona una tecla
                for i in range(len(lista_K)):
                    if evento.key == lista_K[i]:  # Verifica la letra
                        nombre += lista_tecla[i]
                        contador += 1
                    # Llama a nombre_highscore, le envía la letra seleccionada
                    # y contador actual
                        nombre_highscore(lista_tecla[i], contador)

            while contador == 3:  # Se ejecuta mientras contador sea 3
                # para evitar que se ingresen más de tres letras
                for evento in pygame.event.get():  # Verifica entrada de tecla
                    if evento.type == pygame.QUIT:  # Si se cierra la pantalla
                        pygame.quit()  # Se cierra el juego
                    if evento.type == pygame.KEYDOWN:  # Si se presiona tecla
                        if evento.key == pygame.K_SPACE:  # Si es tecla espacio
                            espera = False  # Espera se declara como falso
                            # y así se rompe el ciclo
                            contador = 0  # Se reinicia el contador

        directorio_actual = os.getcwd()  # Obtiene directorio actual
        direccion_nombre = str(directorio_actual) + "/Nombre.txt"  # Agrega
        # nombre de archivo al directorio actual
        nombre_hs = open(direccion_nombre, 'w')  # Abre archivo con nombre de
        # jugador que tiene el récord
        nombre_hs.seek(0)  # Borra lo que esté en el archivo
        nombre_hs.truncate
        nombre_hs.write(str(nombre + " \n"))  # Escribe nombre de jugador con
        # nuevo récord en el archivo
        nombre_hs.close()  # Cierra el archivo


def musica_principal(nivel, cancion):
    '''
    Esta función es para la música de la pantalla principal.
    '''
    pygame.mixer.music.load(cancion)  # Carga música
    pygame.mixer.music.set_volume(nivel)  # Selección volumen
    pygame.mixer.music.play(loops=-1)  # Repetición


# Fin de declaración de funciones ---------------------------------------------

# Main del juego
if __name__ == "__main__":
    game_over = True  # Inicializa game_over como True
    running = True  # Inicializa running como True
    score = 0  # Inicializa score como cero
    directorio_actual = os.getcwd()  # Obtiene directorio actual
    highscore = str(directorio_actual) + "/Highscore.txt"  # Agrega nombre de
    # archivo al directorio actual

    while running:
        if game_over:
            # Llama la función y le envía el nivel de volumen y cancion
            musica_principal(1.8, "assets/sound_astra.mp3")

            # Abrir el archivo 'highscore' een modo lectura y escritura
            hsco = open(highscore, 'r+')
            hscore = hsco.readlines()  # Leer linea en archivo
            hscor = []  # Lista vacía para highscore
            for h in hscore:
                quita_salto = h.rstrip('\n')  # Quitar salto de línea
                hscor.append(quita_salto)  # Añade variable

            # Crear un nuevo highscore
            score_nuevo = ""
            for j in hscor:
                if score > int(j):  # Compara score con highscore
                    hsco.seek(0)  # Busca la primera posición del txt
                    hsco.truncate  # Elimina la puntuación anterior
                    score_nuevo += str(score)
                    score_nuevo += " \n"
                    hsco.write(score_nuevo)  # Escribe el nuevo valor
                    pantalla_highscore(str(score))  # Llama función con score
            hsco.close()                            # como prámetro

            # Regresa a 'pantalla_inicial'
            pantalla_inicial()
            game_over = False
            # Llama la función y le envía el nivel de volumen y canción
            musica_principal(0.5, "assets/music.ogg")
            # La clase Group se utiliza para manejar estos objetos
            all_sprites = pygame.sprite.Group()
            lista_enemigos = pygame.sprite.Group()
            bullets = pygame.sprite.Group()

            jugador = Jugador()
            all_sprites.add(jugador)

            for i in range(8):
                enemigo = Enemigo()
                all_sprites.add(enemigo)
                lista_enemigos.add(enemigo)
            score = 0  # Marcador inica en 0

        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Si se presiona espacio
                    jugador.disparo()             # el jugador dispara

        all_sprites.update()

        # Colisiones entre proyectiles del jugador y los enemigos
        colisiones = pygame.sprite.groupcollide(
                                    lista_enemigos, bullets, True, True)
        for colision in colisiones:
            score += 10  # Por cada enemigo abatido la puntuación aumenta en 10
            explosion = Explosion(colision.rect.center)
            all_sprites.add(explosion)
            enemigo = Enemigo()
            all_sprites.add(enemigo)
            lista_enemigos.add(enemigo)

        # Colisiones entre el jugador y los enemigos
        colisiones = pygame.sprite.spritecollide(
                                        jugador, lista_enemigos, True)
        for colision in colisiones:
            jugador.vida -= 25  # Por cada impacto con un enemigo se pierde
            enemigo = Enemigo()  # una vida
            all_sprites.add(enemigo)
            lista_enemigos.add(enemigo)
            if jugador.vida <= 0:  # Si se pierden todas las vidas
                game_over = True   # se termina el juego
        pantalla.blit(fondo, [0, 0])

        all_sprites.draw(pantalla)

        # Se coloca en la interfaz el puntaje del jugador
        formato_texto(pantalla, str(score), 25, ancho // 2, 10)

        # Se coloca en la interfaz las vidas del jugador
        formato_vida(pantalla, 5, 5, jugador.vida)

        pygame.display.flip()  # Actualiza pantalla
    pygame.quit()  # Se sale de pygame
    exit()  # Fuera del ciclo while running, se termina el juego
