
import sys
import re

new_head = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entrenador IA </title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #09101a;
            --panel-bg: #111a28;
            --panel-border: #1f2d40;
            --cyan: #00d2ff;
            --cyan-glow: rgba(0, 210, 255, 0.4);
            --green: #20e294;
            --red: #ff3b5c;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(rgba(30, 40, 60, 0.4) 1px, transparent 1px),
                linear-gradient(90deg, rgba(30, 40, 60, 0.4) 1px, transparent 1px);
            background-size: 30px 30px;
            color: var(--text-main);
            text-align: center;
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .header { margin-bottom: 30px; }
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            color: transparent;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        h1 i {
            color: var(--cyan);
            filter: drop-shadow(0 0 8px var(--cyan-glow));
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 1.1rem;
            margin: 0;
        }

        .btn-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 40px;
        }

        button {
            padding: 12px 28px;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .btn-primary {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
        }
        .btn-primary:hover {
            box-shadow: 0 6px 20px rgba(0, 198, 255, 0.5);
            transform: translateY(-2px);
        }
        .btn-secondary {
            background-color: #273346;
            color: #cbd5e1;
        }
        .btn-secondary:hover {
            background-color: #334155;
            color: white;
        }

        #main-layout {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            justify-content: center;
            max-width: 1080px;
            width: 100%;
        }
        .column-left {
            display: flex;
            flex-direction: column;
            gap: 20px;
            flex: 1;
            min-width: 320px;
            max-width: 640px;
            align-items: center;
        }
        .column-right {
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 350px;
        }

        #canvas-wrapper {
            position: relative;
            background-color: var(--panel-bg);
            border-radius: 12px;
            aspect-ratio: 4 / 3;
            width: 100%;
            max-width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        #canvas-wrapper::before, #canvas-wrapper::after {
            content: '';
            position: absolute;
            width: 50px;
            height: 50px;
            pointer-events: none;
            z-index: 10;
        }
        #canvas-wrapper::before {
            top: 20px; left: 20px;
            border-top: 3px solid var(--cyan);
            border-left: 3px solid var(--cyan);
        }
        #canvas-wrapper::after {
            bottom: 20px; right: 20px;
            border-bottom: 3px solid var(--cyan);
            border-right: 3px solid var(--cyan);
        }
        #placeholder-box {
            position: absolute;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 15px;
            color: #3b82f6;
            font-size: 14px;
        }
        #placeholder-box i {
            font-size: 48px;
            color: #1e3a8a;
        }
        canvas {
            width: 100% !important;
            height: 100% !important;
            object-fit: cover;
            position: relative;
            z-index: 1;
        }

        .panel {
            background-color: var(--panel-bg);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            text-align: left;
        }
        #status-panel {
            display: flex;
            align-items: center;
            gap: 15px;
            background-color: var(--panel-bg);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 16px 24px;
            font-size: 16px;
            font-weight: 600;
            color: var(--text-main);
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            width: 100%;
            box-sizing: border-box;
        }
        #status-panel i {
            color: var(--cyan);
            font-size: 20px;
        }
        #status-panel.good { border-color: var(--green); }
        #status-panel.good i, #status-panel.good .status-text { color: var(--green); }
        #status-panel.bad { border-color: var(--red); }
        #status-panel.bad i, #status-panel.bad .status-text { color: var(--red); }
        #status-panel.warning { border-color: #f59e0b; }
        #status-panel.warning i, #status-panel.warning .status-text { color: #f59e0b; }

        .panel-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 25px;
            text-transform: uppercase;
        }
        .panel-header i { color: var(--cyan); }

        .metric-row { margin-bottom: 20px; }
        .metric-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 600;
        }
        .metric-name { color: var(--text-main); }
        .metric-value { font-family: 'Orbitron', sans-serif; color: white; }
        .metric-bar-bg {
            width: 100%;
            height: 8px;
            background-color: #1e293b;
            border-radius: 4px;
            overflow: hidden;
        }
        .metric-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #00d2ff, #20e294);
            border-radius: 4px;
            transition: width 0.2s ease-out;
        }

        #tip-panel {
            font-size: 14px;
            color: var(--text-muted);
            border-color: rgba(0, 210, 255, 0.15);
            line-height: 1.5;
        }
        #tip-panel strong { color: var(--cyan); font-weight: 600; }
        #debug { margin-top: 20px; font-family: monospace; color: #64748b; font-size: 12px; }
    </style>
