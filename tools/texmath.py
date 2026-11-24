"""Tiny LaTeX-math subset parser that emits MathML (for HTML/PDF) and OMML (for Word).

Supported: letters, digits, operators, Greek letters, \\frac, ^, _, \\sqrt,
\\left( ... \\right), \\mathrm{}, \\text{}, \\bar/\\hat/\\tilde/\\dot, \\sum,
\\int, common relation and operator symbols, function names and spacing.
"""
import re
from xml.sax.saxutils import escape

GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε", "varepsilon": "ε", "zeta": "ζ",
    "eta": "η", "theta": "θ", "vartheta": "ϑ", "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν",
    "xi": "ξ", "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ", "varphi": "φ",
    "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ",
    "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}
SYMBOLS = {
    "partial": ("mo", "∂"), "nabla": ("mo", "∇"), "cdot": ("mo", "·"), "times": ("mo", "×"),
    "le": ("mo", "≤"), "leq": ("mo", "≤"), "ge": ("mo", "≥"), "geq": ("mo", "≥"), "approx": ("mo", "≈"),
    "infty": ("mn", "∞"), "to": ("mo", "→"), "leftarrow": ("mo", "←"), "rightarrow": ("mo", "→"), "Leftarrow": ("mo", "⇐"), "gets": ("mo", "←"), "in": ("mo", "∈"), "propto": ("mo", "∝"), "pm": ("mo", "±"),
    "ll": ("mo", "≪"), "gg": ("mo", "≫"), "sim": ("mo", "∼"), "neq": ("mo", "≠"), "mid": ("mo", "|"),
    "ldots": ("mo", "…"), "cdots": ("mo", "⋯"), "prime": ("mo", "′"), "sum": ("op", "∑"), "int": ("op", "∫"),
    "prod": ("op", "∏"), "equiv": ("mo", "≡"), "Rightarrow": ("mo", "⇒"), "mapsto": ("mo", "↦"),
    "lbrace": ("mo", "{"), "rbrace": ("mo", "}"), "{": ("mo", "{"), "}": ("mo", "}"), "|": ("mo", "‖"),
    "setminus": ("mo", "∖"), "cap": ("mo", "∩"), "cup": ("mo", "∪"), "forall": ("mo", "∀"), "circ": ("mo", "∘"),
    "langle": ("mo", "⟨"), "rangle": ("mo", "⟩"), "%": ("mo", "%"),
}
FUNCS = {"exp", "ln", "log", "max", "min", "inf", "sup", "sin", "cos", "tanh", "arg", "lim", "det", "sgn"}
ACCENTS = {"bar": "\u0304", "hat": "\u0302", "tilde": "\u0303", "dot": "\u0307", "overline": "\u0305"}
SPACES = {",": 0.17, ";": 0.28, "quad": 1.0, "qquad": 2.0, "!": 0.0, " ": 0.25}

TOKEN = re.compile(r"\\([A-Za-z]+|.)|(\d+(?:\.\d+)?)|([A-Za-z])|(\s+)|(.)", re.S)


def tokenize(s):
    out = []
    for m in TOKEN.finditer(s):
        cmd, num, let, ws, ch = m.groups()
        if cmd is not None:
            out.append(("cmd", cmd))
        elif num is not None:
            out.append(("num", num))
        elif let is not None:
            out.append(("let", let))
        elif ws is not None:
            continue
        else:
            out.append(("ch", ch))
    return out


