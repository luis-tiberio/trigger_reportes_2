from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados
WORKFLOWS = [
    {"repo": "att_reporte", "workflow": "reporte.yml"},
    {"repo": "backlog", "workflow": "backlog.yml"},
    {"repo": "reportes_sp5", "workflow": "main_script.yml"}, # alterado dados.yml para main_script.yml
    {"repo": "reportes_sp15", "workflow": "atualizacao_sp15.yaml"},
    {"repo": "hora_hora_louveira", "workflow": "atualizacao_sp7.yaml"},
    {"repo": "reportes_sp7", "workflow": "atualizacao_sp7.yaml"},
    {"repo": "piso_outbound_mg2", "workflow": "piso10.yml"},
    {"repo": "base_packed_mg2", "workflow": "main_base_to_packed.yaml"},
    {"repo": "piso_outbound_go1", "workflow": "piso10.yml"},
    {"repo": "base_packed_go1", "workflow": "main_base_to_packed.yaml"},
    {"repo": "dados_fmhub_26", "workflow": "atualizacao_lsp26.yaml"},
    {"repo": "backlog_lsp26", "workflow": "backlog_lsp26.yaml"},
    {"repo": "prod_lsp26", "workflow": "reporte.yml"},
    {"repo": "db_leftover_on_time_sp5", "workflow": "main_base_to_packed.yaml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        url = f"https://api.github.com/repos/luis-tiberio/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
