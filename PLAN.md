# PLAN — Contador (roadmap vivo; refinado a cada etapa)

| Etapa | Objetivo | Entregável | Requisito | Stack da etapa | Caso de uso | Testes | Report | Status |
|---|---|---|---|---|---|---|---|---|
| S01 | Design + estrutura visual + docs aprovadas | res/ (colors/styles/2 layouts) + manifest + tests pre | RNF-01 | aapt2/XML | UC-02 (estrutura) | T-S01-01..03 | docs/reports/S01.md | done |
| S02 | App funcional + build CI verde | 2 Activities Java + unsigned.apk no CI | RF-01, RF-02 | Java/aapt2/make | UC-01, UC-02 | T-S02-01..02 | docs/reports/S02.md | ready |
| S03 | Entrega assinada no vault | APK assinado + sha256 em apk-vault/contador | RNF-02, E1 | Actions sign/dist | UC-01 | sign verify + vault check | docs/reports/S03.md | blocked |
| S04 | Instalação + fechamento | App no device + reports finais + eventos gov | E4, E2 | Termux/gov | UC-01, UC-02 | instalação manual c/ evidência | docs/reports/S04.md | blocked |

Gates (por etapa): tests do item verdes no CI + report com evidência commitado + evento run.finished aceito pelo gov. Sem isso: NÃO avançar.
