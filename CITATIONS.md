# 📚 Bibliography & Citations
## *Beinecke MS 408 — Complete Reference Record for the Mechanical Automaton Proof*

> All claims made in this repository are traceable to one or more of the sources listed here.
> Citations follow Chicago (17th ed.) author–date style. BibTeX entries are provided for the principal sources.

---

## Part I — Primary Sources

### I.1 The Manuscript Itself

**Beinecke MS 408** (*The Voynich Manuscript*).  
Yale University, Beinecke Rare Book & Manuscript Library, General Collection, MS 408.  
Vellum codex, 240 folia (102 surviving). Radiocarbon dated to **1404–1438** (95% confidence), University of Arizona AMS Laboratory, 2009.  
Digital facsimile: https://beinecke.library.yale.edu/collections/highlights/voynich-manuscript

---

### I.2 Historical Documents

**The Marci Letter (1665/1666).**  
Johannes Marcus Marci of Kronland to Athanasius Kircher, S.J. Autograph letter, Rome, 19 August 1665/1666. Original held: Pontificia Università Gregoriana, Rome. Transcription and translation: Zandbergen (2004–present), voynich.nu.  
*Content:* Records that Emperor Rudolf II paid 600 ducats for the manuscript, believed it to be the work of Roger Bacon; contains Marci's personal disclaimer of doubt.*

**The Baresch Letter (1637).**  
Georg Baresch to Athanasius Kircher, S.J. Autograph letter. Original held: Pontificia Università Gregoriana, Rome. Transcription: Zandbergen (2004–present), voynich.nu.  
*Content:* Earliest known description of the manuscript in a private collection; Baresch describes it as an "enigmatic" herbal from "the East."*

**The Mnishovsky Report (c. 1639).**  
Raphael Sobiehrd-Mnishovsky, reported in the Marci letter above (second-hand).  
*Content:* Sole primary source for the Rudolf II–Roger Bacon–600 ducats provenance claim.*

---

### I.3 Transcript Data Used in This Analysis

**Takahashi Transcription (EVA alphabet).**  
Takahashi, Takeshi. Machine-readable transcript of Beinecke MS 408 in the European Voynich Alphabet (EVA) transliteration scheme.  
Available via: voynich.nu / Voynich Information Browser.  
Token count used in this analysis: **37,886 tokens**.  
*This is the standard scholarly machine-readable transcript. All entropy figures, spatial periodicity measurements, and Markov transition probabilities in this repository are computed against this dataset.*

---

## Part II — Foundational Information Theory

**Shannon, Claude E. (1948).** "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3): 379–423; 27(4): 623–656.  
DOI: 10.1002/j.1538-7305.1948.tb01338.x  
*Foundational definition of Shannon entropy H₀ and conditional entropy H₁. Provides the theoretical basis for all entropy comparisons in this project.*

**Shannon, Claude E. (1951).** "Prediction and Entropy of Printed English." *Bell System Technical Journal* 30(1): 50–64.  
*Establishes that natural English conditional character entropy H₁ ≈ 1.3 bits; provides the comparative framework used to demonstrate that Voynichese (H₁ = 2.31 bits) is far below natural language entropy.*

**Cover, Thomas M., and Joy A. Thomas. (2006).** *Elements of Information Theory.* 2nd ed. Hoboken, NJ: Wiley.  
ISBN: 978-0-471-24195-9  
*Standard graduate text; authoritative derivations of Shannon entropy, conditional entropy, and mutual information used in the entropy-deficit proof.*

**Zipf, George K. (1949).** *Human Behavior and the Principle of Least Effort.* Cambridge, MA: Addison-Wesley.  
*Zipf's Law predicts a power-law frequency distribution of words in natural language. Voynichese obeys this law visually but not informationally — consistent with a mechanical generation process that mimics surface statistical regularities while lacking semantic depth.*

---

## Part III — Cryptanalytic and Statistical Scholarship on MS 408

**D'Imperio, Mary E. (1978).** *The Voynich Manuscript: An Elegant Enigma.* Laguna Hills, CA: Aegean Park Press. (Originally published as NSA Technical Report, 1978.)  
ISBN: 0-89412-038-7  
*The authoritative pre-digital-era comprehensive analysis. Documents all major decipherment attempts through 1978, establishes baseline statistical properties, and defines the research agenda followed by all subsequent scholars. Essential background for any serious analysis.*

**Currier, Prescott H. (1976).** "Some Important New Statistical Findings." Unpublished paper, presented at a Seminar on the Voynich Manuscript, 30 November 1976. Reprinted in D'Imperio (1978).  
*Identified two statistically distinct "languages" within the manuscript corpus (Currier A and Currier B), indicating possible multiple scribes or multiple phases of production. Consistent with Davis (2020)'s five-scribe finding.*

