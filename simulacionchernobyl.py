import pygame
import random

# Inicializar pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación del Desastre de Chernóbil")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Configuración del reactor
reactor_center = (WIDTH // 2, HEIGHT // 2)
reactor_radius = 100

# Lista de neutrones
neutrons = [{"x": reactor_center[0], "y": reactor_center[1], "vx": random.uniform(-2, 2), "vy": random.uniform(-2, 2)} for _ in range(20)]

# Barra de control automática
bar_width = 20
bar_height = 150
bar_x = reactor_center[0] - bar_width // 2
bar_y = reactor_center[1] - bar_height // 2
bar_speed = 1  # Velocidad de movimiento automático de las barras

# Reloj para controlar el FPS
clock = pygame.time.Clock()

# Variables de simulación
energy = 1  # Representa la energía en el reactor
time_elapsed = 0  # Segundos simulados
simulation_speed = 1  # Velocidad de la simulación en tiempo real
running = True
catastrophe_triggered = False

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Incrementar el tiempo
    time_elapsed += simulation_speed / 60  # Segundos simulados por frame

    # Automatizar barras de control
    if not catastrophe_triggered:
        if time_elapsed <= 20:  # Primeros 20 segundos: Retirar las barras lentamente
            bar_y += bar_speed * simulation_speed / 60
        elif time_elapsed > 20 and time_elapsed <= 40:  # Proceso acelerado
            bar_y += (bar_speed * 2) * simulation_speed / 60

    # Aumentar la energía exponencialmente
    if not catastrophe_triggered:
        energy *= 1 + (0.01 * simulation_speed)  # Energía aumenta exponencialmente

    # Desencadenar la catástrofe
    if energy > 1000 and not catastrophe_triggered:  # Punto crítico
        catastrophe_triggered = True

    # Actualizar posiciones de neutrones
    for neutron in neutrons:
        neutron["x"] += neutron["vx"]
        neutron["y"] += neutron["vy"]

        # Rebote en los bordes del reactor
        if (neutron["x"] - reactor_center[0])**2 + (neutron["y"] - reactor_center[1])**2 > reactor_radius**2:
            neutron["vx"] *= -1
            neutron["vy"] *= -1

    # Dibujar todo
    screen.fill(BLACK)

    if catastrophe_triggered:
        # Mostrar explosión
        pygame.draw.circle(screen, RED, reactor_center, reactor_radius * 2)
    else:
        # Dibujar reactor y barras
        pygame.draw.circle(screen, GRAY, reactor_center, reactor_radius)  # Reactor
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width, bar_height))  # Barra de control

        # Dibujar neutrones
        for neutron in neutrons:
            pygame.draw.circle(screen, RED, (int(neutron["x"]), int(neutron["y"])), 5)

    # Mostrar energía y tiempo
    font = pygame.font.Font(None, 36)
    energy_text = font.render(f"Energía: {int(energy)}", True, WHITE)
    time_text = font.render(f"Tiempo: {int(time_elapsed)} s", True, WHITE)
    screen.blit(energy_text, (10, 10))
    screen.blit(time_text, (10, 50))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
