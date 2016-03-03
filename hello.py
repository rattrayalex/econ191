from random import gauss


n_people = 100
n_houses = 100
n_plots = 100
n_periods = 100

# numpy.random.choice(items, p=probs)
t0_wealth_mu = 400
t0_wealth_sigma = 50

t0_income_mu = 100
t0_income_sigma = 10
ti_income_sigma = 10

house_price_mu = t0_income_mu * 3
house_price_sigma = t0_income_sigma * 3


class Person(object):

  def __init__(self, i):
    self.name = "Person {i}".format(i=i)
    self.wealth = gauss(t0_wealth_mu, t0_wealth_sigma)
    self.income = gauss(t0_income_mu, t0_income_sigma)
    self.houses_owned = []
    self.house_renting = None

  def __str__(self):
    return "{name}: w={w}, i={i}, nho={nho}, hr={hr}".format(
      name=self.name,
      w=self.wealth,
      i=self.income,
      nho=len(self.houses_owned),
      hr=self.house_renting is None,
    )

  def __eq__(self, other):
    if other is None:
      return False
    return self.name == other.name

  def consumption(self, t):
    # TODO: get fancier:
    # github.com/QuantEcon/QuantEcon.applications/
    # blob/master/perm_income/perm_inc_figs.py#L25
    return self.income

  def new_income(self, t):
    old_income = self.income
    # TODO: random walk.
    return max(0, gauss(old_income, ti_income_sigma))

  def collect_rent(self, t):
    houses = self.houses_owned
    rent = sum([house.rent() for house in houses])
    return rent

  def pay_rent(self, t):
    if self.house_renting:
      return self.house_renting.rent()
    return 0

  def pay_taxes(self, t):
    return 0

  def buy_house_if_possible(self, houses):
    # can only buy 1 house per period
    for house in houses:
      if self.can_buy_house(house):
        return self.buy_house(house)
    if not self.houses_owned:
      self.rent_a_house(houses)

  def can_buy_house(self, house):
    return house.is_for_sale() and self.wealth > house.price

  def buy_house(self, house):
    house.buy(self)
    self.wealth -= house.price
    self.houses_owned.append(house)
    if self.house_renting:
      self.house_renting.occupant = None
      self.house_renting = None
      house.occupy(self)
    return house

  def rent_a_house(self, houses):
    if self.house_renting is not None:
      return
    for house in reversed(houses):
      if house.is_unoccupied():
        self.house_renting = house
        return house.occupy(self)
    print 'Homeless!', self

  def update(self, t, houses):
    self.buy_house_if_possible(houses)

    i = self.new_income(t)
    c = self.consumption(t)
    rent_collected = self.collect_rent(t)
    rent_paid = self.pay_rent(t)
    taxes_paid = self.pay_taxes(t)

    wealth = self.wealth + i + rent_collected - c - rent_paid - taxes_paid

    self.wealth = wealth
    self.income = i


class House(object):

  def __init__(self, plot):
    self.price = gauss(house_price_mu, house_price_sigma)
    self.plot = plot
    self.owner = None
    self.occupant = None

  def __str__(self):
    owner_name = self.owner.name if self.owner else None
    occupant_name = self.occupant.name if self.occupant else None
    return "H<owner:{}, occupant:{}, price:{}>".format(
      owner_name, occupant_name, int(self.price))

  def rent(self):
    return self.price / 10

  def is_for_sale(self):
    return self.owner is None

  def buy(self, owner):
    if not self.is_for_sale():
      raise Exception('Not for Sale!')
    self.owner = owner
    return self

  def is_unoccupied(self):
    return self.occupant is None

  def occupy(self, occupant):
    if not self.is_unoccupied():
      raise Exception('Someone lives here already!')
    self.occupant = occupant
    return self


class Plot(object):

  def __init__(self):
    self.value = 100


def print_people(people):
  for person in sorted(people, key=lambda p: p.wealth):
    print person


def main():
  people = [Person(i) for i in range(n_people)]
  plots = [Plot() for i in range(n_plots)]
  houses = sorted([House(p) for p in plots], key=lambda h: h.price)

  print_people(people)

  for t in range(n_periods):
    print t, [str(h) for h in houses]
    for person in people:
      person.update(t, houses)

  print_people(people)


if __name__ == '__main__':
  main()