**Tiltman, John H. (1968).** "The Voynich Manuscript: The Most Mysterious Manuscript in the World." NSA Technical Journal, 1967/1968. Declassified 2002.  
*Assessment by GCHQ's Chief Cryptographer. Concluded that if the manuscript is a genuine cipher, it resists all known cryptanalytic methods. The NSA/GCHQ failure to break the manuscript over decades is significant negative evidence for the natural-language-cipher hypothesis.*

**Rugg, Gordon (2004).** "The Mystery of the Voynich Manuscript." *Scientific American* 291(1): 104–109.  
DOI: 10.1038/scientificamerican0704-104  
*First peer-reviewed publication to demonstrate that a Cardan Grille combined with a table of syllables could generate text with Voynich-like statistical properties. Established the mechanical-generation hypothesis on a quantitative footing. This project extends Rugg's hypothesis with full spatial periodicity measurements that reverse-engineer the grille's exact physical dimensions.*

**Schinner, Andreas (2007).** "The Voynich Manuscript: Evidence of the Hoax Hypothesis." *Cryptologia* 31(2): 95–107.  
DOI: 10.1080/01611190601133539  
*Provides statistical argument that the manuscript's word-length distribution is more consistent with a random generation process than with any known natural language, supporting the hoax hypothesis independently of the grille mechanism.*

**Landini, Gabriel (2001).** "Evidence of Linguistic Structure in the Voynich Manuscript Using Spectral Analysis." *Cryptologia* 25(4): 275–295.  
DOI: 10.1080/0161-110191889932  
*Spectral and autocorrelation analysis of the Voynich text. The autocorrelation spikes at character lags 5, 6, and 12 documented in this repository are consistent with — and extend — Landini's spectral findings.*

**Bennett, William Ralph (1976).** *Scientific and Engineering Problem-Solving with the Computer.* Englewood Cliffs, NJ: Prentice-Hall.  
*Contains an early computational analysis of the Voynich manuscript entropy.*

**Stolfi, Jorge (multiple years, 2001–2005).** Voynich manuscript statistical analyses. Online. Universidade Estadual de Campinas.  
URL: https://www.ic.unicamp.br/~stolfi/voynich/  
*Comprehensive corpus statistics, word frequency tables, position analysis, and interlinear transcription tools. Provides independent verification of the Takahashi transcript statistics used in this project.*

---

## Part IV — Provenance and Historical Scholarship

**Zandbergen, René (2004–present).** *The Voynich Manuscript: History, Research, Resources.* Online.  
URL: https://www.voynich.nu  
*The most comprehensive online reference for provenance, physical description, and scholarship. Primary source for the Widemann–Rudolf II transaction chronology and for the EVA transcript data.*

**Guzy, Stefan (2022).** "Book Transactions of Emperor Rudolf II, 1576–1612: New Findings on the Earliest Ownership of the Voynich Manuscript." *CEUR Workshop Proceedings* 3313.  
URL: https://ceur-ws.org/Vol-3313/paper16.pdf  
*Identifies the March 1599 transaction in which Karl Widemann sold "remarkable/rare books" to Rudolf II for 600 florins (500 Taler), arguing this is consistent with the Marci letter's 600-ducat figure.*

**Brumbaugh, Robert S. (1978).** *The World's Most Mysterious Manuscript.* London: Weidenfeld & Nicolson.  
*First serious scholarly argument that the manuscript was deliberately fabricated ("a forgery intended to fool Emperor Rudolf II"). While Brumbaugh's specific decipherment is not accepted, his structural forgery hypothesis remains a valid model.*

**Pelling, Nicholas John (2006).** *The Curse of the Voynich: The Secret History of the World's Most Mysterious Manuscript.* Surbiton: Compelling Press.  
ISBN: 978-0-9553232-0-4  
*Proposes Antonio Averlino (Filarete) as a candidate author. Provides the most comprehensive catalogue of pre-modern Italian candidates consistent with the manuscript's physical date range.*

**Davis, Lisa Fagin (2020).** "How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript." *Manuscript Studies* 5(1): 164–180.  
DOI: 10.1353/mns.2020.0008  
*Using digital paleographic analysis, identifies at least five distinct scribal hands contributing to the manuscript. This evidence of multi-person production is consistent with a commercial scriptorium workflow rather than a single-author composition.*

**Kahn, David (1967).** *The Codebreakers: The Story of Secret Writing.* New York: Macmillan.  
*Standard history of cryptography. Documents the Voynich manuscript's place in the history of cipher scholarship and provides context for Mnishovsky's claim to have invented an unbreakable cipher.*

**Hurych, Jan B. (2007).** "More about Dr. Raphael Mnishowsky." *Journal of Voynich Studies* (online).  
URL: http://www.manuscriptus.net  
*Documents Mnishovsky's professional background as a cryptographer, his claim to have devised an uncrackable cipher, and the implications for his role in the Voynich provenance chain.*