</head>
<body>

    <div class="header">
        <h1><i class="fa-solid fa-bolt"></i> VERIFICADOR GYM IA</h1>
        <p class="subtitle">Detecta automáticamente qué ejercicio haces y verifica tu postura en tiempo real.</p>
    </div>
    
    <div class="btn-group">
        <button type="button" class="btn-primary" onclick="init()"><i class="fa-solid fa-camera"></i> Activar Cámara e IA</button>
        <button type="button" class="btn-secondary" onclick="stop()"><i class="fa-solid fa-video-slash"></i> Detener</button>
    </div>

    <div id="main-layout">
        <!-- COLUMNA IZQUIERDA -->
        <div class="column-left">
            <div id="canvas-wrapper">
                <div id="placeholder-box">
                    <i class="fa-solid fa-camera-retro"></i>
                    <span>Presiona "Activar Cámara e IA" para comenzar</span>
                </div>
                <canvas id="canvas"></canvas>
            </div>
            <div id="status-panel">
                <i class="fa-solid fa-wave-square"></i>
                <span class="status-text" id="status-text">Esperando a iniciar...</span>
            </div>
        </div>

        <!-- COLUMNA DERECHA -->
        <div class="column-right">
            <div class="panel" id="metrics-panel">
                <div class="panel-header">
                    <i class="fa-solid fa-bullseye"></i> MÉTRICAS
                </div>
                <div id="label-container"></div>
            </div>
            <div class="panel" id="tip-panel">
                <strong>Tip:</strong> Asegúrate de estar bien iluminado y con suficiente espacio para realizar los movimientos.
            </div>
        </div>
    </div>
    
    <div id="debug"></div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.3.1/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/pose@0.8/dist/teachablemachine-pose.min.js"></script>
