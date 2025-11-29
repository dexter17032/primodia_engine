import pygame
from world import World
import config

# PLOTLY (dark mode visualization)
import plotly.graph_objs as go
from plotly.subplots import make_subplots

pygame.init()

screen = pygame.display.set_mode(
    (int(config.WINDOW_WIDTH), int(config.WINDOW_HEIGHT))
)
pygame.display.set_caption("Agent Simulation Live HUD")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

world = World()
running = True
tick = 0

# ---- DATA COLLECTION FOR PLOTTING ----
population_data = []
food_data = []
avg_energy_data = []
avg_horniness_data = []
mating_data = []
babies_data = []
ticks = []

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    world.update()
    stats = world.get_stats()

    # Collect every tick
    population_data.append(stats["agents"])
    food_data.append(stats["foods"])
    avg_energy_data.append(stats["avg_energy"])
    avg_horniness_data.append(stats["avg_horniness"])
    mating_data.append(stats["mating"])
    babies_data.append(stats["babies"])
    ticks.append(tick)

    # ---- DRAW ----
    screen.fill((0, 0, 0))
    world.draw(screen)

    draw_text(screen, f"Tick: {tick}", 10, 10)
    draw_text(screen, f"Agents: {stats['agents']}", 10, 30)
    draw_text(screen, f"Babies Born: {stats['babies']}", 10, 50)
    draw_text(screen, f"Food Count: {stats['foods']}", 10, 70)
    draw_text(screen, f"Mating in Progress: {stats['mating']}", 10, 90)
    draw_text(screen, f"Avg Energy: {stats['avg_energy']}", 10, 110)
    draw_text(screen, f"Avg Horniness: {stats['avg_horniness']}", 10, 130)

    pygame.display.flip()
    clock.tick(config.FPS)
    tick += 1

pygame.quit()
# ------------------------------------------------------------
# SCROLLABLE HTML DASHBOARD WITH FULLSCREEN PLOTS
# ------------------------------------------------------------
import plotly.graph_objects as go

html = """
<html>
<head>
<title>Simulation Dashboard</title>
<style>
    body {
        background-color: black;
        margin: 0;
        padding: 0;
        color: white;
        font-family: Arial;
    }
    .plot-container {
        width: 100%;
        height: 100vh;   /* FULL SCREEN HEIGHT */
        margin-bottom: 50px;
    }
</style>
</head>
<body>
"""

# ---- 1st Plot: Population ----
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=ticks, y=population_data, name="Population"))
fig1.add_trace(go.Scatter(x=ticks, y=babies_data, name="Babies Born"))
fig1.update_layout(template="plotly_dark", title="Population & Births Over Time")
html += f'<div class="plot-container">{fig1.to_html(include_plotlyjs="cdn", full_html=False)}</div>'

# ---- 2nd Plot: Food & Mating ----
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=ticks, y=food_data, name="Food Count"))
fig2.add_trace(go.Scatter(x=ticks, y=mating_data, name="Mating"))
fig2.update_layout(template="plotly_dark", title="Food & Mating Trends")
html += f'<div class="plot-container">{fig2.to_html(include_plotlyjs=False, full_html=False)}</div>'

# ---- 3rd Plot: Energy & Horniness ----
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=ticks, y=avg_energy_data, name="Avg Energy"))
fig3.add_trace(go.Scatter(x=ticks, y=avg_horniness_data, name="Avg Horniness"))
fig3.update_layout(template="plotly_dark", title="Energy & Horniness Over Time")
html += f'<div class="plot-container">{fig3.to_html(include_plotlyjs=False, full_html=False)}</div>'

html += "</body></html>"

with open("simulation_dashboard.html", "w") as f:
    f.write(html)

print("📊 Dashboard saved as simulation_dashboard.html")
print("➡️ Open it in your browser and scroll through the plots.")
