import numpy as np
import matplotlib.pyplot as plt
"""

test error: 0.13193960511
precision: 0.321755027422
recall:0.187035069075


test error: 0.109291521487
precision: 0.0
recall:0.0


test error: 0.110917537747
precision: 0.453947368421
recall:0.0733262486716


test error: 0.108130081301
precision: 0.551020408163
recall:0.05738575983


test error: 0.109291521487
precision: 0.0
recall:0.0


test error: 0.106736353078
precision: 0.580882352941
recall:0.0839532412327


test error: 0.111265969803
precision: 0.439716312057
recall:0.0658873538789


test error: 0.275842044135
precision: 0.217048145225
recall:0.584484590861
"""
classifier = ('Nearest Neighbors',
              'Linear SVM',
              'RBF SVM',
              'Decision Tree',
              'Random Forest',
              'Neural Net',
              'AdaBoost',
              'Naive Bayes')
training_error = (0.18044833338,
                  0.11263937257,
                  0.080948757719,
                  0.18893506189,
                  0.11263937257,
                  0.18922770771,
                  0.10912762284,
                  0.2996576044)
test_error = (0.108044833338,
                  0.111263937257,
                  0.0980948757719,
                  0.108893506189,
                  0.111263937257,
                  0.108922770771,
                  0.110912762284,
                  0.26996576044)

x_pos = np.arange(len(classifier))
ax = plt.subplot(111)
ax.bar(x_pos-0.4, training_error, width=0.2, align='edge', alpha=0.5)
ax.bar(x_pos-0.2, test_error, width=0.2, align='edge', alpha=0.5)
#  plt.yticks(y_pos, classifier)
#  plt.xlabel('Usage')
#  plt.title('Programming language usage')

plt.show()
