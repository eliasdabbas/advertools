

.. automodule:: advertools.code_recipes.spider_strategies
   :members:
   :undoc-members:
   :show-inheritance:


.. raw:: html

        <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How to crawl a list of pages, and those pages only (list mode)?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Simply provide that list as the first argument, for the url_list parameter, and make sure that follow_links=False, which is the default. This simply crawls the given pages, and stops when done."
          }
        },
        {
          "@type": "Question",
          "name": "How can I crawl a website including its sub-domains?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The crawl function takes an optional allowed_domains parameter. If not provided, it defaults to the domains of the URLs in url_list. When the crawler goes through the pages of example.com, it follows links to discover pages. If it finds pages on help.exmaple.com it won’t crawl them (it’s a different domain). The solution, therefore, is to provide a list of domains to the allowed_domains parameter. Make sure you also include the original domain, in this case example.com."
          }
        },
        {
          "@type": "Question",
          "name": "How can I save a copy of the logs of my crawl for auditing them later?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "It’s usually good to keep a copy of the logs of all your crawls to check for errors, exceptions, stats, etc. Pass a path of the file where you want the logs to be saved, in a dictionary to the cutom_settings parameter. A good practice for consistency is to give the same name to the output_file and log file (with a different extension) for easier retreival."
          }
        },
        {
          "@type": "Question",
          "name": "How can I automatically stop my crawl based on a certain condition?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "There are a few conditions that you can use to trigger the crawl to stop, and they mostly have descriptive names:\n\nCLOSESPIDER_ERRORCOUNT: You don’t want to wait three hours for a crawl to finish, only to discover that you had errors all over the place. Set a certain number of errors to trigger the crawler to stop, so you can investigate the issue.\n\nCLOSESPIDER_ITEMCOUNT: Anything scraped from a page is an “item”, h1, title , meta_desc, etc. Set the crawler to stop after getting a certain number of items if you want that.\n\nCLOSESPIDER_PAGECOUNT: Stop the crawler after a certain number of pages have been crawled. This is useful as an exploratory technique, especially with very large websites. It might be good to crawl a few thousand pages, get an idea on its structure, and then run a full crawl with those insights in mind.\n\nCLOSESPIDER_TIMEOUT: Stop the crawler after a certain number of seconds."
          }
        },
        {
          "@type": "Question",
          "name": "How can I (dis)obey robots.txt rules?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The crawler obeys robots.txt rules by default. Sometimes you might want to check the results of crawls without doing that. You can set the ROBOTSTXT_OBEY setting under custom_settings"
          }
        },
        {
          "@type": "Question",
          "name": "How do I set my User-agent while crawling?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Set this parameter under custom_settings dictionary under the key USER_AGENT. The default User-agent can be found by running adv.spider.user_agent"
          }
        },
        {
          "@type": "Question",
          "name": "How can I control the number of concurrent requests while crawling?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Some servers are set for high sensitivity to automated and/or concurrent requests, that you can quickly be blocked/banned. You also want to be polite and not kill those servers, don’t you?\n\nThere are several ways to set that under the custom_settings parameter. The available keys are the following:\n\nCONCURRENT_ITEMS: default 100\nCONCURRENT_REQUESTS : default 16\nCONCURRENT_REQUESTS_PER_DOMAIN: default 8\nCONCURRENT_REQUESTS_PER_IP: default 0"
          }
        },
        {
          "@type": "Question",
          "name": "How can I slow down the crawling so I don’t hit the websites’ servers too hard?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Use the DOWNLOAD_DELAY setting and set the interval to be waited before downloading consecutive page from the same website (in seconds)."
          }
        },
        {
          "@type": "Question",
          "name": "How can I set multiple settings to the same crawl job?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Simply add multiple settings to the custom_settings parameter."
          }
        },
        {
          "@type": "Question",
          "name": "I want to crawl a list of pages, follow links from those pages, but only to a certain specified depth",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Set the DEPTH_LIMIT setting in the custom_settings parameter. A setting of 1 would follow links one level after the provided URLs in url_list"
          }
        },
        {
          "@type": "Question",
          "name": "How do I pause/resume crawling, while making sure I don’t crawl the same page twice?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Handling this is extremely simple, and all you have to do is simply provide a path to a new folder. Make sure it is new and empty, and make sure to only use it for the same crawl job reruns. That’s all you have to worry about. The JOBDIR setting handles this."
          }
        }
      ]
    }
    </script>
    <!--FAQPage Code Generated by https://saijogeorge.com/json-ld-schema-generator/faq/-->