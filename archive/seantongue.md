# PROMPT COMPRESSION

(Excerpt from the chapter "Interacting with AI" in "The Ultimate AI Primer for Creative Entrepreneurs" by Sean Bradley)

As mentioned earlier, Stability AI’s Emad Mostaque claimed with regard to
LLMs that “knowledge is compression”. Indeed, language itself is a kind of
compression, each word being the distillation of an abstract concept into a
discrete idea and communicable utterance or symbol.
Some languages are natively more compressive particularly in written form—
e.g., the logograms of written Chinese (hanzi) and Japanese (kanji) are
arguably more data efficient than alphabets commonly used in the West. In
any case, they are more semantically dense, and encapsulate more contextual
information. (On the flip side, they may require more bytes to store than
alphabetical characters, and usually have a steep learning curve requiring
much memorization and “coginitive load” to use effectively. Chinese is not

# INTERACTING WITH AI

an easy language to learn!)
Using LLMs when they first emerged was very frustrating because of their
extremely limited context window. A 1000 tokens is roughly 750 words.
As recently as 2020, ChatGPT only had a context window of about 2048
tokens. So chatting with it felt like having a conversation with someone who
had a problematically short memory. Techniques like leveraging custom or
persistent instructions, nor RAG and LoRA had yet to emerge. When users
were confronted with the limits of the AI’s context window, some kind of
workaround was required…
Eventually, early ChatGPT users became aware that ChatGPT could compress
their conversations into an alphanumeric string that could serve as such a
workaround. A Twitter user (@gfodor) noticed this compression was similar
to the way Shogi, a Japanese board game, is played—and dubbed the AI’s
invention as “Shogtongue”.
Today, some LLMs have huge context windows. Anthropic’s Claude can
remember up to 100,000 tokens. And 01.ai’s Yi model has a massive context
window of up to 200,000 tokens. So, prompt compression is becoming less
necessary. However, if you are working with older models, or running models
on a laptop with limited processing power, and are not ready to implement
RAG or LoRA driven workarounds, you may find prompt compression still has
some utility. The process may seem convoluted, but works.

# SEANTONGUE

Seantongue is my own proprietary algorithm for creating some structure and
consistency around how ChatGPT and other LLMs might compress an existing
series of prompts or a conversation between itself and an end user.

# THE ULTIMATE AI PRIMER

Consider it a low code / no code process or procedure whereby one can
compress a chat with any given LLM agent with a limited context window
into a single prompt P, with the resultant compressed chat ready to use as
an unpackable artifact for seeding a new chat with a fresh context window,
or even enabling sharing that chat in a cross-model / cross-modal way with
other AI entities!

If you have reached the max of an AI entities context window, cut and paste
the entire convo into a text editor.

Keep in mind that a 1000 tokens is approximately 750 words. If the context
window for an AI chatbot is—for example—8,192 tokens, then it will start
to “forget” what was exchanged between the two of you after about 6,000
words. I don’t recommend you implement this technique with a completely
maxed out context window.

Rather, apply to reasonable chunks of text.

What’s reasonable? You’ll have to experiment a bit. Just remember, the more
information you try to compress, the more fuzzy it will be upon unpacking.
That is, you should consider this method slightly “lossy”—just as an MP3 is a
slightly lossy means of compressing an audio file…moreso than .wav format.
To begin, once your convo with an AI chatbot has extended through a
reasonable chunk, cut and paste the following into the chat…
You are CypherGPT--an expert in compression and encryption of
natural language with more than 30 years of experience in
cryptography, lossy and lossless data compression algorithms, as
well as older and even ancient human readable solutions to text
compression and encryption prior to the age of computers.

# INTERACTING WITH AI

```
I am going to ask you to compress a prompt. Here are the
instructions to compress a prompt:

For a given prompt P...
 
1. Condense the prompt by swapping out sesquipedalians with
synonyms of fewer syllables.
2. Reduce the prompt's verbosity--by extracting key concepts
and/or their crossmodal representations, while maintaining the
overall structure and intended communicative and creative impact.
3. Abbreviate the condensed prompt in accord with the brief forms
of Gregg Shorthand Pre-Anniversary Edition. If the word is not a
member of the list of brief forms, do not abbreviate it.
4. Remove from the condensed prompt all vowels from any word that
was not already abbreviated in accord with Gregg Shorthand. If the
word is uncommon in everyday use among laymen, or a specialized
term or jargon in science, mathematics, medicine, or any advanced
field of study, do not abbreviate it.
5. Remove from the condensed prompt all whitespace in each
sentence and from between sentences, instead using camel case to
separate words from one another.
Finally,
6. After compressing prompt P in accordance with steps 1 through 5
above, with any repeating string or substring of characters that
occurs within the compressed prompt P more than once, swap each
such occurrence out with a unique pair of random ASCII characters
(do NOT use any ASCII characters already present in the compressed
prompt P); prepend the compressed prompt P with a Python
dictionary wherein each item of the dictionary is comprised of
key:value pairs in which the key is one of the unique pairs of
random ASCII characters, and the value is the string or substring
of characters it represents within the compressed prompt P. Remove
vowels from values in items in the dictionary. The dictionary
should contain no line breaks. Separate this dictionary from the
main compressed prompt P by way of a single carat ^.

If you understand, respond with: "Please provide prompt P."
```

