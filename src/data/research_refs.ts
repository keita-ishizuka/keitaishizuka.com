// References for the research page. Bibliographic data is language-neutral, so one list serves
// both locales. Every entry was checked against the .bib files of the corresponding paper.
export interface Ref {
  n: number;
  text: string;
  href?: string;
}

export const refs: Ref[] = [
  {
    n: 1,
    text: 'J. L. Massey, “Linear codes with complementary duals,” Discrete Math. 106–107 (1992) 337–342.',
    href: 'https://doi.org/10.1016/0012-365X(92)90563-U',
  },
  {
    n: 2,
    text: 'M. Baldi, M. Battagliola, R. El Mechri, P. Santini, R. Schiavoni and D. De Zuane, “SPECK: Signatures from permutation equivalence of codes and kernels,” Cryptology ePrint Archive, Paper 2025/923.',
    href: 'https://eprint.iacr.org/2025/923',
  },
  {
    n: 3,
    text: 'M. R. Albrecht, B. Benčina and R. W. F. Lai, “Hollow LWE: A new spin, unbounded updatable encryption from LWE and PCE,” EUROCRYPT 2025, LNCS 15608, 363–392.',
    href: 'https://eprint.iacr.org/2025/340',
  },
  {
    n: 4,
    text: 'C. Carlet and S. Guilley, “Complementary dual codes for counter-measures to side-channel attacks,” Adv. Math. Commun. 10 (2016) 131–150.',
    href: 'https://doi.org/10.3934/amc.2016.10.131',
  },
  {
    n: 5,
    text: 'N. Sendrier, “Finding the permutation between equivalent linear codes: The support splitting algorithm,” IEEE Trans. Inform. Theory 46 (2000) 1193–1203.',
    href: 'https://doi.org/10.1109/18.850662',
  },
  {
    n: 6,
    text: 'T. Brun, I. Devetak and M.-H. Hsieh, “Correcting quantum errors with entanglement,” Science 314 (2006) 436–439.',
    href: 'https://doi.org/10.1126/science.1131563',
  },
  {
    n: 7,
    text: 'M. M. Wilde and T. A. Brun, “Optimal entanglement formulas for entanglement-assisted quantum coding,” Phys. Rev. A 77 (2008) 064302.',
    href: 'https://doi.org/10.1103/PhysRevA.77.064302',
  },
  {
    n: 8,
    text: 'D. E. Taylor, The Geometry of the Classical Groups, Heldermann, Berlin, 1992.',
  },
  {
    n: 9,
    text: 'P. Diaconis and M. Shahshahani, “The subgroup algorithm for generating uniform random variables,” Probab. Engrg. Inform. Sci. 1 (1987) 15–32.',
    href: 'https://doi.org/10.1017/S0269964800000255',
  },
  {
    n: 10,
    text: 'M. R. Albrecht, B. Benčina and R. W. F. Lai, “Algorithms for sampling self-orthogonal and totally self-orthogonal codes in odd characteristic,” arXiv:2610.08664 (2026).',
    href: 'https://arxiv.org/abs/2610.08664',
  },
  {
    n: 11,
    text: 'E. Petrank and R. M. Roth, “Is code equivalence easy to decide?,” IEEE Trans. Inform. Theory 43 (1997) 1602–1604.',
    href: 'https://doi.org/10.1109/18.623157',
  },
  {
    n: 12,
    text: 'M. Bardet, A. Otmani and M. Saeed-Taha, “Permutation code equivalence is not harder than graph isomorphism when hulls are trivial,” ISIT 2019, 2464–2468.',
    href: 'https://doi.org/10.1109/ISIT.2019.8849855',
  },
  {
    n: 13,
    text: 'L. Babai, “Graph isomorphism in quasipolynomial time,” STOC 2016, 684–697.',
    href: 'https://doi.org/10.1145/2897518.2897542',
  },
  {
    n: 14,
    text: 'N. Sendrier and D. E. Simos, “How easy is code equivalence over Fq?,” WCC 2013, Bergen, Norway.',
    href: 'https://inria.hal.science/hal-00790861',
  },
  {
    n: 15,
    text: 'J. S. Leon, “Computing automorphism groups of error-correcting codes,” IEEE Trans. Inform. Theory 28 (1982) 496–511.',
    href: 'https://doi.org/10.1109/TIT.1982.1056498',
  },
];
