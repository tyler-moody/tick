import matplotlib.pyplot as plt
import tick

sends = tick.load('ticks.json')
counts_by_grade = tick.counts_by_grade(sends)
cbg_sorted = sorted(counts_by_grade.items(), key=lambda x:x[0])
counts = [x[0] for x in cbg_sorted]
grades = [x[1] for x in cbg_sorted]

plt.bar(counts, grades)
plt.show()

