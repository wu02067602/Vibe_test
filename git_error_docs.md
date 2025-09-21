## Git 推送帳號切換指南（多帳號／無權限 403 問題）

本指南說明在 Windows（PowerShell）環境下，當你推送到 GitHub 出現 403、或需要切換「具有推送權限的帳號」時，該如何安全處理。重點是：

- **推送權限取決於「認證帳號」**（HTTPS 的登入帳號／PAT，或 SSH 所對應金鑰所屬的帳號），而不是 `git config user.name/email` 的提交作者資訊。
- 優先考慮不修改系統層級的「認證管理員」，改採 SSH 或每個倉庫獨立的 HTTPS 認證。

---

## 快速判斷

1) 檢查遠端與分支
```bash
git remote -v
git branch --show-current
```

2) 如果推送顯示 403 並且訊息像「denied to OtherUser」，代表你目前的認證身分是 `OtherUser`，而非擁有權限的帳號。

---

## 方法一：SSH（建議、長期穩定）

適合想在多個倉庫與帳號間穩定切換，且避免每次輸入密碼／PAT。

1) 將遠端切到 SSH 形式
```bash
git remote set-url origin git@github.com:<OWNER>/<REPO>.git
```

2) 產生或準備對應帳號的 SSH 金鑰（路徑通常在 `C:\Users\<你>\.ssh\`）
```bash
ssh-keygen -t ed25519 -C "<你的 GitHub 帳號>"
```
將產生的「.pub 公鑰」加入該 GitHub 帳號（Settings → SSH and GPG keys）。

3) 驗證目前透過哪個帳號登入 GitHub（期望出現 Hi <你的帳號>!）
```bash
ssh -T git@github.com
```

4) 多帳號情境（可選）：用 `~/.ssh/config` 指定金鑰與 Host 別名，避免混用
```
Host github-<account>
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_<account>
```
然後把遠端指向這個別名（scp 形式 URL 可用 Host 別名）：
```bash
git remote set-url origin git@github-<account>:<OWNER>/<REPO>.git
```

5) 推送
```bash
git push -u origin main
```

---

## 方法二：HTTPS（每個倉庫使用獨立憑證，不改系統認證）

適合短期快速切換，或不想設定 SSH。此法不需要動「Windows 認證管理員」。

1) 讓憑證依倉庫路徑區分（避免跨倉庫互相影響）
```bash
git config --global credential.useHttpPath true
```

2) 在遠端 URL 中指定要使用的帳號
```bash
git remote set-url origin https://<帳號>@github.com/<OWNER>/<REPO>.git
```

3) 首次推送時，依提示在瀏覽器登入或輸入 PAT（Personal Access Token）
```bash
git push -u origin main
```
注意：
- 有啟用 2FA 時，必須使用 PAT 取代密碼。
- PAT 權限至少需包含 `repo`。

---

## 方法三：調整倉庫權限（組織／協作者）

如果你確實需要用目前登入的另一個帳號推送，也可以：
- 在目標倉庫將該帳號加入 Collaborator 或組織 Team，賦予寫入權限。

---

## 常見指令速查

- 檢查遠端：
```bash
git remote -v
```

- 切換遠端（HTTPS → SSH 或更換 URL）：
```bash
git remote set-url origin <new-url>
```

- 顯示目前分支：
```bash
git branch --show-current
```

- 首次推送並建立追蹤：
```bash
git push -u origin main
```

- 將目前分支改名為 main（可選）：
```bash
git branch -M main
```

- 測試 SSH 身分：
```bash
ssh -T git@github.com
```

---

## 故障排除

- 403 並顯示「denied to OtherUser」
  - 代表你的認證帳號錯了。改用「方法一 SSH」並對應正確金鑰，或用「方法二 HTTPS」指定帳號並以該帳號的 PAT 登入。

- 推送時要求輸入密碼
  - 需改用 PAT（有 2FA 時必須如此）。

- `ssh -T` 顯示 Hi 但不是預期帳號
  - 設定 `~/.ssh/config` 為該倉庫指定金鑰，或使用 Host 別名並在遠端 URL 使用該別名。

---

## 你在本倉庫的成功案例（參考）

- 你使用了「方法二（HTTPS）」：
  - 啟用每倉庫憑證隔離：
    ```bash
    git config --global credential.useHttpPath true
    ```
  - 在遠端 URL 指定帳號並推送：
    ```bash
    git remote set-url origin https://<你的帳號>@github.com/<OWNER>/<REPO>.git
    git push -u origin main
    ```
  - 推送成功，建立了 `origin/main` 的追蹤。


