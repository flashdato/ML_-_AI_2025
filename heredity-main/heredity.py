import csv
import itertools
import sys
from types import NoneType



PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and

                people[person]["trait"] != (person in have_trait))

            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    pft = 0.99
    npft = 0.01
    pfo = 0.5
    npfo = 0.5
    pfz = 0.01
    npfz = 0.99
    def prob_one_gene(person):
        if people[person]['mother'] in one_gene and people[person]['father'] in one_gene:
            return (pfo * npfo + npfo * pfo)
        elif people[person]['mother'] in one_gene and people[person]['father'] in two_genes:
            return (pfo * npft + npfo * pft)
        elif people[person]['mother'] in two_genes and people[person]['father'] in one_gene:
            return (pfo * npft + npfo * pft)
        elif people[person]['mother'] in two_genes and people[person]['father'] in two_genes:
            return (pft * npft + npft * pft)
        elif people[person]['mother'] in one_gene or people[person]['father'] in one_gene:
            return (pfo * npfz + pfz * npfo)
        elif people[person]['mother'] in two_genes or people[person]['father'] in two_genes:
            return (pft * npfz + pfz * npft)
        else:
            return(pfz * npfz + npfz * pfz)
    def prob_two_genes(person):
        if people[person]['mother'] in one_gene and people[person]['father'] in one_gene:
            return (pfo * pfo)
        elif people[person]['mother'] in one_gene and people[person]['father'] in two_genes:
            return (pfo * pft)
        elif people[person]['mother'] in two_genes and people[person]['father'] in one_gene:
            return (pft * pfo)
        elif people[person]['mother'] in two_genes and people[person]['father'] in two_genes:
            return (pft * pft)
        elif people[person]['mother'] in one_gene or people[person]['father'] in one_gene:
            return (pfo * pfz)
        elif people[person]['mother'] in two_genes or people[person]['father'] in two_genes:
            return (pft * pfz)
        else:
            return(pfz * pfz)
    def prob_no_genes(person):
        if people[person]['mother'] in one_gene and people[person]['father'] in one_gene:
            return (npfo * npfo)
        elif people[person]['mother'] in one_gene and people[person]['father'] in two_genes:
            return (npfo * npft)
        elif people[person]['mother'] in two_genes and people[person]['father'] in one_gene:
            return (npft * npfo)
        elif people[person]['mother'] in two_genes and people[person]['father'] in two_genes:
            return (npft * npft)
        elif people[person]['mother'] in one_gene or people[person]['father'] in one_gene:
            return (npfo * npfz)
        elif people[person]['mother'] in two_genes or people[person]['father'] in two_genes:
            return (npft * npfz)
        else:
            return(npfz * npfz)

    prbs= []
    for person in people:
        if people[person]['mother'] and people[person]['father']:
            if person in one_gene:
                if person in have_trait:
                    prob = prob_one_gene(person) * PROBS["trait"][1][True]
                    prbs.append(prob)
                else:
                    prob = prob_one_gene(person) * PROBS["trait"][1][False]
                    prbs.append(prob)
            elif person in two_genes:
                if person in have_trait:
                    prob = prob_two_genes(person) * PROBS["trait"][2][True]
                    prbs.append(prob)
                else:
                    prob = prob_two_genes(person) * PROBS["trait"][2][False]
                    prbs.append(prob)
            else:
                if person in have_trait:
                    prob = prob_no_genes(person) * PROBS["trait"][0][True]
                    prbs.append(prob)
                else:
                    prob = prob_no_genes(person) * PROBS["trait"][0][False]
                    prbs.append(prob) 
        else:
            if person in one_gene:
                if person in have_trait:
                    prob = PROBS["gene"][1] * PROBS["trait"][1][True]
                    prbs.append(prob)
                else:
                    prob = PROBS["gene"][1] * PROBS["trait"][1][False]
                    prbs.append(prob)
            elif person in two_genes:
                if person in have_trait:
                    prob = PROBS["gene"][2] * PROBS["trait"][2][True]
                    prbs.append(prob)
                else:
                    prob = PROBS["gene"][2] * PROBS["trait"][2][False]
                    prbs.append(prob)
            else:
                if person in have_trait:
                    prob = PROBS["gene"][0] * PROBS["trait"][0][True]
                    prbs.append(prob)
                else:
                    prob = PROBS["gene"][0] * PROBS["trait"][0][False]
                    prbs.append(prob) 

    p = 1
    for prb in prbs:
        p = p * prb
    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        if person in one_gene:
            if person in have_trait:
                probabilities[person]["gene"][1] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][1] += p
                probabilities[person]["trait"][False] += p
        elif person in two_genes:
            if person in have_trait:
                probabilities[person]["gene"][2] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][2] += p
                probabilities[person]["trait"][False] += p
        else:
            if person in have_trait:
                probabilities[person]["gene"][0] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][0] += p
                probabilities[person]["trait"][False] += p


def normalize(probabilities):
    for person in probabilities:
        k = 1 / (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
        probabilities[person]["trait"][True] = k * probabilities[person]["trait"][True]
        probabilities[person]["trait"][False] = k * probabilities[person]["trait"][False]

        k1 = 1 / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        probabilities[person]["gene"][0] = k1 * probabilities[person]["gene"][0]
        probabilities[person]["gene"][1] = k1 * probabilities[person]["gene"][1]
        probabilities[person]["gene"][2] = k1 * probabilities[person]["gene"][2]

if __name__ == "__main__":
    main()