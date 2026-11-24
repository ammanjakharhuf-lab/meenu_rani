#!/usr/bin/env python3
"""Build manuscript HTML, PDF and DOCX from manuscript/manuscript.md (stdlib only).

Source format (one block per blank-line-separated chunk):
  @@title Text            title          @@meta Text   front-matter line
  ## Heading / ### Sub    headings
  $$ latex $$ {#eq:id}    numbered display equation
  !fig[id](file.png) caption
  !table[id] caption      followed by '| a | b |' rows (first row = header)
  plain text              paragraph
Inline: $math$, **bold**, *italic*, [@key; @key] citations, @eq:id, @fig:id, @tab:id
Citations are numbered in order of first appearance; every reference must be cited.
"""
import base64
import html
import os
import re
import struct
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import texmath  # noqa: E402
from render import FONT_CSS, html_to_pdf  # noqa: E402

DOC_DIR = os.environ.get("DOC_DIR", "manuscript")
MS = os.path.join(ROOT, DOC_DIR)
SRC = os.path.join(MS, os.environ.get("DOC_SRC", "manuscript.md"))
OUT_BASE = os.environ.get("DOC_OUT", "manuscript")


# ------------------------------------------------------------------ parsing
def load_refs():
    refs = {}
    with open(os.path.join(MS, "references.txt")) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                k, v = line.split("|", 1)
                refs[k.strip()] = v.strip()
    return refs


def blocks():
    text = open(SRC).read()
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("<!--"):
            continue
        if chunk.startswith("@@title"):
            out.append(("title", chunk[7:].strip()))
        elif chunk.startswith("@@meta"):
            out.append(("meta", chunk[6:].strip()))
        elif chunk.startswith("### "):
            out.append(("h3", chunk[4:].strip()))
        elif chunk.startswith("## "):
            out.append(("h2", chunk[3:].strip()))
        elif chunk.startswith("$$"):
            m = re.match(r"\$\$(.*)\$\$\s*\{#(eq:[\w-]+)\}", chunk, re.S)
            if not m:
                raise ValueError("bad equation block: " + chunk[:60])
            out.append(("eq", m.group(1).strip(), m.group(2)))
        elif chunk.startswith("!fig["):
            m = re.match(r"!fig\[([\w-]+)\]\(([^)]+)\)\s*(.*)", chunk, re.S)
            out.append(("fig", "fig:" + m.group(1), m.group(2), " ".join(m.group(3).split())))
        elif chunk.startswith("!table["):
            lines = chunk.split("\n")
            m = re.match(r"!table\[([\w-]+)\]\s*(.*)", lines[0])
            cap = m.group(2)
            rows = []
            note = ""
            for ln in lines[1:]:
                ln = ln.strip()
                if ln.startswith("|"):
                    rows.append([c.strip() for c in ln.strip("|").split("|")])
                elif ln.startswith("note:"):
                    note = ln[5:].strip()
                else:
                    cap += " " + ln
            out.append(("table", "tab:" + m.group(1), cap.strip(), rows, note))
        elif chunk.startswith("@@refs"):
            out.append(("refs",))
        elif all(re.match(r"(\d+\.|-)\s", ln.strip()) for ln in chunk.split("\n")):
            items = [re.sub(r"^(\d+\.|-)\s+", "", ln.strip()) for ln in chunk.split("\n")]
            out.append(("list", "ol" if chunk[0].isdigit() else "ul", items))
        else:
            out.append(("p", " ".join(chunk.split())))
    return out


INLINE = re.compile(r"(\$[^$]+\$|\*\*[^*]+\*\*|\*[^*\s][^*]*\*|\[@[^\]]+\]|@(?:eq|fig|tab):[\w-]+)")


