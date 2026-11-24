"""List technical / proper-noun words in the narration with how the voice (espeak) will pronounce them."""
import os, sys, re, glob, json, importlib.util, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(sys.argv[0])); sys.path[:0] = [HERE, os.path.join(HERE, 'lessons')]
words = collections.Counter(); caps = collections.Counter()
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    spec = importlib.util.spec_from_file_location('m', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for s in m.LESSON['slides']:
        says = [st['say'] for st in s['steps']] if s['t'] == 'wb' else (s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')])
        for say in says:
            for sent in re.split(r'(?<=[.?!])\s+', say or ''):
                toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", sent)
                for i, w in enumerate(toks):
                    words[w.lower()] += 1
                    if i > 0 and w[0].isupper(): caps[w] += 1
TECH = re.compile(r'(oid|oidal|ian$|or$|ance$|tive$|ics$|ism$|ase$|ode$|ium$|tron|phas|sin|cos|tan|log|eigen|matrix|vect|integr|deriv|differ|calc|polynom|asympt|hyst|induct|capac|imped|react|resist|transist|semicond|dop|junct|thresh|satur|ohm|volt|amp|watt|farad|henr|hertz|joule|coulomb|tesla|weber|newton|pascal|kelvin|radian|degree|binom|gauss|poisson|bayes|stochast|ergod|convol|laplace|fourier|nyquist|alias|quantiz|modul|demod|multiplex|decod|encod|regist|pipelin|cache|assoc|virtu|semaphor|mutex|deadlock|schedul|thread|kernel|syscall|normaliz|relation|tupl|query|amortiz|depreci|annuit|cmos|nmos|pmos|mosfet|bjt|verilog|vhdl|fpga|asic|synth|debounc|metastab|synchron|interrupt|volatile|pragma|cortex|haar|cascade|kinemat|torque|servo|lidar|pwm|uart|spi|i2c|gpio|adc|dac|nand|xor|karnaugh|boolean|morgan|mealy|moore|hamming|parity|checksum|crypto|cipher|nonce|hash|heap|dijkstra|trie|deque|enum|struct|const|ptr|alloc|iostream|cout|cin|endl|std|lambda|theta|omega|sigma|mu$|phi|psi|rho|epsilon|delta|nabla|del$|euler|newton|leibniz|riemann|taylor|maclaurin|cauchy|lagrange|hermit|jacobian|wronsk|thevenin|norton|kirchhoff|ampere|faraday|lenz|maxwell|gauss|coulomb|biot|savart|snell|doppler|huygens|bohr|planck|schrod|heisenberg|millikan|joule|hooke|kepler|galileo|bernoulli|pascal|archimed|bode|butterworth|chebyshev|nichols|routh|hurwitz|zener|schottky|darlington|miller|early|ebers|shockley|mead|conway|amdahl|moore|neumann|harvard|turing|boole|shannon|von)', re.I)
cand = sorted({w for w in words if len(w) >= 3 and TECH.search(w)} | {w.lower() for w in caps if caps[w] >= 1 and len(w) >= 4})
from kokoro_onnx.tokenizer import Tokenizer
T = Tokenizer()
print(len(words), 'distinct words;', len(cand), 'candidates')
for w in cand:
    print(f'{w:22s} {T.phonemize(w)}')
