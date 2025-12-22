import requests
import subprocess
import time
import threading
import pygame

class ServerHopper:
    def __init__(self, place_id):
        self.place_id = place_id
        self.hopping = False

    def CloseSober(self):
        subprocess.run(["pkill", "-9", "-f", "sober"], check=False)
        subprocess.run(["pkill", "-9", "-f", "RobloxPlayerBeta"], check=False)
        time.sleep(3)

    def GetServers(self):
        url = f"https://games.roblox.com/v1/games/{self.place_id}/servers/Public"
        try:
            r = requests.get(url, params={"sortOrder": "Asc", "limit": 100})
            if r.status_code == 200:
                return r.json()["data"]
        except:
            pass
        return []

    def FindBestServer(self, servers):
        available = [s for s in servers if s["playing"] < s["maxPlayers"]]
        if not available:
            return None
        return sorted(available, key=lambda s: s["playing"])[0]

    def JoinServer(self, job_id):
        link = f"roblox://placeId={self.place_id}&gameInstanceId={job_id}"
        subprocess.Popen(["xdg-open", link])

    def Hop(self):
        if self.hopping:
            return
        self.hopping = True

        print("HOPPING SERVER")
        self.CloseSober()
        servers = self.GetServers()
        best = self.FindBestServer(servers)

        if best:
            self.JoinServer(best["id"])

        time.sleep(7)
        self.hopping = False


# ---------- PYGAME ----------

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Sober Server Hopper")

font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

hopper = ServerHopper(1537690962)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                threading.Thread(target=hopper.Hop, daemon=True).start()

            elif event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30))
    screen.blit(font.render("R - hop server", True, (200, 200, 200)), (80, 100))
    screen.blit(font.render("Q - quit", True, (200, 200, 200)), (80, 140))

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