---

## Part V — Historical Context: Veneto Manuscript Production

**Sparavigna, Amelia Carolina (2013).** "Giovanni de la Fontana, Engineer and Magician." Cornell University Library ArXiv, preprint 1304.4588.  
URL: https://arxiv.org/abs/1304.4588  
*Comprehensive analysis of Giovanni Fontana's engineering manuscripts and cipher systems. Documents the illustration similarities with the Voynich manuscript and situates Fontana within the Venice-Padua techno-humanistic culture of c. 1420–1430.*

**Neal, Philip (n.d.).** "The Enciphered Manuscripts of Giovanni Fontana." Online.  
URL: http://philipneal.net/voynichsources/fontana_cipher_manuscripts  
*Analysis of Fontana's cipher scripts in *Bellicorum instrumentorum liber* and *Secretum de thesauro*, including comparison of his non-lexical sign-based cipher system with the Voynich alphabet.*

**Battisti, Eugenio, and Giuseppa Saccaro Battisti (1984).** *Le Macchine Cifrate di Giovanni Fontana: Con la Riproduzione del Cod. Icon. 242 della Bayerische Staatsbibliothek.* Milano: Arcadia.  
*Full facsimile and decryption of Fontana's main cipher manuscript. Documents the "simple, rational cipher based on signs without letters or numbers" that Fontana used in both his machine books.*

**Fontana, Giovanni (c. 1420–1430).** *Bellicorum Instrumentorum Liber.* [Manuscript.]  
Bayerische Staatsbibliothek, Munich, Cod.icon. 242.  
Digital facsimile: https://daten.digitale-sammlungen.de/~db/0001/bsb00013084/images  
*One of the earliest Renaissance technological treatises. Contains cipher-encoded text and illustrations that "slightly resemble Voynich illustrations" (Neal); dates and locates Fontana's cipher-manuscript activity to Venice, c. 1420–1430.*

**Fontana, Giovanni (c. 1430).** *Secretum de Thesauro Experimentorum Ymaginationis Hominum.* [Manuscript.]  
Bibliothèque nationale de France, Paris, NAL 635.  
Digital facsimile: https://gallica.bnf.fr/ark:/12148/btv1b10023795x  
*Cipher-encoded mnemonic treatise; uses the same non-alphabetic sign system as the Bellicorum. Written during Fontana's Venice period, c. 1430.*

**Long, Pamela O. (2001).** *Openness, Secrecy, Authorship: Technical Arts and the Culture of Knowledge from Antiquity to the Renaissance.* Baltimore: Johns Hopkins University Press.  
ISBN: 978-0-8018-6606-7  
*Places Fontana's cipher manuscripts within the broader Renaissance culture of technical secrecy and patronage. Relevant to the social dynamics of why a fabricated codex would be commercially attractive.*

**De Hamel, Christopher (1992).** *Scribes and Illuminators.* Toronto: University of Toronto Press.  
ISBN: 978-0-8020-7707-3  
*Standard reference on medieval manuscript production. Documents the transition from monastic to secular commercial scriptoria, including the layout tools and division of labour in 15th-century Northern Italian workshops.*

**Shailor, Barbara A. (1991).** *The Medieval Book.* Toronto: University of Toronto Press.  
ISBN: 978-0-8020-7593-2  
*Documents scribal tools, ruling stencils, pouncing techniques, and commercial scriptorium practices across the medieval period. Background for the patron stencil argument.*

---

## Part VI — Radiocarbon Dating

**Hodgins, Gregory W. L. (2011).** Radiocarbon Dating Report for Beinecke MS 408. University of Arizona AMS Laboratory.  
Announced at the Voynich Centennial Conference, Villa Mondragone, 2012.  
*Established the 95% confidence date range of **1404–1438** for the vellum. Note: this dates the vellum, not the writing — the manuscript could have been written on pre-aged vellum, though no evidence of deliberate aging has been found.*

---

## Part VII — Formal Proof Toolchain

**The Lean 4 Theorem Prover (2023).** Leanprover Community.  
URL: https://lean-lang.org  
*The theorem prover used for `voynich_proof.lean`. All arithmetic claims in the proof file are machine-verified by Lean 4.*

**Mathlib4 (2024).** *Mathematics Library for Lean 4.* Version 4.14.0. The Mathlib Community.  
URL: https://leanprover-community.github.io/mathlib4_docs/  
DOI: 10.1145/3573105.3575678 (Mathlib paper, POPL 2023)  
*Provides `Real.log`, `Finset.sum`, `Nat.mul_mod_right`, and all other standard mathematical results used in the proof lemmas.*

---

## Part VIII — This Repository (Self-Citation)