class Parser:
    def __init__(self, s):
        self.t = tokenize(s)
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def next(self):
        tok = self.peek()
        self.i += 1
        return tok

    def parse(self):
        return ("row", self.seq(None))

    def seq(self, stop):
        items = []
        while True:
            tok = self.peek()
            if tok is None:
                break
            if stop == "}" and tok == ("ch", "}"):
                self.next()
                break
            if stop == "right" and tok == ("cmd", "right"):
                break
            atom = self.atom()
            if atom is None:
                continue
            items.append(self.scripts(atom))
        return items

    def group(self):
        tok = self.peek()
        if tok == ("ch", "{"):
            self.next()
            return ("row", self.seq("}"))
        atom = self.atom()
        return atom if atom is not None else ("row", [])

    def text_group(self):
        assert self.next() == ("ch", "{")
        depth, buf = 1, []
        # reconstruct raw text from tokens
        while True:
            tok = self.next()
            if tok is None:
                break
            kind, val = tok
            if tok == ("ch", "{"):
                depth += 1
            elif tok == ("ch", "}"):
                depth -= 1
                if depth == 0:
                    break
            if kind == "cmd":
                buf.append(GREEK.get(val, SYMBOLS.get(val, ("", val))[1] if val in SYMBOLS else (" " if val in SPACES else val)))
            else:
                buf.append(val)
        return "".join(buf)

    def scripts(self, base):
        sub = sup = None
        while True:
            tok = self.peek()
            if tok == ("ch", "_"):
                self.next()
                sub = self.group()
            elif tok == ("ch", "^"):
                self.next()
                sup = self.group()
            elif tok == ("ch", "'"):
                self.next()
                sup = ("mo", "′")
            else:
                break
        if sub is not None and sup is not None:
            return ("subsup", base, sub, sup)
        if sub is not None:
            return ("sub", base, sub)
        if sup is not None:
            return ("sup", base, sup)
        return base

    def atom(self):
        tok = self.next()
        kind, val = tok
        if kind == "num":
            return ("mn", val)
        if kind == "let":
            return ("mi", val, True)
        if kind == "ch":
            if val == "{":
                return ("row", self.seq("}"))
            if val in "+-=<>(),;:/[]|!.":
                return ("mo", {"-": "−"}.get(val, val))
            if val == "~":
                return ("space", 0.25)
            return ("mo", val)
        # commands
        if val in GREEK:
            return ("mi", GREEK[val], val[0].islower())
        if val in SYMBOLS:
            k, c = SYMBOLS[val]
            return ("op", c) if k == "op" else (k, c)
        if val in FUNCS:
            return ("fn", val)
        if val in SPACES:
            return ("space", SPACES[val])
        if val == "frac":
            num = self.group()
            den = self.group()
            return ("frac", num, den)
        if val == "sqrt":
            return ("sqrt", self.group())
        if val in ("mathrm", "text", "operatorname"):
            return ("text", self.text_group())
        if val in ("mathbf", "boldsymbol"):
            return ("bf", self.text_group())
        if val in ("mathit",):
            return ("mi", self.text_group(), True)
        if val in ACCENTS:
            return ("acc", ACCENTS[val], self.group())
        if val == "left":
            o = self.delim()
            body = self.seq("right")
            self.next()  # \right
            c = self.delim()
            return ("fence", o, c, ("row", body))
        if val in ("displaystyle", "limits"):
            return None
        raise ValueError(f"unsupported command \\{val}")

    def delim(self):
        tok = self.next()
        kind, val = tok
        if kind == "cmd":
            return {"{": "{", "}": "}", "|": "‖", "langle": "⟨", "rangle": "⟩", "lbrace": "{", "rbrace": "}"}.get(val, "")
        return "" if val == "." else val


def parse(s):
    return Parser(s).parse()


# ------------------------------------------------------------------ MathML
def mathml(node):
    t = node[0]
    if t == "row":
        return "<mrow>" + "".join(mathml(n) for n in node[1]) + "</mrow>"
    if t == "mi":
        style = "font-style:italic" if node[2] else "font-style:normal"
        return f"<mi mathvariant='normal' style='{style}'>{escape(node[1])}</mi>"
    if t == "mn":
        return f"<mn>{escape(node[1])}</mn>"
    if t == "bf":
        return f"<mi mathvariant='normal' style='font-style:normal;font-weight:bold'>{escape(node[1])}</mi>"
    if t == "mo":
        stretch = " stretchy='false'" if node[1] in "()[]|" else ""
        return f"<mo{stretch}>{escape(node[1])}</mo>"
    if t == "op":
        return f"<mo largeop='true'>{escape(node[1])}</mo>"
    if t == "fn":
        return f"<mi mathvariant='normal' style='font-style:normal'>{node[1]}</mi><mo>&#x2061;</mo>"
    if t == "text":
        return f"<mtext>{escape(node[1])}</mtext>"
    if t == "space":
        return f"<mspace width='{node[1]}em'/>"
    if t == "frac":
        return f"<mfrac>{mathml(node[1])}{mathml(node[2])}</mfrac>"
    if t == "sqrt":
        return f"<msqrt>{mathml(node[1])}</msqrt>"
    if t == "sub":
        return f"<msub>{mathml(node[1])}{mathml(node[2])}</msub>"
    if t == "sup":
        return f"<msup>{mathml(node[1])}{mathml(node[2])}</msup>"
    if t == "subsup":
        if node[1][0] == "op":
            return f"<munderover>{mathml(node[1])}{mathml(node[2])}{mathml(node[3])}</munderover>"
        return f"<msubsup>{mathml(node[1])}{mathml(node[2])}{mathml(node[3])}</msubsup>"
    if t == "acc":
        return f"<mover accent='true'>{mathml(node[2])}<mo>{node[1]}</mo></mover>"
    if t == "fence":
        o = f"<mo stretchy='true'>{escape(node[1])}</mo>" if node[1] else ""
        c = f"<mo stretchy='true'>{escape(node[2])}</mo>" if node[2] else ""
        return f"<mrow>{o}{mathml(node[3])}{c}</mrow>"
    raise ValueError(t)


