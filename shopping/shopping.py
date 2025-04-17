import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number 
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            data.append({
                "evidence": [cell for cell in row[:17]],
                "label": 1 if row[17] == "TRUE" else 0
            })

    for row in data:
        row['evidence'][0] = int(row['evidence'][0])
        row['evidence'][1] = float(row['evidence'][1])
        row['evidence'][2] = int(row['evidence'][2])
        row['evidence'][3] = float(row['evidence'][3])
        row['evidence'][4] = int(row['evidence'][4])
        row['evidence'][5] = float(row['evidence'][5])
        row['evidence'][6] = float(row['evidence'][6])
        row['evidence'][7] = float(row['evidence'][7])
        row['evidence'][8] = float(row['evidence'][8])
        row['evidence'][9] = float(row['evidence'][9])
        
        months = {'Jan': 0, 'Feb' : 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
        for month in months:
            if month == row['evidence'][10]:
                row['evidence'][10] = months[month]
        
        row['evidence'][11] = int(row['evidence'][11])
        row['evidence'][12] = int(row['evidence'][12])
        row['evidence'][13] = int(row['evidence'][13])
        row['evidence'][14] = int(row['evidence'][14])

        if row['evidence'][15] == "Returning_Visitor":
            row['evidence'][15] = 1
        else:
            row['evidence'][15] = 0
        
        if row['evidence'][16] == "TRUE":
            row['evidence'][16] = 1
        else:
            row['evidence'][16] = 0

    return ([row["evidence"] for row in data], [row["label"] for row in data])

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    pos_correct = 0
    pos_total = 0
    neg_correct = 0
    neg_total = 0
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            pos_total += 1
            if actual == predicted:
                pos_correct += 1
        elif actual == 0:
            neg_total += 1
            if actual == predicted:
                neg_correct += 1
    
    sensitivity = pos_correct / pos_total
    specificity = neg_correct / neg_total

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()