import subprocess
import time
from pathlib import Path
from utils import is_market_open

ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"
VENV_STREAMLIT = ROOT / "venv" / "Scripts" / "streamlit.exe"

if is_market_open():
  print("Starte Docker Compose...")
  subprocess.Popen(["docker-compose", "up", "-d"]).wait()
  time.sleep(5)

  print("Starte Producer...")
  subprocess.Popen([str(VENV_PYTHON), "-m", "producer.producer_stocks"])

  print("Starte Consumer...")
  subprocess.Popen([str(VENV_PYTHON), "-m", "consumer.consumer"])  
else:
  print("Lade historische Daten...")

print("Starte Streamlit...")
subprocess.Popen(["streamlit", "run", "dashboard/app.py"])

# import subprocess
# import time
# from pathlib import Path
# from utils import is_market_open

# ROOT = Path(__file__).resolve().parent
# VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"

# producer_proc = None
# consumer_proc = None
# docker_proc = None

# def start_kafka_services():
#     global docker_proc, producer_proc, consumer_proc

#     print("Starte Docker Compose…")
#     docker_proc = subprocess.Popen(["docker-compose", "up", "-d"])
#     time.sleep(5)

#     print("Starte Producer…")
#     producer_proc = subprocess.Popen([str(VENV_PYTHON), "-m", "producer.producer_stocks"])

#     print("Starte Consumer…")
#     consumer_proc = subprocess.Popen([str(VENV_PYTHON), "-m", "consumers.consumer"])


# def stop_kafka_services():
#     global producer_proc, consumer_proc

#     print("Stoppe Producer/Consumer…")

#     if producer_proc and producer_proc.poll() is None:
#         producer_proc.terminate()

#     if consumer_proc and consumer_proc.poll() is None:
#         consumer_proc.terminate()

#     print("Stoppe Docker Compose…")
#     subprocess.Popen(["docker-compose", "down"]).wait()


# def main():
#     if is_market_open():
#         start_kafka_services()
#     else:
#         print("Börse geschlossen → lade historische Daten")

#     # Dashboard starten
#     print("Starte Streamlit…")
#     streamlit_proc = subprocess.Popen(["streamlit", "run", "dashboard/app.py"])

#     try:
#         while True:
#             time.sleep(60)

#             # Check if market status changed
#             if not is_market_open():
#                 stop_kafka_services()
#             else:
#                 # Market reopened?
#                 if producer_proc is None or producer_proc.poll() is not None:
#                     start_kafka_services()

#     except KeyboardInterrupt:
#         print("Beende alles…")
#         stop_kafka_services()
#         streamlit_proc.terminate()


# if __name__ == "__main__":
#     main()
