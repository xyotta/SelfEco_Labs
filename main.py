from Overlay import Overlay
from Stats import Stats
if __name__ == "__main__":
    app = Overlay()
    stats = Stats()
    print(stats.calculate_gpm())
    app.run()