"""

with open(r'c:\Users\LENOVO LOQ\IA\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract script block
start_tag = '<script type="text/javascript">'
end_tag = '</script>\n</body>\n</html>'

start_idx = text.find(start_tag)

if start_idx != -1:
    js_part = text[start_idx:]
    
    # 1. Panel References
    js_part = js_part.replace('let feedbackPanel = document.getElementById("feedback-panel");', '''let statusPanel = document.getElementById("status-panel");
        let statusText = document.getElementById("status-text");''')

    # 2. Init Loading State
    js_part = js_part.replace('feedbackPanel.innerHTML = "Cargando cerebro de IA...";', 'statusText.innerText = "Cargando cerebro de IA...";\n            statusPanel.className = "warning";\n            statusPanel.querySelector("i").className = "fa-solid fa-spinner fa-spin";')
    js_part = js_part.replace('feedbackPanel.style.backgroundColor = "#e4a11b"; // Naranja', '')

    # 3. Init Success State
    js_part = js_part.replace('feedbackPanel.innerHTML = "¡Listo! Empieza a moverte.";', 'statusText.innerText = "¡Listo! Empieza a moverte.";\n                statusPanel.className = "good";\n                statusPanel.querySelector("i").className = "fa-solid fa-check";\n                document.getElementById("placeholder-box").style.display = "none";')
    js_part = js_part.replace('feedbackPanel.style.backgroundColor = "#4ecca3"; // Verde', '')

    # 4. Init Error State
    js_part = js_part.replace('feedbackPanel.innerHTML = "ERROR: No se encontraron los archivos (model.json, weights.bin, etc). Revisa la consola.";', 'statusText.innerText = "ERROR: No se encontraron los archivos del modelo (Revisa la consola).";\n                statusPanel.className = "bad";\n                statusPanel.querySelector("i").className = "fa-solid fa-triangle-exclamation";')
    js_part = js_part.replace('feedbackPanel.style.backgroundColor = "#e94560"; // Rojo', '')

    # 5. Stop State
    js_part = js_part.replace('feedbackPanel.innerHTML = "Detenido. Puedes volver a iniciar.";', 'statusText.innerText = "Detenido. Puedes volver a iniciar.";\n            statusPanel.className = "";\n            statusPanel.querySelector("i").className = "fa-solid fa-video-slash";\n            document.getElementById("placeholder-box").style.display = "flex";')
    js_part = js_part.replace('feedbackPanel.style.backgroundColor = "#555";', '')
    
    # 6. Hide placeholder on play
    js_part = js_part.replace('await webcam.play();', 'await webcam.play();\n                document.getElementById("placeholder-box").style.display = "none";')

    # 7. Labels Generation
    old_label_create = '''                labelContainer = document.getElementById("label-container");
                labelContainer.innerHTML = "";
                for (let i = 0; i < maxPredictions; i++) { 
                    let div = document.createElement("div");
                    div.className = "class-label";
                    labelContainer.appendChild(div);
                }'''
    
    new_label_create = '''                labelContainer = document.getElementById("label-container");
                labelContainer.innerHTML = "";
                for (let i = 0; i < maxPredictions; i++) { 
                    let row = document.createElement("div");
                    row.className = "metric-row";
                    
                    let header = document.createElement("div");
                    header.className = "metric-header";
                    let nameElem = document.createElement("span");
                    nameElem.className = "metric-name";
                    nameElem.innerText = "...";
                    let valElem = document.createElement("span");
                    valElem.className = "metric-value";
                    valElem.innerText = "0%";
                    header.appendChild(nameElem);
                    header.appendChild(valElem);
                    
                    let barBg = document.createElement("div");
                    barBg.className = "metric-bar-bg";
                    let barFill = document.createElement("div");
                    barFill.className = "metric-bar-fill";
                    barBg.appendChild(barFill);
                    
                    row.appendChild(header);
                    row.appendChild(barBg);
                    
                    labelContainer.appendChild(row);
                }'''
    js_part = js_part.replace(old_label_create, new_label_create)

    # 8. Labels Update Loop
    old_label_update = '''            if (nowMs - lastUiUpdateMs > 250) {
                lastUiUpdateMs = nowMs;
                for (let i = 0; i < maxPredictions; i++) {
                    const className = classNames[i];
                    const prob = smoothedProbs[i];
                    labelContainer.childNodes[i].innerHTML = `${className}: ${(prob * 100).toFixed(0)}%`;
                }
            }'''
            
    new_label_update = '''            if (nowMs - lastUiUpdateMs > 100) {
                lastUiUpdateMs = nowMs;
                for (let i = 0; i < maxPredictions; i++) {
                    const className = classNames[i];
                    const prob = smoothedProbs[i];
                    const row = labelContainer.childNodes[i];
                    if (row) {
                        row.querySelector(".metric-name").innerText = className;
                        row.querySelector(".metric-value").innerText = `${(prob * 100).toFixed(0)}%`;
                        row.querySelector(".metric-bar-fill").style.width = `${prob * 100}%`;
                    }
                }
            }'''
    js_part = js_part.replace(old_label_update, new_label_update)

    # 9. Feedback Status Logic
    old_status_update = '''            // Cambiar los colores de la UI
            feedbackPanel.innerHTML = message;
            if (poseOk && confOk && marginOk) {
                feedbackPanel.style.backgroundColor = isCorrect ? "#4ecca3" : "#e94560"; // Verde o Rojo
            } else {
                feedbackPanel.style.backgroundColor = "#555"; // Gris
            }'''
            
    new_status_update = '''            // Cambiar los colores de la UI
            statusText.innerText = message;
            statusPanel.className = "";
            let iconEl = statusPanel.querySelector("i");
            
            if (poseOk && confOk && marginOk) {
                if (isCorrect) {
                    statusPanel.classList.add("good");
                    iconEl.className = "fa-solid fa-check-circle";
                } else {
                    statusPanel.classList.add("bad");
                    iconEl.className = "fa-solid fa-triangle-exclamation";
                }
            } else {
                statusPanel.classList.add("warning");
                iconEl.className = "fa-solid fa-wave-square";
            }'''
    js_part = js_part.replace(old_status_update, new_status_update)

    # Clean old Â¡ if existed due to encoding
    js_part = js_part.replace('Â¡', '¡')

    final_document = new_head + "\n    " + js_part
    
    with open(r'c:\Users\LENOVO LOQ\IA\index.html', 'w', encoding='utf-8') as f:
        f.write(final_document)
else:
    print("Could not find script block")