class Numbering:
    def __init__(self, blks, refs):
        self.refs = refs
        self.cite = {}
        self.label = {}
        neq = nfig = ntab = 0
        for b in blks:
            if b[0] == "eq":
                neq += 1
                self.label[b[2]] = neq
            elif b[0] == "fig":
                nfig += 1
                self.label[b[1]] = nfig
            elif b[0] == "table":
                ntab += 1
                self.label[b[1]] = ntab
        self.counts = (neq, nfig, ntab)
        # citations in document order (captions/tables included where they appear)
        for b in blks:
            for txt in self.texts(b):
                for m in re.finditer(r"\[@([^\]]+)\]", txt):
                    for k in re.split(r"\s*;\s*", m.group(1)):
                        k = k.lstrip("@").strip()
                        if k not in refs:
                            raise KeyError(f"unknown reference {k}")
                        if k not in self.cite:
                            self.cite[k] = len(self.cite) + 1
        missing = set(refs) - set(self.cite)
        if missing:
            raise ValueError(f"uncited references: {sorted(missing)}")

    @staticmethod
    def texts(b):
        if b[0] in ("p", "meta", "h2", "h3"):
            return [b[1]]
        if b[0] == "fig":
            return [b[3]]
        if b[0] == "table":
            return [b[2]] + [c for r in b[3] for c in r] + [b[4]]
        if b[0] == "list":
            return list(b[2])
        return []

    def cite_text(self, inner):
        nums = sorted(self.cite[k.lstrip("@").strip()] for k in re.split(r"\s*;\s*", inner))
        parts, i = [], 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            parts.append(str(nums[i]) if j == i else (f"{nums[i]},{nums[j]}" if j == i + 1 else f"{nums[i]}–{nums[j]}"))
            i = j + 1
        return "[" + ",".join(parts) + "]"

    def xref(self, tok):
        kind, _ = tok[1:].split(":", 1)
        n = self.label[tok[1:]]
        return {"eq": f"Eq. ({n})", "fig": f"Figure {n}", "tab": f"Table {n}"}[kind]