def to_mathml(s, display=False):
    d = " display='block'" if display else ""
    return f"<math xmlns='http://www.w3.org/1998/Math/MathML'{d}>{mathml(parse(s))}</math>"


# ------------------------------------------------------------------ OMML
def _r(text, upright=False):
    rpr = "<m:rPr><m:sty m:val='p'/></m:rPr>" if upright else ""
    return f"<m:r>{rpr}<w:rPr><w:rFonts w:ascii='Cambria Math' w:hAnsi='Cambria Math'/></w:rPr><m:t xml:space='preserve'>{escape(text)}</m:t></m:r>"


def omml(node):
    t = node[0]
    if t == "row":
        return "".join(omml(n) for n in node[1])
    if t == "mi":
        return _r(node[1], upright=not node[2])
    if t in ("mn", "mo", "op"):
        return _r(node[1], upright=True)
    if t == "bf":
        return f"<m:r><m:rPr><m:sty m:val='b'/></m:rPr><m:t xml:space='preserve'>{escape(node[1])}</m:t></m:r>"
    if t == "fn":
        return _r(node[1], upright=True)
    if t == "text":
        return _r(node[1], upright=True)
    if t == "space":
        return _r("\u2009" if node[1] < 0.5 else "\u2003" * int(round(node[1])), upright=True) if node[1] > 0 else ""
    if t == "frac":
        return f"<m:f><m:num>{omml(node[1])}</m:num><m:den>{omml(node[2])}</m:den></m:f>"
    if t == "sqrt":
        return f"<m:rad><m:radPr><m:degHide m:val='1'/></m:radPr><m:deg/><m:e>{omml(node[1])}</m:e></m:rad>"
    if t == "sub":
        return f"<m:sSub><m:e>{omml(node[1])}</m:e><m:sub>{omml(node[2])}</m:sub></m:sSub>"
    if t == "sup":
        return f"<m:sSup><m:e>{omml(node[1])}</m:e><m:sup>{omml(node[2])}</m:sup></m:sSup>"
    if t == "subsup":
        if node[1][0] == "op":
            return (f"<m:nary><m:naryPr><m:chr m:val='{node[1][1]}'/><m:limLoc m:val='undOvr'/></m:naryPr>"
                    f"<m:sub>{omml(node[2])}</m:sub><m:sup>{omml(node[3])}</m:sup><m:e></m:e></m:nary>")
        return f"<m:sSubSup><m:e>{omml(node[1])}</m:e><m:sub>{omml(node[2])}</m:sub><m:sup>{omml(node[3])}</m:sup></m:sSubSup>"
    if t == "acc":
        return f"<m:acc><m:accPr><m:chr m:val='{node[1]}'/></m:accPr><m:e>{omml(node[2])}</m:e></m:acc>"
    if t == "fence":
        return (f"<m:d><m:dPr><m:begChr m:val='{escape(node[1])}'/><m:endChr m:val='{escape(node[2])}'/></m:dPr>"
                f"<m:e>{omml(node[3])}</m:e></m:d>")
    raise ValueError(t)


def to_omml(s):
    return f"<m:oMath>{omml(parse(s))}</m:oMath>"


if __name__ == "__main__":
    test = r"\frac{\partial c}{\partial t} = \nabla\cdot\left(D_c T \nabla c\right) + \alpha_c f(\sigma)(1-T)c - \sum_{k=1}^{N} x_k^{2} + \mathrm{max} \bar{m}"
    print(to_mathml(test, True)[:300])
    print(to_omml(test)[:300])
