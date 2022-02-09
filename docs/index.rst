.. advertools documentation master file, created by
   sphinx-quickstart on Fri Jul  6 20:35:47 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :google-site-verification: GcN6XL_hWV3BP2Y9FNLjmTXxysS7QxJs804KoF15n_c

.. meta::
   :msvalidate.01: 527FAF22ADAF509BA5A2DDC3DDED12F5

.. meta::
    :description lang=en:
        Get productive as an online marketer with a Python package that helps
        in automating many of the important tasks.

.. raw:: html

      <script type="application/ld+json">
   {
     "@context": "http://schema.org",
     "@type": "SoftwareSourceCode",
     "author":
       {
         "@type": "Person",
         "name": "Elias Dabbas",
         "sameAs": ["https://www.linkedin.com/in/eliasdabbas",
                    "https://twitter.com/eliasdabbas",
                    "https://github.com/eliasdabbas"]
       },
     "description": "Productivity and analysis tools for online marketing.",
     "name": "advertools",
     "license": "https://github.com/eliasdabbas/advertools/blob/master/LICENSE",
     "programmingLanguage":
            {
            "@type": "ComputerLanguage",
            "name": "Python"
            },
     "runtimePlatform": "Python3",
     "codeRepository": "https://github.com/eliasdabbas/advertools",
     "keywords": ["marketing", "advertising", "SEO", "SEM",
                  "robots.txt",
                  "XML sitemaps", "AdWords", "PPC", "Social Media", "Twitter",
                  "YouTube", "Emoji", "Text Analysis"
     ],
     "version": "0.10.5"

   }
   </script>

advertools
==========
Online marketing productivity and analysis tools
------------------------------------------------

Crawl websites, Generate keywords for SEM campaigns, create text ads on a large
scale, analyze multiple SERPs at once, gain insights from large social media
posts, and get productive as an online marketer.

If these are things you are interested in, then this package might make your
life a little easier.

.. toctree::
   :titlesonly:

   About advertools <readme>

To install advertools, run the following from the command line::

   pip install advertools
   # OR:
   pip3 install advertools

.. toctree::
   :caption: SEM

   Generate SEM Keywords <advertools.kw_generate>
   Create Text Ads on a Large Scale <advertools.ad_create>
   Create Text Ads From Description Text <advertools.ad_from_string>

.. toctree::
   :caption: SEO

   robots.txt <advertools.robotstxt>
   XML Sitemaps <advertools.sitemaps>
   SEO Spider / Crawler <advertools.spider>
   Crawl Strategies <advertools.code_recipes.spider_strategies>
   Crawl headers (HEAD method only) <advertools.header_spider>
   Crawl Logs Analysis <advertools.logs>
   Reverse DNS Lookup <advertools.reverse_dns_lookup>
   Analyze Search Engine Results (SERPs) <advertools.serp>
   Google's Knowledge Graph <advertools.knowledge_graph>

.. toctree::
   :caption: Text & Content Analysis

   URL Structure Analysis <advertools.urlytics>
   Emoji Tools <advertools.emoji>
   Extract Structured Entities from Text <advertools.extract>
   Stop Words <advertools.stopwords>
   Text Analysis (absolute & weighted word frequency) <advertools.word_frequency>
   Word Tokenization (N-grams) <advertools.word_tokenize>

.. toctree::
   :caption: Social Media

   Twitter Data API <advertools.twitter>
   YouTube Data API <advertools.youtube>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :caption: Index & Change Log

   Index & Change Log <include_changelog>