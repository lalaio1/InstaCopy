<h1 align="center">
  <img src="https://raw.githubusercontent.com/lalaio1/InstaCopy/refs/heads/main/images/banner.png" alt="InstaCopy Banner" width="700">
</h1>

<p align="center">  
  🔥 Clone perfis do Instagram com estilo — baixe posts, bio, foto de perfil e metadados diretamente no seu terminal 🔥  
</p>  

---

## ✨ Funcionalidades

✅ Login no Instagram com CSRF seguro  
✅ Suporte a **Tor** e **proxies personalizados**  
✅ Uso de **User-Agent aleatório**  
✅ Download automático de:  
   - 📸 Fotos  
   - 🎥 Vídeos  
   - 🖼️ Carrosséis  
   - 📝 Legendas  
   - 🗂️ Metadados (JSON)  
✅ Criação automática de pastas organizadas por perfil  
✅ Delay configurável entre requisições  

---

## 📸 Demonstração
![InstaCopy Banner](https://github.com/lalaio1/InstaCopy/blob/main/images/part2.png)
![InstaCopy Banner](https://github.com/lalaio1/InstaCopy/blob/main/images/part3.png)

---

## ⚙️ Instalação

### 🔹 Linux
```bash
git clone https://github.com/lalaio1/InstaCopy
cd InstaCopy
pip install -r requirements.txt
python3 InstaCopy.py -h
````

### 🔹 Termux (Android)

```bash
pkg update && pkg upgrade
pkg install git python
git clone https://github.com/lalaio1/InstaCopy
cd InstaCopy
pip install -r requirements.txt
python InstaCopy.py -h
```

### 🔹 Windows

1. Instale o **Python 3** pelo [python.org](https://www.python.org/downloads/)
2. Instale o **Git** pelo [git-scm.com](https://git-scm.com/)
3. Clone o repositório:

```powershell
git clone https://github.com/lalaio1/InstaCopy
cd InstaCopy
pip install -r requirements.txt
python InstaCopy.py -h
```

---

## 🚀 Uso

Exemplo básico:

```bash
python3 InstaCopy.py -u SEU_USUARIO -p SUA_SENHA -t alvo_insta
```

Com **Tor**:

```bash
python3 InstaCopy.py -u SEU_USUARIO -p SUA_SENHA -t alvo_insta --tor
```

Com **proxy customizado**:

```bash
python3 InstaCopy.py -u SEU_USUARIO -p SUA_SENHA -t alvo_insta --proxy http://127.0.0.1:8080
```

Com **User-Agent aleatório**:

```bash
python3 InstaCopy.py -u SEU_USUARIO -p SUA_SENHA -t alvo_insta --random-agent
```

---

## 📖 Argumentos

| Argumento          | Descrição                                     |
| ------------------ | --------------------------------------------- |
| `-u`, `--user`     | 👤 Usuário do Instagram (obrigatório)         |
| `-p`, `--password` | 🔑 Senha do Instagram (obrigatório)           |
| `-t`, `--target`   | 🎯 Usuário alvo a ser clonado (obrigatório)   |
| `--tor`            | 🕵️ Usar proxy via **Tor** (`127.0.0.1:9050`) |
| `--proxy`          | 🌐 Usar proxy customizado (http/https/socks)  |
| `--random-agent`   | 🎲 Usar **User-Agent** aleatório              |
| `-d`, `--delay`    | ⏱️ Delay entre requisições (padrão: 1s)       |

---

## 📂 Estrutura de saída

```
alvo_insta/
 ├── profile/
 │   └── alvo_insta_profile_pic.jpg
 ├── posts/
 │   ├── 001_post_legenda.jpg
 │   ├── 001_post_legenda_caption.txt
 │   └── 001_post_legenda_metadata.json
 ├── profile_metadata.json
 └── bio.txt
```

---

## 📡 Contato & Créditos

👤 Feito inteiramente por **lalaio1**
📬 Contato: [t.me/lalaio1](https://t.me/lalaio1)
📦 Repositório oficial: [InstaCopy](https://github.com/lalaio1/InstaCopy)