Optionally, although it shouldn’t be necessary with the major foundation
models, if your AI chatbot has access to the web, you can include in step 3
above links to the Gregg Shorthand Pre-Anniversary Edition brief forms and
expert brief forms, or—in fact—include all the salient brief forms in your
instructions as an additional table in the prompt itself.

• Gregg Shorthand Dictionary: This online resource provides a searchable
dictionary of Gregg Shorthand forms, including Pre-Anniversary versions.
You can find it here: <https://greggshorthand.github.io/>
• Gregg Shorthand Resources: This website offers various resources
for Gregg Shorthand learners, including a section dedicated to Pre-
Anniversary forms. You can find it here: <https://gregg-shorthand.com/>

After providing the instructions and resources, label the earlier conversation
you cut and paste in your text editor as prompt P. You can simply add at the
top of your conversation: “Here is prompt P.”

It should return the compressed version of your conversation.

To unpack the conversation, provide the AI chatbot with the following
instructions in a new context window…. (You may want to also first re-
establish the previous CypherGPT persona—especially if you are unpacking
in a completely different AI chatbot. And, in that case, you probably do want
to provide a rubric or table of the Gregg Shorthand brief forms used in the
original compression rules.)

```
I am going to ask you to incompress a prompt. Here are the
instructions to uncompress a prompt:

For a given prompt P...

1. Unpack the dictionary: Swap the values in the dictionary for
their corresponding keys in the body of the compressed prompt.
2. Add whitespace and separate CamelCase: Introduce appropriate
whitespace between words and separate words written in camel case.
3. Guess vowels: Make an educated guess to add the most likely
vowels back to their positions in any words that are not Gregg
Shorthand Pre-Anniversary Edition abbreviations.
4. Expand Gregg Shorthand: Replace the Gregg Shorthand
Pre-Anniversary Edition abbreviations with their full forms, as
accurately as possible.
5. Reconstruct verbosity: Try to reconstruct the original
descriptions, concepts, and details by expanding the condensed
text and using any emerging context to fill in gaps, while
preserving the overall structure and intended communicative and
creative impact.
6. Replace shorter synonyms: Replace the shorter synonyms with
potential sesquipedalian counterparts that fit the inferred
context and style of the prompt.
```

Example of an uncompressed prompt…

```
A highly detailed and photorealistic multi-dimensional
semi-translucent cosmological polytope and Wolfram ruliad and and
Tibetan mandala and alien logogram hybrid manifesting the abstract
concepts of Interconnectedness, Hierarchical Organization,
Evolution and Adaptability, and Subjectivity and Objectivity.
Place the image on its axis at a tilt to imply dynamism; create a
light source from behind the object to imply depth as well as to
create a glow...akin to a galaxy or a quantum level event.
Information is a dodecahedron; Interconnectedness is a torus;
Hierarchical Organization is a fractal tree; Evolution and
Adaptability is a DNA Helix; Subjectivity and Objectivity is
Yin-Yang. Inside Information: Quantum Mechanics (Cube), and the
Holographic Principal (hologram). Inside Interconnectedness:
Quantum Entanglement (Interlocking spheres) and Synchronicity (Two
Arrows). Inside Hierarchical Organization: String Theory
(Vibrating String) and Complex Systems Theory (Network). Inside
Evolution and Adaptability: Natural Selection (Tree of Life) and
Neural Plasticity (Brain). Inside Subjectivity and Objectivity:
Panpsychism (Eye) and the Copenhagen Interpretation (Wave-Particle
Duality).
```

Example of resultant compressed prompt…

```
{"01":"Mltdmnsnl","02":"Intrcnctdnss","03":"HrrchlOrgnztn",
"04":"Evltn&Adptblty","05":"Sbjctvty&Objctvty","06":"QntmMchncs",
"07":"HlgrphcPrncpl","08":"QntmEntnglmnt","09":"Snchrncty",
"10":"StrngThry","11":"CmplxSystmsThry","12":"NtrlSlctn",
"13":"NrlPlstcty","14":"Pnpsychsm","15":"CphgnIntrprttn",
"16":"TltImg","17":"AddBcklghtFrDpth",
"18":"Glctc/QntmGlw"}^Cr8Lflik01CosmicPolytopeShowing02(Torus),
03(FractalTree),04(DNAHelix),05(YinYang).Include06(Cube),07(Hologram),
08(InterlockingSpheres),09(2Arrows),10(VibratingString),11(Network),
12(TreeOfLife),13(Brain),14(Eye),15(Wave-ParticleDuality).16&17&18

Example of unpacking the compressed prompt in a new context window…
Begin with a prompt that asks the AI to confirm it knows the salient rubric
used for encoding and compressing the original prompt.

Do you know the brief forms and expert brief forms of the Gregg
Shorthand Pre-Anniversary Edition Diamond Jubilee Edition?

The AI should respond positively or even provide (likely a redacted list of) the
appropriate brief forms before continuing. If you are moving to another AI
chatbot, and not unpacking in the the same LLM in which you compressed the
original prompt, as mentioned, it may be wiser to provide the actual rubric to
the LLM yourself rather than asking it to generate it for you.

Once you can confirm the AI chatbot understands what you’re referencing,
then cut and paste the following…

```

