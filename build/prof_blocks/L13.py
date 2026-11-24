# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Memory-mapped everything', {'t': 'wb', 'h': 'Memory-mapped I/O in C: one line, decoded', 'lang': 'c', 'cfs': 34, 'steps': [
    {'say': "Here's the line that confuses everyone the first time they open real embedded code. It turns on an L E D by writing to a hardware register at a fixed address. Let's take it apart from the inside out.",
     'w': [{'k': '#define LED_PORT  (*(volatile uint32_t *)0x48000014)', 'at': 1}, {'k': 'LED_PORT |= (1u << 5);     // pin 5 high: LED on', 'at': 1}]},
    {'say': "Start with the number, hex four eight zero zero zero zero one four. That's just an address from the chip's memory map, where the reference manual says the output register of a port lives. On its own, it's only an integer.",
     'w': [{'m': '1.  0x48000014 : an address from the datasheet', 'c': 'blue', 'at': 1, 'gap': 16}]},
    {'say': "The cast in front, open paren, volatile u int thirty two star, says: treat that integer as a pointer to a thirty two bit value. Then the star on the far left dereferences it: not the address, but the thing stored at that address. So LED port now behaves exactly like a variable that lives inside the hardware.",
     'w': [{'m': '2.  (uint32_t *) : make it a pointer to a 32-bit value', 'c': 'green', 'at': 0}, {'m': '3.  * in front : the register itself, not its address', 'c': 'purple', 'at': 1}]},
    {'say': "And volatile tells the compiler: this value can change, or must be written, outside your view. Without it, the optimizer may skip a write it thinks is pointless, or read the register once and never again, and your hardware silently stops responding. Finally, the bit mask from earlier sets just pin five.",
     'w': [{'m': '4.  volatile : never optimize these reads/writes away', 'c': 'red', 'at': 0}, {'m': '5.  |= (1u << 5) : set only bit 5', 'c': 'orange', 'at': 3}]},
]})

G = 'Memory-mapped I/O in C: one line, decoded'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (41, 51), 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': '#define LED_PORT', 'cols': (20, 41), 'c': 'green', 'at': 0}, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (19, 20), 'c': 'purple', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (21, 29), 'c': 'red', 'at': 0}, {'p': ('underline',), 'on': 'LED_PORT |= (1u << 5)', 'c': 'orange', 'at': 3})
