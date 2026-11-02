# Avisos de terceiros

Este repositório inclui material de terceiros. As licenças abaixo valem para as partes indicadas; o restante do repositório é de autoria própria.

---

## AgentSpec — MIT License

O workflow de Spec-Driven Development deste repositório nasceu de uma adaptação do [AgentSpec](https://github.com/luanmorenommaciel/agentspec), de Luan Moreno (v2.1, abril/2026): as cinco fases (Brainstorm → Define → Design → Build → Ship), o Iterate, o Clarity Score, o File Manifest e os templates de artefato. O conteúdo foi traduzido para PT-BR e adaptado para o Genie Code.

Arquivos derivados do AgentSpec:

- `sdd-brainstorm/SKILL.md`, `sdd-brainstorm/BRAINSTORM_TEMPLATE.md`
- `sdd-define/SKILL.md`, `sdd-define/DEFINE_TEMPLATE.md`
- `sdd-design/SKILL.md`, `sdd-design/DESIGN_TEMPLATE.md`
- `sdd-build/SKILL.md`, `sdd-build/BUILD_REPORT_TEMPLATE.md`
- `sdd-ship/SKILL.md`, `sdd-ship/SHIPPED_TEMPLATE.md`
- `sdd-iterate/SKILL.md`
- `sdd-code-reviewer/SKILL.md`
- `custom-test-generator/SKILL.md`

```
MIT License

Copyright (c) 2026 AgentSpec Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## TLC Spec-Driven — CC-BY-4.0 (texto) / MIT (scripts)

Partes do workflow SDD são adaptadas do [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills) (`tlc-spec-driven` v4.1.0, de Felipe Rodrigues, Tech Leads Club). O texto das skills do Tech Leads Club é licenciado sob [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC-BY-4.0); o código é MIT (Copyright (c) 2026 Tech Leads Club). As ideias foram traduzidas para PT-BR e adaptadas para o Genie Code e para engenharia de dados no Databricks.

Adaptado do TLC Spec-Driven, com mudanças:

- `sdd-workflow/SKILL.md`: tamanho da feature (*auto-sizing*), contrato de execução, raio de ação (*blast radius*, aqui com regras do Databricks) e retomada de sessão.

---

## Databricks Agent Skills — Databricks License

As skills `databricks-*` e `spark-python-data-source` são cópia do repositório oficial [`databricks/databricks-agent-skills`](https://github.com/databricks/databricks-agent-skills), sincronizada por workflow e não editada à mão. Licença em [`LICENSE-databricks-agent-skills`](LICENSE-databricks-agent-skills) e atribuições em [`NOTICE-databricks-agent-skills`](NOTICE-databricks-agent-skills).

`databricks-python-dev` vem do antigo [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit) (v0.1.14), sob a mesma Databricks License.