def inline_tokens(text, num):
    """Split text into (kind, value) tokens: text, bold, italic, math."""
    out = []
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(("text", text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith("$"):
            out.append(("math", tok[1:-1]))
        elif tok.startswith("**"):
            out.append(("bold", tok[2:-2]))
        elif tok.startswith("*"):
            out.append(("italic", tok[1:-1]))
        elif tok.startswith("[@"):
            out.append(("text", num.cite_text(tok[2:-1])))
        else:
            out.append(("text", num.xref(tok)))
        pos = m.end()
    if pos < len(text):
        out.append(("text", text[pos:]))
    return out


# ------------------------------------------------------------------ HTML
CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
body { font-family: 'DejaVu LGC Serif', serif; font-size: 10.6pt; line-height: 1.48; color: #111; max-width: 175mm; margin: auto; }
h1.title { font-size: 17pt; line-height: 1.25; text-align: center; margin: 0 0 8pt 0; }
p.meta { text-align: center; margin: 2pt 0; font-size: 10pt; }
h2 { font-size: 12.5pt; margin: 14pt 0 4pt 0; border-bottom: 0.6pt solid #999; padding-bottom: 2pt; }
h3 { font-size: 11pt; margin: 10pt 0 3pt 0; font-style: italic; }
p { text-align: justify; margin: 0 0 6pt 0; hyphens: auto; }
div.eq { display: flex; align-items: center; margin: 6pt 0; page-break-inside: avoid; }
div.eq math { flex: 1; }
div.eq span.n { width: 3.2em; text-align: right; }
math { font-family: 'DejaVu LGC Serif', serif; font-size: 1.02em; }
figure { margin: 10pt 0; page-break-inside: avoid; text-align: center; }
figure img { width: 100%; }
figcaption, .tcap { font-size: 9.4pt; text-align: justify; line-height: 1.38; margin-top: 4pt; }
table { border-collapse: collapse; width: 100%; font-size: 8.9pt; line-height: 1.3; margin: 2pt 0 4pt 0; }
th { border-top: 1pt solid #222; border-bottom: 0.6pt solid #222; padding: 3pt 4pt; text-align: left; vertical-align: bottom; }
td { padding: 2.2pt 4pt; vertical-align: top; border-bottom: 0.3pt solid #ddd; }
tr:last-child td { border-bottom: 1pt solid #222; }
div.table { margin: 10pt 0; page-break-inside: avoid; }
.tnote { font-size: 8.6pt; color: #333; margin-top: 2pt; text-align: justify; }
ul.body, ol.body { margin: 0 0 6pt 0; padding-left: 2em; text-align: justify; }
ul.body li, ol.body li { margin-bottom: 2pt; }
ol.refs { font-size: 9.2pt; padding-left: 2.2em; line-height: 1.38; }
ol.refs li { margin-bottom: 2pt; text-align: justify; }
"""


def html_inline(text, num):
    out = []
    for kind, v in inline_tokens(text, num):
        if kind == "text":
            out.append(html.escape(v, quote=False))
        elif kind == "bold":
            out.append(f"<b>{html_inline(v, num)}</b>")
        elif kind == "italic":
            out.append(f"<i>{html_inline(v, num)}</i>")
        else:
            out.append(texmath.to_mathml(v))
    return "".join(out)


def build_html(blks, num, refs, embed=True):
    o = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Manuscript</title><style>{FONT_CSS}{CSS}</style></head><body>"]
    for b in blks:
        k = b[0]
        if k == "title":
            o.append(f"<h1 class='title'>{html_inline(b[1], num)}</h1>")
        elif k == "meta":
            o.append(f"<p class='meta'>{html_inline(b[1], num)}</p>")
        elif k == "h2":
            o.append(f"<h2>{html_inline(b[1], num)}</h2>")
        elif k == "h3":
            o.append(f"<h3>{html_inline(b[1], num)}</h3>")
        elif k == "p":
            o.append(f"<p>{html_inline(b[1], num)}</p>")
        elif k == "eq":
            o.append(f"<div class='eq'>{texmath.to_mathml(b[1], True)}<span class='n'>({num.label[b[2]]})</span></div>")
        elif k == "fig":
            path = os.path.join(MS, b[2])
            src = ("data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()) if embed else b[2]
            o.append(f"<figure><img src='{src}'/><figcaption><b>Figure {num.label[b[1]]}.</b> {html_inline(b[3], num)}</figcaption></figure>")
        elif k == "table":
            _, lab, cap, rows, note = b
            t = [f"<div class='table'><div class='tcap'><b>Table {num.label[lab]}.</b> {html_inline(cap, num)}</div><table>"]
            t.append("<tr>" + "".join(f"<th>{html_inline(c, num)}</th>" for c in rows[0]) + "</tr>")
            for r in rows[1:]:
                t.append("<tr>" + "".join(f"<td>{html_inline(c, num)}</td>" for c in r) + "</tr>")
            t.append("</table>")
            if note:
                t.append(f"<div class='tnote'>{html_inline(note, num)}</div>")
            t.append("</div>")
            o.append("".join(t))
        elif k == "list":
            o.append(f"<{b[1]} class='body'>" + "".join(f"<li>{html_inline(it, num)}</li>" for it in b[2]) + f"</{b[1]}>")
        elif k == "refs":
            items = sorted(num.cite.items(), key=lambda kv: kv[1])
            o.append("<ol class='refs'>" + "".join(f"<li>{html_inline(refs[key], num)}</li>" for key, _ in items) + "</ol>")
    o.append("</body></html>")
    return "\n".join(o)


# ------------------------------------------------------------------ DOCX
NS = ("xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main' "
      "xmlns:m='http://schemas.openxmlformats.org/officeDocument/2006/math' "
      "xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' "
      "xmlns:wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing' "
      "xmlns:a='http://schemas.openxmlformats.org/drawingml/2006/main' "
      "xmlns:pic='http://schemas.openxmlformats.org/drawingml/2006/picture'")


def x(s):
    return html.escape(s, quote=True)


def wrun(text, bold=False, italic=False, size=None):
    rpr = ""
    if bold or italic or size:
        rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + (f"<w:sz w:val='{size}'/><w:szCs w:val='{size}'/>" if size else "") + "</w:rPr>"
    return f"<w:r>{rpr}<w:t xml:space='preserve'>{x(text)}</w:t></w:r>"


def docx_inline(text, num, bold=False, italic=False, size=None):
    out = []
    for kind, v in inline_tokens(text, num):
        if kind == "text":
            out.append(wrun(v, bold, italic, size))
        elif kind == "bold":
            out.append(docx_inline(v, num, True, italic, size))
        elif kind == "italic":
            out.append(docx_inline(v, num, bold, True, size))
        else:
            out.append(texmath.to_omml(v))
    return "".join(out)


def para(content, style=None, align=None, spacing_after=None, keep=False):
    ppr = ""
    parts = []
    if style:
        parts.append(f"<w:pStyle w:val='{style}'/>")
    if keep:
        parts.append("<w:keepNext/>")
    if spacing_after is not None:
        parts.append(f"<w:spacing w:after='{spacing_after}'/>")
    if align:
        parts.append(f"<w:jc w:val='{align}'/>")
    if parts:
        ppr = "<w:pPr>" + "".join(parts) + "</w:pPr>"
    return f"<w:p>{ppr}{content}</w:p>"


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def build_docx(blks, num, refs, out_path):
    body = []
    media = []
    rels = []
    pic_id = 0
    text_w_emu = int(6.5 * 914400)
    for b in blks:
        k = b[0]
        if k == "title":
            body.append(para(docx_inline(b[1], num), "Title", "center"))
        elif k == "meta":
            body.append(para(docx_inline(b[1], num, size=20), None, "center", 60))
        elif k == "h2":
            body.append(para(docx_inline(b[1], num), "Heading1", keep=True))
        elif k == "h3":
            body.append(para(docx_inline(b[1], num), "Heading2", keep=True))
        elif k == "p":
            body.append(para(docx_inline(b[1], num), None, "both"))
        elif k == "eq":
            n = num.label[b[2]]
            body.append("<w:p><w:pPr><w:tabs><w:tab w:val='center' w:pos='4680'/><w:tab w:val='right' w:pos='9360'/></w:tabs>"
                        "<w:spacing w:before='60' w:after='60'/></w:pPr><w:r><w:tab/></w:r>"
                        f"{texmath.to_omml(b[1])}<w:r><w:tab/><w:t>({n})</w:t></w:r></w:p>")
        elif k == "fig":
            pic_id += 1
            path = os.path.join(MS, b[2])
            w, h = png_size(path)
            cx = text_w_emu
            cy = int(cx * h / w)
            rid = f"rIdImg{pic_id}"
            media.append((f"media/image{pic_id}.png", path))
            rels.append(f"<Relationship Id='{rid}' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image' Target='media/image{pic_id}.png'/>")
            drawing = (f"<w:r><w:drawing><wp:inline distT='0' distB='0' distL='0' distR='0'><wp:extent cx='{cx}' cy='{cy}'/>"
                       f"<wp:docPr id='{pic_id}' name='Figure {pic_id}'/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect='1'/></wp:cNvGraphicFramePr>"
                       "<a:graphic><a:graphicData uri='http://schemas.openxmlformats.org/drawingml/2006/picture'><pic:pic>"
                       f"<pic:nvPicPr><pic:cNvPr id='{pic_id}' name='image{pic_id}.png'/><pic:cNvPicPr/></pic:nvPicPr>"
                       f"<pic:blipFill><a:blip r:embed='{rid}'/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
                       f"<pic:spPr><a:xfrm><a:off x='0' y='0'/><a:ext cx='{cx}' cy='{cy}'/></a:xfrm><a:prstGeom prst='rect'><a:avLst/></a:prstGeom></pic:spPr>"
                       "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>")
            body.append(para(drawing, None, "center", keep=True))
            body.append(para(wrun(f"Figure {num.label[b[1]]}. ", bold=True, size=19) + docx_inline(b[3], num, size=19), "Caption", "both"))
        elif k == "table":
            _, lab, cap, rows, note = b
            body.append(para(wrun(f"Table {num.label[lab]}. ", bold=True, size=19) + docx_inline(cap, num, size=19), "Caption", "both", keep=True))
            ncol = len(rows[0])
            grid = "".join(f"<w:gridCol w:w='{9360 // ncol}'/>" for _ in range(ncol))
            t = ["<w:tbl><w:tblPr><w:tblW w:w='5000' w:type='pct'/><w:tblBorders>"
                 "<w:top w:val='single' w:sz='8' w:color='000000'/><w:bottom w:val='single' w:sz='8' w:color='000000'/>"
                 "<w:insideH w:val='single' w:sz='2' w:color='BBBBBB'/></w:tblBorders>"
                 "<w:tblCellMar><w:left w:w='60' w:type='dxa'/><w:right w:w='60' w:type='dxa'/></w:tblCellMar></w:tblPr>"
                 f"<w:tblGrid>{grid}</w:tblGrid>"]
            for ri, r in enumerate(rows):
                cells = []
                for c in r:
                    tcpr = "<w:tcPr><w:tcBorders><w:bottom w:val='single' w:sz='6' w:color='000000'/></w:tcBorders></w:tcPr>" if ri == 0 else ""
                    cells.append(f"<w:tc>{tcpr}{para(docx_inline(c, num, bold=(ri == 0), size=17), None, None, 0)}</w:tc>")
                hdr = "<w:trPr><w:tblHeader/></w:trPr>" if ri == 0 else ""
                t.append(f"<w:tr>{hdr}{''.join(cells)}</w:tr>")
            t.append("</w:tbl>")
            body.append("".join(t))
            if note:
                body.append(para(docx_inline(note, num, size=16), None, "both"))
            else:
                body.append(para("", None, None, 120))
        elif k == "list":
            for i, it in enumerate(b[2]):
                mark = f"{i + 1}.\t" if b[1] == "ol" else "•\t"
                body.append("<w:p><w:pPr><w:ind w:left='454' w:hanging='284'/><w:jc w:val='both'/></w:pPr>"
                            + wrun(mark) + docx_inline(it, num) + "</w:p>")
        elif k == "refs":
            items = sorted(num.cite.items(), key=lambda kv: kv[1])
            for key, n in items:
                body.append("<w:p><w:pPr><w:pStyle w:val='Reference'/><w:ind w:left='454' w:hanging='454'/></w:pPr>"
                            + wrun(f"{n}.\t", size=19) + docx_inline(refs[key], num, size=19) + "</w:p>")
    sect = ("<w:sectPr><w:footerReference w:type='default' r:id='rIdFooter'/><w:pgSz w:w='11906' w:h='16838'/>"
            "<w:pgMar w:top='1134' w:right='1134' w:bottom='1134' w:left='1134' w:header='567' w:footer='567' w:gutter='0'/>"
            + ("<w:lnNumType w:countBy='1' w:restart='continuous'/>" if os.environ.get("DOC_LINENUM", "1") == "1" else "") + "</w:sectPr>")
    document = f"<?xml version='1.0' encoding='UTF-8' standalone='yes'?><w:document {NS}><w:body>{''.join(body)}{sect}</w:body></w:document>"
    styles = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:styles xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii='Times New Roman' w:hAnsi='Times New Roman' w:cs='Times New Roman' w:eastAsia='Times New Roman'/><w:sz w:val='22'/><w:szCs w:val='22'/><w:lang w:val='en-GB'/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after='120' w:line='300' w:lineRule='auto'/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type='paragraph' w:default='1' w:styleId='Normal'><w:name w:val='Normal'/><w:qFormat/></w:style>
<w:style w:type='paragraph' w:styleId='Title'><w:name w:val='Title'/><w:basedOn w:val='Normal'/><w:qFormat/><w:pPr><w:jc w:val='center'/><w:spacing w:after='200'/></w:pPr><w:rPr><w:b/><w:sz w:val='32'/><w:szCs w:val='32'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Heading1'><w:name w:val='heading 1'/><w:basedOn w:val='Normal'/><w:next w:val='Normal'/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before='280' w:after='100'/><w:outlineLvl w:val='0'/></w:pPr><w:rPr><w:b/><w:sz w:val='26'/><w:szCs w:val='26'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Heading2'><w:name w:val='heading 2'/><w:basedOn w:val='Normal'/><w:next w:val='Normal'/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before='200' w:after='80'/><w:outlineLvl w:val='1'/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val='23'/><w:szCs w:val='23'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Caption'><w:name w:val='caption'/><w:basedOn w:val='Normal'/><w:qFormat/><w:pPr><w:spacing w:before='60' w:after='200' w:line='260' w:lineRule='auto'/></w:pPr><w:rPr><w:sz w:val='19'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Reference'><w:name w:val='Reference'/><w:basedOn w:val='Normal'/><w:pPr><w:spacing w:after='60' w:line='260' w:lineRule='auto'/></w:pPr><w:rPr><w:sz w:val='19'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Footer'><w:name w:val='footer'/><w:basedOn w:val='Normal'/></w:style>
</w:styles>"""
    footer = (f"<?xml version='1.0' encoding='UTF-8' standalone='yes'?><w:ftr {NS}><w:p><w:pPr><w:pStyle w:val='Footer'/><w:jc w:val='center'/></w:pPr>"
              "<w:r><w:fldChar w:fldCharType='begin'/></w:r><w:r><w:instrText xml:space='preserve'> PAGE </w:instrText></w:r>"
              "<w:r><w:fldChar w:fldCharType='separate'/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType='end'/></w:r></w:p></w:ftr>")
    ctypes = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>"
              "<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>"
              "<Default Extension='xml' ContentType='application/xml'/><Default Extension='png' ContentType='image/png'/>"
              "<Override PartName='/word/document.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'/>"
              "<Override PartName='/word/styles.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'/>"
              "<Override PartName='/word/footer1.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml'/>"
              "<Override PartName='/docProps/core.xml' ContentType='application/vnd.openxmlformats-package.core-properties+xml'/></Types>")
    root_rels = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>"
                 "<Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument' Target='word/document.xml'/>"
                 "<Relationship Id='rId2' Type='http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties' Target='docProps/core.xml'/></Relationships>")
    doc_rels = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>"
                "<Relationship Id='rIdStyles' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles' Target='styles.xml'/>"
                "<Relationship Id='rIdFooter' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer' Target='footer1.xml'/>"
                + "".join(rels) + "</Relationships>")
    title = next(b[1] for b in blks if b[0] == "title")
    core = ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><cp:coreProperties xmlns:cp='http://schemas.openxmlformats.org/package/2006/metadata/core-properties' "
            "xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:dcterms='http://purl.org/dc/terms/' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>"
            f"<dc:title>{x(title)}</dc:title><dc:creator>Manuscript draft</dc:creator></cp:coreProperties>")
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ctypes)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/footer1.xml", footer)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("docProps/core.xml", core)
        for name, path in media:
            z.write(path, "word/" + name)


# ------------------------------------------------------------------ stats
def word_count(blks):
    """Words in title, abstract and body text (excludes equations, tables, captions, references)."""
    n = 0
    for b in blks:
        txts = [b[1]] if b[0] in ("p", "h2", "h3", "title") else (list(b[2]) if b[0] == "list" else [])
        for t in txts:
            t = re.sub(r"\$[^$]+\$", " X ", t)
            t = re.sub(r"\[@[^\]]+\]", " ", t)
            n += len(re.findall(r"[A-Za-z0-9][\w'’\-–.%/×]*", t))
    return n


def main():
    refs = load_refs()
    blks = blocks()
    num = Numbering(blks, refs)
    out_html = os.path.join(MS, OUT_BASE + ".html")
    with open(out_html, "w") as f:
        f.write(build_html(blks, num, refs, embed=True))
    html_to_pdf(out_html, os.path.join(MS, OUT_BASE + ".pdf"))
    build_docx(blks, num, refs, os.path.join(MS, OUT_BASE + ".docx"))
    neq, nfig, ntab = num.counts
    print(f"equations={neq} figures={nfig} tables={ntab} references={len(num.cite)} words(body)={word_count(blks)}")
    order = sorted(num.cite.items(), key=lambda kv: kv[1])
    print("citation order:", ", ".join(k for k, _ in order))


if __name__ == "__main__":
    main()
