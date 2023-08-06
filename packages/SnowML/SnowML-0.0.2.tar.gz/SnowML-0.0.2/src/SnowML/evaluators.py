import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from abc import ABC
from sklearn import metrics
from typing import Union, Any
from dataclasses import dataclass

@dataclass
class BaseEvaluator(ABC):
  model: Any
  X_train: Union[pd.Series, np.ndarray]
  X_test: Union[pd.Series, np.ndarray]
  y_train: Union[pd.Series, np.ndarray]
  y_test: Union[pd.Series, np.ndarray]
    
    
@dataclass
class ThresholdEvaluator(BaseEvaluator):
  th: int
    
  @staticmethod
  def optimize_threshold(thresholds, fpr, tpr, th):
    """
    find the best threshold from the roc curve. by finding the threshold
    for the point which is closest to (fpr=0,tpr=1)
    :param thresholds: cut off threshold range for predict probabilities
    :param fpr: false positive rate
    :param tpr: true positive rate
    :return: the best threshold which trying to minimize fpr and maximize tpr
    """
    if th < 1 and th > 0:
        return th
    else:
        fpr_tpr = pd.DataFrame({'thresholds': thresholds, 'fpr': fpr, 'tpr': tpr})
        fpr_tpr['dist'] = (fpr_tpr['fpr']) ** 2 + (fpr_tpr['tpr'] - 1) ** 2

    return fpr_tpr.iloc[fpr_tpr.dist.idxmin(), 0]
    
    
  def get_predictions(self):
    self.probabilities = self.model.predict_proba(self.X_test)[:, 1]
    fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.probabilities)
    
    self.best_threshold = ThresholdEvaluator.optimize_threshold(thresholds, fpr, tpr, self.th)
    self.predictions = self.probabilities > self.best_threshold
    
    
  
  @staticmethod
  def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
      """
      Pretty print for confusion matrix
      :param cm:
      :param labels:
      :param hide_zeroes:
      :param hide_diagonal:
      :param hide_threshold:
      :return: pretty print for confusion matrix
      """

      colwidth = 6
      empty_cell = " " * colwidth
      # Begin CHANGES
      fst_empty_cell = (colwidth - 3) // 2 * " " + "T\P" + (colwidth - 3) // 2 * " "
      if len(fst_empty_cell) < len(empty_cell):
          fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
      # Print header
      print("    " + fst_empty_cell, end=" ")
      # End CHANGES
      for label in labels:
          print("%{0}s".format(colwidth) % label, end=" ")
      print()
      # Print rows
      for i, label1 in enumerate(labels):
          print("    %{0}s".format(colwidth) % label1, end=" ")
          for j in range(len(labels)):
              cell = "%{0}.0f".format(colwidth) % cm[i, j]
              if hide_zeroes:
                  cell = cell if float(cm[i, j]) != 0 else empty_cell
              if hide_diagonal:
                  cell = cell if i != j else empty_cell
              if hide_threshold:
                  cell = cell if cm[i, j] > hide_threshold else empty_cell
              print(cell, end=" ")
          print()
 
  
  def confusion_matrix(self, labels: list):
    print('****************************************************')
    cm = metrics.confusion_matrix(self.y_test, self.predictions, labels)
    print('Confusion Matrix=')
    ThresholdEvaluator.print_cm(cm, labels)
    print('classification_report=')
    print(metrics.classification_report(self.y_test, self.predictions, digits=3, target_names=[str(l) for l in labels]))
    print('FPR:', "{0:.2%}".format(round(metrics.confusion_matrix(self.y_test, self.predictions)[0, 1] /
                                         (metrics.confusion_matrix(self.y_test, self.predictions)[0, 1]
                                          + metrics.confusion_matrix(self.y_test, self.predictions)[0, 0]), 4)))
    self.test_roc_auc_test=round(metrics.roc_auc_score(self.y_test, self.probabilities), 4)
    print('AUC:', "{0:.2%}".format(self.test_roc_auc_test))
    print('Accuracy Score:', "{0:.2%}".format(round(metrics.accuracy_score(self.y_test, self.predictions), 4)))
    print('Best Threshold:', "{0:.2%}".format(round(self.best_threshold, 4)))
    print('****************************************************')
    
    
  def plot_roc_auc(self, with_plots: bool=True):
    
    # Plot test roc
    plt.figure()
    fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.probabilities)
    plt.plot(fpr, tpr, label='test')
    
    # Plot train
    probabilities = self.model.predict_proba(self.X_train)[:,1]
    fpr, tpr, thresholds = metrics.roc_curve(self.y_train, probabilities)
    if with_plots:
        plt.plot(fpr, tpr, label='train')
        plt.plot([0, 1], [0, 1], 'r--', label='random guess')
        plt.title("Area under the ROC = {}".format(self.test_roc_auc_test), fontsize=18)
        plt.legend()
        plt.show()

        rcl_per_disp = metrics.plot_precision_recall_curve(self.model, self.X_test, self.y_test)
        plt.show()

        roc_disp = metrics.plot_roc_curve(self.model, self.X_test, self.y_test)
        plt.cla()
        plt.clf()
        plt.close()
