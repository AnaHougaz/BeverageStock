# Guia: Da Documentação ao Site Público com Doxygen e GitHub Pages

Este guia descreve como gerar documentação de código Python com **Doxygen** e publicá-la gratuitamente em um site utilizando **GitHub Pages**.

---

## 1. Gerar a documentação com Doxygen

Após criar seus arquivos `.py` e o arquivo de configuração `Doxyfile` (sem extensão) no VS Code, abra o terminal no diretório onde esses arquivos estão localizados e execute:

```bash
doxygen Doxyfile
````

O Doxygen criará uma pasta chamada `docs/`, que conterá outra pasta `html/` com diversos arquivos.
O arquivo principal é:

```
docs/html/index.html
```

---

## 2. Visualizar o site localmente

Para abrir a documentação localmente:

1. No VS Code, clique com o **botão direito** sobre o arquivo `index.html`.
2. Selecione **Reveal in File Explorer**.
3. No explorador de arquivos, clique com o **botão direito** sobre `index.html`.
4. Escolha **Abrir com → Internet Explorer** (ou outro navegador).

Isso exibirá o site gerado localmente.

---

## 3. Ajustar o Doxygen para o GitHub Pages

Por padrão, o Doxygen cria a estrutura:

```
docs/html/index.html
```

No entanto, o **GitHub Pages** só reconhece o conteúdo dentro da pasta `docs/` na raiz do repositório.
Para corrigir isso, é necessário alterar a saída HTML no `Doxyfile`.

### Antes

```bash
# HTML antes
GENERATE_HTML          = YES
HTML_OUTPUT            = html
HTML_FILE_EXTENSION    = .html
```

### Depois

```bash
# HTML depois
GENERATE_HTML          = YES
HTML_OUTPUT            = .
HTML_FILE_EXTENSION    = .html
```

Essas alterações fazem com que o arquivo `index.html` seja gerado diretamente dentro da pasta `docs/`, sem o subdiretório `html/`.

---

## 4. Regenerar a documentação

Após editar o `Doxyfile`:

1. Exclua a pasta antiga `docs/`.
2. Gere novamente a documentação:

```bash
doxygen Doxyfile
```

A nova estrutura será:

```
docs/
 ├── index.html
 ├── classes.html
 ├── ...
```

---

## 5. Publicar no GitHub Pages

1. Envie os seguintes arquivos para um repositório no GitHub:

   * `Doxyfile`
   * seus arquivos `.py`
   * a pasta `docs/`

2. No repositório, acesse **Settings → Pages**.

3. Em **Branch**, selecione:

   * **main**
   * **/docs**

4. Clique em **Save**.

Após alguns minutos, o GitHub Pages disponibilizará um link público para o seu site.

---

## 6. Estrutura final esperada

```
.
├── Doxyfile
├── script.py
└── docs/
    ├── index.html
    ├── classes.html
    ├── files.html
    └── ...
```

Após a publicação, o site ficará acessível no link indicado em **Settings → Pages**.

```
```