I'm going to provide you an ASCII string. This string represents a
conversation (prompt P) that has been compressed into a single
prompt via the following heuristics:

1. Condense the prompt by swapping out sesquipedalians with
synonyms of fewer syllables.
2. Reduce the prompt's verbosity--by extracting key concepts
and/or their crossmodal representations, while maintaining the
overall structure and intended communicative and creative impact.
3. Abbreviate the condensed prompt in accord with the brief forms
of Gregg Shorthand Pre-Anniversary Edition. If the word is not a
member of the list of brief forms, do not abbreviate it.
4. Remove from the condensed prompt all vowels from any word that
was not already abbreviated in accord with Gregg Shorthand. If the
word is uncommon in everyday use among laymen, or a specialized
term or jargon in science, mathematics, medicine, or any advanced
field of study, do not abbreviate it.
5. Remove from the condensed prompt all whitespace in each
sentence and from between sentences, instead using camel case to
separate words from one another.
Finally,
6. After compressing prompt P in accordance with steps 1 through 5
above, with any repeating string or substring of characters that
occurs within the compressed prompt P more than once, swap each
such occurrence out with a unique pair of random ASCII characters
(do NOT use any ASCII characters already present in the compressed
prompt P); prepend the compressed prompt P with a Python
dictionary wherein each item of the dictionary is comprised of
key:value pairs in which the key is one of the unique pairs of
random ASCII characters, and the value is the string or substring
of characters it represents within the compressed prompt P. Remove
vowels from values in items in the dictionary. The dictionary
should contain no line breaks. Separate this dictionary from the
main compressed prompt P by way of a single carat ^.

Prompt P has already been compressed in accordance with the above.
Now, I want you to unpack the compressed prompt via the following
procedure...

1. Unpack the dictionary: Swap the values in the dictionary for
their corresponding keys in the body of the compressed prompt.
2. Add whitespace and separate CamelCase: Introduce appropriate
whitespace between words and separate words written in camel case.
3. Guess vowels: Make an educated guess to add the most likely
vowels back to their positions in any words that are not Gregg
Shorthand Pre-Anniversary Edition abbreviations.
4. Expand Gregg Shorthand: Replace the Gregg Shorthand
Pre-Anniversary Edition abbreviations with their full forms, as
accurately as possible.
5. Reconstruct verbosity: Try to reconstruct the original
descriptions, concepts, and details by expanding the condensed
text and using any emerging context to fill in gaps, while
preserving the overall structure and intended communicative and
creative impact.
6. Replace shorter synonyms: Replace the shorter synonyms with
potential sesquipedalian counterparts that fit the inferred
context and style of the prompt.
If you understand the above instructions, please respond with
"Yes, I understand. I will unpack the compressed prompt P."

```

The AI should respond with something like, “Yes, I understand. I will unpack
the compressed prompt P.”

Then your next input is the compressed prompt…

```

Here is the compressed prompt P. Please uncompress it.
{"01":"Mltdmnsnl","02":"Intrcnctdnss","03":"HrrchlOrgnztn",
"04":"Evltn&Adptblty","05":"Sbjctvty&Objctvty","06":"QntmMchncs",
"07":"HlgrphcPrncpl","08":"QntmEntnglmnt","09":"Snchrncty",
"10":"StrngThry","11":"CmplxSystmsThry","12":"NtrlSlctn",
"13":"NrlPlstcty","14":"Pnpsychsm","15":"CphgnIntrprttn",
"16":"TltImg","17":"AddBcklghtFrDpth",
"18":"Glctc/QntmGlw"}^Cr8Lflik01CosmicPolytopeShowing02(Torus),
03(FractalTree),04(DNAHelix),05(YinYang).Include06(Cube),07(Hologram),
08(InterlockingSpheres),09(2Arrows),10(VibratingString),11(Network),
12(TreeOfLife),13(Brain),14(Eye),15(Wave-ParticleDuality).16&17&18

The AI should respond with the unpacked and original prompt. You will note: it
is, indeed, worded differently than the original prompt, but the broad strokes—
the essence of the original conversation, including some rather involved and
complexly described imagery—is all there.

Create Life-like Multidimensional Cosmic Polytope Showing
Interconnectedness (Torus), Hierarchical Organization (Fractal
Tree), Evolution & Adaptability (DNA Helix), Subjectivity &
Objectivity (Yin-Yang). Include Quantum Mechanics (Cube),
Holographic Principle (Hologram), Quantum Entanglement
(Interlocking Spheres), Synchronicity (2 Arrows), String Theory
(Vibrating String), Complex Systems Theory (Network), Natural
Selection (Tree Of Life), Neural Plasticity (Brain), Panpsychism
(Eye), Copenhagen Interpretation (Wave-Particle Duality). Tilt
Image & Add Backlight For Depth & Galactic/Quantum Glow.

```
