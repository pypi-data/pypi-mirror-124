import pygame
pygame.init()
import load
import os
from Modules.Engine.interface.text import TEXT
from Modules.Engine.thread import THREAD

# load.loading()





class MAIN:
    def __init__(self):
        self.running = True
        self.images = load.loading()
        self.images["tooltip"] = pygame.image.load(os.path.join("TEXT", "back.png"))
        while True:
            path = input("Please insert Path: ")
            if os.path.exists(path):
                self.file_path = path
                self.surface = self.prepare()
                break
            else:
                print("File not found.")
        self.width = 500
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("%s - GML-Editor" % os.path.split(self.file_path)[1].split(".")[0])
        self.file_modified = os.path.getmtime(self.file_path)
        self.thread_going = False
        self.threading = None

    def prepare(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            st = "".join(file.readlines())
        d = TEXT(max_width=500)
        c, h, w = d.init(st, self.images)
        return d.parse(c, self.images, self.images["tooltip"], w, h)

    def run(self):
        while self.running:
            if not self.thread_going and os.path.getmtime(self.file_path) != self.file_modified:
                self.thread_going = True
                self.file_modified = os.path.getmtime(self.file_path)
                self.threading = THREAD(target=self.prepare)
                self.threading.start()
            elif self.threading is not None and not self.threading.alive():
                result = self.threading.join()
                if result is not None:
                    self.surface = result
                else:
                    print("Error in GML-code")
                self.threading = None
                self.thread_going = False
            self.screen.blit(pygame.transform.scale(self.images["tooltip"], (self.width, self.height)), (0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.display.quit()
                    q = input("Do you want to quit (J/n): ")
                    if q == "J":
                        self.running = False
                        return
                    pygame.display.init()
                    self.screen = pygame.display.set_mode((self.width, self.height))
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        q = input("Do you want to quit (J/n): ")
                        if q == "J":
                            self.running = False
                            return
                        pygame.display.init()
                        self.screen = pygame.display.set_mode((self.width, self.height))
                    elif e.key == pygame.K_m:
                        pygame.display.quit()
                        path = input("Please insert Path: ")
                        if os.path.exists(path):
                            self.file_path = path
                            self.surface = self.prepare()
                        pygame.display.init()
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        pygame.display.set_caption("%s - GML-Editor" % os.path.split(self.file_path)[1].split(".")[0])
            if self.surface.get_height() > self.height:
                old = self.surface.get_width() / self.surface.get_height()
                self.surface = pygame.transform.scale(self.surface, (int((self.height-20)*old), self.height-20))
            self.screen.blit(self.surface, (10, 10))
            pygame.display.update()


if __name__ == "__main__":
    wiki = MAIN()
    wiki.run()
