import math

def royalHITS(listOfPairs):

    pages = set()
    dict = {}

    # extract all the utls from the list
    for pair in listOfPairs:
        pages.add(pair[0])
        pages.add(pair[1])

    # initialize the authority and the hub of the pages to 1
    for page in pages:
        # for each page set [authority = 1, hub = 1]
        dict[page] = [1, 1]

    # do the algorithm for 10,000 steps
    for step in range(1, 10000):
        norm = 0
        for key in dict.keys():  # update all authority values first
            dict[key][0] = 0
            for pair in listOfPairs:
                if pair[1] == key:  # the set of pages that links to the current page
                    dict[key][0] += dict[pair[0]][1]
            norm += pow(dict[key][0], 2)  # calculate the sum of the squared auth values to normalise
        norm = math.sqrt(norm)
        for key in dict.keys():  # update the auth score
            dict[key][0] /= norm  # normalise the auth value
        norm = 0
        for key in dict.keys():  # update all hub values
            dict[key][1] = 0
            for pair in listOfPairs:
                if pair[0] == key:  # the set of pages that the page links to
                    dict[key][1] += dict[pair[1]][0]
            norm += pow(dict[key][1], 2)
        norm = math.sqrt(norm)
        for key in dict.keys():  # update the hub score
            dict[key][1] /= norm  # normalise the hub value
    return dict

