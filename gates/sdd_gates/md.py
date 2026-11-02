"""md.py — leitura dos artefatos SDD em markdown, compartilhada pelos gates.

Os gates (define e os que vierem) leem os mesmos artefatos do mesmo
jeito: seções por título, tabelas, a linha de aprovação. Se cada gate tivesse a
sua cópia dessas regras, um dia um exigiria o que o outro não lê. Por isso elas
moram aqui.

Python puro (só biblioteca padrão). Nunca lê o código do projeto, só markdown.
"""

import re
import unicodedata

# `**Aprovado**: 2026-11-02 — usuário: "pode seguir"` (aceita - ou — e aspas retas ou curvas)
APROVACAO_RE = re.compile(
    r'\*\*Aprovado\*\*:\s*(\d{4}-\d{2}-\d{2})\s*[—–-]\s*usu[aá]rio:\s*["“](.+?)["”]'
)
PLACEHOLDER_RE = re.compile(r"\{[^{}\n]{1,80}\}")


def normaliza(texto):
    """Minúsculas, sem acento e sem espaço extra — para comparar títulos e nomes."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sem_acento).strip().lower()


def sem_blocos_de_codigo(linhas):
    """Troca o conteúdo de blocos ``` por linhas vazias (mantém a numeração)."""
    saida, dentro = [], False
    for linha in linhas:
        if linha.lstrip().startswith("```"):
            dentro = not dentro
            saida.append("")
            continue
        saida.append("" if dentro else linha)
    return saida


def sem_comentarios_html(linhas):
    """Remove comentários <!-- ... --> (instruções do template para quem preenche)."""
    texto = "\n".join(linhas)
    texto = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)
    return texto.split("\n")


def prepara(texto):
    """Linhas prontas para os gates: sem blocos de código e sem comentários HTML."""
    return sem_comentarios_html(sem_blocos_de_codigo(texto.splitlines()))


def nivel_titulo(linha):
    m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", linha)
    return (len(m.group(1)), m.group(2)) if m else (0, None)


def secao(linhas, titulo, nivel=None):
    """Linhas de uma seção (sem o título), até o próximo título de nível igual ou maior.

    `titulo` casa com o texto inteiro do título, normalizado, ou com o título
    seguido de um complemento entre parênteses: "Diferenças em relação à fonte"
    casa "Diferenças em relação à fonte (opcional)", mas "Requisitos" não casa
    "Requisitos implícitos de dados". Devolve None se a seção não existe.
    """
    alvo = normaliza(titulo)
    for i, linha in enumerate(linhas):
        n, texto = nivel_titulo(linha)
        t = normaliza(texto) if texto else ""
        if n and (nivel is None or n == nivel) and (t == alvo or t.startswith(alvo + " (")):
            fim = len(linhas)
            for j in range(i + 1, len(linhas)):
                m, _ = nivel_titulo(linhas[j])
                if m and m <= n:
                    fim = j
                    break
            return linhas[i + 1:fim]
    return None


def celulas(linha):
    """Células de uma linha de tabela markdown; None se não for linha de tabela."""
    s = linha.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    partes = re.split(r"(?<!\\)\|", s[1:-1])
    return [p.strip() for p in partes]


def eh_separador(cel):
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cel if c) and any(cel)


def tabelas(linhas):
    """Tabelas de um trecho: lista de (cabeçalho normalizado, linhas de dados)."""
    resultado, i = [], 0
    while i < len(linhas):
        cab = celulas(linhas[i])
        sep = celulas(linhas[i + 1]) if i + 1 < len(linhas) else None
        if cab and sep and eh_separador(sep):
            dados, j = [], i + 2
            while j < len(linhas) and celulas(linhas[j]) is not None:
                dados.append(celulas(linhas[j]))
                j += 1
            resultado.append(([normaliza(c) for c in cab], dados))
            i = j
        else:
            i += 1
    return resultado


def coluna(cabecalho, nome):
    """Índice da coluna cujo título começa com `nome` (normalizado); None se não houver."""
    alvo = normaliza(nome)
    for i, c in enumerate(cabecalho):
        if c.startswith(alvo):
            return i
    return None


def vazia(celula):
    """Célula sem conteúdo útil: vazia, só traço, ou placeholder do template."""
    c = (celula or "").strip()
    return c in ("", "-", "—", "...") or bool(PLACEHOLDER_RE.fullmatch(c))


def aprovacoes(linhas):
    """Lista de (data, palavras do usuário) das linhas de aprovação."""
    return [m.groups() for linha in linhas for m in [APROVACAO_RE.search(linha)] if m]


def placeholders(linhas):
    """Números de linha (1-based) que ainda têm {placeholder} do template."""
    return [i + 1 for i, linha in enumerate(linhas) if PLACEHOLDER_RE.search(linha)]


class Relatorio:
    """Junta erros e avisos e decide o código de saída (0 ok, 1 falhou)."""

    def __init__(self, nome):
        self.nome, self.erros, self.avisos = nome, [], []

    def erro(self, msg):
        self.erros.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)

    def imprime_e_sai(self, estrito=False):
        for msg in self.erros:
            print(f"  ERRO   {msg}")
        for msg in self.avisos:
            print(f"  AVISO  {msg}")
        falhou = bool(self.erros) or (estrito and bool(self.avisos))
        if falhou:
            print(f"\n{self.nome}: FALHOU — {len(self.erros)} erro(s), {len(self.avisos)} aviso(s). Corrija e rode de novo.")
        else:
            print(f"{self.nome}: OK — {len(self.avisos)} aviso(s)")
        return 1 if falhou else 0
