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
    with open(filename) as curr_file:
        file_reader=csv.reader(curr_file)
        next(file_reader)
        months={"Jan":0,"Feb":1,"Mar":2,"Apr":3,"May":4,"June":5,"Jul":6,"Aug":7,"Sep":8,"Oct":9,"Nov":10,"Dec":11}
        visitors={"Revisiting_visitors":1,"New_visitor":0}
        weekends={"TRUE":1,"FALSE":0}
        purchase={"TRUE":1,"FALSE":0}
        evidence=list()
        labels=list()
        analysis=tuple()

        for line in file_reader:
            curr_line=line[::]
            for val in [0,2,4,11,12,13,14]:
                curr_line[val]=int(curr_line[val])
            for val in [1,3,5,6,7,8,9]:
                curr_line[val]=float(curr_line[val])
            curr_line[10]=months[curr_line[10]]
            curr_line[16]=weekends[curr_line[16]]
            if curr_line[15] not in visitors.values():
                curr_line[15]=0
            else:
                curr_line[15]=visitors[curr_line[15]]
            curr_line[17]=purchase[curr_line[17]]
            evidence.append(curr_line[:17])
            labels.append(curr_line[17])

            analysis=(evidence,labels)

    return analysis

        
def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    tra1=KNeighborsClassifier(n_neighbors=1)
    tra1.fit(evidence,labels)
    return tra1
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity=0.0
    specificity=0.0
    identified_positive_value_accurate=0
    identified_negative_value_accurate=0
    evaluation=tuple()

    for tag,estimate in zip(labels,predictions):
        if tag==1:
            if tag==estimate:
                identified_positive_value_accurate += 1
        if tag==0:
            if tag==estimate:
                identified_negative_value_accurate += 1

    sensitivity=float(identified_positive_value_accurate/labels.count(1))
    specificity=float(identified_negative_value_accurate/labels.count(0))

    evaluation=(sensitivity,specificity)
    return evaluation


if __name__ == "__main__":
    main()
