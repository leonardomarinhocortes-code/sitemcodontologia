# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Site institucional da **Dra. Nathália Marra — Marra Cortes Odontologia** (odontopediatria em Patos de Minas — MG).

- URL de produção: `https://marracortesodontologia.com.br/`
- Repositório GitHub: `leonardomarinhocortes-code/sitemcodontologia`
- Deploy: push direto na branch `master` (hospedagem via GitHub Pages ou equivalente)

## Estrutura

```
index.html      — arquivo único: HTML + CSS embutido + JS embutido
favicon.ico     — ícone do site
fotos/          — imagens do consultório (IMG_6077.jpg … IMG_6120.jpg)
```

Não há build, bundler, framework ou dependências externas instaladas localmente. Tudo roda direto no browser.

## Seções do index.html

| ID | Seção |
|---|---|
| `#hero` | Apresentação principal com CTA WhatsApp |
| `#trust` | Indicadores de confiança (números/selos) |
| `#diferenciais` | Diferenciais do consultório |
| `#servicos` | Serviços oferecidos |
| `#ambiente` | Galeria de fotos do ambiente |
| `#sobre` | Biografia da Dra. Nathália |
| `#faq` | Perguntas frequentes |
| `#contato` | Endereço, telefone e mapa |

## CSS — Design Tokens (`index.html:56`)

Paleta e tipografia definidas como custom properties em `:root`:

- Cores: `--bege`, `--dourado`, `--dourado-escuro`, `--marrom-escuro`, `--marrom-texto`, `--verde-wpp`
- Tipografia: `--fs-body` (DM Sans) e `--fs-head` (Playfair Display) via Google Fonts
- Componentes prontos: `.btn`, `.btn-gold`, `.btn-wpp`, `.btn-ghost`, `.btn-lg`, `.container`, `.eyebrow`, `.section`, `.section-head`

## JavaScript (`index.html:~1540`)

- `IntersectionObserver` para animações de entrada (classe `.reveal`)
- Sem outras dependências JS — vanilla puro

## Contato e dados fixos

- WhatsApp: `(34) 99727-0834`
- Endereço: R. Agenor Maciel, 170 — Sala 405/406 — Edifício Centenário, Patos de Minas — MG, 38700-046
- Instagram: `@dranathaliamarra`
- Schema.org do tipo `Dentist` no `<head>` para SEO local

## Como visualizar localmente

Abrir `index.html` diretamente no browser ou servir com qualquer servidor estático:

```bash
npx serve .
```

## Deploy

```bash
git add .
git commit -m "mensagem"
git push origin master
```
