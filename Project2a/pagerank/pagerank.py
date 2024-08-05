import os
import random
import re
import sys
import copy

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

    # Only include links to other pages in the corpus
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
    transition_model_page=dict()
    total_links=len(corpus[page])
    total_pages=len(corpus)
    if total_links!=0:
        for i in corpus:
            if i in corpus[page]:
                transition_model_page[i]=damping_factor/total_links+(1-damping_factor)/total_pages
            else:
                transition_model_page[i]=(1-damping_factor)/total_pages
        return transition_model_page
    else:
        for i in corpus:
            transition_model_page[i]=(1-damping_factor)/total_pages
        return transition_model_page    
        



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict=dict()
    visit_count=dict()
    total_page_no=list()
    total_link_no=list()
    for page,link in corpus.items():
        total_page_no.append(page)
        total_link_no.append(link)
        visit_count[page]=0
    random_page=random.choices(total_page_no)[0]
    initial_sample=transition_model(corpus,random_page,damping_factor)
    dict_keys=list()
    dict_values=list()
    for key,value in initial_sample.items():
        dict_keys.append(key)
        dict_values.append(value)
    next_page=random.choices(dict_keys,weights=dict_values)[0]
    visit_count[next_page]+=1

    for k in range(n):
        next_sampledata=transition_model(corpus,next_page,damping_factor)
        dictn_keys=list()
        dictn_values=list()
        for key,value in next_sampledata.items():
            dictn_keys.append(key)
            dictn_values.append(value)

        next_page=random.choices(dictn_keys,weights=dictn_values)[0]
        visit_count[next_page]+=1

    for c in corpus:
        pagerank_dict[c]=visit_count[c]/n

    print("\nsum of all the pageranks:",round(sum(pagerank_dict.values())))
    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prev_dict=dict()
    N=len(corpus)
    for keys in corpus.keys():
        prev_dict[keys]=1/N
    
    difference=1
    while difference>=0.001:
        difference=0
        new_dict=copy.deepcopy(prev_dict)

        for present_page,present_page_links in corpus.items():
            chances=0
            for pres_page,pres_page_link in corpus.items():
                if pres_page_link:
                    if present_page in pres_page_link:
                        total_links=len(corpus[pres_page])
                        chances=chances+prev_dict[pres_page]/total_links
            prev_dict[present_page]=(1-damping_factor)/N +damping_factor*chances

            diffnew=abs(prev_dict[present_page]-new_dict[present_page])
            total=sum(prev_dict.values())
            if difference<diffnew:
                difference=diffnew
    for page,rank in prev_dict.items():
        prev_dict[page]=rank/total
    print("\nsum of all the pageranks:",round(sum(prev_dict.values())))
    return prev_dict
 


if __name__ == "__main__":
    main()
