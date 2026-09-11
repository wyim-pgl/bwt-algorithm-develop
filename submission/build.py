#!/usr/bin/env python3
"""Build author-review PDFs/DOCX with installed Pandoc and XeLaTeX.

Run from the repository root; no network access or benchmark execution.
The main PDF uses TeX Live's OUP authoring class. The supplement uses a
single-column landscape layout to keep all original wide tables readable.
"""
import re
import subprocess
import shutil
import sys
from pathlib import Path

out = Path('submission/build')
out.mkdir(parents=True, exist_ok=True)

def latex(text):
    return subprocess.run(['pandoc', '-f', 'markdown', '-t', 'latex'],
                          input=text, text=True, check=True, capture_output=True).stdout

text = Path('manuscript.md').read_text()
front, rest = text.split('## Abstract\n', 1)
abstract, rest = rest.split('## 1 Introduction', 1)
body, legends = ('## 1 Introduction' + rest).split('## Figure legends', 1)
assert front.startswith('# ')
title = front.splitlines()[0][2:]
figures = []
for image, number, caption, alt in re.findall(
        r'!\[[^\]]*\]\(([^)]+)\)\s+\*\*Fig\. (\d)\.\*\* ([^\n]+)\s+\*\*Alt text:\*\* ([^\n]+)', legends):
    pdf = Path(image).with_suffix('.pdf')
    assert pdf.is_file(), pdf
    figures.append(r'\begin{figure*}[t]\centering' + '\n' +
                   r'\includegraphics[width=\textwidth]{' + str(pdf) + '}\n' +
                   r'\caption{' + latex(caption).strip() + '}\n' +
                   # Journal figure-accessibility text, printed directly below the legend.
                   r'{\footnotesize\emph{Alt text:} ' + latex(alt).strip() + '}\n' +
                   r'\label{fig:' + number + '}\n' + r'\end{figure*}')
assert len(figures) == 2
header = r'''\documentclass[unnumsec,webpdf,contemporary,large,namedate]{oup-authoring-template}
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{refcount,lastpage}
\usepackage{newunicodechar}
\newunicodechar{≤}{\ensuremath{\leq}}
\newunicodechar{≥}{\ensuremath{\geq}}
% Newer class releases (v1.5, 2026) dropped \authormark; keep it harmless.
\providecommand{\authormark}[1]{}
% Do not print the template's false "Published by OUP" copyright footer.
\makeatletter\let\ps@opening\ps@plain\makeatother
\begin{document}
\journaltitle{Bioinformatics --- author submission draft}
\DOI{}
\copyrightyear{2026}
\pubyear{2026}
\appnotes{Application Note}
\firstpage{1}
\lastpage{\getpagerefnumber{LastPage}}
\title[BWTandem]{TITLE}
\author[1]{Filip Ramazan}
\author[1,$\ast$]{Won C. Yim}
\authormark{Ramazan and Yim}
\address[1]{\orgdiv{Department of Biochemistry and Molecular Biology}, \orgname{University of Nevada, Reno}, \orgaddress{\state{NV}, \postcode{89557}, \country{USA}}}
\corresp[$\ast$]{Correspondence: \href{mailto:wyim@unr.edu}{wyim@unr.edu}}
\abstract{ABSTRACT}
\keywords{tandem repeats; FM-index; genome annotation; satellites}
\maketitle
'''.replace('TITLE', latex(title).strip()).replace('ABSTRACT', latex(abstract).strip().replace('\n\n', r'\\' + '\n'))
tex = out / 'manuscript.tex'
tex.write_text(header + latex(body) + '\n'.join(figures) + '\n\\end{document}\n')
for _ in range(2):
    subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                    '-output-directory=' + str(out), str(tex)], check=True)

# The full supplement retains the long source's tables and declarations.
# Group all seven images with their full external legends; identifiers are
# supplied by the approved display map, not Pandoc's automatic numbering.
supp = Path('supplementary.md').read_text()
pattern = r'!\[Supplementary Fig\. (S\d+)\]\(([^)]+)\)\s+(\*\*Supplementary Fig\. S\d+\.[^\n]+(?:\n(?!\n)[^\n]+)*)'
def structural_figure(match):
    number, image, caption = match.groups()
    height = '140mm' if number == 'S7' else '110mm'
    return ('\n```{=latex}\n' + r'\noindent\begin{minipage}{\linewidth}\centering' + '\n' +
            r'\includegraphics[height=' + height + r',width=0.95\linewidth,keepaspectratio]{' + image + '}\n' +
            r'\par\medskip\raggedright ' + latex(caption).strip() + '\n' +
            r'\end{minipage}' + '\n```\n')
supp, grouped = re.subn(pattern, structural_figure, supp)
assert grouped == 7
supp_input = out / 'supplementary-layout.md'
supp_input.write_text(supp)
subprocess.run(['pandoc', str(supp_input), '-f', 'markdown-implicit_figures',
                '-o', str(out / 'supplementary.pdf'),
                '--pdf-engine=xelatex', '-V', 'geometry:a4paper,landscape,margin=15mm',
                '-V', 'fontsize:10pt', '-V', 'mainfont:DejaVu Serif',
                '-V', 'monofont:DejaVu Sans Mono', '-V', 'colorlinks:true',
                '--include-in-header=submission/supplement-header.tex'], check=True)
for name in ('manuscript', 'supplementary'):
    word_source = Path(name + '.md')
    if name == 'supplementary':
        word_source = out / 'supplementary-word.md'
        word_text = Path('supplementary.md').read_text()
        word_text = word_text.replace('](submission/figures/fig5_array_structure.png)',
                                      '](submission/figures/fig5_array_structure.png){height=140mm}')
        word_source.write_text(word_text)
    subprocess.run(['pandoc', str(word_source), '-f', 'markdown-implicit_figures-smart',
                    '-o', str(out / (name + '.docx'))], check=True)
    # Preserve the plain Pandoc export for independent content/style comparison.
    shutil.copyfile(out / (name + '.docx'), out / (name + '-pandoc.docx'))
    subprocess.run([sys.executable, 'submission/lab-docx/lab_docx.py',
                    str(out / (name + '.docx')), '--species', 'Arabidopsis thaliana',
                    '--species', 'Zea mays'], check=True)
print('Built PDFs and DOCX in submission/build/. Inspect layout and warnings before release.')
