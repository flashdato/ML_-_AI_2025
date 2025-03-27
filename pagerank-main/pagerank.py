import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to oth
    # per pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    keys = []
    for key in corpus:
        keys.append(key)
    model = {}
    if len(links) > 0:
        links_prop = damping_factor / len(links)
        gen_prop = (1 - damping_factor) / len(keys)
        for key in keys:
            if key in links:
                model[key] = links_prop + gen_prop
            else:
                model[key] = gen_prop
    elif len(links) == 0:
        for key in keys:
            prop = 1 / len(keys)
            model[key] = prop
    
    return model
    
    



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    keys = []
    f_dict = {}
    for key in corpus:
        keys.append(key)
        f_dict[key] = 0
    samples = [] 
    page = random.choice(list(corpus))
    for _ in range(n):
        samples.append(page)
        props = transition_model(corpus, page, damping_factor)
        links = []
        for key in props:
            links.append(key)
        chanses = []
        for link in links:
            chanse = int(props[link] * 1000)
            chanses.append(chanse)
        page = random.choices(links, weights=chanses, k=1)[0]
    for page in samples:
       f_dict[page] += 1 / n
    return f_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = []
    f_dict = {}
    N = len(corpus)
    for key in corpus:
        keys.append(key)
        f_dict[key] = 1 / N

    while True:
        i = 0
        for link in keys:
            value = (1 - damping_factor) / N
            for key in keys:
                links = corpus[key]
                if len(links) == 0:
                    value += damping_factor * (f_dict[key] / N)
                if link in links:
                    value += damping_factor * (f_dict[key] / len(links))
            if abs(value - f_dict[link]) > 0.00001:
                f_dict[link] = value
                i += 1
            else:
                f_dict[link] = value
        if i == 0:
            return f_dict
                
            



if __name__ == "__main__":
    main()