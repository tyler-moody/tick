import matplotlib.pyplot as plt
import tick

sends = tick.load('ticks.json')
counts_by_grade = tick.counts_by_grade(sends)
counts = [x[0] for x in counts_by_grade]
grades = [x[1] for x in counts_by_grade]

plt.bar(counts, grades)
plt.show()

