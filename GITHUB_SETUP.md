# 🚀 GitHub Ke Liye Instructions

## Step 1: GitHub par nayi repository banao

1. GitHub.com par jao: https://github.com/new
2. Repository name likho: **auth_system**
3. Description (optional): "Professional Security Dashboard with Role-Based Access Control"
4. Visibility: **Public** (ya Private, jo tum chahte ho)
5. ❌ "Initialize this repository with a README" - UNCHECK kro
6. ❌ "Add .gitignore" - UNCHECK kro (humne pehle se banai hai)
7. "Create repository" button par click kro

## Step 2: Remote add karo aur push karo

Repository banane ke baad, ye commands run karo:

```bash
cd "c:\Users\Neel Rana\OneDrive\Desktop\cyberguard"

git remote add origin https://github.com/Neelrana12/auth_system.git

git branch -M main

git push -u origin main
```

## GitHub Credentials

Agar GitHub ask kare credentials ka, to:
- **Username**: Neelrana12
- **Personal Access Token**: GitHub par jakar Settings > Developer settings > Personal access tokens > Tokens (classic) > "Generate new token" se banao
  - Select scopes: `repo` (full control of private repositories)
  - Copy token aur terminal mein paste kro jab password maange

## Success! 🎉

Push complete hone ke baad, GitHub par dekh sakte ho:
https://github.com/Neelrana12/auth_system

---

**Kafi important: Personal Access Token kabhi public mat karna!**