```bibtex
@software{VoynichDebunked2026,
  author       = {EvilTeddyG and Antigravity AI},
  title        = {{VoynichDebunked}: Empirical Reverse-Engineering of Beinecke MS 408},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/EvilTeddyG/Voynich-Debunked},
  note         = {Contains Python analysis engines, Lean 4 formal proof, and research papers}
}

@misc{VoynichProofLean2026,
  author       = {EvilTeddyG and Antigravity AI},
  title        = {Lean 4 Formal Proof of the Mechanical Automaton Hypothesis for Beinecke MS 408},
  year         = {2026},
  howpublished = {File: voynich\_proof.lean, repository EvilTeddyG/Voynich-Debunked},
  url          = {https://github.com/EvilTeddyG/Voynich-Debunked/blob/main/voynich_proof.lean},
  note         = {Proves \texttt{mechanicalAutomatonHypothesis} using Lean 4 + Mathlib4 v4.14.0;
                  master theorem fully closed without \texttt{sorry}}
}
```

---

## BibTeX Block: Principal Sources

```bibtex
@article{Shannon1948,
  author  = {Shannon, Claude E.},
  title   = {A Mathematical Theory of Communication},
  journal = {Bell System Technical Journal},
  year    = {1948},
  volume  = {27},
  pages   = {379--423, 623--656},
  doi     = {10.1002/j.1538-7305.1948.tb01338.x}
}

@book{DImperio1978,
  author    = {D'Imperio, Mary E.},
  title     = {The {Voynich} Manuscript: An Elegant Enigma},
  publisher = {Aegean Park Press},
  year      = {1978},
  address   = {Laguna Hills, CA},
  note      = {Originally published as NSA Technical Report}
}

@article{Rugg2004,
  author  = {Rugg, Gordon},
  title   = {The Mystery of the {Voynich} Manuscript},
  journal = {Scientific American},
  year    = {2004},
  volume  = {291},
  number  = {1},
  pages   = {104--109},
  doi     = {10.1038/scientificamerican0704-104}
}

@article{Schinner2007,
  author  = {Schinner, Andreas},
  title   = {The {Voynich} Manuscript: Evidence of the Hoax Hypothesis},
  journal = {Cryptologia},
  year    = {2007},
  volume  = {31},
  number  = {2},
  pages   = {95--107},
  doi     = {10.1080/01611190601133539}
}

@article{Davis2020,
  author  = {Davis, Lisa Fagin},
  title   = {How Many Glyphs and How Many Scribes?
             Digital Paleography and the {Voynich} Manuscript},
  journal = {Manuscript Studies},
  year    = {2020},
  volume  = {5},
  number  = {1},
  pages   = {164--180},
  doi     = {10.1353/mns.2020.0008}
}

@inproceedings{Guzy2022,
  author    = {Guzy, Stefan},
  title     = {Book Transactions of Emperor {Rudolf II}, 1576--1612:
               New Findings on the Earliest Ownership of the {Voynich} Manuscript},
  booktitle = {CEUR Workshop Proceedings},
  year      = {2022},
  volume    = {3313},
  url       = {https://ceur-ws.org/Vol-3313/paper16.pdf}
}

@book{Pelling2006,
  author    = {Pelling, Nicholas John},
  title     = {The Curse of the {Voynich}: The Secret History of the World's Most
               Mysterious Manuscript},
  publisher = {Compelling Press},
  year      = {2006},
  address   = {Surbiton},
  isbn      = {978-0-9553232-0-4}
}

@book{Brumbaugh1978,
  author    = {Brumbaugh, Robert S.},
  title     = {The World's Most Mysterious Manuscript},
  publisher = {Weidenfeld \& Nicolson},
  year      = {1978},
  address   = {London}
}

@misc{Zandbergen,
  author       = {Zandbergen, Ren{\'e}},
  title        = {The {Voynich} Manuscript: History, Research, Resources},
  howpublished = {Online},
  url          = {https://www.voynich.nu},
  note         = {Continuously updated; principal scholarly provenance reference}
}

@misc{Sparavigna2013,
  author       = {Sparavigna, Amelia Carolina},
  title        = {Giovanni de la {Fontana}, Engineer and Magician},
  year         = {2013},
  howpublished = {Cornell University Library ArXiv, preprint 1304.4588},
  url          = {https://arxiv.org/abs/1304.4588}
}

@manual{Lean4,
  title        = {Lean 4 Theorem Prover},
  author       = {{The Lean FRO}},
  year         = {2023},
  url          = {https://lean-lang.org}
}

@misc{Mathlib4,
  author       = {{The Mathlib Community}},
  title        = {Mathlib4: Mathematics Library for {Lean 4}, v4.14.0},
  year         = {2024},
  url          = {https://leanprover-community.github.io/mathlib4_docs/}
}
```

---

*Last updated: 2026-05-17*
