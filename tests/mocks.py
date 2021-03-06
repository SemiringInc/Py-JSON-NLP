import datetime
from collections import OrderedDict

from pyjsonnlp.microservices import Microservice

from pyjsonnlp.pipeline import Pipeline


class MockMicroservice(Microservice):
    def get_text(self) -> str:
        return 'mock text'

    def write_json(self, j: OrderedDict):
        return {'mock': 'json'}

    def write_text(self, conll: str):
        return 'mock conll'

    def get_output_format(self) -> str:
        return 'jsonnlp'

    def get_args(self) -> dict:
        return {'text': 'some text'}

    def handle_error(self, error: Exception):
        return None


class MockPipeline(Pipeline):
    @staticmethod
    def process(text='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                **kwargs) -> OrderedDict:
        return OrderedDict(**kwargs)


class MockResponse:
    @property
    def status_code(self):
        return 200

    @property
    def text(self):
        return u'<!DOCTYPE html>\n<html lang="en-US">\n\n  <head>\n    <meta charset=\'utf-8\'>\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <meta name="viewport" content="width=device-width,maximum-scale=2">\n    <link rel="stylesheet" type="text/css" media="screen" href="/assets/css/style.css?v=c467a1053650c4b666f28aa667e19ec54af99702">\n\n<!-- Begin Jekyll SEO tag v2.5.0 -->\n<title>Relationship Extraction | NLP-progress</title>\n<meta name="generator" content="Jekyll v3.7.4" />\n<meta property="og:title" content="Relationship Extraction" />\n<meta property="og:locale" content="en_US" />\n<meta name="description" content="Repository to track the progress in Natural Language Processing (NLP), including the datasets and the current state-of-the-art for the most common NLP tasks." />\n<meta property="og:description" content="Repository to track the progress in Natural Language Processing (NLP), including the datasets and the current state-of-the-art for the most common NLP tasks." />\n<link rel="canonical" href="http://nlpprogress.com/english/relationship_extraction.html" />\n<meta property="og:url" content="http://nlpprogress.com/english/relationship_extraction.html" />\n<meta property="og:site_name" content="NLP-progress" />\n<script type="application/ld+json">\n{"headline":"Relationship Extraction","@type":"WebPage","url":"http://nlpprogress.com/english/relationship_extraction.html","description":"Repository to track the progress in Natural Language Processing (NLP), including the datasets and the current state-of-the-art for the most common NLP tasks.","@context":"http://schema.org"}</script>\n<!-- End Jekyll SEO tag -->\n\n  </head>\n\n  <body>\n\n    <!-- HEADER -->\n    <div id="header_wrap" class="outer">\n        <header class="inner">\n          <a id="forkme_banner" href="https://github.com/sebastianruder/NLP-progress">View on GitHub</a>\n\n          <h1 id="project_title">NLP-progress</h1>\n          <h2 id="project_tagline">Repository to track the progress in Natural Language Processing (NLP), including the datasets and the current state-of-the-art for the most common NLP tasks.</h2>\n\n          \n        </header>\n    </div>\n\n    <!-- MAIN CONTENT -->\n    <div id="main_content_wrap" class="outer">\n      <section id="main_content" class="inner">\n        <h1 id="relationship-extraction">Relationship Extraction</h1>\n\n<p>Relationship extraction is the task of extracting semantic relationships from a text. Extracted relationships usually\noccur between two or more entities of a certain type (e.g. Person, Organisation, Location) and fall into a number of\nsemantic categories (e.g. married to, employed by, lives in).</p>\n\n<h3 id="new-york-times-corpus">New York Times Corpus</h3>\n\n<p>The standard corpus for distantly supervised relationship extraction is the New York Times (NYT) corpus, published in\n<a href="http://www.riedelcastro.org//publications/papers/riedel10modeling.pdf">Riedel et al, 2010</a>.</p>\n\n<p>This contains text from the <a href="https://catalog.ldc.upenn.edu/ldc2008t19">New York Times Annotated Corpus</a> with named\nentities extracted from the text using the Stanford NER system and automatically linked to entities in the Freebase\nknowledge base. Pairs of named entities are labelled with relationship types by aligning them against facts in the\nFreebase knowledge base. (The process of using a separate database to provide label is known as ‘distant supervision’)</p>\n\n<p>Example:</p>\n<blockquote>\n  <p><strong>Elevation Partners</strong>, the $1.9 billion private equity group that was founded by <strong>Roger McNamee</strong></p>\n</blockquote>\n\n<p><code class="highlighter-rouge">(founded_by, Elevation_Partners, Roger_McNamee)</code></p>\n\n<p>Different papers have reported various metrics since the release of the dataset, making it difficult to compare systems\ndirectly. The main metrics used are either precision at N results or plots of the precision-recall. The range of recall\nhas increased over the years as systems improve, with earlier systems having very low precision at 30% recall.</p>\n\n<table>\n  <thead>\n    <tr>\n      <th>Model</th>\n      <th>P@10%</th>\n      <th>P@30%</th>\n      <th>Paper / Source</th>\n      <th>Code</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>RESIDE (Vashishth et al., 2018)</td>\n      <td>73.6</td>\n      <td>59.5</td>\n      <td><a href="http://malllabiisc.github.io/publications/papers/reside_emnlp18.pdf">RESIDE: Improving Distantly-Supervised Neural Relation Extraction using Side Information</a></td>\n      <td><a href="https://github.com/malllabiisc/RESIDE">RESIDE</a></td>\n    </tr>\n    <tr>\n      <td>PCNN+ATT (Lin et al., 2016)</td>\n      <td>69.4</td>\n      <td>51.8</td>\n      <td><a href="http://www.aclweb.org/anthology/P16-1200">Neural Relation Extraction with Selective Attention over Instances</a></td>\n      <td><a href="https://github.com/thunlp/OpenNRE/">OpenNRE</a></td>\n    </tr>\n    <tr>\n      <td>MIML-RE (Surdeneau et al., 2012)</td>\n      <td>60.7+</td>\n      <td>-</td>\n      <td><a href="http://www.aclweb.org/anthology/D12-1042">Multi-instance Multi-label Learning for Relation Extraction</a></td>\n      <td><a href="https://nlp.stanford.edu/software/mimlre.shtml">Mimlre</a></td>\n    </tr>\n    <tr>\n      <td>MultiR (Hoffman et al., 2011)</td>\n      <td>60.9+</td>\n      <td>-</td>\n      <td><a href="http://www.aclweb.org/anthology/P11-1055">Knowledge-Based Weak Supervision for Information Extraction of Overlapping Relations</a></td>\n      <td><a href="http://aiweb.cs.washington.edu/ai/raphaelh/mr/">MultiR</a></td>\n    </tr>\n    <tr>\n      <td>(Mintz et al., 2009)</td>\n      <td>39.9+</td>\n      <td>-</td>\n      <td><a href="http://www.aclweb.org/anthology/P09-1113">Distant supervision for relation extraction without labeled data</a></td>\n      <td>\xa0</td>\n    </tr>\n  </tbody>\n</table>\n\n<p>(+) Obtained from results in the paper “Neural Relation Extraction with Selective Attention over Instances”</p>\n\n<h3 id="semeval-2010-task-8">SemEval-2010 Task 8</h3>\n\n<p><a href="http://www.aclweb.org/anthology/S10-1006">SemEval-2010</a> introduced ‘Task 8 - Multi-Way Classification of Semantic\nRelations Between Pairs of Nominals’. The task is, given a sentence and two tagged nominals, to predict the relation\nbetween those nominals <em>and</em> the direction of the relation. The dataset contains nine general semantic relations\ntogether with a tenth ‘OTHER’ relation.</p>\n\n<p>Example:</p>\n<blockquote>\n  <p>There were apples, <strong>pears</strong> and oranges in the <strong>bowl</strong>.</p>\n</blockquote>\n\n<p><code class="highlighter-rouge">(content-container, pears, bowl)</code></p>\n\n<p>The main evaluation metric used is macro-averaged F1, averaged across the nine proper relationships (i.e. excluding the\nOTHER relation), taking directionality of the relation into account.</p>\n\n<p>Several papers have used additional data (e.g. pre-trained word embeddings, WordNet) to improve performance. The figures\nreported here are the highest achieved by the model using any external resources.</p>\n\n<h4 id="end-to-end-models">End-to-End Models</h4>\n\n<table>\n  <thead>\n    <tr>\n      <th>Model</th>\n      <th>F1</th>\n      <th>Paper / Source</th>\n      <th>Code</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td><em>CNN-based Models</em></td>\n      <td>\xa0</td>\n      <td>\xa0</td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>Multi-Attention CNN (Wang et al. 2016)</td>\n      <td><strong>88.0</strong></td>\n      <td><a href="http://aclweb.org/anthology/P16-1123">Relation Classification via Multi-Level Attention CNNs</a></td>\n      <td><a href="https://github.com/lawlietAi/relation-classification-via-attention-model">lawlietAi’s Reimplementation</a></td>\n    </tr>\n    <tr>\n      <td>Attention CNN (Huang and Y Shen, 2016)</td>\n      <td>84.3<br />85.9<sup><a href="#footnote">*</a></sup></td>\n      <td><a href="http://www.aclweb.org/anthology/C16-1238">Attention-Based Convolutional Neural Network for Semantic Relation Extraction</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>CR-CNN (dos Santos et al., 2015)</td>\n      <td>84.1</td>\n      <td><a href="https://www.aclweb.org/anthology/P15-1061">Classifying Relations by Ranking with Convolutional Neural Network</a></td>\n      <td><a href="https://github.com/pratapbhanu/CRCNN">pratapbhanu’s Reimplementation</a></td>\n    </tr>\n    <tr>\n      <td>CNN (Zeng et al., 2014)</td>\n      <td>82.7</td>\n      <td><a href="http://www.aclweb.org/anthology/C14-1220">Relation Classification via Convolutional Deep Neural Network</a></td>\n      <td><a href="https://github.com/roomylee/cnn-relation-extraction">roomylee’s Reimplementation</a></td>\n    </tr>\n    <tr>\n      <td><em>RNN-based Models</em></td>\n      <td>\xa0</td>\n      <td>\xa0</td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>Entity Attention Bi-LSTM (Lee and Seo, 2018)</td>\n      <td><strong>85.2</strong></td>\n      <td><a href="">Semantic Relation Classification via Bidirectional LSTM Networks with Entity-aware Attention using Latent Entity Typing</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>Hierarchical Attention Bi-LSTM (Xiao and C Liu, 2016)</td>\n      <td>84.3</td>\n      <td><a href="http://www.aclweb.org/anthology/C16-1119">Semantic Relation Classification via Hierarchical Recurrent Neural Network with Attention</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>Attention Bi-LSTM (Zhou et al., 2016)</td>\n      <td>84.0</td>\n      <td><a href="http://www.aclweb.org/anthology/P16-2034">Attention-Based Bidirectional Long Short-Term Memory Networks for Relation Classification</a></td>\n      <td><a href="https://github.com/SeoSangwoo/Attention-Based-BiLSTM-relation-extraction">SeoSangwoo’s Reimplementation</a></td>\n    </tr>\n    <tr>\n      <td>Bi-LSTM (Zhang et al., 2015)</td>\n      <td>82.7<br />84.3<sup><a href="#footnote">*</a></sup></td>\n      <td><a href="http://www.aclweb.org/anthology/Y15-1009">Bidirectional long short-term memory networks for relation classification</a></td>\n      <td>\xa0</td>\n    </tr>\n  </tbody>\n</table>\n\n<p><a name="footnote">*</a>: It uses external lexical resources, such as WordNet, part-of-speech tags, dependency tags, and named entity tags.</p>\n\n<h4 id="dependency-models">Dependency Models</h4>\n\n<table>\n  <thead>\n    <tr>\n      <th>Model</th>\n      <th>F1</th>\n      <th>Paper / Source</th>\n      <th>Code</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>BRCNN (Cai et al., 2016)</td>\n      <td><strong>86.3</strong></td>\n      <td><a href="http://www.aclweb.org/anthology/P16-1072">Bidirectional Recurrent Convolutional Neural Network for Relation Classification</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>DRNNs (Xu et al., 2016)</td>\n      <td>86.1</td>\n      <td><a href="https://arxiv.org/abs/1601.03651">Improved Relation Classification by Deep Recurrent Neural Networks with Data Augmentation</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>depLCNN + NS (Xu et al., 2015a)</td>\n      <td>85.6</td>\n      <td><a href="https://www.aclweb.org/anthology/D/D15/D15-1062.pdf">Semantic Relation Classification via Convolutional Neural Networks with Simple Negative Sampling</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>SDP-LSTM (Xu et al., 2015b)</td>\n      <td>83.7</td>\n      <td><a href="https://arxiv.org/abs/1508.03720">Classifying Relations via Long Short Term Memory Networks along Shortest Dependency Path</a></td>\n      <td><a href="https://github.com/Sshanu/Relation-Classification">Sshanu’s Reimplementation</a></td>\n    </tr>\n    <tr>\n      <td>DepNN (Liu et al., 2015)</td>\n      <td>83.6</td>\n      <td><a href="http://www.aclweb.org/anthology/P15-2047">A Dependency-Based Neural Network for Relation Classification</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>FCN (Yu et al., 2014)</td>\n      <td>83.0</td>\n      <td><a href="https://www.cs.cmu.edu/~mgormley/papers/yu+gormley+dredze.nipsw.2014.pdf">Factor-based compositional embedding models</a></td>\n      <td>\xa0</td>\n    </tr>\n    <tr>\n      <td>MVRNN (Socher et al., 2012)</td>\n      <td>82.4</td>\n      <td><a href="http://aclweb.org/anthology/D12-1110">Semantic Compositionality through Recursive Matrix-Vector Spaces</a></td>\n      <td><a href="https://github.com/pratapbhanu/MVRNN">pratapbhanu’s Reimplementation</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<h1 id="fewrel">FewRel</h1>\n\n<p>The Few-Shot Relation Classification Dataset (FewRel) is a different setting from the previous datasets. This dataset consists of 70K sentences expressing 100 relations annotated by crowdworkers on Wikipedia corpus. The few-shot learning task follows the N-way K-shot meta learning setting. It is both the largest supervised relation classification dataset as well as the largest few-shot learning dataset till now.</p>\n\n<p>The public leaderboard is available on the <a href="http://zhuhao.me/fewrel">FewRel website</a>.</p>\n\n<p><a href="/">Go back to the README</a></p>\n\n      </section>\n    </div>\n\n    <!-- FOOTER  -->\n    <div id="footer_wrap" class="outer">\n      <footer class="inner">\n        \n        <p class="copyright">NLP-progress maintained by <a href="https://github.com/sebastianruder">sebastianruder</a></p>\n        \n        <p>Published with <a href="https://pages.github.com">GitHub Pages</a></p>\n      </footer>\n    </div>\n\n    \n  </body>\n</html>\n'

    def json(self):
        return {'ok': True}


class MockBadResponse:
    @property
    def status_code(self):
        return 500

    @property
    def reason(self):
        return 'Error!'


class MockArgs:
    def __init__(self, mock_format):
        self.mock_format = mock_format

    def get(self, k, v=None):
        return self.mock_format


class MockRequest:
    def __init__(self, mock_format):
        self.mock_args = MockArgs(mock_format)

    @property
    def args(self):
        return self.mock_args


class NewDate(datetime.datetime):
    @classmethod
    def now(cls, **kwargs):
        return datetime.datetime(2019, 1, 25, 17, 4, 34, 295386)


datetime.datetime = NewDate
