# 🧹 Bot de Faxina — Masmorra

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

Bot que organiza e divide automaticamente a faxina semanal entre os moradores de uma república, enviando o aviso direto no WhatsApp — sem precisar de ninguém lembrar ou montar a escala manualmente.

## 💡 Como funciona

A república tem **8 moradores** e **7 tarefas de limpeza** (algumas exigem 2 pessoas, como a cozinha). Toda semana o bot:

1. Calcula quantas semanas se passaram desde uma data de referência.
2. Rotaciona a fila de moradores nessa mesma quantidade de posições, usando uma `deque` — garantindo um rodízio justo, sem repetir a mesma ordem toda semana.
3. Distribui os moradores nas tarefas, na ordem da fila já rotacionada.
4. Monta a mensagem e envia via [CallMeBot](https://www.callmebot.com/) para o grupo/número configurado.

### Exemplo de mensagem gerada

```
⛔ *Faxina de QUARTA-FEIRA 26/08*

Sala + lavabo - Mixirika
Copa - Bbzaum
Escada dentro de casa - Paldselfi
Cozinha - Jab + Ze do Caroco
Banheiro principal - B.Guilherme
Banheiro do quarto - B.Henryke
Escada da entrada - B.Lucas
```

## ⚙️ Automação

O envio é 100% automático via **GitHub Actions** ([`escala.yml`](./.github/workflows/escala.yml)):

- Roda todo **quarta-feira às 01:00 UTC** (00:00 no horário de Brasília), via `cron`.
- Também pode ser disparado manualmente pela aba **Actions** do repositório (`workflow_dispatch`).
- As credenciais (`PHONE_NUMBER` e `API_KEY`) ficam guardadas como **GitHub Secrets**, nunca expostas no código.

## 🚀 Como usar em outra república

1. Faça um fork ou copie o repositório.
2. Edite as listas no topo de `Faxina_Masmorra.py`:
   - `moradores`: nomes das pessoas, na ordem inicial da fila.
   - `tarefas`: cômodos/tarefas e quantas pessoas cada uma exige.
   - `data_inicio`: a data em que essa ordem inicial passa a valer.
3. Crie uma conta gratuita no [CallMeBot](https://www.callmebot.com/whatsapp/) e gere sua API key.
4. No repositório, vá em **Settings → Secrets and variables → Actions** e adicione:
   - `PHONE_NUMBER` — número autorizado no CallMeBot.
   - `API_KEY` — chave gerada pelo CallMeBot.
5. Pronto — o workflow assume a partir daí, toda quarta-feira.

## 🛠️ Tecnologias

- **Python 3.10** — lógica de rotação e montagem da mensagem.
- **`collections.deque`** — rotação eficiente da fila de moradores.
- **[CallMeBot API](https://www.callmebot.com/)** — envio da mensagem via WhatsApp.
- **GitHub Actions** — agendamento e execução automática (`cron` + `workflow_dispatch`).
