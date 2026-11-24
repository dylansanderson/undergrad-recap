import os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(sys.argv[0])); sys.path.insert(0, HERE)
import tts, soundfile as sf
k = tts._kokoro()
for s in ["A phasor turns a sinusoidal signal into a single complex number.",
          "Thevenin's theorem and Kirchhoff's laws come from the same idea.",
          "The MOSFET drives the GPIO pin, and XOR gives the parity.",
          "Use your arm to point, but the ARM core handles the SysTick interrupt.",
          "No dictionary words in this sentence at all."]:
    sp = tts.lex_spans(s)
    print(s, '\n   ', tts.to_phonemes(k, s, 'en-us', sp) if sp else '(text path)', '\n   sig:', tts.lex_sig(s)[:80])
a, marks = tts.speak("A phasor turns a sinusoidal signal into a single complex number. Debouncing a button needs a timer.")
sf.write(os.path.join(HERE, 'out', 'lex_test.wav'), a, tts.SR)
print('ok', round(len(a) / tts.SR, 2), 's', [m[0] for m in marks])
