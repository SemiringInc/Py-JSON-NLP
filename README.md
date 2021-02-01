# Python JSON-NLP Module

(C) 2020-2021 by [Semiring Inc.]

Contributions from [Damir Cavar], [Oren Baldinger], [Maanvitha Gongalla], [Anurag Kumar], Murali Kammili, and others during 2019.

Brought to you by the [NLP-Lab.org]. New Maintainer since 2020 is [Semiring Inc.].

This new version now is 0.6 and it is no longer compatible with version 0.2.33. If you use the old JSON-NLP standard in your code, make sure you require version 0.2.33 of *pyjsonnlp*. This new version is compatible with the newest version of [Go JSON-NLP].



## Introduction

There is a growing number of Natural Language Processing (NLP) tools, modules, pipelines. There does not seem to be any standard for the output format. Here we are focusing on a standard for the output format syntax. Some future version of [JSON-NLP] might address the output semantics as well.

[JSON-NLP] is a standard for the most important outputs NLP pipelines and components can generate. The relevant documentation can be found in the [JSON-NLP] GitHub repo and on its website at the [NLP-Lab] and [Semiring Inc.].

The Python [JSON-NLP] module contains general mapping functions for [JSON-NLP] to [CoNLL-U], a validator for the generated output, an NLP pipeline interface (for [Flair], [spaCy], [NLTK], [Polyglot], [Xrenner], [Stanford CoreNLP] etc.), and various utility functions.

There is a [Java JSON-NLP](https://github.com/dcavar/J-JSON-NLP) Maven module as well, there is a [Go implementation of a JSON-NLP wrapper](https://github.com/SemiringInc/GoJSONNLP), and there are wrappers for numerous popular NLP pipelines and tools linked from the [NLP-Lab.org] and [Semiring Inc.] websites.


## Installation

For more details, see [JSON-NLP].

This module is a wrapper for outputs from different NLP pipelines and modules into a standardized [JSON-NLP] format.

To install this package, run the following command:

    pip install pyjsonnlp

You might have to use *pip3* on some systems.


## Validation

[JSON-NLP] is based on a schema, maintained by [NLP-Lab.org] and [Semiring Inc.], to comprehensively and concisely represent linguistic annotations. 

We provide a validator to help ensure that generated JSON validates against the schema:

    result = MyPipeline().proces(text="I am a sentence")
    assert pyjsonnlp.validation.is_valid(result)


## Conversion

To enable interoperability with other annotation formats, we support conversions between them.
Note that conversion could be lossy, if the relative depths of annotation are not the same.
Currently we have a [CoNLL-U] to [JSON-NLP] converter, that covers most annotations:

    pyjsonnlp.conversion.parse_conllu(conllu_text)
    
To convert the other direction:

    pyjsonnlp.conversion.to_conllu(jsonnlp)



[Damir Cavar]: https://www.linkedin.com/in/damircavar/ "Damir Cavar"
[Oren Baldinger]: https://oren.baldinger.me/ "Oren Baldinger"
[Anurag Kumar]: https://github.com/anuragkumar95/ "Anurag Kumar"
[Maanvitha Gongalla]: https://maanvithag.github.io/MaanvithaGongalla/
[NLP-Lab.org]: http://nlp-lab.org/ "NLP-Lab.org"
[JSON-NLP]: https://github.com/SemiringInc/JSON-NLP "JSON-NLP"
[Flair]: https://github.com/zalandoresearch/flair "Flair"
[spaCy]: https://spacy.io/ "spaCy"
[NLTK]: http://nltk.org/ "Natural Language Processing Toolkit"
[Polyglot]: https://github.com/aboSamoor/polyglot "Polyglot" 
[Xrenner]: https://github.com/amir-zeldes/xrenner "Xrenner"
[CoNLL-U]: https://universaldependencies.org/format.html "CoNNL-U"
[Semiring Inc.]: https://semiring.com/ "Semiring Inc."
[Go JSON-NLP]: https://github.com/SemiringInc/GoJSONNLP "Go JSON-NLP"
