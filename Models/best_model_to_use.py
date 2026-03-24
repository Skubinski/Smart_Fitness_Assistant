# # from decision_tree_classifier import total_accuracy_dtc
# from mlp_classifier import total_accuracy_mlp
# from random_forest_classifier import total_accuracy_rfc
# import matplotlib.pyplot as plt
# import numpy as np
#
# # avg_dtc = total_accuracy_dtc / 100
# avg_rfc = total_accuracy_rfc / 100
# avg_mlp = total_accuracy_mlp / 100
#
# # print(f"Decision Tree Classifier Accuracy: {avg_dtc:.2f}")
# print(f"Random Forest Classifier Accuracy: {avg_rfc:.2f}")
# print(f"MLP Classifier Accuracy: {avg_mlp:.2f}")
#
# best_model = max([
#     # [('Decision Tree Classifier', avg_dtc),
#      ('Random Forest Classifier', avg_rfc),
#      ('MLP Classifier', avg_mlp)],
#     key=lambda x: x[1]
# )
#
# print(f"The best option is {best_model[0]}")
#
#
# models = np.array(['Decision Tree', 'Random Forest', 'MLP'])
# # accuracies = np.array([avg_dtc, avg_rfc, avg_mlp])
#
# plt.bar(models, accuracies)
# plt.ylim(0, 1)
# plt.title('Average Accuracy of Classifiers')
# plt.ylabel('Accuracy')
# plt.xlabel('Model')
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# for i, acc in enumerate(accuracies):
#     plt.text(i, acc + 0.01, f"{acc:.2f}", ha='center')
#
#
# plt.show()