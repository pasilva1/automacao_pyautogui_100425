from flask import Flask, jsonify
import pyautogui
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Desativa o fail-safe do PyAutoGUI
pyautogui.FAILSAFE = False


def abrir_bloco_de_notas():
    try:
        print(f"[{datetime.now()}] Executando automação com PyAutoGUI...")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write('notepad.exe')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(
            'Automação feita com Flask + PyAutoGUI + APScheduler!', interval=0.05)
        print("[OK] Automação concluída com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao executar automação: {e}")


@app.route('/abrir_bloco_de_notas')
def executar_manual():
    try:
        abrir_bloco_de_notas()
        return jsonify({"status": "ok", "mensagem": "Automação executada manualmente."})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# Agendador
scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
scheduler.add_job(
    func=abrir_bloco_de_notas,
    trigger='cron',
    hour=15,
    minute=55,
    second=5,
    misfire_grace_time=300,
    id='abrir_bloco')
scheduler.start()

if __name__ == '__main__':
    print("Servidor Flask iniciado. Aguardando requisições ou agendamento...")
    app.run(host="0.0.0.0", port=5000, debug=True)
