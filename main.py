from Person import Person
from Plot import Plot
from House import House

n_people = 100
n_houses = 100
n_plots = 100
n_periods = 100


class Simulation(object):
  def __init__(self):
    self.people = [Person(i) for i in range(n_people)]
    self.plots = [Plot() for i in range(n_plots)]
    self.houses = sorted([House(p) for p in self.plots], key=lambda h: h.price)
    self.print_people()

  def run(self):
    for t in range(n_periods):
      print t, [str(h) for h in self.houses]
      for person in self.people:
        person.update(t, self.houses)
    self.print_people()

  def print_people(self):
    for person in sorted(self.people, key=lambda p: p.wealth):
      print person


def main():
  sim = Simulation()
  sim.run()


if __name__ == '__main__':
  main()
