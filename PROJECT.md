# Contador
## Objetivo
App Android mínimo e real: contador de toques persistente, com 2 telas (principal e Sobre). Serve de validação E2E da skill apk-factory v2 (garantismo total).
## Entregáveis
- E1: APK instalável assinado no vault privado (camillanapoles/apk-vault/contador/)
- E2: Pipeline CI verde com gates GWT por etapa + job report
- E3: Governança: DB SQLite fonte única + FastAPI CRUD/eventos deterministas
- E4: App instalado e verificado no device do dono
## Requisitos
- RF-01: Tela principal exibe contador e botão +1 que incrementa e persiste (SharedPreferences)
- RF-02: Botão "Sobre" abre segunda tela (AboutActivity) com info do app
- RNF-01: minSdk 24, dark theme, sem dependências externas (aapt2 puro)
- RNF-02: Repo público; APK só no vault privado; keystore em secrets
## Stack
app: Java puro + aapt2 (make) / ci: GitHub Actions / gov: FastAPI 0.99 + pydantic 1.10 + SQLite (Termux)
## Casos de uso (GWT)
- UC-01 Contar: Given app aberto com contador N / When usuário toca "+1 toque" / Then contador mostra N+1 e valor sobrevive a restart do app
- UC-02 Sobre: Given tela principal / When usuário toca "Sobre" / Then abre AboutActivity mostrando nome/versão do app, sem crash
## Fora de escopo
- Lista de contadores múltiplos, notificações, ícone launcher custom ( fica p/ projeto real)
