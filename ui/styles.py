CSS = """
    <style>
    :root {
        --bg: #0e1116;
        --panel: #151a21;
        --panel-action: #475841;
        --text: #e6e8eb;
        --muted: #9aa4b2;
        --accent: #684A52;
        --danger: #e5533d;
        --log-bg: #0b0f14;
    }

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg);
        color: var(--text);
    }

    .container {
        max-width: 380px;
        margin: 40px auto;
        padding: 20px;
    }

    .panel {
        background: rgba(21, 26, 33, 0.78); /* transparence contrôlée */
        border-radius: 16px;
        padding: 24px 20px;
        box-shadow:
            0 20px 40px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    .panel-wide {
        background: rgba(21, 26, 33, 0.78);
        border-radius: 16px;
        padding: 24px;
        box-shadow:
            0 20px 40px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);

        width: calc(100vw - 32px);   /* presque plein écran */
        max-width: 1600px;           /* limite raisonnable desktop */
        margin: 20px auto;

        overflow-x: auto;
    }



    h1, h2 {
        margin: 0 0 10px 0;
        font-weight: 600;
    }

    .subtitle {
        font-size: 13px;
        color: var(--muted);
        margin-bottom: 20px;
    }

    #status {
        padding: 1px;
        border-radius: 10px;
        font-size: 14px;
        margin-bottom: 30px;
        text-align: center;
        font-family: 'OCR A Std', monospace;
    }

    .btn {
        width: 100%;
        padding: 14px;
        margin: 4px 0;
        font-size: 15px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        background: var(--accent);
        color: var(--text);
        font-weight: 600;
        
    }

    .btn.secondary {
        background: var(--panel-action);
        color: var(--text);
    }

    .btn.logs {
        background: #3a3f47;
        color: var(--text);
    }

    .btn.danger {
        background: var(--danger);
        color: white;
    }

    .btn:active {
        transform: scale(0.97);
    }

    input {
        width: 100%;
        padding: 14px;
        margin: 8px 0;
        border-radius: 10px;
        border: none;
        background: var(--panel-action);
        color: var(--text);
        font-size: 15px;
    }

    input::placeholder {
        color: var(--muted);
    }

    pre {
        background: var(--log-bg);
        color: #9effc2;
        padding: 16px;
        border-radius: 12px;
        font-size: 12px;
        overflow-x: auto;
        white-space: pre;
        
    }
    
    #title {
        font-size: 32px;
        margin-bottom: 0;
        text-align: center;
    }
    
    #subtitle {
        text-align: center;
        margin-top: 4px;
    }
    
    .mood-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 20px 0;
    }

    .mood-chips input {
        display: none;
    }

    .mood-chips label {
        padding: 10px 16px;
        border-radius: 20px;
        background: #9AA899;
        cursor: pointer;
        transition: 0.2s;
    }

    .mood-chips input:checked + label {
        background: #222;
        color: white;
    }
    
    .input-logs {
        background: #3a3f47;
        color: var(--text);
    }

    .input-logs::placeholder {
        color: var(--muted);
    }
    
    </style>
    """