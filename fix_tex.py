import re

def fix_latex():
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Write the Abstract / Resumen
    old_abs = r"Acá pongo el resumen que lo pongo al final."
    new_abs = "Este artículo describe el diseño, selección de materiales y análisis mecánico de un conjunto reductor de engranajes cilíndricos rectos destinado a un sistema de banda transportadora industrial. El reductor acopla un motor trifásico de 15 kW a 1500 rpm, proporcionando una relación de transmisión de 1.63 para reducir la velocidad a aproximadamente 919 rpm e incrementar el par torsor de salida. Se detallan los cálculos cinemáticos y dinámicos, la verificación de los rodamientos de bolas según estándar DIN 625 y el análisis estructural estático y por fatiga del eje. Adicionalmente, se presenta el modelado CAD del mecanismo de transmisión y la justificación técnica de los materiales (acero 20MnCr5, C45 y AISI 316), garantizando especificaciones de durabilidad bajo carga continua."
    content = content.replace(old_abs, new_abs)

    # 2. Fix IEEE Citations (Converting APA to bracketed numeric)
    cites = {
        "(Tarancón, 2018)": "\\cite{tarancon2018}",
        "(AOX Actuator, s.f.)": "\\cite{aox}",
        "(López García et al., 2023)": "\\cite{lopez}",
        "(Conveyor Solution, s.f.)": "\\cite{conveyor}",
        "(Guomao, 2026)": "\\cite{guomao}",
        "(The Snell Group, s.f.)": "\\cite{snell}",
        "(SKF Group, 2018)": "\\cite{skf}"
    }
    for old, new in cites.items():
        content = content.replace(old, new)
        
    # 3. Convert Large Tables to Table* (spanning both IEEE columns)
    # Replaces first two instances of \begin{table}[htbp] with \begin{table*}[htbp]
    content = content.replace(r"\begin{table}[htbp]", r"\begin{table*}[htbp]", 2)
    content = content.replace(r"\end{table}", r"\end{table*}", 2)

    # 4. Longtable to tabularx (Longtable crashes IEEE format)
    old_longtable = r"""\begin{center}
\captionof{table}{Identificación de elementos del conjunto reductor}
\label{tab:elementos-conjunto-reductor}
\end{center}

\begin{longtable}{
    >{\centering\arraybackslash}p{0.8cm}
    >{\raggedright\arraybackslash}p{4.2cm}
    >{\centering\arraybackslash}p{2cm}
    >{\raggedright\arraybackslash}p{7cm}
}
\toprule
\textbf{N.º} & \textbf{Elemento} & \textbf{Cantidad} & \textbf{Función} \\
\midrule
\endfirsthead

\toprule
\textbf{N.º} & \textbf{Elemento} & \textbf{Cantidad} & \textbf{Función} \\
\midrule
\endhead

\bottomrule
\endfoot"""
    
    new_longtable = r"""\begin{table*}[htbp]
\centering
\caption{Identificación de elementos del conjunto reductor}
\label{tab:elementos-conjunto-reductor}
\begin{tabularx}{\textwidth}{
    >{\centering\arraybackslash}p{0.8cm}
    >{\raggedright\arraybackslash}p{4.2cm}
    >{\centering\arraybackslash}p{2cm}
    >{\raggedright\arraybackslash}X
}
\toprule
\textbf{N.º} & \textbf{Elemento} & \textbf{Cantidad} & \textbf{Función} \\
\midrule"""
    
    content = content.replace(old_longtable, new_longtable)
    content = content.replace(r"\end{longtable}", r"\end{tabularx}\vspace{10pt}\end{table*}")

    # 5. Fix column widths for inner tables
    content = content.replace(r"\begin{tabularx}{\textwidth}", r"\begin{tabularx}{\linewidth}")
    # but restore the ones that are in table* back to textwidth
    content = content.replace(r"\begin{tabularx}{\linewidth}{" + "\n" + r"    >{\raggedright\arraybackslash}X", r"\begin{tabularx}{\textwidth}{" + "\n" + r"    >{\raggedright\arraybackslash}X")

    # 6. Change all image sizes to span line width instead of huge textwidth scaling
    content = content.replace(r"width=0.55\textwidth", r"width=\linewidth")
    content = content.replace(r"width=0.65\textwidth", r"width=\linewidth")

    # 7. Add bibliography
    biblio = r"""
% ══════════════════════════════════════════════════════════════
%  REFERENCIAS
% ══════════════════════════════════════════════════════════════
\begin{thebibliography}{10}
\bibitem{tarancon2018} Tarancón, J. (2018). \textit{Conjunto reductor}.
\bibitem{aox} AOX Actuator. (s.f.). \textit{Relación de transmisión}.
\bibitem{lopez} López García et al. (2023). \textit{Sistemas de elevación}.
\bibitem{conveyor} Conveyor Solution. (s.f.). \textit{Bandas transportadoras}.
\bibitem{guomao} Guomao. (2026). \textit{Catálogo de reductores}.
\bibitem{snell} The Snell Group. (s.f.). \textit{Factores de servicio}.
\bibitem{skf} SKF Group. (2018). \textit{Rodamientos industriales}.
\end{thebibliography}
\end{document}
"""
    content = content.replace(r"\end{document}", biblio)

    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_latex()